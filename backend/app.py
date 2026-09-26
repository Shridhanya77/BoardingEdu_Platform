"""
BoardingEdu Flask application entry point.

Phase 15: Testing + deployment-ready API.
"""

from flask import Flask, jsonify
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException

from config import Config
from extensions import cors, db, jwt
from routes import register_blueprints
from utils.responses import error_response


def create_app(config_class=Config):
    """Application factory — config, extensions, blueprints, error handlers."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    _init_extensions(app)
    register_blueprints(app)
    _register_error_handlers(app)

    with app.app_context():
        import models  # noqa: F401

    @app.get("/")
    def index():
        """Friendly landing page so opening localhost:5000 is not a bare 404."""
        return jsonify(
            {
                "success": True,
                "service": "BoardingEdu API",
                "phase": 15,
                "message": "API is running. Use the endpoints below.",
                "endpoints": {
                    "health": "GET /api/health",
                    "auth": "POST /api/auth/login | register | GET /me",
                    "schools": "GET /api/schools (search/filter)",
                    "shortlists": "GET|POST /api/shortlists",
                    "enquiries": "GET|POST /api/enquiries",
                    "admin": "GET /api/admin/dashboard",
                },
            }
        )

    @app.get("/api/health")
    def health():
        db_ok = False
        db_error = None
        try:
            db.session.execute(text("SELECT 1"))
            db_ok = True
        except Exception as exc:  # noqa: BLE001 — connectivity probe only
            db_error = str(exc.__class__.__name__)

        return jsonify(
            {
                "success": True,
                "status": "ok" if db_ok else "degraded",
                "service": "BoardingEdu API",
                "phase": 15,
                "database": "connected" if db_ok else "unreachable",
                "database_error": db_error,
                "auth": "enabled",
            }
        )

    return app


def _init_extensions(app):
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(
        app,
        resources={r"/api/*": {"origins": app.config.get("CORS_ORIGINS", "*")}},
        supports_credentials=True,
    )

    @jwt.unauthorized_loader
    def _unauthorized_callback(reason):
        return error_response(
            "Authentication required. Please log in.",
            401,
        )

    @jwt.invalid_token_loader
    def _invalid_token_callback(reason):
        return error_response(
            "Invalid token. Please log in again.",
            401,
        )

    @jwt.expired_token_loader
    def _expired_token_callback(jwt_header, jwt_payload):
        return error_response(
            "Your session has expired. Please log in again.",
            401,
        )


def _register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(err):
        return error_response(getattr(err, "description", "Bad request."), 400)

    @app.errorhandler(404)
    def not_found(err):
        return error_response(
            "Resource not found. Try GET / or GET /api/health.",
            404,
        )

    @app.errorhandler(405)
    def method_not_allowed(err):
        return error_response("Method not allowed.", 405)

    @app.errorhandler(SQLAlchemyError)
    def sqlalchemy_error(err):
        # Do not expose DB details to clients
        return error_response("A database error occurred.", 500)

    @app.errorhandler(Exception)
    def unhandled_error(err):
        if isinstance(err, HTTPException):
            return error_response(
                err.description or err.name or "Request error.",
                err.code or 500,
            )
        # Production-safe: no stack traces in JSON responses
        if app.debug:
            app.logger.exception("Unhandled error: %s", err)
        return error_response("Unexpected server error.", 500)


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

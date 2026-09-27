"""
BoardingEdu Flask application entry point.

Phase 15: Testing + deployment-ready API.
"""

import logging

from flask import Flask, jsonify
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException

from config import Config
from extensions import cors, db, jwt
from routes import register_blueprints
from utils.responses import error_response


def _ensure_schema_and_seed(app):
    """Run on startup: create tables if missing, and seed demo data only if empty.

    Safe to run on every process start — never double-seeds.
    """
    with app.app_context():
        import models  # noqa: F401  (ensure SQLAlchemy mappers registered)

        try:
            db.create_all()
            db.session.commit()
            app.logger.info("Database tables ensured.")
        except Exception as exc:  # noqa: BLE001
            app.logger.exception("db.create_all() failed: %s", exc)
            return

        from models import Facility, School

        try:
            schools_count = db.session.query(School.id).count()
            facilities_count = db.session.query(Facility.id).count()
        except Exception as exc:  # noqa: BLE001 — table may not exist yet
            app.logger.warning("Could not count tables: %s", exc)
            return

        if schools_count == 0 or facilities_count == 0:
            app.logger.info(
                "Empty database detected (%d schools, %d facilities) — running demo seed.",
                schools_count,
                facilities_count,
            )
            try:
                from seed import seed as run_seed

                run_seed(reset=False)
                db.session.commit()
                app.logger.info("Demo seed completed successfully.")
            except Exception as exc:  # noqa: BLE001
                app.logger.exception("Demo seed failed: %s", exc)
                db.session.rollback()


def create_app(config_class=Config):
    """Application factory — config, extensions, blueprints, error handlers."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    logging.basicConfig(level=logging.INFO)
    if not app.debug:
        app.logger.setLevel(logging.INFO)

    _init_extensions(app)
    register_blueprints(app)
    _register_error_handlers(app)

    _ensure_schema_and_seed(app)

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
        schools_count = None
        try:
            db.session.execute(text("SELECT 1"))
            db_ok = True
            try:
                from models import School

                schools_count = db.session.query(School.id).count()
            except Exception:  # noqa: BLE001
                schools_count = None
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
                "schools_loaded": schools_count,
                "auth": "enabled",
            }
        )

    return app


def _init_extensions(app):
    import re

    db.init_app(app)
    jwt.init_app(app)
    allowed_origins = app.config.get(
        "CORS_ORIGINS",
        [
            "http://localhost:4173",
            "http://127.0.0.1:4173",
            "http://localhost:4175",
            "http://127.0.0.1:4175",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
    )

    vercel_pattern = re.compile(r"^https://.+\.vercel\.app$")
    render_pattern = re.compile(r"^https://.+\.onrender\.com$")

    def _cors_origin_check(origin):
        if origin in allowed_origins:
            return origin
        if vercel_pattern.match(origin or ""):
            return origin
        if render_pattern.match(origin or ""):
            return origin
        return False

    cors.init_app(
        app,
        resources={r"/api/*": {"origins": _cors_origin_check}},
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
        app.logger.error("SQLAlchemyError: %s", err)
        return error_response("A database error occurred.", 500)

    @app.errorhandler(Exception)
    def unhandled_error(err):
        if isinstance(err, HTTPException):
            return error_response(
                err.description or err.name or "Request error.",
                err.code or 500,
            )
        app.logger.exception("Unhandled error: %s", err)
        return error_response("Unexpected server error.", 500)


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


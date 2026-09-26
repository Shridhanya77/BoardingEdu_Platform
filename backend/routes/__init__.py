"""Register API blueprints."""

from routes.auth import auth_bp
from routes.schools import schools_bp
from routes.shortlists import shortlists_bp
from routes.enquiries import enquiries_bp
from routes.admin import admin_bp


def register_blueprints(app):
    """Attach all route blueprints to the Flask app."""
    app.register_blueprint(auth_bp)
    app.register_blueprint(schools_bp)
    app.register_blueprint(shortlists_bp)
    app.register_blueprint(enquiries_bp)
    app.register_blueprint(admin_bp)

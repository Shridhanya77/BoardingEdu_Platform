"""JWT / role-based authorization decorators."""

from functools import wraps

from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request

from extensions import db
from models import User
from utils.responses import error_response


def get_current_user():
    """Return the User for the JWT identity, or None."""
    identity = get_jwt_identity()
    if identity is None:
        return None
    try:
        user_id = int(identity)
    except (TypeError, ValueError):
        return None
    return db.session.get(User, user_id)


def login_required(fn):
    """Require any authenticated user; injects `current_user`."""

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception:
            return error_response("Authentication required. Please log in.", 401)

        user = get_current_user()
        if user is None:
            return error_response("Invalid or expired token. Please log in again.", 401)

        return fn(*args, current_user=user, **kwargs)

    return wrapper


def role_required(*allowed_roles):
    """Require authentication and one of the given roles; injects `current_user`."""

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
            except Exception:
                return error_response("Authentication required. Please log in.", 401)

            user = get_current_user()
            if user is None:
                return error_response(
                    "Invalid or expired token. Please log in again.", 401
                )

            claims = get_jwt() or {}
            role = user.role or claims.get("role")
            if role not in allowed_roles:
                return error_response(
                    "You do not have permission to access this resource.", 403
                )

            return fn(*args, current_user=user, **kwargs)

        return wrapper

    return decorator

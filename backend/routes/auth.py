"""Authentication API routes."""

from flask import Blueprint, request

from services.auth_service import AuthError, authenticate_user, register_user
from utils.decorators import login_required
from utils.responses import error_response, success_response
from utils.validators import validate_login_payload, validate_register_payload

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.post("/register")
def register():
    """
    Public registration for parent/student only.
    Body: name, email, phone, password, role
    """
    if not request.is_json:
        return error_response("Request body must be JSON.", 400)

    cleaned, errors = validate_register_payload(request.get_json(silent=True))
    if errors:
        return error_response("Validation failed.", 400, errors=errors)

    try:
        user, token = register_user(cleaned)
    except AuthError as exc:
        return error_response(exc.message, exc.status_code)
    except Exception:
        return error_response("Unexpected server error.", 500)

    return success_response(
        data={"user": user.to_dict(), "access_token": token},
        message="Registration successful.",
        status_code=201,
    )


@auth_bp.post("/login")
def login():
    """Authenticate with email + password; return JWT."""
    if not request.is_json:
        return error_response("Request body must be JSON.", 400)

    cleaned, errors = validate_login_payload(request.get_json(silent=True))
    if errors:
        return error_response("Validation failed.", 400, errors=errors)

    try:
        user, token = authenticate_user(cleaned)
    except AuthError as exc:
        return error_response(exc.message, exc.status_code)
    except Exception:
        return error_response("Unexpected server error.", 500)

    return success_response(
        data={"user": user.to_dict(), "access_token": token},
        message="Login successful.",
    )


@auth_bp.get("/me")
@login_required
def me(current_user):
    """Return the authenticated user's profile."""
    return success_response(data={"user": current_user.to_dict()})

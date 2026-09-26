"""Authentication business logic."""

from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError

from extensions import db
from models import User


class AuthError(Exception):
    """Domain error with HTTP status for route layer mapping."""

    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def register_user(cleaned):
    """
    Create a parent/student account.
    `cleaned` must already pass validate_register_payload.
    Returns (user, access_token).
    """
    existing = User.query.filter_by(email=cleaned["email"]).first()
    if existing:
        raise AuthError("An account with this email already exists.", 409)

    user = User(
        name=cleaned["name"],
        email=cleaned["email"],
        phone=cleaned["phone"],
        role=cleaned["role"],
    )
    user.set_password(cleaned["password"])

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise AuthError("An account with this email already exists.", 409)
    except Exception:
        db.session.rollback()
        raise AuthError("Unable to create account. Please try again later.", 500)

    token = _issue_token(user)
    return user, token


def authenticate_user(cleaned):
    """
    Verify credentials and return (user, access_token).
    Uses a generic message to avoid email enumeration.
    """
    user = User.query.filter_by(email=cleaned["email"]).first()
    if user is None or not user.check_password(cleaned["password"]):
        raise AuthError("Invalid email or password.", 401)

    token = _issue_token(user)
    return user, token


def get_user_by_id(user_id):
    """Load a user by primary key."""
    if user_id is None:
        return None
    try:
        uid = int(user_id)
    except (TypeError, ValueError):
        return None
    return db.session.get(User, uid)


def _issue_token(user):
    """Create a JWT whose identity is the user id; role stored in claims."""
    return create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role, "email": user.email},
    )

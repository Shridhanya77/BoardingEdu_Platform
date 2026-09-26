"""Shortlist API routes."""

from flask import Blueprint, request

from services.shortlist_service import (
    ShortlistServiceError,
    add_shortlist,
    list_user_shortlists,
    remove_shortlist,
)
from utils.decorators import role_required
from utils.responses import error_response, success_response

shortlists_bp = Blueprint("shortlists", __name__, url_prefix="/api/shortlists")


@shortlists_bp.get("")
@role_required("parent", "student")
def get_shortlists(current_user):
    try:
        items = list_user_shortlists(current_user.id)
    except Exception:
        return error_response("Unable to load shortlists.", 500)
    return success_response(data={"items": items})


@shortlists_bp.post("")
@role_required("parent", "student")
def post_shortlist(current_user):
    if not request.is_json:
        return error_response("Request body must be JSON.", 400)
    data = request.get_json(silent=True) or {}
    school_id = data.get("school_id")
    try:
        school_id = int(school_id)
    except (TypeError, ValueError):
        return error_response("school_id is required and must be an integer.", 400)

    try:
        item = add_shortlist(current_user.id, school_id)
    except ShortlistServiceError as exc:
        return error_response(exc.message, exc.status_code)
    except Exception:
        return error_response("Unexpected server error.", 500)

    return success_response(
        data={"shortlist": item},
        message="School added to shortlist.",
        status_code=201,
    )


@shortlists_bp.delete("/<int:school_id>")
@role_required("parent", "student")
def delete_shortlist(school_id, current_user):
    try:
        remove_shortlist(current_user.id, school_id)
    except ShortlistServiceError as exc:
        return error_response(exc.message, exc.status_code)
    except Exception:
        return error_response("Unexpected server error.", 500)
    return success_response(message="School removed from shortlist.")

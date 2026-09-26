"""Admin API routes."""

from flask import Blueprint, request

from services.admin_service import get_dashboard_stats, list_users
from services.enquiry_service import (
    EnquiryServiceError,
    list_all_enquiries,
    update_enquiry_status,
)
from utils.decorators import role_required
from utils.responses import error_response, success_response
from models import ENQUIRY_STATUSES

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@admin_bp.get("/dashboard")
@role_required("admin")
def dashboard(current_user):
    try:
        stats = get_dashboard_stats()
    except Exception:
        return error_response("Unable to load dashboard.", 500)
    return success_response(data={"stats": stats})


@admin_bp.get("/users")
@role_required("admin")
def users(current_user):
    try:
        items = list_users()
    except Exception:
        return error_response("Unable to load users.", 500)
    return success_response(data={"items": items})


@admin_bp.get("/enquiries")
@role_required("admin")
def admin_enquiries(current_user):
    status = (request.args.get("status") or "").strip() or None
    try:
        items = list_all_enquiries(status=status)
    except Exception:
        return error_response("Unable to load enquiries.", 500)
    return success_response(data={"items": items})


@admin_bp.put("/enquiries/<int:enquiry_id>/status")
@role_required("admin")
def admin_update_enquiry_status(enquiry_id, current_user):
    if not request.is_json:
        return error_response("Request body must be JSON.", 400)
    data = request.get_json(silent=True) or {}
    status = (data.get("status") or "").strip()
    if not status:
        return error_response("status is required.", 400)
    if status not in ENQUIRY_STATUSES:
        return error_response(
            f"status must be one of: {', '.join(ENQUIRY_STATUSES)}.",
            400,
        )
    try:
        enquiry = update_enquiry_status(enquiry_id, status)
    except EnquiryServiceError as exc:
        return error_response(exc.message, exc.status_code)
    except Exception:
        return error_response("Unexpected server error.", 500)
    return success_response(
        data={"enquiry": enquiry},
        message="Enquiry status updated.",
    )

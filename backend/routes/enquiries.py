"""Admission enquiry API routes."""

from flask import Blueprint, request

from services.enquiry_service import (
    EnquiryServiceError,
    create_enquiry,
    get_enquiry_for_user,
    list_all_enquiries,
    list_enquiries_for_user,
)
from utils.decorators import login_required, role_required
from utils.responses import error_response, success_response
from utils.validators import validate_enquiry_payload

enquiries_bp = Blueprint("enquiries", __name__, url_prefix="/api/enquiries")


@enquiries_bp.post("")
@role_required("parent", "student")
def post_enquiry(current_user):
    if not request.is_json:
        return error_response("Request body must be JSON.", 400)

    cleaned, errors = validate_enquiry_payload(request.get_json(silent=True))
    if errors:
        return error_response("Validation failed.", 400, errors=errors)

    try:
        enquiry = create_enquiry(current_user.id, cleaned)
    except EnquiryServiceError as exc:
        return error_response(exc.message, exc.status_code)
    except Exception:
        return error_response("Unexpected server error.", 500)

    return success_response(
        data={"enquiry": enquiry.to_dict()},
        message="Admission enquiry submitted.",
        status_code=201,
    )


@enquiries_bp.get("")
@login_required
def get_enquiries(current_user):
    try:
        if current_user.role == "admin":
            status = (request.args.get("status") or "").strip() or None
            items = list_all_enquiries(status=status)
        else:
            items = list_enquiries_for_user(current_user.id)
    except Exception:
        return error_response("Unable to load enquiries.", 500)
    return success_response(data={"items": items})


@enquiries_bp.get("/<int:enquiry_id>")
@login_required
def get_enquiry(enquiry_id, current_user):
    try:
        enquiry = get_enquiry_for_user(enquiry_id, current_user)
    except EnquiryServiceError as exc:
        return error_response(exc.message, exc.status_code)
    except Exception:
        return error_response("Unexpected server error.", 500)
    return success_response(data={"enquiry": enquiry})

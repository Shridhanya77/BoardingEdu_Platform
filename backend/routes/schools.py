"""School CRUD, search/filter, and related-resource API routes."""

import logging

from flask import Blueprint, request

from services.school_service import (
    SchoolServiceError,
    create_school,
    delete_school,
    get_filter_options,
    get_school_facilities,
    get_school_fees,
    get_school_images,
    get_school_infrastructure,
    get_school_or_404,
    list_schools,
    update_school,
)
from utils.decorators import role_required
from utils.responses import error_response, success_response
from utils.validators import validate_school_payload

schools_bp = Blueprint("schools", __name__, url_prefix="/api/schools")
logger = logging.getLogger(__name__)


def _parse_positive_int(value, default, maximum=None):
    try:
        number = int(value)
    except (TypeError, ValueError):
        return default
    if number < 1:
        return default
    if maximum is not None:
        return min(number, maximum)
    return number


def _parse_optional_int(value):
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _parse_bool(value):
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def _parse_facility_ids(args):
    """Accept facility_ids=1,2,3 or repeated facility_ids=1&facility_ids=2."""
    raw_list = args.getlist("facility_ids")
    if not raw_list:
        # also allow facilities=1,2,3
        raw = args.get("facilities") or args.get("facility_ids")
        if not raw:
            return []
        raw_list = [raw]

    ids = []
    for chunk in raw_list:
        for part in str(chunk).split(","):
            part = part.strip()
            if not part:
                continue
            try:
                ids.append(int(part))
            except ValueError:
                continue
    # unique, preserve order
    return list(dict.fromkeys(ids))


def _parse_school_filters(args):
    name = (args.get("name") or args.get("q") or "").strip() or None
    city = (args.get("city") or "").strip() or None
    board = (args.get("board") or "").strip() or None
    school_type = (args.get("school_type") or "").strip() or None
    gender = (args.get("gender") or "").strip() or None
    sort = (args.get("sort") or "name").strip().lower()

    hostel_raw = args.get("hostel_available")
    if hostel_raw is None:
        hostel_raw = args.get("boarding")
    hostel_available = _parse_bool(hostel_raw)

    min_fee = _parse_optional_int(args.get("min_fee"))
    max_fee = _parse_optional_int(args.get("max_fee"))
    if min_fee is not None and min_fee < 0:
        min_fee = 0
    if max_fee is not None and max_fee < 0:
        max_fee = 0

    return {
        "name": name,
        "city": city,
        "board": board,
        "school_type": school_type,
        "gender": gender,
        "hostel_available": hostel_available,
        "min_fee": min_fee,
        "max_fee": max_fee,
        "facility_ids": _parse_facility_ids(args),
        "sort": sort,
    }


@schools_bp.get("")
def get_schools():
    """
    Public school listing with search, filters, sort, and pagination.

    Query params:
      name|q, city, board, school_type, gender, hostel_available|boarding,
      min_fee, max_fee, facility_ids (comma-separated), sort, page, per_page
    """
    page = _parse_positive_int(request.args.get("page"), 1)
    per_page = _parse_positive_int(request.args.get("per_page"), 12, maximum=50)
    filters = _parse_school_filters(request.args)

    if (
        filters["min_fee"] is not None
        and filters["max_fee"] is not None
        and filters["min_fee"] > filters["max_fee"]
    ):
        return error_response("min_fee cannot be greater than max_fee.", 400)

    try:
        result = list_schools(page=page, per_page=per_page, filters=filters)
    except Exception as exc:
        logger.exception("list_schools failed: %s", exc)
        return error_response("Unable to load schools.", 500)

    return success_response(data=result)


@schools_bp.get("/filters")
def school_filter_options():
    """Distinct cities/boards/types/genders + facilities for filter UIs."""
    try:
        options = get_filter_options()
    except Exception as exc:
        logger.exception("get_filter_options failed: %s", exc)
        return error_response("Unable to load filter options.", 500)
    return success_response(data=options)


@schools_bp.get("/<int:school_id>")
def get_school(school_id):
    """Public school detail including fees, facilities, images, infrastructure."""
    try:
        school = get_school_or_404(school_id)
    except SchoolServiceError as exc:
        return error_response(exc.message, exc.status_code)

    return success_response(data={"school": school.to_dict(detailed=True)})


@schools_bp.post("")
@role_required("admin")
def post_school(current_user):
    """Admin: create a school (optional nested fees/images/infrastructure/facility_ids)."""
    if not request.is_json:
        return error_response("Request body must be JSON.", 400)

    cleaned, errors = validate_school_payload(request.get_json(silent=True), partial=False)
    if errors:
        return error_response("Validation failed.", 400, errors=errors)

    try:
        school = create_school(cleaned)
    except SchoolServiceError as exc:
        return error_response(exc.message, exc.status_code)
    except Exception:
        return error_response("Unexpected server error.", 500)

    return success_response(
        data={"school": school.to_dict(detailed=True)},
        message="School created successfully.",
        status_code=201,
    )


@schools_bp.put("/<int:school_id>")
@role_required("admin")
def put_school(school_id, current_user):
    """Admin: update a school. Omit nested keys to leave related rows unchanged."""
    if not request.is_json:
        return error_response("Request body must be JSON.", 400)

    cleaned, errors = validate_school_payload(request.get_json(silent=True), partial=True)
    if errors:
        return error_response("Validation failed.", 400, errors=errors)
    if not cleaned:
        return error_response("No fields provided to update.", 400)

    try:
        school = update_school(school_id, cleaned)
    except SchoolServiceError as exc:
        return error_response(exc.message, exc.status_code)
    except Exception:
        return error_response("Unexpected server error.", 500)

    return success_response(
        data={"school": school.to_dict(detailed=True)},
        message="School updated successfully.",
    )


@schools_bp.delete("/<int:school_id>")
@role_required("admin")
def remove_school(school_id, current_user):
    """Admin: delete a school and cascaded related rows."""
    try:
        delete_school(school_id)
    except SchoolServiceError as exc:
        return error_response(exc.message, exc.status_code)
    except Exception:
        return error_response("Unexpected server error.", 500)

    return success_response(message="School deleted successfully.")


@schools_bp.get("/<int:school_id>/fees")
def school_fees(school_id):
    try:
        fees = get_school_fees(school_id)
    except SchoolServiceError as exc:
        return error_response(exc.message, exc.status_code)
    return success_response(data={"fees": fees})


@schools_bp.get("/<int:school_id>/facilities")
def school_facilities(school_id):
    try:
        facilities = get_school_facilities(school_id)
    except SchoolServiceError as exc:
        return error_response(exc.message, exc.status_code)
    return success_response(data={"facilities": facilities})


@schools_bp.get("/<int:school_id>/infrastructure")
def school_infrastructure(school_id):
    try:
        items = get_school_infrastructure(school_id)
    except SchoolServiceError as exc:
        return error_response(exc.message, exc.status_code)
    return success_response(data={"infrastructure": items})


@schools_bp.get("/<int:school_id>/images")
def school_images(school_id):
    try:
        images = get_school_images(school_id)
    except SchoolServiceError as exc:
        return error_response(exc.message, exc.status_code)
    return success_response(data={"images": images})

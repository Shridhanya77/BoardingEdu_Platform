"""School CRUD, search/filter, and related-resource business logic."""

from sqlalchemy import func, or_
from sqlalchemy.orm import joinedload

from extensions import db
from models import (
    Facility,
    Infrastructure,
    School,
    SchoolFacility,
    SchoolFee,
    SchoolImage,
)

SORT_OPTIONS = {
    "name": School.name.asc(),
    "name_asc": School.name.asc(),
    "name_desc": School.name.desc(),
    "fee_asc": School.min_fee.asc().nullslast(),
    "fee_desc": School.max_fee.desc().nullslast(),
    "rating": School.rating.desc().nullslast(),
    "rating_desc": School.rating.desc().nullslast(),
    "rating_asc": School.rating.asc().nullslast(),
}


class SchoolServiceError(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def list_schools(page=1, per_page=12, filters=None):
    """
    Paginated school list with optional search, filters, and sort.

    Supported filter keys:
      name, city, board, school_type, gender, hostel_available,
      min_fee, max_fee, facility_ids (list[int]), sort
    """
    filters = filters or {}
    page = max(1, page)
    per_page = min(max(1, per_page), 50)

    query = School.query.options(
        joinedload(School.images),
        joinedload(School.facility_links).joinedload(SchoolFacility.facility),
    )

    query = _apply_filters(query, filters)

    sort_key = (filters.get("sort") or "name").strip().lower()
    order_clause = SORT_OPTIONS.get(sort_key, School.name.asc())
    query = query.order_by(order_clause)

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return {
        "items": [school.to_dict(detailed=False) for school in pagination.items],
        "pagination": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "pages": pagination.pages,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev,
        },
        "filters_applied": _public_filters(filters),
    }


def get_filter_options():
    """Distinct values useful for frontend filter dropdowns."""
    cities = [
        row[0]
        for row in db.session.query(School.city)
        .filter(School.city.isnot(None))
        .distinct()
        .order_by(School.city.asc())
        .all()
        if row[0]
    ]
    boards = [
        row[0]
        for row in db.session.query(School.board)
        .filter(School.board.isnot(None))
        .distinct()
        .order_by(School.board.asc())
        .all()
        if row[0]
    ]
    school_types = [
        row[0]
        for row in db.session.query(School.school_type)
        .filter(School.school_type.isnot(None))
        .distinct()
        .order_by(School.school_type.asc())
        .all()
        if row[0]
    ]
    genders = [
        row[0]
        for row in db.session.query(School.gender)
        .filter(School.gender.isnot(None))
        .distinct()
        .order_by(School.gender.asc())
        .all()
        if row[0]
    ]
    facilities = [f.to_dict() for f in Facility.query.order_by(Facility.name.asc()).all()]
    return {
        "cities": cities,
        "boards": boards,
        "school_types": school_types,
        "genders": genders,
        "facilities": facilities,
        "sort_options": [
            {"value": "name", "label": "Name (A–Z)"},
            {"value": "fee_asc", "label": "Fee: low to high"},
            {"value": "fee_desc", "label": "Fee: high to low"},
            {"value": "rating", "label": "Rating"},
        ],
    }


def list_facilities():
    return [f.to_dict() for f in Facility.query.order_by(Facility.name.asc()).all()]


def _apply_filters(query, filters):
    name = (filters.get("name") or "").strip()
    if name:
        query = query.filter(School.name.ilike(f"%{name}%"))

    city = (filters.get("city") or "").strip()
    if city:
        query = query.filter(School.city.ilike(f"%{city}%"))

    board = (filters.get("board") or "").strip()
    if board:
        query = query.filter(func.lower(School.board) == board.lower())

    school_type = (filters.get("school_type") or "").strip()
    if school_type:
        query = query.filter(func.lower(School.school_type) == school_type.lower())

    gender = (filters.get("gender") or "").strip()
    if gender:
        query = query.filter(func.lower(School.gender) == gender.lower())

    hostel = filters.get("hostel_available")
    if hostel is not None:
        query = query.filter(School.hostel_available.is_(bool(hostel)))

    # Fee range overlap: school fees intersect [min_fee, max_fee]
    min_fee = filters.get("min_fee")
    max_fee = filters.get("max_fee")
    if min_fee is not None:
        query = query.filter(
            or_(School.max_fee.is_(None), School.max_fee >= min_fee)
        )
    if max_fee is not None:
        query = query.filter(
            or_(School.min_fee.is_(None), School.min_fee <= max_fee)
        )

    facility_ids = filters.get("facility_ids") or []
    if facility_ids:
        # School must have ALL selected facilities
        for facility_id in facility_ids:
            query = query.filter(
                School.id.in_(
                    db.session.query(SchoolFacility.school_id).filter(
                        SchoolFacility.facility_id == facility_id
                    )
                )
            )

    return query


def _public_filters(filters):
    """Echo applied filters (JSON-safe) back to the client."""
    return {
        "name": filters.get("name") or None,
        "city": filters.get("city") or None,
        "board": filters.get("board") or None,
        "school_type": filters.get("school_type") or None,
        "gender": filters.get("gender") or None,
        "hostel_available": filters.get("hostel_available"),
        "min_fee": filters.get("min_fee"),
        "max_fee": filters.get("max_fee"),
        "facility_ids": filters.get("facility_ids") or [],
        "sort": filters.get("sort") or "name",
    }


def get_school_or_404(school_id):
    school = (
        School.query.options(
            joinedload(School.fees),
            joinedload(School.images),
            joinedload(School.infrastructure),
            joinedload(School.facility_links).joinedload(SchoolFacility.facility),
        )
        .filter_by(id=school_id)
        .first()
    )
    if school is None:
        raise SchoolServiceError("School not found.", 404)
    return school


def create_school(cleaned):
    school = School(
        name=cleaned["name"],
        city=cleaned["city"],
        description=cleaned.get("description"),
        address=cleaned.get("address"),
        state=cleaned.get("state"),
        board=cleaned.get("board"),
        school_type=cleaned.get("school_type"),
        gender=cleaned.get("gender"),
        min_fee=cleaned.get("min_fee"),
        max_fee=cleaned.get("max_fee"),
        hostel_available=cleaned.get("hostel_available", False),
        rating=cleaned.get("rating") if cleaned.get("rating") is not None else 4.0,
        phone=cleaned.get("phone"),
        email=cleaned.get("email"),
        website=cleaned.get("website"),
        admission_process=cleaned.get("admission_process"),
        academic_info=cleaned.get("academic_info"),
        sports_info=cleaned.get("sports_info"),
        transport_info=cleaned.get("transport_info"),
        hostel_info=cleaned.get("hostel_info"),
    )
    db.session.add(school)
    db.session.flush()

    _apply_nested(school, cleaned)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise SchoolServiceError("Unable to create school. Please try again.", 500)

    return get_school_or_404(school.id)


def update_school(school_id, cleaned):
    school = get_school_or_404(school_id)

    scalar_fields = (
        "name",
        "description",
        "address",
        "city",
        "state",
        "board",
        "school_type",
        "gender",
        "min_fee",
        "max_fee",
        "hostel_available",
        "rating",
        "phone",
        "email",
        "website",
        "admission_process",
        "academic_info",
        "sports_info",
        "transport_info",
        "hostel_info",
    )
    for field in scalar_fields:
        if field in cleaned:
            setattr(school, field, cleaned[field])

    _apply_nested(school, cleaned, replace_existing=True)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise SchoolServiceError("Unable to update school. Please try again.", 500)

    return get_school_or_404(school.id)


def delete_school(school_id):
    school = get_school_or_404(school_id)
    try:
        db.session.delete(school)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise SchoolServiceError("Unable to delete school. Please try again.", 500)
    return True


def get_school_fees(school_id):
    school = get_school_or_404(school_id)
    return [fee.to_dict() for fee in school.fees]


def get_school_facilities(school_id):
    school = get_school_or_404(school_id)
    return [facility.to_dict() for facility in school.facilities]


def get_school_infrastructure(school_id):
    school = get_school_or_404(school_id)
    return [item.to_dict() for item in school.infrastructure]


def get_school_images(school_id):
    school = get_school_or_404(school_id)
    return [image.to_dict() for image in school.images]


def _apply_nested(school, cleaned, replace_existing=False):
    if "facility_ids" in cleaned:
        _set_facilities(school, cleaned["facility_ids"])

    if "fees" in cleaned:
        if replace_existing:
            school.fees.clear()
            db.session.flush()
        for fee in cleaned["fees"]:
            school.fees.append(SchoolFee(**fee))

    if "images" in cleaned:
        if replace_existing:
            school.images.clear()
            db.session.flush()
        for image in cleaned["images"]:
            school.images.append(SchoolImage(**image))

    if "infrastructure" in cleaned:
        if replace_existing:
            school.infrastructure.clear()
            db.session.flush()
        for item in cleaned["infrastructure"]:
            school.infrastructure.append(Infrastructure(**item))


def _set_facilities(school, facility_ids):
    unique_ids = list(dict.fromkeys(facility_ids))
    if unique_ids:
        found = Facility.query.filter(Facility.id.in_(unique_ids)).all()
        found_ids = {f.id for f in found}
        missing = [fid for fid in unique_ids if fid not in found_ids]
        if missing:
            raise SchoolServiceError(
                f"Unknown facility_ids: {missing}",
                400,
            )

    school.facility_links.clear()
    db.session.flush()
    for facility_id in unique_ids:
        school.facility_links.append(
            SchoolFacility(school_id=school.id, facility_id=facility_id)
        )

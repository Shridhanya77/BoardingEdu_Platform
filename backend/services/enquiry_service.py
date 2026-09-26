"""Admission enquiry business logic."""

from sqlalchemy.orm import joinedload

from extensions import db
from models import AdmissionEnquiry, ENQUIRY_STATUSES
from services.school_service import get_school_or_404


class EnquiryServiceError(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def create_enquiry(user_id, cleaned):
    get_school_or_404(cleaned["school_id"])

    enquiry = AdmissionEnquiry(
        user_id=user_id,
        school_id=cleaned["school_id"],
        student_name=cleaned["student_name"],
        parent_name=cleaned["parent_name"],
        class_name=cleaned.get("class_name"),
        academic_year=cleaned.get("academic_year"),
        phone=cleaned.get("phone"),
        email=cleaned.get("email"),
        message=cleaned.get("message"),
        status="Pending",
    )
    try:
        db.session.add(enquiry)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise EnquiryServiceError("Unable to submit enquiry.", 500)

    return _load_enquiry(enquiry.id)


def list_enquiries_for_user(user_id):
    rows = (
        AdmissionEnquiry.query.options(
            joinedload(AdmissionEnquiry.school),
            joinedload(AdmissionEnquiry.user),
        )
        .filter_by(user_id=user_id)
        .order_by(AdmissionEnquiry.created_at.desc())
        .all()
    )
    return [row.to_dict() for row in rows]


def list_all_enquiries(status=None):
    query = AdmissionEnquiry.query.options(
        joinedload(AdmissionEnquiry.school),
        joinedload(AdmissionEnquiry.user),
    )
    if status:
        query = query.filter(AdmissionEnquiry.status == status)
    rows = query.order_by(AdmissionEnquiry.created_at.desc()).all()
    return [row.to_dict() for row in rows]


def get_enquiry_for_user(enquiry_id, user):
    enquiry = _load_enquiry(enquiry_id)
    if enquiry is None:
        raise EnquiryServiceError("Enquiry not found.", 404)
    if user.role != "admin" and enquiry.user_id != user.id:
        raise EnquiryServiceError("You do not have access to this enquiry.", 403)
    return enquiry.to_dict()


def update_enquiry_status(enquiry_id, status):
    if status not in ENQUIRY_STATUSES:
        raise EnquiryServiceError(
            f"status must be one of: {', '.join(ENQUIRY_STATUSES)}.",
            400,
        )
    enquiry = db.session.get(AdmissionEnquiry, enquiry_id)
    if enquiry is None:
        raise EnquiryServiceError("Enquiry not found.", 404)
    enquiry.status = status
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise EnquiryServiceError("Unable to update enquiry status.", 500)
    return _load_enquiry(enquiry_id).to_dict()


def _load_enquiry(enquiry_id):
    return (
        AdmissionEnquiry.query.options(
            joinedload(AdmissionEnquiry.school),
            joinedload(AdmissionEnquiry.user),
        )
        .filter_by(id=enquiry_id)
        .first()
    )

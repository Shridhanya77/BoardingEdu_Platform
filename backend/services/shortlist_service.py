"""Shortlist business logic."""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from extensions import db
from models import School, SchoolFacility, Shortlist
from services.school_service import get_school_or_404


class ShortlistServiceError(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def list_user_shortlists(user_id):
    rows = (
        Shortlist.query.options(
            joinedload(Shortlist.school)
            .joinedload(School.images),
            joinedload(Shortlist.school)
            .joinedload(School.facility_links)
            .joinedload(SchoolFacility.facility),
        )
        .filter_by(user_id=user_id)
        .order_by(Shortlist.created_at.desc())
        .all()
    )
    return [row.to_dict() for row in rows]


def add_shortlist(user_id, school_id):
    get_school_or_404(school_id)

    existing = Shortlist.query.filter_by(user_id=user_id, school_id=school_id).first()
    if existing:
        raise ShortlistServiceError("School is already in your shortlist.", 409)

    row = Shortlist(user_id=user_id, school_id=school_id)
    try:
        db.session.add(row)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ShortlistServiceError("School is already in your shortlist.", 409)
    except Exception:
        db.session.rollback()
        raise ShortlistServiceError("Unable to shortlist school.", 500)

    return (
        Shortlist.query.options(joinedload(Shortlist.school))
        .filter_by(id=row.id)
        .first()
        .to_dict()
    )


def remove_shortlist(user_id, school_id):
    row = Shortlist.query.filter_by(user_id=user_id, school_id=school_id).first()
    if row is None:
        raise ShortlistServiceError("School is not in your shortlist.", 404)
    try:
        db.session.delete(row)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise ShortlistServiceError("Unable to remove shortlist.", 500)
    return True


def is_shortlisted(user_id, school_id):
    return (
        Shortlist.query.filter_by(user_id=user_id, school_id=school_id).first()
        is not None
    )

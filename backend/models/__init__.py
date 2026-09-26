"""
SQLAlchemy models for BoardingEdu.

Import this package so all tables register with `db.Model.metadata`
before `db.create_all()` runs.
"""

from models.user import User
from models.facility import Facility, SchoolFacility
from models.school import School, SchoolFee, SchoolImage, Infrastructure
from models.shortlist import Shortlist
from models.enquiry import AdmissionEnquiry, ENQUIRY_STATUSES

__all__ = [
    "User",
    "Facility",
    "SchoolFacility",
    "School",
    "SchoolFee",
    "SchoolImage",
    "Infrastructure",
    "Shortlist",
    "AdmissionEnquiry",
    "ENQUIRY_STATUSES",
]

"""Admission enquiry model."""

from datetime import datetime, timezone

from extensions import db

ENQUIRY_STATUSES = ("Pending", "Contacted", "In Review", "Closed")


def utcnow():
    return datetime.now(timezone.utc)


class AdmissionEnquiry(db.Model):
    __tablename__ = "admission_enquiries"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    school_id = db.Column(
        db.Integer, db.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False
    )
    student_name = db.Column(db.String(120), nullable=False)
    parent_name = db.Column(db.String(120), nullable=False)
    class_name = db.Column(db.String(50))
    academic_year = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(255))
    message = db.Column(db.Text)
    status = db.Column(db.String(30), nullable=False, default="Pending", index=True)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow)
    updated_at = db.Column(
        db.DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )

    user = db.relationship("User", back_populates="enquiries")
    school = db.relationship("School", back_populates="enquiries")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "school_id": self.school_id,
            "student_name": self.student_name,
            "parent_name": self.parent_name,
            "class_name": self.class_name,
            "academic_year": self.academic_year,
            "phone": self.phone,
            "email": self.email,
            "message": self.message,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "school": (
                {
                    "id": self.school.id,
                    "name": self.school.name,
                    "city": self.school.city,
                }
                if self.school
                else None
            ),
            "user": (
                {
                    "id": self.user.id,
                    "name": self.user.name,
                    "email": self.user.email,
                }
                if self.user
                else None
            ),
        }

    def __repr__(self) -> str:
        return f"<AdmissionEnquiry {self.id} status={self.status}>"

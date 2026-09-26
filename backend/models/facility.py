"""Facility catalogue and school–facility association."""

from extensions import db


class Facility(db.Model):
    __tablename__ = "facilities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)

    school_links = db.relationship(
        "SchoolFacility", back_populates="facility", cascade="all, delete-orphan"
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }

    def __repr__(self) -> str:
        return f"<Facility {self.name}>"


class SchoolFacility(db.Model):
    """Many-to-many link between schools and facilities."""

    __tablename__ = "school_facilities"
    __table_args__ = (
        db.UniqueConstraint("school_id", "facility_id", name="uq_school_facility"),
    )

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(
        db.Integer, db.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False
    )
    facility_id = db.Column(
        db.Integer, db.ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False
    )

    school = db.relationship("School", back_populates="facility_links")
    facility = db.relationship("Facility", back_populates="school_links")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "school_id": self.school_id,
            "facility_id": self.facility_id,
            "facility": self.facility.to_dict() if self.facility else None,
        }

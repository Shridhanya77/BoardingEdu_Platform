"""School and related fee / image / infrastructure models."""

from datetime import datetime, timezone

from extensions import db


def utcnow():
    return datetime.now(timezone.utc)


class School(db.Model):
    __tablename__ = "schools"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text)
    address = db.Column(db.String(500))
    city = db.Column(db.String(100), nullable=False, index=True)
    state = db.Column(db.String(100))
    board = db.Column(db.String(50), index=True)  # CBSE, ICSE, IB, State, etc.
    school_type = db.Column(db.String(50))  # Day School, Boarding, Day-Boarding
    gender = db.Column(db.String(30))  # Co-ed, Boys, Girls
    min_fee = db.Column(db.Integer)
    max_fee = db.Column(db.Integer)
    hostel_available = db.Column(db.Boolean, default=False)
    # Demo rating (1.0–5.0) used for listing/sort — labelled as sample data in UI
    rating = db.Column(db.Float, default=4.0)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(255))
    website = db.Column(db.String(255))
    admission_process = db.Column(db.Text)
    academic_info = db.Column(db.Text)
    sports_info = db.Column(db.Text)
    transport_info = db.Column(db.Text)
    hostel_info = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow)
    updated_at = db.Column(
        db.DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )

    fees = db.relationship(
        "SchoolFee", back_populates="school", cascade="all, delete-orphan"
    )
    images = db.relationship(
        "SchoolImage", back_populates="school", cascade="all, delete-orphan"
    )
    infrastructure = db.relationship(
        "Infrastructure", back_populates="school", cascade="all, delete-orphan"
    )
    facility_links = db.relationship(
        "SchoolFacility", back_populates="school", cascade="all, delete-orphan"
    )
    shortlists = db.relationship(
        "Shortlist", back_populates="school", cascade="all, delete-orphan"
    )
    enquiries = db.relationship(
        "AdmissionEnquiry", back_populates="school", cascade="all, delete-orphan"
    )

    @property
    def facilities(self):
        return [link.facility for link in self.facility_links if link.facility]

    def to_dict(self, detailed: bool = False) -> dict:
        data = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "board": self.board,
            "school_type": self.school_type,
            "gender": self.gender,
            "min_fee": self.min_fee,
            "max_fee": self.max_fee,
            "hostel_available": self.hostel_available,
            "rating": self.rating,
            "phone": self.phone,
            "email": self.email,
            "website": self.website,
            "facilities": [f.to_dict() for f in self.facilities],
            "primary_image": self.images[0].image_url if self.images else None,
        }
        if detailed:
            data.update(
                {
                    "admission_process": self.admission_process,
                    "academic_info": self.academic_info,
                    "sports_info": self.sports_info,
                    "transport_info": self.transport_info,
                    "hostel_info": self.hostel_info,
                    "fees": [fee.to_dict() for fee in self.fees],
                    "images": [img.to_dict() for img in self.images],
                    "infrastructure": [item.to_dict() for item in self.infrastructure],
                    "created_at": (
                        self.created_at.isoformat() if self.created_at else None
                    ),
                    "updated_at": (
                        self.updated_at.isoformat() if self.updated_at else None
                    ),
                }
            )
        return data

    def __repr__(self) -> str:
        return f"<School {self.name} ({self.city})>"


class SchoolFee(db.Model):
    __tablename__ = "school_fees"

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(
        db.Integer, db.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False
    )
    class_name = db.Column(db.String(50), nullable=False)
    admission_fee = db.Column(db.Integer, default=0)
    tuition_fee = db.Column(db.Integer, default=0)
    hostel_fee = db.Column(db.Integer, default=0)
    transport_fee = db.Column(db.Integer, default=0)
    other_fee = db.Column(db.Integer, default=0)
    annual_fee = db.Column(db.Integer, default=0)

    school = db.relationship("School", back_populates="fees")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "school_id": self.school_id,
            "class_name": self.class_name,
            "admission_fee": self.admission_fee,
            "tuition_fee": self.tuition_fee,
            "hostel_fee": self.hostel_fee,
            "transport_fee": self.transport_fee,
            "other_fee": self.other_fee,
            "annual_fee": self.annual_fee,
        }


class SchoolImage(db.Model):
    __tablename__ = "school_images"

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(
        db.Integer, db.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False
    )
    image_url = db.Column(db.String(500), nullable=False)
    caption = db.Column(db.String(255))

    school = db.relationship("School", back_populates="images")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "school_id": self.school_id,
            "image_url": self.image_url,
            "caption": self.caption,
        }


class Infrastructure(db.Model):
    __tablename__ = "infrastructure"

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(
        db.Integer, db.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False
    )
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    school = db.relationship("School", back_populates="infrastructure")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "school_id": self.school_id,
            "category": self.category,
            "description": self.description,
        }

"""Parent/student school shortlist."""

from datetime import datetime, timezone

from extensions import db


def utcnow():
    return datetime.now(timezone.utc)


class Shortlist(db.Model):
    __tablename__ = "shortlists"
    __table_args__ = (
        db.UniqueConstraint("user_id", "school_id", name="uq_user_school_shortlist"),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    school_id = db.Column(
        db.Integer, db.ForeignKey("schools.id", ondelete="CASCADE"), nullable=False
    )
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow)

    user = db.relationship("User", back_populates="shortlists")
    school = db.relationship("School", back_populates="shortlists")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "school_id": self.school_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "school": self.school.to_dict() if self.school else None,
        }

    def __repr__(self) -> str:
        return f"<Shortlist user={self.user_id} school={self.school_id}>"

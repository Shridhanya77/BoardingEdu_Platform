"""Admin dashboard statistics and user listing."""

from models import AdmissionEnquiry, School, Shortlist, User


def get_dashboard_stats():
    total_schools = School.query.count()
    total_users = User.query.filter(User.role != "admin").count()
    total_shortlists = Shortlist.query.count()
    total_enquiries = AdmissionEnquiry.query.count()
    pending = AdmissionEnquiry.query.filter_by(status="Pending").count()
    contacted = AdmissionEnquiry.query.filter_by(status="Contacted").count()
    in_review = AdmissionEnquiry.query.filter_by(status="In Review").count()
    closed = AdmissionEnquiry.query.filter_by(status="Closed").count()

    return {
        "total_schools": total_schools,
        "total_users": total_users,
        "total_shortlists": total_shortlists,
        "total_enquiries": total_enquiries,
        "pending_enquiries": pending,
        "contacted_enquiries": contacted,
        "in_review_enquiries": in_review,
        "closed_enquiries": closed,
    }


def list_users():
    users = (
        User.query.filter(User.role != "admin")
        .order_by(User.created_at.desc())
        .all()
    )
    return [user.to_dict() for user in users]

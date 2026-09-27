# This file contains reusable SQLAlchemy queries.

from sqlalchemy import func

from models import (
    Company,
    Application,
    Interview
)


# DASHBOARD STATISTICS

def get_dashboard_statistics(db):

    total_applications = (
        db.query(Application)
        .count()
    )

    total_companies = (
        db.query(Company)
        .count()
    )

    total_interviews = (
        db.query(Interview)
        .count()
    )

    total_offers = (
        db.query(Application)
        .filter(
            Application.status == "Offer"
        )
        .count()
    )

    total_rejected = (
        db.query(Application)
        .filter(
            Application.status == "Rejected"
        )
        .count()
    )

    return {
        "applications": total_applications,
        "companies": total_companies,
        "interviews": total_interviews,
        "offers": total_offers,
        "rejected": total_rejected
    }



# APPLICATION STATUS

def get_status_counts(db):

    return (
        db.query(
            Application.status,
            func.count(Application.id)
        )
        .group_by(
            Application.status
        )
        .all()
    )

# APPLICATIONS BY COMPANY


def get_company_application_counts(db):

    return (
        db.query(
            Company.name,
            func.count(Application.id)
        )
        .outerjoin(
            Application,
            Company.id == Application.company_id
        )
        .group_by(
            Company.name
        )
        .all()
    )

# INTERVIEW STATUS

def get_interview_status_counts(db):

    return (
        db.query(
            Interview.status,
            func.count(Interview.id)
        )
        .group_by(
            Interview.status
        )
        .all()
    )
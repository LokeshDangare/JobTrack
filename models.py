from datetime import datetime, date

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    DateTime,
    ForeignKey,
    Float
)

from sqlalchemy.orm import relationship

from database import Base


# COMPANY TABLE

class Company(Base):

    __tablename__ = "companies"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name = Column(
        String(150),
        nullable=False
    )

    industry = Column(
        String(100)
    )

    location = Column(
        String(150)
    )

    website = Column(
        String(300)
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    # Relationship
    applications = relationship(
        "Application",
        back_populates="company",
        cascade="all, delete-orphan"
    )


# APPLICATION TABLE

class Application(Base):

    __tablename__ = "applications"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    company_id = Column(
        Integer,
        ForeignKey("companies.id"),
        nullable=False
    )

    job_title = Column(
        String(150),
        nullable=False
    )

    job_type = Column(
        String(50)
    )

    location = Column(
        String(150)
    )

    application_date = Column(
        Date,
        default=date.today
    )

    job_url = Column(
        String(500)
    )

    status = Column(
        String(50),
        default="Applied"
    )

    salary = Column(
        Float
    )

    notes = Column(
        Text
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    # Relationships

    company = relationship(
        "Company",
        back_populates="applications"
    )

    interviews = relationship(
        "Interview",
        back_populates="application",
        cascade="all, delete-orphan"
    )


# INTERVIEW TABLE

class Interview(Base):

    __tablename__ = "interviews"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    application_id = Column(
        Integer,
        ForeignKey("applications.id"),
        nullable=False
    )

    round_number = Column(
        Integer
    )

    interview_type = Column(
        String(100)
    )

    interview_date = Column(
        Date
    )

    status = Column(
        String(50),
        default="Scheduled"
    )

    interviewer = Column(
        String(150)
    )

    notes = Column(
        Text
    )

    # Relationship

    application = relationship(
        "Application",
        back_populates="interviews"
    )
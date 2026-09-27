import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# MYSQL CONFIGURATION

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "JobTrackDB")


# VALIDATION

if not DB_USER:
    raise ValueError("DB_USER is missing in .env")

if not DB_PASSWORD:
    raise ValueError("DB_PASSWORD is missing in .env")


# MYSQL CONNECTION URL

DATABASE_URL = (
    f"mysql+mysqlconnector://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# SQLALCHEMY ENGINE

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)


# SESSION

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

# BASE

Base = declarative_base()


# DATABASE SESSION

def get_db():

    return SessionLocal()


# CREATE TABLES

def init_db():

    from models import (
        Company,
        Application,
        Interview
    )

    Base.metadata.create_all(
        bind=engine
    )
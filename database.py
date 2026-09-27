import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "JobTrackDB")

if not DB_USER:
    raise ValueError("DB_USER is missing in .env")

if DB_PASSWORD is None:
    raise ValueError("DB_PASSWORD is missing in .env")

# Safely create MySQL connection URL.
# This correctly handles special characters such as @, #, !, $, etc.
from sqlalchemy.engine import URL

DATABASE_URL = URL.create(
    drivername="mysql+mysqlconnector",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=int(DB_PORT),
    database=DB_NAME
)

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()


def get_db():
    return SessionLocal()


def init_db():
    from models import Company, Application, Interview

    Base.metadata.create_all(bind=engine)
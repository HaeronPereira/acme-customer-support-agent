import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Load variables from .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL not found in .env")

# SQLAlchemy Engine
engine = create_engine(
    DATABASE_URL,
    echo=False  # Shows SQL queries in the console (great for debugging)
)

# Database Session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all models
Base = declarative_base()


def get_db():
    """
    FastAPI dependency for creating a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """
    Create all database tables.
    """
    Base.metadata.create_all(bind=engine)

def get_session():
    """
    Returns a database session for internal application use.
    """
    return SessionLocal()
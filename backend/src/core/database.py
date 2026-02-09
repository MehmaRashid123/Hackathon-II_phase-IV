"""
Database connection and session management.
Uses SQLModel for ORM and PostgreSQL as the database.
"""
from sqlmodel import create_engine, Session, SQLModel
from .config import settings


# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.ENVIRONMENT == "development",  # Log SQL in development
    pool_pre_ping=True,  # Verify connections before using
)


def get_session():
    """
    Dependency function to get database session.
    Yields a session and ensures it's closed after use.
    """
    with Session(engine) as session:
        yield session


def init_db():
    """
    Initialize database by creating all tables.
    Should be called on application startup.
    """
    SQLModel.metadata.create_all(engine)

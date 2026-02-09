"""
Database configuration and session management for Neon PostgreSQL.

This module provides:
- SQLModel engine configuration with connection pooling
- Database session dependency for FastAPI
- Database initialization utilities
"""

from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import QueuePool
import os
from typing import Generator
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get DATABASE_URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable is not set. "
        "Please configure it in .env file with your Neon PostgreSQL connection string."
    )

# Create SQLModel engine with connection pooling
# Max 20 connections as per plan.md performance requirements
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries in development
    poolclass=QueuePool,
    pool_size=10,  # Number of connections to maintain
    max_overflow=10,  # Additional connections when pool is exhausted (total max: 20)
    pool_pre_ping=True,  # Verify connections before using them
    pool_recycle=3600,  # Recycle connections after 1 hour
)


def create_db_and_tables():
    """
    Create all database tables defined in SQLModel models.

    Should be called once during application startup.
    """
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a database session.

    Yields:
        Session: SQLModel database session

    Usage:
        @app.get("/items")
        def get_items(session: Session = Depends(get_session)):
            items = session.exec(select(Item)).all()
            return items
    """
    with Session(engine) as session:
        yield session

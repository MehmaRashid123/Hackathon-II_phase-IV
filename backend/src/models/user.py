"""
User SQLModel for database schema.

Represents a registered user account with authentication credentials.
"""

from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid


class User(SQLModel, table=True):
    """
    User entity for authentication and authorization.

    Attributes:
        id: Unique identifier (UUID)
        email: User's email address (unique, used for login)
        hashed_password: Bcrypt-hashed password (never plain-text)
        created_at: Account creation timestamp
        updated_at: Last modification timestamp
    """

    __tablename__ = "users"

    # Primary key - UUID for security and scalability
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        nullable=False,
        description="Unique identifier for the user"
    )

    # Email - unique identifier for login
    email: str = Field(
        max_length=255,
        unique=True,
        index=True,
        nullable=False,
        description="User's email address (unique, used for authentication)"
    )

    # Password - always stored as bcrypt hash
    hashed_password: str = Field(
        max_length=255,
        nullable=False,
        description="Bcrypt-hashed password (60 chars for bcrypt, up to 255 for flexibility)"
    )

    # Timestamps - automatic tracking
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Account creation timestamp (UTC)"
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"onupdate": datetime.utcnow},
        description="Last modification timestamp (UTC, auto-updated)"
    )

    class Config:
        """SQLModel configuration."""
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        }

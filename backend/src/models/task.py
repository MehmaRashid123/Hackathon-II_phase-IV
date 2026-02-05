"""
Task SQLModel for persistent task storage.

This module defines the Task entity for the todo application.
Each task belongs to a single user and contains task details.
"""

from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional
import uuid


class Task(SQLModel, table=True):
    """
    Task model representing a todo item.

    **Schema Design**:
    - Each task belongs to one user (many-to-one relationship)
    - Foreign key constraint with CASCADE delete (user deleted → tasks deleted)
    - Indexes on user_id and created_at for efficient filtering and sorting

    **Fields**:
    - id: UUID primary key
    - title: Task title (1-500 characters, required)
    - description: Task description (0-5000 characters, optional)
    - is_completed: Completion status (default: False)
    - created_at: Timestamp of task creation (UTC)
    - updated_at: Timestamp of last update (UTC)
    - user_id: Owner's UUID (foreign key to users.id)
    """

    __tablename__ = "tasks"

    # Primary key
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        nullable=False,
        description="Unique identifier for the task"
    )

    # Task details
    title: str = Field(
        max_length=500,
        nullable=False,
        description="Task title (1-500 characters)"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=5000,
        nullable=True,
        description="Optional task description (0-5000 characters)"
    )

    is_completed: bool = Field(
        default=False,
        nullable=False,
        description="Task completion status (default: False)"
    )

    # Timestamps (UTC)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp of task creation (UTC)"
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp of last update (UTC)",
        sa_column_kwargs={"onupdate": datetime.utcnow}
    )

    # Foreign key to users table (CASCADE delete)
    user_id: uuid.UUID = Field(
        foreign_key="users.id",
        nullable=False,
        index=True,  # Index for efficient filtering by user
        description="Owner's UUID (foreign key to users.id with CASCADE delete)"
    )

    class Config:
        """SQLModel configuration."""
        # Add composite index on (user_id, created_at) for efficient sorting
        # This will be added in the Alembic migration
        indexes = [
            {"fields": ["user_id"]},  # Single index on user_id
            {"fields": ["user_id", "created_at"]},  # Composite index for sorting
        ]

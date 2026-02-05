"""
Activity SQLModel for audit logging and activity feed.

This module defines the Activity entity for tracking workspace changes.
Activities are logged asynchronously to minimize performance impact on CRUD operations.
"""

from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional
import uuid
from enum import Enum


class ActivityType(str, Enum):
    """Types of activities that can be logged."""
    TASK_CREATED = "TASK_CREATED"
    TASK_UPDATED = "TASK_UPDATED"
    TASK_STATUS_CHANGED = "TASK_STATUS_CHANGED"
    TASK_COMPLETED = "TASK_COMPLETED"
    TASK_DELETED = "TASK_DELETED"
    PROJECT_CREATED = "PROJECT_CREATED"
    PROJECT_UPDATED = "PROJECT_UPDATED"
    PROJECT_DELETED = "PROJECT_DELETED"
    MEMBER_ADDED = "MEMBER_ADDED"
    MEMBER_REMOVED = "MEMBER_REMOVED"
    MEMBER_ROLE_CHANGED = "MEMBER_ROLE_CHANGED"


class Activity(SQLModel, table=True):
    """
    Activity model for audit logging and activity feed.

    **Schema Design**:
    - Each activity belongs to one workspace (many-to-one relationship)
    - Each activity references one user who performed the action
    - Optional reference to task or project entity
    - Composite index on (workspace_id, created_at) for efficient feed queries
    - Automatic archiving/deletion strategy for old activities (30-90 days retention)

    **Fields**:
    - id: UUID primary key
    - workspace_id: Foreign key to workspaces.id
    - user_id: Foreign key to users.id (who performed the action)
    - activity_type: ActivityType enum
    - description: Human-readable description (e.g., "Task 'Build API' moved to Done")
    - task_id: Optional foreign key to tasks.id (if activity relates to task)
    - project_id: Optional foreign key to projects.id (if activity relates to project)
    - created_at: Timestamp of activity (UTC)
    """

    __tablename__ = "activities"

    # Primary key
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        nullable=False,
        description="Unique identifier for the activity"
    )

    # Foreign keys
    workspace_id: uuid.UUID = Field(
        foreign_key="workspaces.id",
        nullable=False,
        index=True,
        description="Foreign key to workspaces.id"
    )

    user_id: uuid.UUID = Field(
        foreign_key="users.id",
        nullable=False,
        index=True,
        description="Foreign key to users.id (who performed the action)"
    )

    # Activity details
    activity_type: ActivityType = Field(
        nullable=False,
        description="Type of activity (TASK_CREATED, TASK_UPDATED, etc.)"
    )

    description: str = Field(
        max_length=500,
        nullable=False,
        description="Human-readable description of the activity"
    )

    # Optional entity references
    task_id: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key="tasks.id",
        nullable=True,
        index=True,
        description="Optional foreign key to tasks.id (if activity relates to task)"
    )

    project_id: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key="projects.id",
        nullable=True,
        index=True,
        description="Optional foreign key to projects.id (if activity relates to project)"
    )

    # Timestamp
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        index=True,
        description="Timestamp of activity (UTC)"
    )

    # Relationships
    workspace: "Workspace" = Relationship(back_populates="activities")
    user: "User" = Relationship(back_populates="activities")
    task: Optional["Task"] = Relationship(back_populates="activities")
    project: Optional["Project"] = Relationship(back_populates="activities")

    class Config:
        """SQLModel configuration."""
        # Composite index on (workspace_id, created_at) for efficient feed queries
        indexes = [
            {"fields": ["workspace_id", "created_at"]},
        ]

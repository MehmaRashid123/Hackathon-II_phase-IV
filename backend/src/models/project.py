from typing import List, Optional
from datetime import datetime
import uuid

from sqlmodel import Field, Relationship, SQLModel

from backend.src.models.user import User  # Import User model
from backend.src.models.task import Task  # Import Task model for relationships
from backend.src.models.section import Section # Forward reference, will import when created


class Project(SQLModel, table=True):
    """
    Project model representing a container for tasks and sections.
    """

    __tablename__ = "projects"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        nullable=False,
        description="Unique identifier for the project"
    )
    name: str = Field(
        max_length=255,
        nullable=False,
        description="Name of the project"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp of project creation (UTC)"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp of last update (UTC)",
        sa_column_kwargs={"onupdate": datetime.utcnow}
    )

    user_id: uuid.UUID = Field(
        foreign_key="users.id",
        nullable=False,
        index=True,
        description="Owner's UUID (foreign key to users.id)"
    )

    # Workspace integration (007-interactive-workspace-views)
    workspace_id: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key="workspaces.id",
        nullable=True,
        index=True,
        description="Foreign key to workspaces.id (workspace this project belongs to)"
    )

    # Relationships
    user: User = Relationship(back_populates="projects")
    workspace: Optional["Workspace"] = Relationship(back_populates="projects")
    activities: List["Activity"] = Relationship(back_populates="project")
    sections: List["Section"] = Relationship(
        back_populates="project",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    tasks: List["Task"] = Relationship(
        back_populates="project",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

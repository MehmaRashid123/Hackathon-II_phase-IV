from typing import List, Optional
from datetime import datetime
import uuid

from sqlmodel import Field, Relationship, SQLModel


class Section(SQLModel, table=True):
    """
    Section model representing an organizational unit within a Project to group tasks.
    """

    __tablename__ = "sections"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        nullable=False,
        description="Unique identifier for the section"
    )
    name: str = Field(
        max_length=255,
        nullable=False,
        description="Name of the section"
    )
    order: int = Field(
        default=0,
        nullable=False,
        description="Order of the section within the project"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp of section creation (UTC)"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp of last update (UTC)",
        sa_column_kwargs={"onupdate": datetime.utcnow}
    )

    project_id: uuid.UUID = Field(
        foreign_key="project.id",
        nullable=False,
        index=True,
        description="Foreign key to the project this section belongs to"
    )

    # Relationships
    project: 'Project' = Relationship(back_populates="sections")
    tasks: List["Task"] = Relationship(
        back_populates="section"
    )

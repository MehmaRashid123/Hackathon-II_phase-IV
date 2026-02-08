from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

class Project(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    workspace_id: UUID = Field(foreign_key="workspace.id", index=True, nullable=False)
    created_by: UUID = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, sa_column_kwargs={"onupdate": datetime.utcnow})

    # Relationships
    workspace: "Workspace" = Relationship(back_populates="projects")
    creator: "User" = Relationship(back_populates="projects")
    sections: List["Section"] = Relationship(back_populates="project")
    tasks: List["Task"] = Relationship(back_populates="project")
    activities: List["Activity"] = Relationship(back_populates="project")

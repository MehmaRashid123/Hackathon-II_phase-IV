from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

class Workspace(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    created_by: UUID = Field(foreign_key="users.id", index=True) # User who created the workspace
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, sa_column_kwargs={"onupdate": datetime.utcnow})

    # Relationships
    creator: "User" = Relationship()
    members: List["WorkspaceMember"] = Relationship(back_populates="workspace")
    projects: List["Project"] = Relationship(back_populates="workspace")
    tasks: List["Task"] = Relationship(back_populates="workspace")
    activities: List["Activity"] = Relationship(back_populates="workspace")

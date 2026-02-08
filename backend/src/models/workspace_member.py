from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from enum import Enum

from sqlmodel import Field, Relationship, SQLModel

class WorkspaceRole(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"

class WorkspaceMember(SQLModel, table=True):
    __tablename__ = "workspacemember"
    
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    workspace_id: UUID = Field(foreign_key="workspace.id", primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", primary_key=True)
    role: WorkspaceRole = Field(default=WorkspaceRole.MEMBER) # Role of the user in this workspace
    joined_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    workspace: "Workspace" = Relationship(back_populates="members")
    user: "User" = Relationship(back_populates="workspace_members") # Assuming User model will have 'workspace_members' back_populates

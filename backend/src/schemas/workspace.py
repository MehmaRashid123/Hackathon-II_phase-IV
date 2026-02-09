from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from src.models.workspace_member import WorkspaceRole

# Workspace Schemas
class WorkspaceBase(BaseModel):
    name: str
    description: Optional[str] = None

class WorkspaceCreate(WorkspaceBase):
    pass

class WorkspaceUpdate(WorkspaceBase):
    name: Optional[str] = None

class WorkspaceRead(WorkspaceBase):
    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime
    members: List["WorkspaceMemberRead"] = [] # Forward reference

    class Config:
        from_attributes = True

# WorkspaceMember Schemas
class WorkspaceMemberBase(BaseModel):
    user_id: UUID
    role: WorkspaceRole = WorkspaceRole.MEMBER

class WorkspaceMemberCreate(WorkspaceMemberBase):
    pass

class WorkspaceMemberUpdate(BaseModel):
    role: WorkspaceRole

class WorkspaceMemberRead(WorkspaceMemberBase):
    id: UUID
    workspace_id: UUID
    joined_at: datetime
    user_email: Optional[str] = None # To display user email directly

    class Config:
        from_attributes = True

# Update forward references
WorkspaceRead.update_forward_refs()

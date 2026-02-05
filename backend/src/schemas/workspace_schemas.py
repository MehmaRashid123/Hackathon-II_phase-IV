"""
Pydantic schemas for Workspace API.

Request and response models for workspace management endpoints.
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List
import uuid
from backend.src.models.workspace import WorkspaceRole


# Request schemas
class WorkspaceCreate(BaseModel):
    """Schema for creating a new workspace."""
    name: str = Field(..., min_length=1, max_length=255, description="Workspace name")


class WorkspaceUpdate(BaseModel):
    """Schema for updating workspace details."""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Workspace name")


class WorkspaceMemberUpdate(BaseModel):
    """Schema for updating a workspace member's role."""
    role: WorkspaceRole = Field(..., description="New role for the member")


class WorkspaceMemberInvite(BaseModel):
    """Schema for inviting a user to a workspace."""
    user_id: uuid.UUID = Field(..., description="User ID to invite")
    role: WorkspaceRole = Field(default=WorkspaceRole.MEMBER, description="Role to assign")


# Response schemas
class WorkspaceMemberResponse(BaseModel):
    """Schema for workspace member in responses."""
    model_config = ConfigDict(from_attributes=True)

    workspace_id: uuid.UUID
    user_id: uuid.UUID
    role: WorkspaceRole
    joined_at: datetime


class WorkspaceResponse(BaseModel):
    """Schema for workspace in responses."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    created_at: datetime
    updated_at: datetime
    members: List[WorkspaceMemberResponse] = []


class WorkspaceListResponse(BaseModel):
    """Schema for listing workspaces."""
    workspaces: List[WorkspaceResponse]
    total: int

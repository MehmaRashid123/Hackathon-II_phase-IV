"""
Pydantic schemas for Activity API.

Request and response models for activity feed endpoints.
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List
import uuid
from backend.src.models.activity import ActivityType


# Response schemas
class ActivityResponse(BaseModel):
    """Schema for activity in responses."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    workspace_id: uuid.UUID
    user_id: uuid.UUID
    activity_type: ActivityType
    description: str
    task_id: Optional[uuid.UUID] = None
    project_id: Optional[uuid.UUID] = None
    created_at: datetime


class ActivityListResponse(BaseModel):
    """Schema for listing activities with pagination."""
    activities: List[ActivityResponse]
    total: int
    page: int = Field(..., ge=1, description="Current page number")
    page_size: int = Field(..., ge=1, le=100, description="Items per page")
    has_more: bool = Field(..., description="Whether there are more pages")

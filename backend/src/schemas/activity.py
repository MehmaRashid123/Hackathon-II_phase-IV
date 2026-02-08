from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from src.models.activity import ActivityType

class ActivityRead(BaseModel):
    id: UUID
    workspace_id: UUID
    user_id: UUID
    task_id: Optional[UUID] = None
    project_id: Optional[UUID] = None
    activity_type: ActivityType
    description: str
    created_at: datetime
    
    user_email: Optional[str] = None # For display purposes
    task_title: Optional[str] = None # For display purposes
    project_name: Optional[str] = None # For display purposes

    class Config:
        from_attributes = True

from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field as PydanticField

from src.models.task import TaskPriority, TaskStatus

# Shared Base Schemas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.TO_DO
    project_id: Optional[UUID] = None
    assigned_to: Optional[UUID] = None

class TaskCreate(TaskBase):
    # workspace_id and created_by will be set by the API based on context
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    project_id: Optional[UUID] = None
    assigned_to: Optional[UUID] = None

class TaskStatusUpdate(BaseModel):
    status: TaskStatus = PydanticField(..., description="The new status for the task.")

class TaskRead(TaskBase):
    id: UUID
    workspace_id: Optional[UUID] = None  # Optional for personal tasks
    created_by: Optional[UUID] = None  # Optional for personal tasks
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    
    creator_email: Optional[str] = None
    assignee_email: Optional[str] = None

    class Config:
        from_attributes = True


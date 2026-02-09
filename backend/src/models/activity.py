from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from enum import Enum

from sqlmodel import Field, Relationship, SQLModel

class ActivityType(str, Enum):
    TASK_CREATED = "task_created"
    TASK_STATUS_CHANGED = "task_status_changed"
    TASK_PRIORITY_CHANGED = "task_priority_changed"
    TASK_ASSIGNED = "task_assigned"
    TASK_DELETED = "task_deleted"
    WORKSPACE_CREATED = "workspace_created"
    WORKSPACE_MEMBER_ADDED = "workspace_member_added"
    WORKSPACE_MEMBER_ROLE_CHANGED = "workspace_member_role_changed" # Added
    WORKSPACE_DELETED = "workspace_deleted" # Added
    WORKSPACE_UPDATED = "workspace_updated" # Added
    PROJECT_CREATED = "project_created" # Added for new functionality
    PROJECT_UPDATED = "project_updated" # Added for new functionality
    PROJECT_DELETED = "project_deleted" # Added for new functionality
    # ... other activity types

class Activity(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    workspace_id: UUID = Field(foreign_key="workspace.id", index=True, nullable=False)
    user_id: UUID = Field(foreign_key="users.id", index=True, nullable=False) # User who performed the action
    task_id: Optional[UUID] = Field(default=None, foreign_key="tasks.id", index=True) # Optional: if activity is task-related
    project_id: Optional[UUID] = Field(default=None, foreign_key="project.id", index=True) # Optional: if activity is project-related
    activity_type: ActivityType = Field(nullable=False)
    description: str = Field(nullable=False) # Human-readable description of the activity
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    workspace: "Workspace" = Relationship(back_populates="activities")
    user: "User" = Relationship(back_populates="activities") # Assuming User model will have 'activities' back_populates
    task: Optional["Task"] = Relationship(back_populates="activities")
    project: Optional["Project"] = Relationship(back_populates="activities") # Added for new functionality

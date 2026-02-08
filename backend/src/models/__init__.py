"""
Models package for the task management application.

Exports all SQLModel entities for database schema and ORM operations.
"""

from src.models.user import User
from src.models.workspace import Workspace
from src.models.workspace_member import WorkspaceMember, WorkspaceRole
from src.models.project import Project
from src.models.section import Section
from src.models.task import Task, TaskPriority, TaskStatus
from src.models.activity import Activity, ActivityType

__all__ = [
    "User",
    "Workspace",
    "WorkspaceMember",
    "WorkspaceRole",
    "Project",
    "Section",
    "Task",
    "TaskPriority",
    "TaskStatus",
    "Activity",
    "ActivityType",
]

# Update forward references for all models to resolve circular dependencies
for model_name in __all__:
    model = globals()[model_name]
    if hasattr(model, "update_forward_refs"):
        model.update_forward_refs()

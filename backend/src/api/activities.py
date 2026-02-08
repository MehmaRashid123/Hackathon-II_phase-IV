from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, func

from src.database import get_session
from src.models.user import User
from src.models.workspace_member import WorkspaceMember
from src.models.activity import Activity, ActivityType
from src.models.task import Task
from src.models.project import Project
from src.schemas.activity import ActivityRead
from src.middleware.auth import get_current_user

router = APIRouter(prefix="/workspaces/{workspace_id}/activities", tags=["Activities"])

@router.get("/", response_model=List[ActivityRead])
def list_workspace_activities(
    workspace_id: UUID,
    offset: int = 0,
    limit: int = 100,
    activity_type: Optional[ActivityType] = None,
    user_id: Optional[UUID] = None,
    task_id: Optional[UUID] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Retrieve a list of activities within a specific workspace.
    User must be a member of the workspace.
    """
    # Check if user is a member of the workspace
    member = session.exec(
        select(WorkspaceMember).where(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == current_user.id,
        )
    ).first()

    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not a member of this workspace."
        )

    statement = select(Activity, User, Task, Project).where(
        Activity.workspace_id == workspace_id
    )

    if activity_type:
        statement = statement.where(Activity.activity_type == activity_type)
    if user_id:
        statement = statement.where(Activity.user_id == user_id)
    if task_id:
        statement = statement.where(Activity.task_id == task_id)

    # Join with User, Task, Project for display purposes
    statement = statement.join(User, isouter=True) # User who performed the action
    statement = statement.join(Task, isouter=True) # Task related to the activity
    statement = statement.join(Project, isouter=True) # Project related to the activity

    statement = statement.order_by(Activity.created_at.desc()).offset(offset).limit(limit)
    
    activities_data = session.exec(statement).all()

    result = []
    for activity, user, task, project in activities_data:
        activity_read = ActivityRead.model_validate(activity)
        activity_read.user_email = user.email if user else None
        activity_read.task_title = task.title if task else None
        activity_read.project_name = project.name if project else None
        result.append(activity_read)

    return result

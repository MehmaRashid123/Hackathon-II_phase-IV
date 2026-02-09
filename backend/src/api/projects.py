from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from src.database import get_session
from src.models.user import User
from src.models.project import Project
from src.models.workspace_member import WorkspaceMember, WorkspaceRole
from src.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from src.middleware.auth import get_current_user
from src.services.activity_service import ActivityService
from src.models.activity import ActivityType

router = APIRouter(prefix="/workspaces/{workspace_id}/projects", tags=["Projects"])

@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(
    workspace_id: UUID,
    project_create: ProjectCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Create a new project within a specific workspace.
    User must be a member (at least MEMBER role) of the workspace.
    """
    if project_create.workspace_id != workspace_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Workspace ID in path and body do not match."
        )

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

    project = Project(
        **project_create.model_dump(),
        created_by=current_user.id,
        workspace_id=workspace_id # Ensure workspace_id is taken from path
    )
    session.add(project)
    session.commit()
    session.refresh(project)
    
    ActivityService.log_activity(
        db=session,
        workspace_id=workspace_id,
        user_id=current_user.id,
        activity_type=ActivityType.PROJECT_CREATED,
        description=f"Project '{project.name}' created in workspace '{workspace_id}'."
    )
    return ProjectRead.model_validate(project)

@router.get("/", response_model=List[ProjectRead])
def list_projects(
    workspace_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Retrieve a list of projects within a specific workspace.
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

    projects = session.exec(
        select(Project).where(Project.workspace_id == workspace_id)
    ).all()
    return [ProjectRead.model_validate(project) for project in projects]

@router.get("/{project_id}", response_model=ProjectRead)
def get_project_by_id(
    workspace_id: UUID,
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Retrieve a single project by its ID within a specific workspace.
    User must be a member of the workspace and the project must belong to the workspace.
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

    project = session.exec(
        select(Project).where(Project.id == project_id, Project.workspace_id == workspace_id)
    ).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found in this workspace."
        )
    return ProjectRead.model_validate(project)

@router.put("/{project_id}", response_model=ProjectRead)
def update_project(
    workspace_id: UUID,
    project_id: UUID,
    project_update: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Update an existing project.
    User must be an OWNER or ADMIN of the workspace.
    """
    member = session.exec(
        select(WorkspaceMember).where(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == current_user.id,
        )
    ).first()

    if not member or member.role not in [WorkspaceRole.OWNER, WorkspaceRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have permission to update projects in this workspace."
        )

    project = session.exec(
        select(Project).where(Project.id == project_id, Project.workspace_id == workspace_id)
    ).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found in this workspace."
        )

    # Track changes for activity logging
    changes = []
    old_name = project.name
    old_description = project.description

    update_data_dict = project_update.model_dump(exclude_unset=True)
    for field, value in update_data_dict.items():
        setattr(project, field, value)
        if field == "name" and old_name != value:
            changes.append(f"name from '{old_name}' to '{value}'")
        elif field == "description" and old_description != value:
            changes.append(f"description updated")

    session.add(project)
    session.commit()
    session.refresh(project)

    if changes:
        ActivityService.log_activity(
            db=session,
            workspace_id=workspace_id,
            user_id=current_user.id,
            project_id=project_id,
            activity_type=ActivityType.PROJECT_UPDATED,
            description=f"Project '{project.name}' updated: {', '.join(changes)}"
        )
    return ProjectRead.model_validate(project)

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    workspace_id: UUID,
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Delete a project.
    User must be an OWNER or ADMIN of the workspace.
    """
    member = session.exec(
        select(WorkspaceMember).where(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == current_user.id,
        )
    ).first()

    if not member or member.role not in [WorkspaceRole.OWNER, WorkspaceRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have permission to delete projects in this workspace."
        )

    project = session.exec(
        select(Project).where(Project.id == project_id, Project.workspace_id == workspace_id)
    ).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found in this workspace."
        )

    # Store project name before deleting for activity log
    project_name = project.name

    session.delete(project)
    session.commit()
    
    ActivityService.log_activity(
        db=session,
        workspace_id=workspace_id,
        user_id=current_user.id,
        project_id=project_id,
        activity_type=ActivityType.PROJECT_DELETED,
        description=f"Project '{project_name}' deleted from workspace '{workspace_id}'."
    )
    return

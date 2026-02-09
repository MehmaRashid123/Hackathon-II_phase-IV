from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from src.database import get_session
from src.models.user import User
from src.models.workspace import Workspace
from src.models.workspace_member import WorkspaceMember, WorkspaceRole
from src.schemas.workspace import (
    WorkspaceCreate,
    WorkspaceRead,
    WorkspaceUpdate,
    WorkspaceMemberCreate,
    WorkspaceMemberRead,
    WorkspaceMemberUpdate,
)
from src.middleware.auth import get_current_user
from src.services.activity_service import ActivityService
from src.models.activity import ActivityType

router = APIRouter(prefix="/workspaces", tags=["Workspaces"])

@router.post("/", response_model=WorkspaceRead, status_code=status.HTTP_201_CREATED)
def create_workspace(
    workspace_create: WorkspaceCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Create a new workspace.
    """
    workspace = Workspace(**workspace_create.model_dump(), created_by=current_user.id)
    session.add(workspace)
    session.commit()
    session.refresh(workspace)

    # Automatically make the creator an OWNER of the workspace
    workspace_member = WorkspaceMember(
        workspace_id=workspace.id,
        user_id=current_user.id,
        role=WorkspaceRole.OWNER,
    )
    session.add(workspace_member)
    session.commit()
    session.refresh(workspace_member)
    
    # Refresh workspace again to load members relationship
    session.refresh(workspace)
    
    # Log activity for workspace creation (non-blocking)
    try:
        ActivityService.log_activity(
            db=session,
            workspace_id=workspace.id,
            user_id=current_user.id,
            activity_type=ActivityType.WORKSPACE_CREATED,
            description=f"Workspace '{workspace.name}' created."
        )
    except Exception as e:
        # Activity logging is non-critical, rollback and continue
        session.rollback()
        print(f"Warning: Failed to log activity: {e}")
        # Re-attach the workspace to the session
        session.add(workspace)
        session.refresh(workspace)

    # Populate members with user_email for WorkspaceRead
    workspace_read = WorkspaceRead.model_validate(workspace)
    workspace_read.members = [
        WorkspaceMemberRead(
            id=member.id,
            workspace_id=member.workspace_id,
            user_id=member.user_id,
            role=member.role,
            joined_at=member.joined_at,
            user_email=current_user.email # Only creator's email is known here
        ) for member in workspace.members
    ]

    return workspace_read
@router.get("/", response_model=List[WorkspaceRead])
def list_workspaces(
    offset: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Retrieve a list of workspaces the current user is a member of.
    """
    statement = (
        select(Workspace)
        .join(WorkspaceMember)
        .where(WorkspaceMember.user_id == current_user.id)
        .offset(offset)
        .limit(limit)
    )
    workspaces = session.exec(statement).all()
    
    # Populate members with user_email for WorkspaceRead
    result = []
    for ws in workspaces:
        ws_read = WorkspaceRead.model_validate(ws)
        ws_members = session.exec(
            select(WorkspaceMember, User)
            .join(User)
            .where(WorkspaceMember.workspace_id == ws.id)
        ).all()
        ws_read.members = [
            WorkspaceMemberRead(
                id=member.WorkspaceMember.id,
                workspace_id=member.WorkspaceMember.workspace_id,
                user_id=member.WorkspaceMember.user_id,
                role=member.WorkspaceMember.role,
                joined_at=member.WorkspaceMember.joined_at,
                user_email=member.User.email
            ) for member in ws_members
        ]
        result.append(ws_read)
    
    return result

@router.get("/{workspace_id}", response_model=WorkspaceRead)
def get_workspace_by_id(
    workspace_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Retrieve a single workspace by its ID.
    """
    statement = (
        select(Workspace)
        .join(WorkspaceMember)
        .where(Workspace.id == workspace_id, WorkspaceMember.user_id == current_user.id)
    )
    workspace = session.exec(statement).first()

    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found or user not a member"
        )
    
    # Populate members with user_email for WorkspaceRead
    workspace_read = WorkspaceRead.model_validate(workspace)
    ws_members = session.exec(
        select(WorkspaceMember, User)
        .join(User)
        .where(WorkspaceMember.workspace_id == workspace.id)
    ).all()
    workspace_read.members = [
        WorkspaceMemberRead(
            id=member.WorkspaceMember.id,
            workspace_id=member.WorkspaceMember.workspace_id,
            user_id=member.WorkspaceMember.user_id,
            role=member.WorkspaceMember.role,
            joined_at=member.WorkspaceMember.joined_at,
            user_email=member.User.email
        ) for member in ws_members
    ]

    return workspace_read


@router.put("/{workspace_id}", response_model=WorkspaceRead)
def update_workspace(
    workspace_id: UUID,
    workspace_update: WorkspaceUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Update an existing workspace. Only workspace owners or admins can update.
    """
    # Check if user is a member and has permission
    member_statement = select(WorkspaceMember).where(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == current_user.id,
    )
    member = session.exec(member_statement).first()

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found or user not a member"
        )

    if member.role not in [WorkspaceRole.OWNER, WorkspaceRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have permission to update this workspace",
        )

    workspace = session.get(Workspace, workspace_id)
    if not workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")

    # Track changes for activity logging
    changes = []
    old_name = workspace.name
    old_description = workspace.description

    update_data_dict = workspace_update.model_dump(exclude_unset=True)
    for field, value in update_data_dict.items():
        setattr(workspace, field, value)
        if field == "name" and old_name != value:
            changes.append(f"name from '{old_name}' to '{value}'")
        elif field == "description" and old_description != value:
            changes.append(f"description updated")
    
    session.add(workspace)
    session.commit()
    session.refresh(workspace)

    if changes:
        ActivityService.log_activity(
            db=session,
            workspace_id=workspace.id,
            user_id=current_user.id,
            activity_type=ActivityType.WORKSPACE_UPDATED,
            description=f"Workspace '{workspace.name}' updated: {', '.join(changes)}"
        )

    # Populate members for WorkspaceRead
    workspace_read = WorkspaceRead.model_validate(workspace)
    ws_members = session.exec(
        select(WorkspaceMember, User)
        .join(User)
        .where(WorkspaceMember.workspace_id == workspace.id)
    ).all()
    workspace_read.members = [
        WorkspaceMemberRead(
            id=member.WorkspaceMember.id,
            workspace_id=member.WorkspaceMember.workspace_id,
            user_id=member.WorkspaceMember.user_id,
            role=member.WorkspaceMember.role,
            joined_at=member.WorkspaceMember.joined_at,
            user_email=member.User.email
        ) for member in ws_members
    ]

    return workspace_read


@router.delete("/{workspace_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workspace(
    workspace_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Delete a workspace. Only workspace owners can delete.
    """
    # Check if user is an OWNER
    member_statement = select(WorkspaceMember).where(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == current_user.id,
        WorkspaceMember.role == WorkspaceRole.OWNER,
    )
    member = session.exec(member_statement).first()

    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have permission (must be OWNER) to delete this workspace",
        )

    workspace = session.get(Workspace, workspace_id)
    if not workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")

    # Store workspace name before deleting for activity log
    workspace_name = workspace.name
    
    session.delete(workspace)
    session.commit()
    
    ActivityService.log_activity(
        db=session,
        workspace_id=workspace_id,
        user_id=current_user.id,
        activity_type=ActivityType.WORKSPACE_DELETED,
        description=f"Workspace '{workspace_name}' deleted."
    )
    return

# --- Workspace Member Endpoints ---

@router.post(
    "/{workspace_id}/members",
    response_model=WorkspaceMemberRead,
    status_code=status.HTTP_201_CREATED,
)
def add_workspace_member(
    workspace_id: UUID,
    member_create: WorkspaceMemberCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Add a new member to a workspace. Only workspace owners or admins can add members.
    """
    # Check if user has permission
    current_user_member_statement = select(WorkspaceMember).where(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == current_user.id,
    )
    current_user_member = session.exec(current_user_member_statement).first()

    if not current_user_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found or user not a member"
        )
    if current_user_member.role not in [WorkspaceRole.OWNER, WorkspaceRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have permission to add members to this workspace",
        )

    # Check if target user exists
    target_user = session.get(User, member_create.user_id)
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Target user not found"
        )

    # Check if target user is already a member
    existing_member_statement = select(WorkspaceMember).where(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == member_create.user_id,
    )
    existing_member = session.exec(existing_member_statement).first()
    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User is already a member of this workspace"
        )

    workspace_member = WorkspaceMember(
        workspace_id=workspace_id,
        user_id=member_create.user_id,
        role=member_create.role,
    )
    session.add(workspace_member)
    session.commit()
    session.refresh(workspace_member)
    
    ActivityService.log_activity(
        db=session,
        workspace_id=workspace_id,
        user_id=current_user.id,
        activity_type=ActivityType.WORKSPACE_MEMBER_ADDED,
        description=f"User '{target_user.email}' added to workspace as '{workspace_member.role.value}'."
    )

    return WorkspaceMemberRead(
        id=workspace_member.id,
        workspace_id=workspace_member.workspace_id,
        user_id=workspace_member.user_id,
        role=workspace_member.role,
        joined_at=workspace_member.joined_at,
        user_email=target_user.email
    )
@router.delete("/{workspace_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_workspace_member(
    workspace_id: UUID,
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Remove a member from a workspace. Only workspace owners or admins can remove members.
    A user cannot remove themselves if they are the only OWNER.
    """
    # Check if current user has permission
    current_user_member_statement = select(WorkspaceMember).where(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == current_user.id,
    )
    current_user_member = session.exec(current_user_member_statement).first()

    if not current_user_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found or user not a member"
        )
    if current_user_member.role not in [WorkspaceRole.OWNER, WorkspaceRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have permission to remove members from this workspace",
        )

    # Prevent removing the last owner
    if current_user_member.role == WorkspaceRole.OWNER and current_user_member.user_id == user_id:
        owner_count = session.exec(
            select(WorkspaceMember)
            .where(WorkspaceMember.workspace_id == workspace_id, WorkspaceMember.role == WorkspaceRole.OWNER)
        ).count()
        if owner_count == 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot remove the last owner of a workspace."
            )

    # Find the member to remove
    member_to_remove_statement = select(WorkspaceMember).where(
        WorkspaceMember.workspace_id == workspace_id, WorkspaceMember.user_id == user_id
    )
    member_to_remove = session.exec(member_to_remove_statement).first()

    if not member_to_remove:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Member not found in this workspace"
        )

    # Owners can remove anyone, admins can remove members/viewers
    if current_user_member.role == WorkspaceRole.ADMIN and member_to_remove.role in [WorkspaceRole.OWNER, WorkspaceRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins cannot remove owners or other admins."
        )

    session.delete(member_to_remove)
    session.commit()
    return

@router.patch("/{workspace_id}/members/{user_id}", response_model=WorkspaceMemberRead)
def update_workspace_member_role(
    workspace_id: UUID,
    user_id: UUID,
    member_update: WorkspaceMemberUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Update a member's role in a workspace. Only workspace owners or admins can update roles.
    Admins cannot promote to OWNER or change roles of OWNERs/ADMINs.
    """
    # Check if current user has permission
    current_user_member_statement = select(WorkspaceMember).where(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == current_user.id,
    )
    current_user_member = session.exec(current_user_member_statement).first()

    if not current_user_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found or user not a member"
        )
    if current_user_member.role not in [WorkspaceRole.OWNER, WorkspaceRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have permission to update member roles in this workspace",
        )

    # Find the member to update
    member_to_update_statement = select(WorkspaceMember).where(
        WorkspaceMember.workspace_id == workspace_id, WorkspaceMember.user_id == user_id
    )
    member_to_update = session.exec(member_to_update_statement).first()

    if not member_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Member not found in this workspace"
        )

    # Permission checks for role changes
    if current_user_member.role == WorkspaceRole.ADMIN:
        # Admins cannot change owner roles
        if member_to_update.role == WorkspaceRole.OWNER or member_update.role == WorkspaceRole.OWNER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admins cannot change owner roles or promote to owner.",
            )
        # Admins cannot change other admin roles
        if member_to_update.role == WorkspaceRole.ADMIN and user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admins cannot change roles of other admins.",
            )

    # Update the member's role
    old_role = member_to_update.role # Capture old role before update
    old_role = member_to_update.role # Capture old role before update
    member_to_update.role = member_update.role
    session.add(member_to_update)
    session.commit()
    session.refresh(member_to_update)
    
    target_user = session.get(User, member_to_update.user_id)
    if old_role != member_to_update.role:
        ActivityService.log_activity(
            db=session,
            workspace_id=workspace_id,
            user_id=current_user.id,
            activity_type=ActivityType.WORKSPACE_MEMBER_ROLE_CHANGED,
            description=f"User '{target_user.email}' role changed from '{old_role.value}' to '{member_to_update.role.value}' in workspace."
        )
    
    return WorkspaceMemberRead(
        id=member_to_update.id,
        workspace_id=member_to_update.workspace_id,
        user_id=member_to_update.user_id,
        role=member_to_update.role,
        joined_at=member_to_update.joined_at,
            user_email=target_user.email if target_user else None
        )

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from src.database import get_session
from src.models.user import User
from src.models.workspace_member import WorkspaceMember
from src.schemas.analytics import (
    StatusDistributionItem,
    PriorityBreakdownItem,
    CompletionTrendItem,
    WorkspaceAnalyticsRead,
)
from src.middleware.auth import get_current_user
from src.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/workspaces/{workspace_id}/analytics", tags=["Analytics"])

@router.get("/", response_model=WorkspaceAnalyticsRead)
def get_all_analytics_for_workspace(
    workspace_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    days: int = 7,
):
    """
    Retrieve all analytics data for a specific workspace.
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

    status_dist = AnalyticsService.get_status_distribution(session, workspace_id)
    priority_break = AnalyticsService.get_priority_breakdown(session, workspace_id)
    completion_trend = AnalyticsService.get_completion_trend(session, workspace_id, days)

    return WorkspaceAnalyticsRead(
        status_distribution=status_dist,
        priority_breakdown=priority_break,
        completion_trend=completion_trend,
    )

@router.get("/status", response_model=List[StatusDistributionItem])
def get_status_distribution(
    workspace_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Retrieve task status distribution for a specific workspace.
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
    return AnalyticsService.get_status_distribution(session, workspace_id)

@router.get("/priority", response_model=List[PriorityBreakdownItem])
def get_priority_breakdown(
    workspace_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Retrieve task priority breakdown for a specific workspace.
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
    return AnalyticsService.get_priority_breakdown(session, workspace_id)

@router.get("/completion-trend", response_model=List[CompletionTrendItem])
def get_completion_trend(
    workspace_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    days: int = 7,
):
    """
    Retrieve task completion trend for a specific workspace.
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
    return AnalyticsService.get_completion_trend(session, workspace_id, days)

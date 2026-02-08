"""
Activity logging service for workspace audit trail.

Provides asynchronous activity logging to minimize performance impact on CRUD operations.
"""

from sqlmodel import Session, select, func
from datetime import datetime, timedelta
from typing import Optional
import uuid

from src.models.activity import Activity, ActivityType
from src.schemas.activity_schemas import ActivityResponse, ActivityListResponse


class ActivityService:
    """Service for activity logging and feed queries."""

    @staticmethod
    def log_activity(
        db: Session,
        workspace_id: uuid.UUID,
        user_id: uuid.UUID,
        activity_type: ActivityType,
        description: str,
        task_id: Optional[uuid.UUID] = None,
        project_id: Optional[uuid.UUID] = None
    ) -> Activity:
        """
        Log a workspace activity.

        This method should be called asynchronously (background task) to avoid
        blocking the main request. Performance impact: < 10ms write operation.

        Args:
            db: Database session
            workspace_id: Workspace where activity occurred
            user_id: User who performed the action
            activity_type: Type of activity (TASK_CREATED, etc.)
            description: Human-readable description
            task_id: Optional task reference
            project_id: Optional project reference

        Returns:
            Created Activity entity
        """
        activity = Activity(
            workspace_id=workspace_id,
            user_id=user_id,
            activity_type=activity_type,
            description=description,
            task_id=task_id,
            project_id=project_id
        )
        db.add(activity)
        db.commit()
        db.refresh(activity)
        return activity

    @staticmethod
    def get_workspace_activities(
        db: Session,
        workspace_id: uuid.UUID,
        page: int = 1,
        page_size: int = 50
    ) -> ActivityListResponse:
        """
        Get paginated activity feed for a workspace.

        Performance: < 100ms with proper indexing on (workspace_id, created_at).

        Args:
            db: Database session
            workspace_id: Workspace to query
            page: Page number (1-indexed)
            page_size: Items per page (max 100)

        Returns:
            ActivityListResponse with paginated activities
        """
        # Enforce max page size
        page_size = min(page_size, 100)
        offset = (page - 1) * page_size

        # Query total count
        count_statement = select(func.count(Activity.id)).where(
            Activity.workspace_id == workspace_id
        )
        total = db.exec(count_statement).first() or 0

        # Query paginated activities (newest first)
        statement = (
            select(Activity)
            .where(Activity.workspace_id == workspace_id)
            .order_by(Activity.created_at.desc())
            .offset(offset)
            .limit(page_size)
        )
        activities = db.exec(statement).all()

        # Convert to response models
        activity_responses = [
            ActivityResponse.model_validate(activity)
            for activity in activities
        ]

        has_more = (offset + page_size) < total

        return ActivityListResponse(
            activities=activity_responses,
            total=total,
            page=page,
            page_size=page_size,
            has_more=has_more
        )

    @staticmethod
    def get_task_activities(
        db: Session,
        task_id: uuid.UUID,
        limit: int = 20
    ) -> list[ActivityResponse]:
        """
        Get recent activities for a specific task.

        Args:
            db: Database session
            task_id: Task to query
            limit: Maximum number of activities to return

        Returns:
            List of ActivityResponse (newest first)
        """
        statement = (
            select(Activity)
            .where(Activity.task_id == task_id)
            .order_by(Activity.created_at.desc())
            .limit(limit)
        )
        activities = db.exec(statement).all()

        return [
            ActivityResponse.model_validate(activity)
            for activity in activities
        ]

    @staticmethod
    def cleanup_old_activities(
        db: Session,
        retention_days: int = 90
    ) -> int:
        """
        Delete activities older than retention period.

        Should be run as a scheduled background job (e.g., daily cron).

        Args:
            db: Database session
            retention_days: Number of days to retain activities

        Returns:
            Number of activities deleted
        """
        cutoff_date = datetime.utcnow() - timedelta(days=retention_days)

        statement = select(Activity).where(Activity.created_at < cutoff_date)
        old_activities = db.exec(statement).all()

        count = len(old_activities)
        for activity in old_activities:
            db.delete(activity)

        db.commit()
        return count

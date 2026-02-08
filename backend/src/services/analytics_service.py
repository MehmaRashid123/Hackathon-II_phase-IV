from sqlmodel import Session, select, func
from typing import List, Dict
from datetime import date, timedelta
import uuid

from src.models.task import Task, TaskStatus, TaskPriority
from src.models.workspace_member import WorkspaceMember
from src.schemas.analytics import (
    StatusDistributionItem,
    PriorityBreakdownItem,
    CompletionTrendItem,
)
from src.models.user import User # Assuming User model exists and has an ID

class AnalyticsService:
    @staticmethod
    def get_status_distribution(session: Session, workspace_id: uuid.UUID) -> List[StatusDistributionItem]:
        """
        Calculates the distribution of tasks by status for a given workspace.
        """
        results = session.exec(
            select(Task.status, func.count(Task.id))
            .where(Task.workspace_id == workspace_id)
            .group_by(Task.status)
        ).all()
        return [StatusDistributionItem(status=status, count=count) for status, count in results]

    @staticmethod
    def get_priority_breakdown(session: Session, workspace_id: uuid.UUID) -> List[PriorityBreakdownItem]:
        """
        Calculates the breakdown of tasks by priority for a given workspace.
        """
        results = session.exec(
            select(Task.priority, func.count(Task.id))
            .where(Task.workspace_id == workspace_id)
            .group_by(Task.priority)
        ).all()
        return [PriorityBreakdownItem(priority=priority, count=count) for priority, count in results]

    @staticmethod
    def get_completion_trend(session: Session, workspace_id: uuid.UUID, days: int = 7) -> List[CompletionTrendItem]:
        """
        Calculates the daily trend of tasks created vs. tasks completed for a given workspace
        over the last 'days' number of days.
        """
        today = date.today()
        trends: Dict[date, Dict[str, int]] = {
            today - timedelta(days=i): {"tasks_created": 0, "tasks_completed": 0} for i in range(days)
        }

        # Tasks created
        created_results = session.exec(
            select(func.date(Task.created_at), func.count(Task.id))
            .where(Task.workspace_id == workspace_id)
            .where(Task.created_at >= today - timedelta(days=days))
            .group_by(func.date(Task.created_at))
        ).all()

        for d, count in created_results:
            trends[d]["tasks_created"] = count

        # Tasks completed
        completed_results = session.exec(
            select(func.date(Task.completed_at), func.count(Task.id))
            .where(Task.workspace_id == workspace_id)
            .where(Task.completed_at != None)
            .where(Task.completed_at >= today - timedelta(days=days))
            .group_by(func.date(Task.completed_at))
        ).all()

        for d, count in completed_results:
            trends[d]["tasks_completed"] = count

        # Convert to list of CompletionTrendItem, sorted by date
        sorted_trends = sorted(trends.items())
        return [
            CompletionTrendItem(date=d, tasks_created=data["tasks_created"], tasks_completed=data["tasks_completed"])
            for d, data in sorted_trends
        ]

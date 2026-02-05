"""
Analytics service for task data aggregation and visualization.

Provides efficient database-level aggregation for analytics charts.
Reduces 1000+ tasks to 10-30 data points for optimal chart rendering performance.
"""

from sqlmodel import Session, select, func, col
from datetime import datetime, timedelta
from typing import Dict, List, Any
import uuid

from backend.src.models.task import Task, StatusEnum, PriorityEnum
from backend.src.schemas.analytics_schemas import (
    AnalyticsResponse,
    AnalyticsSummary,
    StatusDistribution,
    PriorityBreakdown,
    CompletionTrendDataPoint,
)


class AnalyticsService:
    """Service for analytics data aggregation."""

    @staticmethod
    def get_status_distribution(
        db: Session,
        workspace_id: uuid.UUID
    ) -> List[StatusDistribution]:
        """
        Get task status distribution for pie chart.

        Aggregates tasks by status with counts and percentages.
        Performance: Single aggregation query, < 100ms for 1000+ tasks.
        """
        # Aggregate tasks by status
        statement = (
            select(
                Task.status,
                func.count(Task.id).label("count")
            )
            .where(Task.workspace_id == workspace_id)
            .group_by(Task.status)
        )
        results = db.exec(statement).all()

        # Calculate total and percentages
        total = sum(r.count for r in results)

        if total == 0:
            return []

        distribution = [
            StatusDistribution(
                status=str(status.value),
                count=count,
                percentage=round((count / total) * 100, 2)
            )
            for status, count in results
        ]

        return distribution

    @staticmethod
    def get_priority_breakdown(
        db: Session,
        workspace_id: uuid.UUID
    ) -> List[PriorityBreakdown]:
        """
        Get task priority breakdown for bar chart.

        Aggregates tasks by priority with completion status breakdown.
        Performance: Single aggregation query with CASE expression.
        """
        # Aggregate by priority with completion breakdown
        statement = (
            select(
                Task.priority,
                func.count(Task.id).label("total_count"),
                func.sum(
                    func.case(
                        (Task.status == StatusEnum.DONE, 1),
                        else_=0
                    )
                ).label("completed_count")
            )
            .where(Task.workspace_id == workspace_id)
            .group_by(Task.priority)
        )
        results = db.exec(statement).all()

        breakdown = [
            PriorityBreakdown(
                priority=str(priority.value),
                count=total_count,
                completed=completed_count or 0,
                pending=total_count - (completed_count or 0)
            )
            for priority, total_count, completed_count in results
        ]

        return breakdown

    @staticmethod
    def get_completion_trend(
        db: Session,
        workspace_id: uuid.UUID,
        days: int = 30
    ) -> List[CompletionTrendDataPoint]:
        """
        Get task completion trend for line/bar chart.

        Aggregates tasks created vs completed over the last N days.
        Performance: Two aggregation queries with date truncation, < 200ms.
        """
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=days)

        # Query for tasks created per day
        created_statement = (
            select(
                func.date(Task.created_at).label("date"),
                func.count(Task.id).label("count")
            )
            .where(
                Task.workspace_id == workspace_id,
                func.date(Task.created_at) >= start_date,
                func.date(Task.created_at) <= end_date
            )
            .group_by(func.date(Task.created_at))
        )
        created_results = db.exec(created_statement).all()
        created_by_date = {str(date): count for date, count in created_results}

        # Query for tasks completed per day
        completed_statement = (
            select(
                func.date(Task.updated_at).label("date"),
                func.count(Task.id).label("count")
            )
            .where(
                Task.workspace_id == workspace_id,
                Task.status == StatusEnum.DONE,
                func.date(Task.updated_at) >= start_date,
                func.date(Task.updated_at) <= end_date
            )
            .group_by(func.date(Task.updated_at))
        )
        completed_results = db.exec(completed_statement).all()
        completed_by_date = {str(date): count for date, count in completed_results}

        # Generate daily data points
        trend = []
        current_date = start_date
        while current_date <= end_date:
            date_str = str(current_date)
            trend.append(
                CompletionTrendDataPoint(
                    date=date_str,
                    created=created_by_date.get(date_str, 0),
                    completed=completed_by_date.get(date_str, 0)
                )
            )
            current_date += timedelta(days=1)

        return trend

    @staticmethod
    def get_analytics_summary(
        db: Session,
        workspace_id: uuid.UUID
    ) -> AnalyticsSummary:
        """
        Get analytics summary with overall task metrics.

        Performance: Single aggregation query with CASE expressions.
        """
        statement = (
            select(
                func.count(Task.id).label("total"),
                func.sum(
                    func.case(
                        (Task.status == StatusEnum.DONE, 1),
                        else_=0
                    )
                ).label("completed"),
                func.sum(
                    func.case(
                        (Task.status != StatusEnum.DONE, 1),
                        else_=0
                    )
                ).label("pending")
            )
            .where(Task.workspace_id == workspace_id)
        )
        result = db.exec(statement).first()

        total = result.total or 0
        completed = result.completed or 0
        pending = result.pending or 0
        completion_rate = round((completed / total) * 100, 2) if total > 0 else 0.0

        return AnalyticsSummary(
            total_tasks=total,
            completed_tasks=completed,
            pending_tasks=pending,
            completion_rate=completion_rate
        )

    @staticmethod
    def get_comprehensive_analytics(
        db: Session,
        workspace_id: uuid.UUID
    ) -> AnalyticsResponse:
        """
        Get comprehensive analytics with all chart data.

        Combines all analytics queries into a single response.
        Performance: < 500ms for 1000+ tasks (4-5 aggregation queries).
        """
        return AnalyticsResponse(
            workspace_id=str(workspace_id),
            summary=AnalyticsService.get_analytics_summary(db, workspace_id),
            status_distribution=AnalyticsService.get_status_distribution(db, workspace_id),
            priority_breakdown=AnalyticsService.get_priority_breakdown(db, workspace_id),
            completion_trend=AnalyticsService.get_completion_trend(db, workspace_id),
            generated_at=datetime.utcnow()
        )

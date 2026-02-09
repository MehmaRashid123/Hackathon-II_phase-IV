"""
Pydantic schemas for Analytics API.

Request and response models for analytics and data aggregation endpoints.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime


# Response schemas for individual chart types
class StatusDistribution(BaseModel):
    """Schema for status distribution pie chart data."""
    status: str = Field(..., description="Task status (TO_DO, IN_PROGRESS, REVIEW, DONE)")
    count: int = Field(..., ge=0, description="Number of tasks in this status")
    percentage: float = Field(..., ge=0, le=100, description="Percentage of total tasks")


class PriorityBreakdown(BaseModel):
    """Schema for priority workload bar chart data."""
    priority: str = Field(..., description="Task priority (LOW, MEDIUM, HIGH, URGENT)")
    count: int = Field(..., ge=0, description="Number of tasks with this priority")
    completed: int = Field(..., ge=0, description="Number of completed tasks with this priority")
    pending: int = Field(..., ge=0, description="Number of pending tasks with this priority")


class CompletionTrendDataPoint(BaseModel):
    """Schema for single data point in completion trend chart."""
    date: str = Field(..., description="Date in YYYY-MM-DD format")
    completed: int = Field(..., ge=0, description="Tasks completed on this date")
    created: int = Field(..., ge=0, description="Tasks created on this date")


class AnalyticsSummary(BaseModel):
    """Schema for overall analytics summary."""
    total_tasks: int = Field(..., ge=0, description="Total number of tasks")
    completed_tasks: int = Field(..., ge=0, description="Number of completed tasks")
    pending_tasks: int = Field(..., ge=0, description="Number of pending tasks")
    completion_rate: float = Field(..., ge=0, le=100, description="Percentage of tasks completed")


# Comprehensive analytics response
class AnalyticsResponse(BaseModel):
    """Schema for comprehensive analytics data."""
    workspace_id: str = Field(..., description="Workspace UUID")
    summary: AnalyticsSummary
    status_distribution: List[StatusDistribution] = Field(default_factory=list)
    priority_breakdown: List[PriorityBreakdown] = Field(default_factory=list)
    completion_trend: List[CompletionTrendDataPoint] = Field(default_factory=list)
    generated_at: datetime = Field(..., description="Timestamp when analytics were generated")


# Individual endpoint responses
class StatusDistributionResponse(BaseModel):
    """Schema for status distribution endpoint."""
    workspace_id: str
    status_distribution: List[StatusDistribution]


class PriorityBreakdownResponse(BaseModel):
    """Schema for priority breakdown endpoint."""
    workspace_id: str
    priority_breakdown: List[PriorityBreakdown]


class CompletionTrendResponse(BaseModel):
    """Schema for completion trend endpoint."""
    workspace_id: str
    completion_trend: List[CompletionTrendDataPoint]
    start_date: str = Field(..., description="Start date of trend period (YYYY-MM-DD)")
    end_date: str = Field(..., description="End date of trend period (YYYY-MM-DD)")

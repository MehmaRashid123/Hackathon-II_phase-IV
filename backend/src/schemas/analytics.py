from datetime import date
from typing import List, Optional
from pydantic import BaseModel

from src.models.task import TaskStatus, TaskPriority

class StatusDistributionItem(BaseModel):
    status: TaskStatus
    count: int

class PriorityBreakdownItem(BaseModel):
    priority: TaskPriority
    count: int

class CompletionTrendItem(BaseModel):
    date: date
    tasks_created: int
    tasks_completed: int

class WorkspaceAnalyticsRead(BaseModel):
    status_distribution: List[StatusDistributionItem]
    priority_breakdown: List[PriorityBreakdownItem]
    completion_trend: List[CompletionTrendItem]

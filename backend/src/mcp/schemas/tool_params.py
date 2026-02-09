"""
Pydantic schemas for MCP tool parameters.

These schemas define and validate the parameters for each MCP tool,
ensuring type safety and proper validation before tool execution.
"""
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class AddTaskParams(BaseModel):
    """
    Parameters for add_task tool.
    
    Attributes:
        user_id: UUID of the user (required for multi-tenant isolation)
        title: Task title (required, max 255 chars)
        description: Task description (optional, max 2000 chars)
    """
    user_id: str = Field(
        ...,
        description="UUID of the user creating the task",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Task title",
        examples=["Buy groceries"]
    )
    description: str = Field(
        default="",
        max_length=2000,
        description="Task description (optional)",
        examples=["Milk, eggs, bread"]
    )
    
    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        """Validate title is not empty or whitespace."""
        if not v.strip():
            raise ValueError("Title cannot be empty or whitespace")
        return v.strip()
    
    @field_validator('description')
    @classmethod
    def description_strip(cls, v: str) -> str:
        """Strip whitespace from description."""
        return v.strip() if v else ""


class ListTasksParams(BaseModel):
    """
    Parameters for list_tasks tool.
    
    Attributes:
        user_id: UUID of the user (required for multi-tenant isolation)
        completed: Optional filter by completion status
    """
    user_id: str = Field(
        ...,
        description="UUID of the user",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
    completed: Optional[bool] = Field(
        default=None,
        description="Filter by completion status (optional)",
        examples=[True, False, None]
    )


class CompleteTaskParams(BaseModel):
    """
    Parameters for complete_task tool.
    
    Attributes:
        user_id: UUID of the user (required for multi-tenant isolation)
        task_id: UUID of the task to complete
    """
    user_id: str = Field(
        ...,
        description="UUID of the user",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
    task_id: str = Field(
        ...,
        description="UUID of the task to complete",
        examples=["770e8400-e29b-41d4-a716-446655440000"]
    )


class DeleteTaskParams(BaseModel):
    """
    Parameters for delete_task tool.
    
    Attributes:
        user_id: UUID of the user (required for multi-tenant isolation)
        task_id: UUID of the task to delete
    """
    user_id: str = Field(
        ...,
        description="UUID of the user",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
    task_id: str = Field(
        ...,
        description="UUID of the task to delete",
        examples=["770e8400-e29b-41d4-a716-446655440000"]
    )


class UpdateTaskParams(BaseModel):
    """
    Parameters for update_task tool.
    
    Attributes:
        user_id: UUID of the user (required for multi-tenant isolation)
        task_id: UUID of the task to update
        title: New title (optional)
        description: New description (optional)
    """
    user_id: str = Field(
        ...,
        description="UUID of the user",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
    task_id: str = Field(
        ...,
        description="UUID of the task to update",
        examples=["770e8400-e29b-41d4-a716-446655440000"]
    )
    title: Optional[str] = Field(
        default=None,
        max_length=255,
        description="New task title (optional)",
        examples=["Buy groceries and milk"]
    )
    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="New task description (optional)",
        examples=["Don't forget organic milk"]
    )
    
    @field_validator('title')
    @classmethod
    def title_not_empty_if_provided(cls, v: Optional[str]) -> Optional[str]:
        """Validate title is not empty if provided."""
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty or whitespace if provided")
        return v.strip() if v else None
    
    @field_validator('description')
    @classmethod
    def description_strip_if_provided(cls, v: Optional[str]) -> Optional[str]:
        """Strip whitespace from description if provided."""
        return v.strip() if v else None
    
    def model_post_init(self, __context) -> None:
        """Validate that at least one field is provided."""
        if self.title is None and self.description is None:
            raise ValueError("At least one field (title or description) must be provided")

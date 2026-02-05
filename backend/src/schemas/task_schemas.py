"""
Task API request/response schemas.

This module defines Pydantic models for task-related API operations:
- TaskCreate: Schema for creating new tasks
- TaskUpdate: Schema for updating existing tasks
- TaskResponse: Schema for task responses (API output)

**Validation Rules**:
- Title: 1-500 characters (required)
- Description: 0-5000 characters (optional)
"""

from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
import uuid
from backend.src.models.task import StatusEnum


class TaskCreate(BaseModel):
    """
    Schema for creating a new task.

    **Validation**:
    - title: Required, 1-500 characters, must not be empty/whitespace-only
    - description: Optional, 0-5000 characters

    **Example**:
    ```json
    {
        "title": "Complete project documentation",
        "description": "Write comprehensive docs for the API"
    }
    ```
    """

    title: str = Field(
        min_length=1,
        max_length=500,
        description="Task title (1-500 characters, required)"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=5000,
        description="Task description (0-5000 characters, optional)"
    )

    @field_validator('title')
    @classmethod
    def validate_title_not_empty(cls, v: str) -> str:
        """Ensure title is not just whitespace."""
        if not v or not v.strip():
            raise ValueError('Title cannot be empty or whitespace-only')
        return v.strip()

    @field_validator('description')
    @classmethod
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        """Trim description whitespace if provided."""
        if v is not None:
            v = v.strip()
            # Return None if description is empty after trimming
            return v if v else None
        return v

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "title": "Complete project documentation",
                "description": "Write comprehensive API documentation with examples"
            }
        }


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task.

    **Note**: All fields are optional. Only provided fields will be updated.

    **Validation**:
    - title: Optional, 1-500 characters if provided
    - description: Optional, 0-5000 characters if provided (can be set to null to clear)

    **Example**:
    ```json
    {
        "title": "Updated task title",
        "description": "Updated description"
    }
    ```
    """

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=500,
        description="Updated task title (1-500 characters, optional)"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=5000,
        description="Updated task description (0-5000 characters, optional, null to clear)"
    )

    @field_validator('title')
    @classmethod
    def validate_title_not_empty(cls, v: Optional[str]) -> Optional[str]:
        """Ensure title is not just whitespace if provided."""
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError('Title cannot be empty or whitespace-only')
            return v
        return v

    @field_validator('description')
    @classmethod
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        """Trim description whitespace if provided."""
        if v is not None:
            v = v.strip()
            return v if v else None
        return v

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "title": "Updated: Complete project documentation",
                "description": "Updated description with more details"
            }
        }


class TaskResponse(BaseModel):
    """
    Schema for task responses (API output).

    This schema represents the complete task object returned by API endpoints.

    **Fields**:
    - id: Unique task identifier (UUID)
    - title: Task title
    - description: Task description (may be null)
    - is_completed: Completion status
    - status: Task status (TO_DO, IN_PROGRESS, REVIEW, DONE)
    - created_at: Timestamp of creation (UTC)
    - updated_at: Timestamp of last update (UTC)
    - user_id: Owner's user ID (UUID)
    - workspace_id: Workspace ID (UUID, optional)

    **Example**:
    ```json
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "title": "Complete project documentation",
        "description": "Write comprehensive API documentation",
        "is_completed": false,
        "status": "TO_DO",
        "created_at": "2024-01-01T12:00:00Z",
        "updated_at": "2024-01-01T12:00:00Z",
        "user_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
        "workspace_id": "450e8400-e29b-41d4-a716-446655440001"
    }
    ```
    """

    id: uuid.UUID = Field(description="Unique task identifier")
    title: str = Field(description="Task title")
    description: Optional[str] = Field(description="Task description (may be null)")
    is_completed: bool = Field(description="Completion status (true/false)")
    status: StatusEnum = Field(description="Task status")
    created_at: datetime = Field(description="Timestamp of task creation (UTC)")
    updated_at: datetime = Field(description="Timestamp of last update (UTC)")
    user_id: uuid.UUID = Field(description="Owner's user ID")
    workspace_id: Optional[uuid.UUID] = Field(default=None, description="Workspace ID (optional)")

    class Config:
        """Pydantic configuration."""
        from_attributes = True  # Enable ORM mode for SQLModel conversion
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Complete project documentation",
                "description": "Write comprehensive API documentation with examples",
                "is_completed": False,
                "status": "TO_DO",
                "created_at": "2024-01-01T12:00:00Z",
                "updated_at": "2024-01-01T12:00:00Z",
                "user_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
                "workspace_id": "450e8400-e29b-41d4-a716-446655440001"
            }
        }


class TaskStatusUpdate(BaseModel):
    """
    Schema for updating task status (Kanban drag-and-drop).

    **Validation**:
    - status: Required, must be one of: TO_DO, IN_PROGRESS, REVIEW, DONE

    **Example**:
    ```json
    {
        "status": "IN_PROGRESS"
    }
    ```
    """

    status: StatusEnum = Field(description="New task status (TO_DO, IN_PROGRESS, REVIEW, DONE)")

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "status": "IN_PROGRESS"
            }
        }


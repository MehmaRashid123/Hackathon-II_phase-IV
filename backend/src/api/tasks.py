"""
Task API endpoints.

This module defines all task-related API routes with strict user isolation.
Every endpoint enforces that users can only access their own tasks.

**Endpoints**:
- GET /api/{user_id}/tasks - List all user's tasks
- POST /api/{user_id}/tasks - Create new task
- GET /api/{user_id}/tasks/{id} - Get single task
- PUT /api/{user_id}/tasks/{id} - Update task
- PATCH /api/{user_id}/tasks/{id}/complete - Toggle completion
- DELETE /api/{user_id}/tasks/{id} - Delete task
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from src.database import get_session
from src.schemas.task_schemas import TaskCreate, TaskUpdate, TaskResponse
from src.services.task_service import TaskService
from src.middleware.auth import validate_user_id


# Create router for task endpoints
router = APIRouter(prefix="/api", tags=["Tasks"])


@router.get(
    "/{user_id}/tasks",
    response_model=List[TaskResponse],
    status_code=status.HTTP_200_OK,
    summary="List all user's tasks",
    description="""
    Retrieve all tasks for the authenticated user, ordered by creation date (newest first).

    **Security**: Requires valid JWT token. User can only access their own tasks.

    **Returns:**
    - HTTP 200: List of tasks (may be empty array if no tasks)
    - HTTP 401: If authentication fails
    - HTTP 403: If user_id in URL doesn't match authenticated user

    **Authorization**: Bearer {jwt_token}
    """
)
async def list_tasks(
    user_id: str = Depends(validate_user_id),
    session: Session = Depends(get_session)
) -> List[TaskResponse]:
    """
    List all tasks for authenticated user.

    The validate_user_id dependency ensures user_id matches the authenticated user.
    This prevents User A from accessing User B's tasks.

    Args:
        user_id: User ID from URL (validated to match JWT token)
        session: Database session (injected)

    Returns:
        List[TaskResponse]: All user's tasks, newest first (empty array if none)

    Example Request:
        GET /api/7c9e6679-7425-40de-944b-e07fc1f90ae7/tasks
        Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

    Example Response (200):
        [
            {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Complete project documentation",
                "description": "Write comprehensive API docs",
                "is_completed": false,
                "created_at": "2024-01-01T12:00:00Z",
                "updated_at": "2024-01-01T12:00:00Z",
                "user_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7"
            }
        ]

    Example Response (Empty, 200):
        []
    """
    # Get all tasks for user (ordered by created_at DESC)
    tasks = TaskService.get_user_tasks(session, user_id)

    # Return list of tasks (empty array if no tasks)
    return [TaskResponse.model_validate(task) for task in tasks]


@router.post(
    "/{user_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="""
    Create a new task for the authenticated user.

    **Security**: Requires valid JWT token. User can only create tasks for themselves.

    **Validation**:
    - Title: Required, 1-500 characters
    - Description: Optional, 0-5000 characters

    **Returns:**
    - HTTP 201: Task created successfully
    - HTTP 400: If user_id is invalid format
    - HTTP 401: If authentication fails
    - HTTP 403: If user_id in URL doesn't match authenticated user
    - HTTP 422: If validation fails (empty title, too long, etc.)

    **Authorization**: Bearer {jwt_token}
    """
)
async def create_task(
    task_data: TaskCreate,
    user_id: str = Depends(validate_user_id),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Create a new task for authenticated user.

    Args:
        task_data: TaskCreate schema with title and optional description
        user_id: User ID from URL (validated to match JWT token)
        session: Database session (injected)

    Returns:
        TaskResponse: Newly created task

    Raises:
        HTTPException 422: If validation fails (Pydantic)

    Example Request:
        POST /api/7c9e6679-7425-40de-944b-e07fc1f90ae7/tasks
        Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
        Content-Type: application/json

        {
            "title": "Complete project documentation",
            "description": "Write comprehensive API documentation"
        }

    Example Response (201):
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "title": "Complete project documentation",
            "description": "Write comprehensive API documentation",
            "is_completed": false,
            "created_at": "2024-01-01T12:00:00Z",
            "updated_at": "2024-01-01T12:00:00Z",
            "user_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7"
        }
    """
    # Create task via service layer
    new_task = TaskService.create_task(session, user_id, task_data)

    # Return created task
    return TaskResponse.model_validate(new_task)


@router.put(
    "/{user_id}/tasks/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Update an existing task",
    description="""
    Update a task's details (title and/or description).

    **Security**: Requires valid JWT token. User can only update their own tasks.

    **Note**: All fields in request body are optional. Only provided fields will be updated.

    **Returns:**
    - HTTP 200: Task updated successfully
    - HTTP 400: If task_id or user_id is invalid format
    - HTTP 401: If authentication fails
    - HTTP 403: If user tries to update another user's task
    - HTTP 404: If task not found
    - HTTP 422: If validation fails

    **Authorization**: Bearer {jwt_token}
    """
)
async def update_task(
    task_id: str,
    update_data: TaskUpdate,
    user_id: str = Depends(validate_user_id),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Update an existing task's details.

    Args:
        task_id: Task ID from URL path
        update_data: TaskUpdate schema with optional title/description
        user_id: User ID from URL (validated to match JWT token)
        session: Database session (injected)

    Returns:
        TaskResponse: Updated task

    Raises:
        HTTPException 404: If task not found
        HTTPException 403: If task belongs to another user
        HTTPException 422: If validation fails

    Example Request:
        PUT /api/7c9e6679-7425-40de-944b-e07fc1f90ae7/tasks/550e8400-e29b-41d4-a716-446655440000
        Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
        Content-Type: application/json

        {
            "title": "Updated: Complete project documentation",
            "description": "Updated description with more details"
        }

    Example Response (200):
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "title": "Updated: Complete project documentation",
            "description": "Updated description with more details",
            "is_completed": false,
            "created_at": "2024-01-01T12:00:00Z",
            "updated_at": "2024-01-01T14:00:00Z",
            "user_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7"
        }
    """
    # Update task via service layer (enforces ownership)
    updated_task = TaskService.update_task(session, user_id, task_id, update_data)

    # Return updated task
    return TaskResponse.model_validate(updated_task)


@router.patch(
    "/{user_id}/tasks/{task_id}/complete",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Toggle task completion status",
    description="""
    Toggle a task's completion status (completed ↔ not completed).

    **Security**: Requires valid JWT token. User can only toggle their own tasks.

    **Returns:**
    - HTTP 200: Task completion status toggled successfully
    - HTTP 400: If task_id or user_id is invalid format
    - HTTP 401: If authentication fails
    - HTTP 403: If user tries to toggle another user's task
    - HTTP 404: If task not found

    **Authorization**: Bearer {jwt_token}
    """
)
async def toggle_task_completion(
    task_id: str,
    user_id: str = Depends(validate_user_id),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Toggle task completion status.

    If task is completed, it becomes not completed (and vice versa).

    Args:
        task_id: Task ID from URL path
        user_id: User ID from URL (validated to match JWT token)
        session: Database session (injected)

    Returns:
        TaskResponse: Task with toggled completion status

    Raises:
        HTTPException 404: If task not found
        HTTPException 403: If task belongs to another user

    Example Request:
        PATCH /api/7c9e6679-7425-40de-944b-e07fc1f90ae7/tasks/550e8400-e29b-41d4-a716-446655440000/complete
        Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

    Example Response (200):
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "title": "Complete project documentation",
            "description": "Write comprehensive API documentation",
            "is_completed": true,  # Toggled from false to true
            "created_at": "2024-01-01T12:00:00Z",
            "updated_at": "2024-01-01T15:00:00Z",
            "user_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7"
        }
    """
    # Toggle completion status via service layer (enforces ownership)
    toggled_task = TaskService.toggle_task_completion(session, user_id, task_id)

    # Return updated task
    return TaskResponse.model_validate(toggled_task)


@router.get(
    "/{user_id}/tasks/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a specific task",
    description="""
    Retrieve details of a specific task by ID.

    **Security**: Requires valid JWT token. User can only access their own tasks.

    **Returns:**
    - HTTP 200: Task details returned successfully
    - HTTP 400: If task_id or user_id is invalid format
    - HTTP 401: If authentication fails
    - HTTP 403: If user tries to access another user's task
    - HTTP 404: If task not found

    **Authorization**: Bearer {jwt_token}
    """
)
async def get_task(
    task_id: str,
    user_id: str = Depends(validate_user_id),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Get a specific task by ID.

    Args:
        task_id: Task ID from URL path
        user_id: User ID from URL (validated to match JWT token)
        session: Database session (injected)

    Returns:
        TaskResponse: Task details

    Raises:
        HTTPException 404: If task not found
        HTTPException 403: If task belongs to another user

    Example Request:
        GET /api/7c9e6679-7425-40de-944b-e07fc1f90ae7/tasks/550e8400-e29b-41d4-a716-446655440000
        Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

    Example Response (200):
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "title": "Complete project documentation",
            "description": "Write comprehensive API documentation",
            "is_completed": false,
            "created_at": "2024-01-01T12:00:00Z",
            "updated_at": "2024-01-01T12:00:00Z",
            "user_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7"
        }
    """
    # Get task via service layer (enforces ownership)
    task = TaskService.get_task_by_id(session, user_id, task_id)

    # Return task details
    return TaskResponse.model_validate(task)


@router.delete(
    "/{user_id}/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="""
    Permanently delete a task.

    **Security**: Requires valid JWT token. User can only delete their own tasks.

    **Returns:**
    - HTTP 204: Task deleted successfully (no response body)
    - HTTP 400: If task_id or user_id is invalid format
    - HTTP 401: If authentication fails
    - HTTP 403: If user tries to delete another user's task
    - HTTP 404: If task not found

    **Authorization**: Bearer {jwt_token}
    """
)
async def delete_task(
    task_id: str,
    user_id: str = Depends(validate_user_id),
    session: Session = Depends(get_session)
) -> None:
    """
    Delete a task permanently.

    Args:
        task_id: Task ID from URL path
        user_id: User ID from URL (validated to match JWT token)
        session: Database session (injected)

    Returns:
        None (HTTP 204 No Content)

    Raises:
        HTTPException 404: If task not found
        HTTPException 403: If task belongs to another user

    Example Request:
        DELETE /api/7c9e6679-7425-40de-944b-e07fc1f90ae7/tasks/550e8400-e29b-41d4-a716-446655440000
        Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

    Example Response (204):
        No content (empty response body)
    """
    # Delete task via service layer (enforces ownership)
    TaskService.delete_task(session, user_id, task_id)

    # Return 204 No Content (FastAPI handles this automatically)
    return None

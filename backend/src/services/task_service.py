"""
Task business logic service layer.

This module provides the TaskService class which handles all task-related
business logic with strict user isolation. Every method ensures that users
can only access their own tasks.

**Security**: All methods filter by user_id to prevent horizontal privilege escalation.
"""

from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from fastapi import HTTPException, status
import uuid

from src.models.task import Task
from src.schemas.task_schemas import TaskCreate, TaskUpdate


class TaskService:
    """
    Service layer for task operations with user isolation.

    All methods enforce user isolation by filtering queries with user_id.
    This ensures User A cannot access User B's tasks.

    **Critical Security Pattern**:
    Every database query MUST include: `.where(Task.user_id == user_id)`
    """

    @staticmethod
    def get_user_tasks(session: Session, user_id: str) -> List[Task]:
        """
        Retrieve all tasks for a specific user, ordered by creation date (newest first).

        Args:
            session: Database session
            user_id: User's UUID (string format)

        Returns:
            List[Task]: All tasks belonging to the user, ordered by created_at DESC

        Example:
            tasks = TaskService.get_user_tasks(session, "7c9e6679-7425-40de-944b-e07fc1f90ae7")
            # Returns all tasks for that user, newest first
        """
        # Parse user_id to UUID
        user_uuid = uuid.UUID(user_id)

        # Query tasks filtered by user_id, ordered by created_at descending
        statement = (
            select(Task)
            .where(Task.user_id == user_uuid)
            .order_by(Task.created_at.desc())
        )

        tasks = session.exec(statement).all()
        return list(tasks)

    @staticmethod
    def create_task(session: Session, user_id: str, task_data: TaskCreate) -> Task:
        """
        Create a new task for a specific user.

        Args:
            session: Database session
            user_id: User's UUID (string format)
            task_data: TaskCreate schema with title and optional description

        Returns:
            Task: Newly created task object

        Raises:
            HTTPException 422: If validation fails (handled by Pydantic)

        Example:
            task_data = TaskCreate(title="Complete docs", description="Write API docs")
            task = TaskService.create_task(session, user_id, task_data)
        """
        # Parse user_id to UUID
        user_uuid = uuid.UUID(user_id)

        # Create new task with validated data
        new_task = Task(
            title=task_data.title,
            description=task_data.description,
            user_id=user_uuid,
            is_completed=False,  # Default to not completed
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        # Save to database
        session.add(new_task)
        session.commit()
        session.refresh(new_task)

        return new_task

    @staticmethod
    def get_task_by_id(session: Session, user_id: str, task_id: str) -> Task:
        """
        Retrieve a specific task by ID, ensuring it belongs to the user.

        **Security**: This method enforces user isolation by filtering by BOTH
        task_id AND user_id. User A cannot access User B's tasks.

        Args:
            session: Database session
            user_id: User's UUID (string format)
            task_id: Task's UUID (string format)

        Returns:
            Task: Task object if found and belongs to user

        Raises:
            HTTPException 404: If task not found or doesn't belong to user

        Example:
            task = TaskService.get_task_by_id(session, user_id, task_id)
        """
        # Parse UUIDs
        user_uuid = uuid.UUID(user_id)
        task_uuid = uuid.UUID(task_id)

        # Query task filtered by BOTH id AND user_id (security critical!)
        statement = (
            select(Task)
            .where(Task.id == task_uuid)
            .where(Task.user_id == user_uuid)
        )

        task = session.exec(statement).first()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} not found or you don't have permission to access it"
            )

        return task

    @staticmethod
    def update_task(
        session: Session,
        user_id: str,
        task_id: str,
        update_data: TaskUpdate
    ) -> Task:
        """
        Update a task's details, ensuring it belongs to the user.

        **Security**: Uses get_task_by_id which enforces user ownership.

        Args:
            session: Database session
            user_id: User's UUID (string format)
            task_id: Task's UUID (string format)
            update_data: TaskUpdate schema with optional title/description

        Returns:
            Task: Updated task object

        Raises:
            HTTPException 404: If task not found or doesn't belong to user
            HTTPException 403: If user tries to access another user's task

        Example:
            update_data = TaskUpdate(title="Updated title")
            task = TaskService.update_task(session, user_id, task_id, update_data)
        """
        # Get task (this enforces ownership via user_id check)
        task = TaskService.get_task_by_id(session, user_id, task_id)

        # Update only the fields that were provided
        if update_data.title is not None:
            task.title = update_data.title

        if update_data.description is not None:
            task.description = update_data.description

        # Update timestamp
        task.updated_at = datetime.utcnow()

        # Save changes
        session.add(task)
        session.commit()
        session.refresh(task)

        return task

    @staticmethod
    def delete_task(session: Session, user_id: str, task_id: str) -> None:
        """
        Delete a task, ensuring it belongs to the user.

        **Security**: Uses get_task_by_id which enforces user ownership.

        Args:
            session: Database session
            user_id: User's UUID (string format)
            task_id: Task's UUID (string format)

        Returns:
            None

        Raises:
            HTTPException 404: If task not found or doesn't belong to user
            HTTPException 403: If user tries to delete another user's task

        Example:
            TaskService.delete_task(session, user_id, task_id)
        """
        # Get task (this enforces ownership via user_id check)
        task = TaskService.get_task_by_id(session, user_id, task_id)

        # Delete from database
        session.delete(task)
        session.commit()

    @staticmethod
    def toggle_task_completion(session: Session, user_id: str, task_id: str) -> Task:
        """
        Toggle a task's completion status (completed ↔ not completed).

        **Security**: Uses get_task_by_id which enforces user ownership.

        Args:
            session: Database session
            user_id: User's UUID (string format)
            task_id: Task's UUID (string format)

        Returns:
            Task: Task with toggled is_completed status

        Raises:
            HTTPException 404: If task not found or doesn't belong to user
            HTTPException 403: If user tries to modify another user's task

        Example:
            task = TaskService.toggle_task_completion(session, user_id, task_id)
            # If task.is_completed was False, it's now True (and vice versa)
        """
        # Get task (this enforces ownership via user_id check)
        task = TaskService.get_task_by_id(session, user_id, task_id)

        # Flip the completion status
        task.is_completed = not task.is_completed

        # Update timestamp
        task.updated_at = datetime.utcnow()

        # Save changes
        session.add(task)
        session.commit()
        session.refresh(task)

        return task

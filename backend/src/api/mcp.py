"""
MCP API Router

Exposes MCP tools as REST API endpoints for the chatbot frontend.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from sqlmodel import Session

from src.database import engine
from src.services.task_service import TaskService
from src.models.task import Task

router = APIRouter(prefix="/api/mcp", tags=["MCP Tools"])


# Request/Response Models
class AddTaskRequest(BaseModel):
    user_id: str
    title: str
    description: Optional[str] = None


class ListTasksRequest(BaseModel):
    user_id: str
    completed: Optional[bool] = None


class CompleteTaskRequest(BaseModel):
    user_id: str
    task_id: str


class DeleteTaskRequest(BaseModel):
    user_id: str
    task_id: str


class UpdateTaskRequest(BaseModel):
    user_id: str
    task_id: str
    title: Optional[str] = None
    description: Optional[str] = None


# Helper function to serialize task
def serialize_task(task):
    """Serialize task to JSON-compatible dict"""
    return {
        "task_id": str(task.id),
        "title": task.title,
        "description": task.description,
        "completed": task.status == "DONE",
        "status": task.status,
        "priority": task.priority,
        "created_at": task.created_at.isoformat() if task.created_at else None,
        "updated_at": task.updated_at.isoformat() if task.updated_at else None,
        "completed_at": task.completed_at.isoformat() if task.completed_at else None,
    }


@router.post("/add_task")
async def add_task(request: AddTaskRequest):
    """
    Create a new task via MCP tool.
    
    Args:
        request: AddTaskRequest with user_id, title, and optional description
    
    Returns:
        Created task details
    """
    try:
        print(f"📝 Creating task: {request.title} for user {request.user_id}")
        
        with Session(engine) as session:
            # Create task directly without workspace requirement for chatbot
            from datetime import datetime
            task = Task(
                title=request.title,
                description=request.description or "",
                created_by=UUID(request.user_id),
                status="TO_DO",
                priority="MEDIUM",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(task)
            session.commit()
            session.refresh(task)
            
            print(f"✅ Task created successfully: {task.id}")
            return serialize_task(task)
    except Exception as e:
        print(f"❌ Error in add_task: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/list_tasks")
async def list_tasks(request: ListTasksRequest):
    """
    List all tasks for a user via MCP tool.
    
    Args:
        request: ListTasksRequest with user_id and optional completed filter
    
    Returns:
        List of tasks and count
    """
    try:
        with Session(engine) as session:
            # Get all tasks for user using the correct method
            tasks = TaskService.get_user_tasks(session, request.user_id)
            
            # Filter by completion status if specified
            if request.completed is not None:
                if request.completed:
                    tasks = [t for t in tasks if t.status == "DONE"]
                else:
                    tasks = [t for t in tasks if t.status != "DONE"]
            
            return {
                "tasks": [serialize_task(task) for task in tasks],
                "count": len(tasks)
            }
    except Exception as e:
        print(f"Error in list_tasks: {str(e)}")  # Debug logging
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/complete_task")
async def complete_task(request: CompleteTaskRequest):
    """
    Mark a task as complete via MCP tool.
    
    Args:
        request: CompleteTaskRequest with user_id and task_id
    
    Returns:
        Updated task details
    """
    try:
        with Session(engine) as session:
            # Get task
            task = session.get(Task, UUID(request.task_id))
            
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")
            
            # Verify ownership
            if str(task.created_by) != request.user_id:
                raise HTTPException(status_code=403, detail="Not authorized")
            
            # Update status
            task.status = "DONE"
            task.completed_at = datetime.utcnow()
            task.updated_at = datetime.utcnow()
            
            session.add(task)
            session.commit()
            session.refresh(task)
            
            return serialize_task(task)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in complete_task: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/delete_task")
async def delete_task(request: DeleteTaskRequest):
    """
    Delete a task via MCP tool.
    
    Args:
        request: DeleteTaskRequest with user_id and task_id
    
    Returns:
        Success message
    """
    try:
        with Session(engine) as session:
            # Get task
            task = session.get(Task, UUID(request.task_id))
            
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")
            
            # Verify ownership
            if str(task.created_by) != request.user_id:
                raise HTTPException(status_code=403, detail="Not authorized")
            
            session.delete(task)
            session.commit()
            
            return {
                "success": True,
                "message": "Task deleted successfully"
            }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in delete_task: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/update_task")
async def update_task(request: UpdateTaskRequest):
    """
    Update a task via MCP tool.
    
    Args:
        request: UpdateTaskRequest with user_id, task_id, and optional title/description
    
    Returns:
        Updated task details
    """
    try:
        if not request.title and not request.description:
            raise HTTPException(
                status_code=400,
                detail="At least one field (title or description) must be provided"
            )
        
        with Session(engine) as session:
            # Get task
            task = session.get(Task, UUID(request.task_id))
            
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")
            
            # Verify ownership
            if str(task.created_by) != request.user_id:
                raise HTTPException(status_code=403, detail="Not authorized")
            
            # Update fields
            if request.title:
                task.title = request.title
            if request.description:
                task.description = request.description
            
            task.updated_at = datetime.utcnow()
            
            session.add(task)
            session.commit()
            session.refresh(task)
            
            return serialize_task(task)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in update_task: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

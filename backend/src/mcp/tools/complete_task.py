"""
MCP Tool: complete_task

Marks a task as complete. This tool enables AI agents to mark tasks
as done when users indicate they've finished them.
"""
from uuid import UUID
from ..server import mcp_server
from ..schemas.tool_params import CompleteTaskParams
from ..utils import serialize_task, handle_tool_error, format_not_found_error
from ...core.database import Session, engine
from ...services.task_service import TaskService


@mcp_server.call_tool()
async def complete_task(name: str, arguments: dict) -> list[dict]:
    """
    MCP tool handler for completing a task.
    
    Args:
        name: Tool name (should be "complete_task")
        arguments: Tool arguments containing user_id and task_id
    
    Returns:
        List containing a single dict with updated task details or error
    
    Example:
        Input: {"user_id": "123...", "task_id": "770..."}
        Output: [{"task_id": "770...", "title": "Buy groceries", "completed": true, ...}]
    """
    try:
        # Validate parameters
        params = CompleteTaskParams(**arguments)
        
        # Complete task using service
        with Session(engine) as session:
            service = TaskService(session)
            task = service.complete_task(
                user_id=UUID(params.user_id),
                task_id=UUID(params.task_id)
            )
            
            if not task:
                return [format_not_found_error("Task", params.task_id)]
            
            # Return JSON-serializable result using centralized serializer
            return [serialize_task(task)]
    
    except Exception as e:
        # Use centralized error handler
        return [handle_tool_error(e)]


# Tool metadata for MCP server
complete_task.metadata = {
    "name": "complete_task",
    "description": "Mark a task as complete",
    "parameters": {
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "description": "UUID of the user"
            },
            "task_id": {
                "type": "string",
                "description": "UUID of the task to complete"
            }
        },
        "required": ["user_id", "task_id"]
    }
}

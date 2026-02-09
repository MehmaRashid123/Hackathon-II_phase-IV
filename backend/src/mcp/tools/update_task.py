"""
MCP Tool: update_task

Updates task details (title and/or description). This tool enables AI agents
to modify existing tasks based on user requests.
"""
from uuid import UUID
from ..server import mcp_server
from ..schemas.tool_params import UpdateTaskParams
from ..utils import serialize_task, handle_tool_error, format_not_found_error
from ...core.database import Session, engine
from ...services.task_service import TaskService


@mcp_server.call_tool()
async def update_task(name: str, arguments: dict) -> list[dict]:
    """
    MCP tool handler for updating a task.
    
    Args:
        name: Tool name (should be "update_task")
        arguments: Tool arguments containing user_id, task_id, and optional title/description
    
    Returns:
        List containing a single dict with updated task details or error
    
    Example:
        Input: {"user_id": "123...", "task_id": "770...", "title": "Buy groceries and milk"}
        Output: [{"task_id": "770...", "title": "Buy groceries and milk", ...}]
    """
    try:
        # Validate parameters
        params = UpdateTaskParams(**arguments)
        
        # Update task using service
        with Session(engine) as session:
            service = TaskService(session)
            task = service.update_task(
                user_id=UUID(params.user_id),
                task_id=UUID(params.task_id),
                title=params.title,
                description=params.description
            )
            
            if not task:
                return [format_not_found_error("Task", params.task_id)]
            
            # Return JSON-serializable result using centralized serializer
            return [serialize_task(task)]
    
    except Exception as e:
        # Use centralized error handler
        return [handle_tool_error(e)]


# Tool metadata for MCP server
update_task.metadata = {
    "name": "update_task",
    "description": "Update task details (title and/or description)",
    "parameters": {
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "description": "UUID of the user"
            },
            "task_id": {
                "type": "string",
                "description": "UUID of the task to update"
            },
            "title": {
                "type": "string",
                "description": "New task title (optional, max 255 characters)",
                "default": None
            },
            "description": {
                "type": "string",
                "description": "New task description (optional, max 2000 characters)",
                "default": None
            }
        },
        "required": ["user_id", "task_id"]
    }
}

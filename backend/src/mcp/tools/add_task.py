"""
MCP Tool: add_task

Creates a new task for the user. This tool enables AI agents to add tasks
to the user's task list through natural language commands.
"""
from uuid import UUID
from ..server import mcp_server
from ..schemas.tool_params import AddTaskParams
from ..utils import serialize_task, handle_tool_error
from ...core.database import Session, engine
from ...services.task_service import TaskService


@mcp_server.call_tool()
async def add_task(name: str, arguments: dict) -> list[dict]:
    """
    MCP tool handler for adding a new task.
    
    Args:
        name: Tool name (should be "add_task")
        arguments: Tool arguments containing user_id, title, and optional description
    
    Returns:
        List containing a single dict with task details or error
    
    Example:
        Input: {"user_id": "123...", "title": "Buy groceries", "description": "Milk, eggs"}
        Output: [{"task_id": "770...", "title": "Buy groceries", "completed": false, ...}]
    """
    try:
        # Validate parameters
        params = AddTaskParams(**arguments)
        
        # Create task using service
        with Session(engine) as session:
            service = TaskService(session)
            task = service.create_task(
                user_id=UUID(params.user_id),
                title=params.title,
                description=params.description
            )
            
            # Return JSON-serializable result using centralized serializer
            return [serialize_task(task)]
    
    except Exception as e:
        # Use centralized error handler
        return [handle_tool_error(e)]


# Tool metadata for MCP server
add_task.metadata = {
    "name": "add_task",
    "description": "Create a new task for the user",
    "parameters": {
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "description": "UUID of the user creating the task"
            },
            "title": {
                "type": "string",
                "description": "Task title (required, max 255 characters)"
            },
            "description": {
                "type": "string",
                "description": "Task description (optional, max 2000 characters)",
                "default": ""
            }
        },
        "required": ["user_id", "title"]
    }
}

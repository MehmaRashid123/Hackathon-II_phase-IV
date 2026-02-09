"""
MCP Tool: list_tasks

Lists all tasks for the user with optional filtering by completion status.
This tool enables AI agents to retrieve and display the user's task list.
"""
from uuid import UUID
from ..server import mcp_server
from ..schemas.tool_params import ListTasksParams
from ..utils import serialize_task, handle_tool_error
from ...core.database import Session, engine
from ...services.task_service import TaskService


@mcp_server.call_tool()
async def list_tasks(name: str, arguments: dict) -> list[dict]:
    """
    MCP tool handler for listing tasks.
    
    Args:
        name: Tool name (should be "list_tasks")
        arguments: Tool arguments containing user_id and optional completed filter
    
    Returns:
        List containing a single dict with tasks array and count
    
    Example:
        Input: {"user_id": "123...", "completed": false}
        Output: [{"tasks": [...], "count": 5}]
    """
    try:
        # Validate parameters
        params = ListTasksParams(**arguments)
        
        # Get tasks using service
        with Session(engine) as session:
            service = TaskService(session)
            tasks = service.get_tasks(
                user_id=UUID(params.user_id),
                completed=params.completed
            )
            
            # Return JSON-serializable result using centralized serializer
            return [{
                "tasks": [serialize_task(task) for task in tasks],
                "count": len(tasks)
            }]
    
    except Exception as e:
        # Use centralized error handler
        return [handle_tool_error(e)]


# Tool metadata for MCP server
list_tasks.metadata = {
    "name": "list_tasks",
    "description": "List all tasks for the user with optional completion filter",
    "parameters": {
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "description": "UUID of the user"
            },
            "completed": {
                "type": "boolean",
                "description": "Filter by completion status (optional)",
                "default": None
            }
        },
        "required": ["user_id"]
    }
}

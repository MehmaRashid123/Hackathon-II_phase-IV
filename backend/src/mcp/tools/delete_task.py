"""
MCP Tool: delete_task

Deletes a task. This tool enables AI agents to remove tasks from
the user's task list when they're no longer needed.
"""
from uuid import UUID
from ..server import mcp_server
from ..schemas.tool_params import DeleteTaskParams
from ..utils import handle_tool_error, format_not_found_error
from ...core.database import Session, engine
from ...services.task_service import TaskService


@mcp_server.call_tool()
async def delete_task(name: str, arguments: dict) -> list[dict]:
    """
    MCP tool handler for deleting a task.
    
    Args:
        name: Tool name (should be "delete_task")
        arguments: Tool arguments containing user_id and task_id
    
    Returns:
        List containing a single dict with success status or error
    
    Example:
        Input: {"user_id": "123...", "task_id": "770..."}
        Output: [{"success": true, "message": "Task deleted successfully"}]
    """
    try:
        # Validate parameters
        params = DeleteTaskParams(**arguments)
        
        # Delete task using service
        with Session(engine) as session:
            service = TaskService(session)
            success = service.delete_task(
                user_id=UUID(params.user_id),
                task_id=UUID(params.task_id)
            )
            
            if not success:
                return [format_not_found_error("Task", params.task_id)]
            
            # Return success response
            return [{
                "success": True,
                "message": "Task deleted successfully"
            }]
    
    except Exception as e:
        # Use centralized error handler
        return [handle_tool_error(e)]


# Tool metadata for MCP server
delete_task.metadata = {
    "name": "delete_task",
    "description": "Delete a task",
    "parameters": {
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "description": "UUID of the user"
            },
            "task_id": {
                "type": "string",
                "description": "UUID of the task to delete"
            }
        },
        "required": ["user_id", "task_id"]
    }
}

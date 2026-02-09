"""
MCP Tool Definitions for OpenAI Function Calling

Defines tool schemas that map MCP tools to OpenAI function calling format.
Each tool includes name, description, and parameter schema.
"""

from typing import List, Dict, Any


# Tool definition for adding tasks
ADD_TASK_TOOL = {
    "type": "function",
    "function": {
        "name": "add_task",
        "description": "Create a new task in the user's task list. Use this when the user wants to add, create, or remember something they need to do.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The task title or description. Should be clear and concise (e.g., 'Buy groceries', 'Call mom', 'Finish report')."
                },
                "description": {
                    "type": "string",
                    "description": "Optional additional details about the task. Use this for extra context or notes.",
                    "default": ""
                }
            },
            "required": ["title"]
        }
    }
}


# Tool definition for listing tasks
LIST_TASKS_TOOL = {
    "type": "function",
    "function": {
        "name": "list_tasks",
        "description": "Retrieve all tasks from the user's task list. Use this when the user wants to see their tasks, check what they need to do, or review their list.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}


# Tool definition for completing tasks
COMPLETE_TASK_TOOL = {
    "type": "function",
    "function": {
        "name": "complete_task",
        "description": "Mark a task as completed. Use this when the user indicates they've finished a task or want to mark it as done.",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "string",
                    "description": "The unique identifier (UUID) of the task to complete. You must first list tasks to get the task_id."
                }
            },
            "required": ["task_id"]
        }
    }
}


# Tool definition for deleting tasks
DELETE_TASK_TOOL = {
    "type": "function",
    "function": {
        "name": "delete_task",
        "description": "Permanently delete a task from the user's task list. Use this when the user wants to remove a task they no longer need.",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "string",
                    "description": "The unique identifier (UUID) of the task to delete. You must first list tasks to get the task_id."
                }
            },
            "required": ["task_id"]
        }
    }
}


# Tool definition for updating tasks
UPDATE_TASK_TOOL = {
    "type": "function",
    "function": {
        "name": "update_task",
        "description": "Update the title or description of an existing task. Use this when the user wants to modify or edit task details.",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "string",
                    "description": "The unique identifier (UUID) of the task to update. You must first list tasks to get the task_id."
                },
                "title": {
                    "type": "string",
                    "description": "New title for the task. Only provide if the user wants to change the title."
                },
                "description": {
                    "type": "string",
                    "description": "New description for the task. Only provide if the user wants to change the description."
                }
            },
            "required": ["task_id"]
        }
    }
}


def get_all_tools() -> List[Dict[str, Any]]:
    """
    Get all available MCP tools in OpenAI function calling format.
    
    Returns:
        List of tool definitions ready for OpenAI API
    
    Example:
        tools = get_all_tools()
        response = openai.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[...],
            tools=tools
        )
    """
    return [
        ADD_TASK_TOOL,
        LIST_TASKS_TOOL,
        COMPLETE_TASK_TOOL,
        DELETE_TASK_TOOL,
        UPDATE_TASK_TOOL
    ]


def get_tool_by_name(tool_name: str) -> Dict[str, Any]:
    """
    Get a specific tool definition by name.
    
    Args:
        tool_name: Name of the tool (e.g., 'add_task', 'list_tasks')
    
    Returns:
        Tool definition dictionary
    
    Raises:
        ValueError: If tool name is not found
    
    Example:
        tool = get_tool_by_name('add_task')
        print(tool['function']['description'])
    """
    tools_map = {
        "add_task": ADD_TASK_TOOL,
        "list_tasks": LIST_TASKS_TOOL,
        "complete_task": COMPLETE_TASK_TOOL,
        "delete_task": DELETE_TASK_TOOL,
        "update_task": UPDATE_TASK_TOOL
    }
    
    if tool_name not in tools_map:
        raise ValueError(
            f"Tool '{tool_name}' not found. "
            f"Available tools: {', '.join(tools_map.keys())}"
        )
    
    return tools_map[tool_name]


def get_tool_names() -> List[str]:
    """
    Get list of all available tool names.
    
    Returns:
        List of tool names
    
    Example:
        >>> get_tool_names()
        ['add_task', 'list_tasks', 'complete_task', 'delete_task', 'update_task']
    """
    return [
        "add_task",
        "list_tasks",
        "complete_task",
        "delete_task",
        "update_task"
    ]


# Validate all tools have required structure
def _validate_tools():
    """Validate that all tool definitions have correct structure."""
    for tool in get_all_tools():
        assert "type" in tool, "Tool missing 'type' field"
        assert tool["type"] == "function", "Tool type must be 'function'"
        assert "function" in tool, "Tool missing 'function' field"
        
        func = tool["function"]
        assert "name" in func, "Function missing 'name' field"
        assert "description" in func, "Function missing 'description' field"
        assert "parameters" in func, "Function missing 'parameters' field"
        
        params = func["parameters"]
        assert "type" in params, "Parameters missing 'type' field"
        assert "properties" in params, "Parameters missing 'properties' field"
        assert "required" in params, "Parameters missing 'required' field"


# Run validation on import
_validate_tools()

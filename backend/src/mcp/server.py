"""
MCP Server initialization and tool registration.

This module sets up the MCP server that exposes tools for AI agents
to interact with the task management system.
"""
import logging
from typing import Dict, Any, Callable
from mcp.server import Server
from mcp.server.stdio import stdio_server

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global MCP server instance
mcp_server = Server("task-management-mcp-server")

# Registry for tool functions
_tool_registry: Dict[str, Callable] = {}


def register_tool(name: str, func: Callable) -> None:
    """
    Register a tool function with the MCP server.
    
    Args:
        name: Tool name (e.g., "add_task")
        func: Tool function to register
    """
    _tool_registry[name] = func
    logger.info(f"Registered MCP tool: {name}")


def register_tools() -> None:
    """
    Register all MCP tools with the server.
    This function should be called after all tool modules are imported.
    """
    from .tools import add_task, list_tasks, complete_task, delete_task, update_task
    
    # Register all tools
    tools = [
        ("add_task", add_task.add_task),
        ("list_tasks", list_tasks.list_tasks),
        ("complete_task", complete_task.complete_task),
        ("delete_task", delete_task.delete_task),
        ("update_task", update_task.update_task),
    ]
    
    for tool_name, tool_func in tools:
        register_tool(tool_name, tool_func)
    
    logger.info(f"Registered {len(tools)} MCP tools")


async def run_server():
    """
    Run the MCP server using stdio transport.
    This is the main entry point for the MCP server.
    """
    logger.info("Starting MCP server...")
    
    # Register all tools before starting
    register_tools()
    
    # Run server with stdio transport
    async with stdio_server() as (read_stream, write_stream):
        await mcp_server.run(
            read_stream,
            write_stream,
            mcp_server.create_initialization_options()
        )


def get_tool(name: str) -> Callable:
    """
    Get a registered tool function by name.
    
    Args:
        name: Tool name
    
    Returns:
        Tool function
    
    Raises:
        KeyError: If tool is not registered
    """
    if name not in _tool_registry:
        raise KeyError(f"Tool '{name}' is not registered")
    return _tool_registry[name]


def list_registered_tools() -> list[str]:
    """
    Get list of all registered tool names.
    
    Returns:
        List of tool names
    """
    return list(_tool_registry.keys())


# Tool decorator for easy registration
def mcp_tool(name: str):
    """
    Decorator to register a function as an MCP tool.
    
    Usage:
        @mcp_tool("my_tool")
        def my_tool_function(param1: str) -> dict:
            return {"result": "success"}
    
    Args:
        name: Tool name
    """
    def decorator(func: Callable) -> Callable:
        # Register the tool with MCP server
        @mcp_server.call_tool()
        async def tool_handler(name: str, arguments: dict) -> list[Any]:
            """Handle tool calls from MCP clients."""
            try:
                result = func(**arguments)
                return [result]
            except Exception as e:
                logger.error(f"Error executing tool {name}: {e}")
                return [{"error": str(e)}]
        
        # Also register in our registry
        register_tool(name, func)
        return func
    
    return decorator


if __name__ == "__main__":
    """Run MCP server directly."""
    import asyncio
    
    asyncio.run(run_server())

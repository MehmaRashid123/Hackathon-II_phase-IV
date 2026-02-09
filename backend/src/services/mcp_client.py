"""
MCP Client Wrapper

Client for calling MCP tools with user_id injection and error handling.
"""

import httpx
from typing import Dict, Any, Optional, List
from uuid import UUID
import logging

from src.config import settings


logger = logging.getLogger(__name__)


class MCPClientError(Exception):
    """Base exception for MCP client errors."""
    pass


class MCPConnectionError(MCPClientError):
    """Raised when connection to MCP server fails."""
    pass


class MCPToolExecutionError(MCPClientError):
    """Raised when MCP tool execution fails."""
    pass


class MCPClient:
    """
    Client for calling MCP tools.
    
    Automatically injects user_id into all tool calls and handles errors.
    
    Attributes:
        base_url: Base URL of MCP server
        timeout: Request timeout in seconds
        user_id: User ID to inject into all tool calls
    
    Example:
        client = MCPClient(user_id="550e8400-e29b-41d4-a716-446655440000")
        result = await client.add_task("Buy groceries", "Milk, eggs, bread")
    """
    
    def __init__(
        self,
        user_id: str,
        base_url: str = "http://localhost:8000/api/mcp",
        timeout: float = 5.0
    ):
        """
        Initialize MCP client.
        
        Args:
            user_id: User ID to inject into all tool calls
            base_url: Base URL of MCP server
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.user_id = user_id
        
        # Validate user_id is a valid UUID
        try:
            UUID(user_id)
        except ValueError:
            raise ValueError(f"Invalid user_id format: {user_id}")
    
    async def _call_tool(
        self,
        tool_name: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Call an MCP tool with error handling.
        
        Args:
            tool_name: Name of the tool to call
            parameters: Tool parameters (user_id will be injected)
        
        Returns:
            Tool execution result
        
        Raises:
            MCPConnectionError: If connection to MCP server fails
            MCPToolExecutionError: If tool execution fails
        """
        # Inject user_id into parameters
        parameters["user_id"] = self.user_id
        
        url = f"{self.base_url}/{tool_name}"
        
        logger.info(f"Calling MCP tool: {tool_name} with params: {parameters}")
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    url,
                    json=parameters,
                    headers={"Content-Type": "application/json"}
                )
                
                # Check for HTTP errors
                if response.status_code >= 500:
                    raise MCPConnectionError(
                        f"MCP server error: {response.status_code} - {response.text}"
                    )
                
                if response.status_code >= 400:
                    raise MCPToolExecutionError(
                        f"Tool execution failed: {response.status_code} - {response.text}"
                    )
                
                result = response.json()
                logger.info(f"Tool {tool_name} executed successfully")
                return result
                
        except httpx.TimeoutException as e:
            logger.error(f"MCP tool {tool_name} timed out: {e}")
            raise MCPConnectionError(
                f"MCP server timeout after {self.timeout}s"
            ) from e
        
        except httpx.ConnectError as e:
            logger.error(f"Failed to connect to MCP server: {e}")
            raise MCPConnectionError(
                f"Cannot connect to MCP server at {self.base_url}"
            ) from e
        
        except Exception as e:
            logger.error(f"Unexpected error calling MCP tool {tool_name}: {e}")
            raise MCPClientError(f"Unexpected error: {str(e)}") from e
    
    async def add_task(
        self,
        title: str,
        description: str = ""
    ) -> Dict[str, Any]:
        """
        Add a new task.
        
        Args:
            title: Task title
            description: Optional task description
        
        Returns:
            Created task details
        
        Example:
            result = await client.add_task("Buy groceries", "Milk, eggs")
            # Returns: {"task_id": "...", "title": "Buy groceries", ...}
        """
        return await self._call_tool("add_task", {
            "title": title,
            "description": description
        })
    
    async def list_tasks(self) -> Dict[str, Any]:
        """
        List all tasks for the user.
        
        Returns:
            Dictionary with 'tasks' list and 'count'
        
        Example:
            result = await client.list_tasks()
            # Returns: {"tasks": [...], "count": 5}
        """
        return await self._call_tool("list_tasks", {})
    
    async def complete_task(self, task_id: str) -> Dict[str, Any]:
        """
        Mark a task as completed.
        
        Args:
            task_id: UUID of the task to complete
        
        Returns:
            Updated task details
        
        Example:
            result = await client.complete_task("550e8400-e29b-41d4-a716-446655440000")
            # Returns: {"task_id": "...", "status": "DONE", ...}
        """
        return await self._call_tool("complete_task", {
            "task_id": task_id
        })
    
    async def delete_task(self, task_id: str) -> Dict[str, Any]:
        """
        Delete a task.
        
        Args:
            task_id: UUID of the task to delete
        
        Returns:
            Success confirmation
        
        Example:
            result = await client.delete_task("550e8400-e29b-41d4-a716-446655440000")
            # Returns: {"success": True, "message": "Task deleted"}
        """
        return await self._call_tool("delete_task", {
            "task_id": task_id
        })
    
    async def update_task(
        self,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update a task's title or description.
        
        Args:
            task_id: UUID of the task to update
            title: New title (optional)
            description: New description (optional)
        
        Returns:
            Updated task details
        
        Raises:
            ValueError: If neither title nor description is provided
        
        Example:
            result = await client.update_task(
                "550e8400-e29b-41d4-a716-446655440000",
                title="Buy groceries and cook"
            )
        """
        if title is None and description is None:
            raise ValueError("Must provide at least one of: title, description")
        
        parameters = {"task_id": task_id}
        if title is not None:
            parameters["title"] = title
        if description is not None:
            parameters["description"] = description
        
        return await self._call_tool("update_task", parameters)
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"MCPClient(user_id={self.user_id}, base_url={self.base_url})"


def create_mcp_client(user_id: str) -> MCPClient:
    """
    Factory function to create MCP client with default settings.
    
    Args:
        user_id: User ID for the client
    
    Returns:
        Configured MCPClient instance
    
    Example:
        client = create_mcp_client("550e8400-e29b-41d4-a716-446655440000")
        result = await client.add_task("Buy groceries")
    """
    return MCPClient(
        user_id=user_id,
        base_url="http://localhost:8000/api/mcp",
        timeout=5.0
    )

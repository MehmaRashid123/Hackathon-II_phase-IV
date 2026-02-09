"""
MCP (Model Context Protocol) server implementation.
Provides tools for AI agents to interact with task management.
"""
from .server import mcp_server, register_tools

__all__ = ["mcp_server", "register_tools"]

"""
MCP utility modules.

Provides helper functions for JSON serialization, error handling,
and other common operations across MCP tools.
"""
from .serialization import (
    serialize_task,
    serialize_datetime,
    serialize_uuid,
    serialize_model,
)
from .errors import (
    MCPError,
    ValidationError,
    NotFoundError,
    PermissionError,
    DatabaseError,
    format_error,
    format_validation_error,
    format_not_found_error,
    safe_error_message,
    handle_tool_error,
)

__all__ = [
    # Serialization
    "serialize_task",
    "serialize_datetime",
    "serialize_uuid",
    "serialize_model",
    # Error classes
    "MCPError",
    "ValidationError",
    "NotFoundError",
    "PermissionError",
    "DatabaseError",
    # Error formatting
    "format_error",
    "format_validation_error",
    "format_not_found_error",
    "safe_error_message",
    "handle_tool_error",
]

"""
Error handling utilities for MCP tools.

Provides consistent error formatting and custom exception classes
for MCP tool operations. All errors are designed to be JSON-serializable
and provide clear messages to AI agents without leaking sensitive information.
"""
from typing import Dict, Any, Optional


class MCPError(Exception):
    """
    Base exception class for MCP tool errors.
    
    All MCP-specific exceptions should inherit from this class.
    Provides consistent error formatting for tool responses.
    
    Attributes:
        message: Human-readable error message
        code: Optional error code for categorization
        details: Optional additional error details
    """
    
    def __init__(
        self,
        message: str,
        code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize MCP error.
        
        Args:
            message: Error message describing what went wrong
            code: Optional error code (e.g., "VALIDATION_ERROR", "NOT_FOUND")
            details: Optional dictionary with additional error context
        """
        self.message = message
        self.code = code or "MCP_ERROR"
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert error to JSON-serializable dictionary.
        
        Returns:
            Dictionary with error information
        """
        result = {
            "error": self.message,
            "code": self.code,
        }
        
        if self.details:
            result["details"] = self.details
        
        return result


class ValidationError(MCPError):
    """
    Exception raised when tool parameters fail validation.
    
    Used for invalid input data, missing required fields,
    or data that doesn't meet constraints.
    
    Example:
        >>> raise ValidationError("Title cannot be empty")
        >>> raise ValidationError("Invalid UUID format", details={"field": "user_id"})
    """
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="VALIDATION_ERROR", details=details)


class NotFoundError(MCPError):
    """
    Exception raised when a requested resource is not found.
    
    Used when a task, user, or other entity doesn't exist
    or the user doesn't have access to it.
    
    Example:
        >>> raise NotFoundError("Task not found")
        >>> raise NotFoundError("Task not found", details={"task_id": "123..."})
    """
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="NOT_FOUND", details=details)


class PermissionError(MCPError):
    """
    Exception raised when a user doesn't have permission for an operation.
    
    Used for authorization failures and access control violations.
    
    Example:
        >>> raise PermissionError("You don't have access to this task")
    """
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="PERMISSION_DENIED", details=details)


class DatabaseError(MCPError):
    """
    Exception raised when a database operation fails.
    
    Used for database connection issues, query failures,
    or constraint violations.
    
    Example:
        >>> raise DatabaseError("Failed to save task")
    """
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="DATABASE_ERROR", details=details)


def format_error(
    message: str,
    code: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Format an error message as a JSON-serializable dictionary.
    
    This is the standard format for all MCP tool error responses.
    Use this function to ensure consistent error formatting across tools.
    
    Args:
        message: Human-readable error message
        code: Optional error code for categorization
        details: Optional additional error context
    
    Returns:
        Dictionary with error information
    
    Example:
        >>> format_error("Task not found")
        {'error': 'Task not found'}
        
        >>> format_error("Invalid input", code="VALIDATION_ERROR", details={"field": "title"})
        {'error': 'Invalid input', 'code': 'VALIDATION_ERROR', 'details': {'field': 'title'}}
    """
    result = {"error": message}
    
    if code:
        result["code"] = code
    
    if details:
        result["details"] = details
    
    return result


def format_validation_error(message: str, field: Optional[str] = None) -> Dict[str, Any]:
    """
    Format a validation error with optional field information.
    
    Convenience function for common validation error scenarios.
    
    Args:
        message: Error message
        field: Optional field name that failed validation
    
    Returns:
        Formatted error dictionary
    
    Example:
        >>> format_validation_error("Title cannot be empty", field="title")
        {'error': 'Title cannot be empty', 'code': 'VALIDATION_ERROR', 'details': {'field': 'title'}}
    """
    details = {"field": field} if field else None
    return format_error(message, code="VALIDATION_ERROR", details=details)


def format_not_found_error(resource: str, resource_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Format a not found error for a specific resource.
    
    Convenience function for common not found scenarios.
    
    Args:
        resource: Type of resource (e.g., "Task", "User")
        resource_id: Optional ID of the resource
    
    Returns:
        Formatted error dictionary
    
    Example:
        >>> format_not_found_error("Task", "123...")
        {'error': 'Task not found', 'code': 'NOT_FOUND', 'details': {'resource_id': '123...'}}
    """
    message = f"{resource} not found"
    details = {"resource_id": resource_id} if resource_id else None
    return format_error(message, code="NOT_FOUND", details=details)


def safe_error_message(error: Exception, default_message: str = "An error occurred") -> str:
    """
    Extract a safe error message from an exception.
    
    Prevents leaking sensitive information (like database connection strings,
    internal paths, etc.) in error messages sent to AI agents.
    
    Args:
        error: Exception to extract message from
        default_message: Fallback message if error message is unsafe
    
    Returns:
        Safe error message string
    
    Example:
        >>> try:
        ...     raise ValueError("Invalid UUID format")
        ... except Exception as e:
        ...     safe_error_message(e)
        'Invalid UUID format'
    """
    error_message = str(error)
    
    # List of sensitive patterns to filter out
    sensitive_patterns = [
        "postgresql://",
        "postgres://",
        "password=",
        "secret=",
        "token=",
        "api_key=",
        "/home/",
        "/usr/",
        "C:\\",
        "Traceback",
    ]
    
    # Check if error message contains sensitive information
    for pattern in sensitive_patterns:
        if pattern.lower() in error_message.lower():
            return default_message
    
    # Return original message if safe
    return error_message


def handle_tool_error(error: Exception) -> Dict[str, Any]:
    """
    Handle any exception and convert it to a standardized error response.
    
    This is the main error handler for MCP tools. It catches all exceptions
    and converts them to JSON-serializable error dictionaries.
    
    Args:
        error: Exception that occurred during tool execution
    
    Returns:
        Formatted error dictionary
    
    Example:
        >>> try:
        ...     # Tool operation
        ...     raise ValidationError("Invalid input")
        ... except Exception as e:
        ...     return [handle_tool_error(e)]
    """
    # Handle custom MCP errors
    if isinstance(error, MCPError):
        return error.to_dict()
    
    # Handle standard Python exceptions
    if isinstance(error, ValueError):
        return format_error(
            safe_error_message(error, "Invalid input value"),
            code="VALIDATION_ERROR"
        )
    
    if isinstance(error, KeyError):
        return format_error(
            safe_error_message(error, "Missing required field"),
            code="VALIDATION_ERROR"
        )
    
    if isinstance(error, TypeError):
        return format_error(
            safe_error_message(error, "Invalid data type"),
            code="VALIDATION_ERROR"
        )
    
    # Generic error handler
    return format_error(
        safe_error_message(error, "An unexpected error occurred"),
        code="INTERNAL_ERROR"
    )
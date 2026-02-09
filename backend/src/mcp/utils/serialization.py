"""
JSON serialization helpers for MCP tools.

Provides utilities to convert Python objects (datetime, UUID, SQLModel instances)
into JSON-serializable formats that AI agents can consume.
"""
from datetime import datetime
from typing import Optional, Any, Dict
from uuid import UUID


def serialize_datetime(dt: Optional[datetime]) -> Optional[str]:
    """
    Convert datetime to ISO 8601 string format.
    
    Args:
        dt: Datetime object to serialize (can be None)
    
    Returns:
        ISO 8601 formatted string or None if input is None
    
    Example:
        >>> from datetime import datetime
        >>> dt = datetime(2026, 2, 9, 10, 30, 0)
        >>> serialize_datetime(dt)
        '2026-02-09T10:30:00'
    """
    if dt is None:
        return None
    return dt.isoformat()


def serialize_uuid(uuid_obj: UUID) -> str:
    """
    Convert UUID to string format.
    
    Args:
        uuid_obj: UUID object to serialize
    
    Returns:
        String representation of UUID
    
    Example:
        >>> from uuid import UUID
        >>> uuid_obj = UUID('550e8400-e29b-41d4-a716-446655440000')
        >>> serialize_uuid(uuid_obj)
        '550e8400-e29b-41d4-a716-446655440000'
    """
    return str(uuid_obj)


def serialize_task(task: Any) -> Dict[str, Any]:
    """
    Convert Task model to JSON-serializable dictionary.
    
    This is the primary serialization function for Task objects returned
    by MCP tools. It ensures all fields are JSON-serializable by converting
    datetime objects to ISO 8601 strings and UUIDs to strings.
    
    Args:
        task: Task model instance (from src.models.task.Task)
    
    Returns:
        Dictionary with JSON-serializable task data
    
    Example:
        >>> task = Task(
        ...     id=UUID('770e8400-e29b-41d4-a716-446655440000'),
        ...     user_id=UUID('123e4567-e89b-12d3-a456-426614174000'),
        ...     title='Buy groceries',
        ...     description='Milk, eggs, bread',
        ...     completed=False,
        ...     created_at=datetime(2026, 2, 9, 10, 0, 0),
        ...     updated_at=datetime(2026, 2, 9, 10, 0, 0),
        ...     completed_at=None
        ... )
        >>> serialize_task(task)
        {
            'task_id': '770e8400-e29b-41d4-a716-446655440000',
            'title': 'Buy groceries',
            'description': 'Milk, eggs, bread',
            'completed': False,
            'created_at': '2026-02-09T10:00:00',
            'updated_at': '2026-02-09T10:00:00',
            'completed_at': None
        }
    """
    return {
        "task_id": serialize_uuid(task.id),
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "created_at": serialize_datetime(task.created_at),
        "updated_at": serialize_datetime(task.updated_at),
        "completed_at": serialize_datetime(task.completed_at),
    }


def serialize_model(model: Any, exclude: Optional[set] = None) -> Dict[str, Any]:
    """
    Generic serialization for SQLModel instances.
    
    Converts any SQLModel instance to a JSON-serializable dictionary,
    automatically handling datetime and UUID fields.
    
    Args:
        model: SQLModel instance to serialize
        exclude: Optional set of field names to exclude from serialization
    
    Returns:
        Dictionary with JSON-serializable data
    
    Note:
        This is a generic fallback. Prefer specific serializers like
        serialize_task() for better control over output format.
    """
    if exclude is None:
        exclude = set()
    
    result = {}
    
    # Get model fields
    for field_name in model.__fields__.keys():
        if field_name in exclude:
            continue
        
        value = getattr(model, field_name, None)
        
        # Handle different types
        if isinstance(value, datetime):
            result[field_name] = serialize_datetime(value)
        elif isinstance(value, UUID):
            result[field_name] = serialize_uuid(value)
        elif value is None:
            result[field_name] = None
        else:
            result[field_name] = value
    
    return result

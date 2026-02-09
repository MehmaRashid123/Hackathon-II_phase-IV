"""
Chat API Schemas

Pydantic models for chat request/response payloads.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class ChatRequest(BaseModel):
    """
    Request payload for chat endpoint.
    
    Attributes:
        message: User's natural language input (1-2000 characters)
        conversation_id: Optional conversation ID to continue existing conversation
    
    Example:
        {
            "message": "Add a task to buy groceries",
            "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
        }
    """
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="User's natural language message",
        example="Add a task to buy groceries"
    )
    conversation_id: Optional[str] = Field(
        None,
        description="Optional conversation ID to continue existing conversation",
        example="550e8400-e29b-41d4-a716-446655440000"
    )

    @validator('message')
    def message_not_empty(cls, v):
        """Validate message is not just whitespace."""
        if not v or not v.strip():
            raise ValueError('Message cannot be empty or whitespace only')
        return v.strip()

    @validator('conversation_id')
    def validate_conversation_id(cls, v):
        """Validate conversation_id is a valid UUID if provided."""
        if v is not None:
            try:
                UUID(v)
            except ValueError:
                raise ValueError('conversation_id must be a valid UUID')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Show me all my tasks",
                "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }


class ToolCall(BaseModel):
    """
    Details of a tool call executed by the agent.
    
    Attributes:
        tool_name: Name of the MCP tool called
        parameters: Parameters passed to the tool
        result: Result returned by the tool
    
    Example:
        {
            "tool_name": "add_task",
            "parameters": {"title": "Buy groceries", "description": ""},
            "result": {"task_id": "...", "title": "Buy groceries", "status": "TO_DO"}
        }
    """
    tool_name: str = Field(
        ...,
        description="Name of the MCP tool that was called",
        example="add_task"
    )
    parameters: dict = Field(
        ...,
        description="Parameters passed to the tool",
        example={"title": "Buy groceries", "description": ""}
    )
    result: Optional[dict] = Field(
        None,
        description="Result returned by the tool execution",
        example={"task_id": "550e8400-e29b-41d4-a716-446655440000", "title": "Buy groceries"}
    )

    class Config:
        json_schema_extra = {
            "example": {
                "tool_name": "add_task",
                "parameters": {
                    "title": "Buy groceries",
                    "description": "Milk, eggs, bread"
                },
                "result": {
                    "task_id": "550e8400-e29b-41d4-a716-446655440000",
                    "title": "Buy groceries",
                    "status": "TO_DO"
                }
            }
        }


class ChatResponse(BaseModel):
    """
    Response payload from chat endpoint.
    
    Attributes:
        conversation_id: ID of the conversation (new or existing)
        message: Agent's natural language response
        tool_calls: Optional list of tools executed during processing
        timestamp: When the response was generated
    
    Example:
        {
            "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
            "message": "Done! I've added 'Buy groceries' to your task list.",
            "tool_calls": [...],
            "timestamp": "2024-01-01T12:00:00Z"
        }
    """
    conversation_id: str = Field(
        ...,
        description="Conversation ID (new or existing)",
        example="550e8400-e29b-41d4-a716-446655440000"
    )
    message: str = Field(
        ...,
        description="Agent's natural language response",
        example="Done! I've added 'Buy groceries' to your task list."
    )
    tool_calls: Optional[List[ToolCall]] = Field(
        None,
        description="List of tools executed during processing"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the response was generated"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
                "message": "Done! I've added 'Buy groceries' to your task list.",
                "tool_calls": [
                    {
                        "tool_name": "add_task",
                        "parameters": {
                            "title": "Buy groceries",
                            "description": ""
                        },
                        "result": {
                            "task_id": "650e8400-e29b-41d4-a716-446655440001",
                            "title": "Buy groceries",
                            "status": "TO_DO"
                        }
                    }
                ],
                "timestamp": "2024-01-01T12:00:00Z"
            }
        }


class ConversationMessage(BaseModel):
    """
    A single message in conversation history.
    
    Used internally to build agent context from database.
    
    Attributes:
        role: Message role (user or assistant)
        content: Message content
        timestamp: When the message was sent
    """
    role: str = Field(
        ...,
        description="Message role: 'user' or 'assistant'",
        pattern="^(user|assistant)$"
    )
    content: str = Field(
        ...,
        description="Message content"
    )
    timestamp: datetime = Field(
        ...,
        description="When the message was sent"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "role": "user",
                "content": "Add a task to buy groceries",
                "timestamp": "2024-01-01T12:00:00Z"
            }
        }

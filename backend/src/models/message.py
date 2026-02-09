"""
Message model for storing individual messages within conversations.

Messages represent exchanges between users and the AI assistant, including
user inputs, assistant responses, and tool execution results.
"""
from datetime import datetime
from typing import Optional, Literal
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Relationship


# Type alias for message roles
MessageRole = Literal["user", "assistant", "tool"]


class Message(SQLModel, table=True):
    """
    Message entity for conversation exchanges.
    
    Attributes:
        id: Unique message identifier (UUID)
        conversation_id: Foreign key to conversations table
        user_id: Foreign key to users table (for multi-tenant isolation)
        role: Message role (user, assistant, or tool)
        content: Message text content
        created_at: Timestamp when message was created
        conversation: Relationship to Conversation model (many-to-one)
    """
    __tablename__ = "messages"
    
    # Primary key
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    
    # Foreign keys
    conversation_id: UUID = Field(
        foreign_key="conversations.id",
        nullable=False,
        index=True
    )
    user_id: UUID = Field(
        foreign_key="users.id",
        nullable=False,
        index=True
    )
    
    # Data fields
    role: str = Field(max_length=20, nullable=False)
    content: str = Field(max_length=10000, nullable=False)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")
    
    def validate_role(self) -> None:
        """
        Validate that role is one of the allowed values.
        
        Raises:
            ValueError: If role is not 'user', 'assistant', or 'tool'
        """
        allowed_roles = {"user", "assistant", "tool"}
        if self.role not in allowed_roles:
            raise ValueError(
                f"Invalid role '{self.role}'. Must be one of: {', '.join(allowed_roles)}"
            )
    
    class Config:
        """SQLModel configuration."""
        json_schema_extra = {
            "example": {
                "id": "660e8400-e29b-41d4-a716-446655440000",
                "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "role": "user",
                "content": "Add a task to buy groceries",
                "created_at": "2026-02-09T10:00:00Z"
            }
        }

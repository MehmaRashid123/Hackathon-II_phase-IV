"""
Conversation model for storing chat conversations.

A conversation represents a dialogue session between a user and the AI assistant.
Each conversation belongs to a user and contains multiple messages.
"""
from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Relationship


class Conversation(SQLModel, table=True):
    """
    Conversation entity for chat sessions.
    
    Attributes:
        id: Unique conversation identifier (UUID)
        user_id: Foreign key to users table
        title: Optional conversation title (auto-generated or user-defined)
        created_at: Timestamp when conversation was created
        updated_at: Timestamp when conversation was last updated
        messages: Relationship to Message model (one-to-many)
    """
    __tablename__ = "conversations"
    
    # Primary key
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    
    # Foreign keys
    user_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
    
    # Data fields
    title: Optional[str] = Field(default=None, max_length=255)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    messages: List["Message"] = Relationship(back_populates="conversation")
    
    class Config:
        """SQLModel configuration."""
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Task Management Chat",
                "created_at": "2026-02-09T10:00:00Z",
                "updated_at": "2026-02-09T10:30:00Z"
            }
        }

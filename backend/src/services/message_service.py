"""
Message service for managing conversation messages.

Provides operations for adding and retrieving messages within conversations
with strict user_id filtering for multi-tenant isolation.
"""
from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from ..models.message import Message, MessageRole


class MessageService:
    """Service for message management operations."""
    
    def __init__(self, session: Session):
        """
        Initialize message service with database session.
        
        Args:
            session: SQLModel database session
        """
        self.session = session
    
    def add_message(
        self,
        conversation_id: UUID,
        user_id: UUID,
        role: str,
        content: str
    ) -> Message:
        """
        Add a new message to a conversation.
        
        Args:
            conversation_id: UUID of the conversation
            user_id: UUID of the user (for multi-tenant isolation)
            role: Message role ('user', 'assistant', or 'tool')
            content: Message content (max 10000 chars)
        
        Returns:
            Created Message object
        
        Raises:
            ValueError: If role is invalid or content is empty/too long
        """
        # Validate role
        allowed_roles = {"user", "assistant", "tool"}
        if role not in allowed_roles:
            raise ValueError(
                f"Invalid role '{role}'. Must be one of: {', '.join(allowed_roles)}"
            )
        
        # Validate content
        if not content or not content.strip():
            raise ValueError("Message content cannot be empty")
        
        if len(content) > 10000:
            raise ValueError("Message content cannot exceed 10000 characters")
        
        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content.strip()
        )
        
        # Validate role using model method
        message.validate_role()
        
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)
        
        return message
    
    def get_messages(
        self,
        user_id: UUID,
        conversation_id: UUID,
        limit: int = 50
    ) -> List[Message]:
        """
        Get all messages in a conversation for a user.
        
        Args:
            user_id: UUID of the user
            conversation_id: UUID of the conversation
            limit: Maximum number of messages to return (default: 50)
        
        Returns:
            List of Message objects ordered by creation time (oldest first)
        """
        statement = (
            select(Message)
            .where(
                Message.conversation_id == conversation_id,
                Message.user_id == user_id
            )
            .order_by(Message.created_at.asc())
            .limit(limit)
        )
        
        results = self.session.exec(statement)
        return list(results.all())
    
    def get_message_by_id(
        self,
        user_id: UUID,
        message_id: UUID
    ) -> Optional[Message]:
        """
        Get a specific message by ID, ensuring it belongs to the user.
        
        Args:
            user_id: UUID of the user
            message_id: UUID of the message
        
        Returns:
            Message object if found and belongs to user, None otherwise
        """
        statement = select(Message).where(
            Message.id == message_id,
            Message.user_id == user_id
        )
        
        result = self.session.exec(statement)
        return result.first()
    
    def get_recent_messages(
        self,
        user_id: UUID,
        conversation_id: UUID,
        count: int = 10
    ) -> List[Message]:
        """
        Get the most recent messages in a conversation.
        
        Args:
            user_id: UUID of the user
            conversation_id: UUID of the conversation
            count: Number of recent messages to return (default: 10)
        
        Returns:
            List of Message objects ordered by creation time (newest first)
        """
        statement = (
            select(Message)
            .where(
                Message.conversation_id == conversation_id,
                Message.user_id == user_id
            )
            .order_by(Message.created_at.desc())
            .limit(count)
        )
        
        results = self.session.exec(statement)
        # Reverse to get chronological order (oldest to newest)
        return list(reversed(list(results.all())))
    
    def count_messages(
        self,
        user_id: UUID,
        conversation_id: UUID
    ) -> int:
        """
        Count total messages in a conversation for a user.
        
        Args:
            user_id: UUID of the user
            conversation_id: UUID of the conversation
        
        Returns:
            Total number of messages
        """
        statement = select(Message).where(
            Message.conversation_id == conversation_id,
            Message.user_id == user_id
        )
        
        results = self.session.exec(statement)
        return len(list(results.all()))

"""
Conversation History Service

Service for managing conversation history in the database.
Handles fetching, creating, and saving conversations and messages.
"""

from typing import List, Dict, Any, Optional
from uuid import UUID, uuid4
from datetime import datetime
from sqlmodel import Session, select
import logging

from src.models.conversation import Conversation
from src.models.message import Message
from src.schemas.chat import ConversationMessage


logger = logging.getLogger(__name__)


class ConversationServiceError(Exception):
    """Base exception for conversation service errors."""
    pass


class ConversationNotFoundError(ConversationServiceError):
    """Raised when conversation is not found."""
    pass


class ConversationService:
    """
    Service for managing conversation history.
    
    Provides methods for creating conversations, fetching history,
    and saving messages with proper transaction handling.
    """
    
    @staticmethod
    def create_conversation(
        session: Session,
        user_id: str,
        title: Optional[str] = None
    ) -> Conversation:
        """
        Create a new conversation for a user.
        
        Args:
            session: Database session
            user_id: User ID (UUID string)
            title: Optional conversation title
        
        Returns:
            Created Conversation instance
        
        Example:
            conversation = ConversationService.create_conversation(
                session,
                user_id="550e8400-e29b-41d4-a716-446655440000",
                title="Task Management Chat"
            )
        """
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            raise ValueError(f"Invalid user_id format: {user_id}")
        
        # Auto-generate title if not provided
        if title is None:
            title = f"Chat {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
        
        conversation = Conversation(
            user_id=user_uuid,
            title=title,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        
        logger.info(f"Created conversation {conversation.id} for user {user_id}")
        return conversation
    
    @staticmethod
    def get_conversation(
        session: Session,
        conversation_id: str,
        user_id: str
    ) -> Conversation:
        """
        Get a conversation by ID with user validation.
        
        Args:
            session: Database session
            conversation_id: Conversation ID (UUID string)
            user_id: User ID for authorization check
        
        Returns:
            Conversation instance
        
        Raises:
            ConversationNotFoundError: If conversation not found or doesn't belong to user
        
        Example:
            conversation = ConversationService.get_conversation(
                session,
                conversation_id="550e8400-e29b-41d4-a716-446655440000",
                user_id="123e4567-e89b-12d3-a456-426614174000"
            )
        """
        try:
            conv_uuid = UUID(conversation_id)
            user_uuid = UUID(user_id)
        except ValueError as e:
            raise ValueError(f"Invalid UUID format: {e}")
        
        statement = select(Conversation).where(
            Conversation.id == conv_uuid,
            Conversation.user_id == user_uuid
        )
        conversation = session.exec(statement).first()
        
        if not conversation:
            raise ConversationNotFoundError(
                f"Conversation {conversation_id} not found for user {user_id}"
            )
        
        return conversation
    
    @staticmethod
    def get_conversation_history(
        session: Session,
        conversation_id: str,
        user_id: str,
        limit: int = 50
    ) -> List[ConversationMessage]:
        """
        Get conversation history (messages) for a conversation.
        
        Args:
            session: Database session
            conversation_id: Conversation ID (UUID string)
            user_id: User ID for authorization check
            limit: Maximum number of messages to retrieve (default: 50)
        
        Returns:
            List of ConversationMessage objects ordered by creation time
        
        Raises:
            ConversationNotFoundError: If conversation not found
        
        Example:
            history = ConversationService.get_conversation_history(
                session,
                conversation_id="550e8400-e29b-41d4-a716-446655440000",
                user_id="123e4567-e89b-12d3-a456-426614174000",
                limit=50
            )
        """
        # Verify conversation exists and belongs to user
        conversation = ConversationService.get_conversation(
            session, conversation_id, user_id
        )
        
        try:
            conv_uuid = UUID(conversation_id)
        except ValueError:
            raise ValueError(f"Invalid conversation_id format: {conversation_id}")
        
        # Fetch messages ordered by creation time
        statement = (
            select(Message)
            .where(Message.conversation_id == conv_uuid)
            .order_by(Message.created_at.asc())
            .limit(limit)
        )
        messages = session.exec(statement).all()
        
        # Convert to ConversationMessage schema
        history = [
            ConversationMessage(
                role=msg.role,
                content=msg.content,
                timestamp=msg.created_at
            )
            for msg in messages
        ]
        
        logger.info(
            f"Retrieved {len(history)} messages for conversation {conversation_id}"
        )
        return history
    
    @staticmethod
    def save_messages(
        session: Session,
        conversation_id: str,
        user_id: str,
        user_message: str,
        assistant_message: str
    ) -> None:
        """
        Save user and assistant messages to conversation.
        
        Uses a transaction to ensure both messages are saved atomically.
        
        Args:
            session: Database session
            conversation_id: Conversation ID (UUID string)
            user_id: User ID (UUID string)
            user_message: User's message content
            assistant_message: Assistant's response content
        
        Raises:
            ConversationNotFoundError: If conversation not found
        
        Example:
            ConversationService.save_messages(
                session,
                conversation_id="550e8400-e29b-41d4-a716-446655440000",
                user_id="123e4567-e89b-12d3-a456-426614174000",
                user_message="Add a task to buy groceries",
                assistant_message="Done! I've added 'Buy groceries' to your list."
            )
        """
        # Verify conversation exists and belongs to user
        conversation = ConversationService.get_conversation(
            session, conversation_id, user_id
        )
        
        try:
            conv_uuid = UUID(conversation_id)
            user_uuid = UUID(user_id)
        except ValueError as e:
            raise ValueError(f"Invalid UUID format: {e}")
        
        try:
            # Create user message
            user_msg = Message(
                conversation_id=conv_uuid,
                user_id=user_uuid,
                role="user",
                content=user_message,
                created_at=datetime.utcnow()
            )
            
            # Create assistant message
            assistant_msg = Message(
                conversation_id=conv_uuid,
                user_id=user_uuid,
                role="assistant",
                content=assistant_message,
                created_at=datetime.utcnow()
            )
            
            # Save both messages in transaction
            session.add(user_msg)
            session.add(assistant_msg)
            
            # Update conversation timestamp
            conversation.updated_at = datetime.utcnow()
            session.add(conversation)
            
            session.commit()
            
            logger.info(
                f"Saved 2 messages to conversation {conversation_id}"
            )
            
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to save messages: {e}")
            raise ConversationServiceError(
                f"Failed to save messages: {str(e)}"
            ) from e
    
    @staticmethod
    def get_or_create_conversation(
        session: Session,
        user_id: str,
        conversation_id: Optional[str] = None
    ) -> Conversation:
        """
        Get existing conversation or create a new one.
        
        If conversation_id is provided, retrieves that conversation.
        Otherwise, creates a new conversation for the user.
        
        Args:
            session: Database session
            user_id: User ID (UUID string)
            conversation_id: Optional conversation ID to retrieve
        
        Returns:
            Conversation instance (existing or new)
        
        Example:
            # Get existing conversation
            conv = ConversationService.get_or_create_conversation(
                session,
                user_id="123e4567-e89b-12d3-a456-426614174000",
                conversation_id="550e8400-e29b-41d4-a716-446655440000"
            )
            
            # Create new conversation
            conv = ConversationService.get_or_create_conversation(
                session,
                user_id="123e4567-e89b-12d3-a456-426614174000"
            )
        """
        if conversation_id:
            try:
                return ConversationService.get_conversation(
                    session, conversation_id, user_id
                )
            except ConversationNotFoundError:
                logger.warning(
                    f"Conversation {conversation_id} not found, creating new one"
                )
                # Fall through to create new conversation
        
        # Create new conversation
        return ConversationService.create_conversation(session, user_id)
    
    @staticmethod
    def list_user_conversations(
        session: Session,
        user_id: str,
        limit: int = 20
    ) -> List[Conversation]:
        """
        List all conversations for a user.
        
        Args:
            session: Database session
            user_id: User ID (UUID string)
            limit: Maximum number of conversations to retrieve
        
        Returns:
            List of Conversation instances ordered by updated_at (newest first)
        
        Example:
            conversations = ConversationService.list_user_conversations(
                session,
                user_id="123e4567-e89b-12d3-a456-426614174000",
                limit=20
            )
        """
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            raise ValueError(f"Invalid user_id format: {user_id}")
        
        statement = (
            select(Conversation)
            .where(Conversation.user_id == user_uuid)
            .order_by(Conversation.updated_at.desc())
            .limit(limit)
        )
        conversations = session.exec(statement).all()
        
        logger.info(f"Retrieved {len(conversations)} conversations for user {user_id}")
        return conversations

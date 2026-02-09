"""
Unit tests for ConversationService.

Tests conversation creation, history retrieval, and message saving.
"""

import pytest
from uuid import uuid4
from datetime import datetime
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool

from src.models.conversation import Conversation
from src.models.message import Message
from src.models.user import User
from src.services.conversation_service import (
    ConversationService,
    ConversationNotFoundError,
    ConversationServiceError
)


@pytest.fixture(name="session")
def session_fixture():
    """Create an in-memory database session for testing."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="test_user")
def test_user_fixture(session: Session):
    """Create a test user."""
    user = User(
        id=uuid4(),
        email="test@example.com",
        hashed_password="hashed_password"
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


class TestCreateConversation:
    """Tests for create_conversation method."""
    
    def test_create_conversation_with_title(self, session: Session, test_user: User):
        """Test creating a conversation with a custom title."""
        conversation = ConversationService.create_conversation(
            session,
            user_id=str(test_user.id),
            title="Test Chat"
        )
        
        assert conversation.id is not None
        assert conversation.user_id == test_user.id
        assert conversation.title == "Test Chat"
        assert isinstance(conversation.created_at, datetime)
        assert isinstance(conversation.updated_at, datetime)
    
    def test_create_conversation_without_title(self, session: Session, test_user: User):
        """Test creating a conversation with auto-generated title."""
        conversation = ConversationService.create_conversation(
            session,
            user_id=str(test_user.id)
        )
        
        assert conversation.id is not None
        assert conversation.title is not None
        assert "Chat" in conversation.title
    
    def test_create_conversation_invalid_user_id(self, session: Session):
        """Test that invalid user_id raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            ConversationService.create_conversation(
                session,
                user_id="not-a-uuid"
            )
        assert "Invalid user_id format" in str(exc_info.value)


class TestGetConversation:
    """Tests for get_conversation method."""
    
    def test_get_existing_conversation(self, session: Session, test_user: User):
        """Test retrieving an existing conversation."""
        # Create conversation
        conversation = ConversationService.create_conversation(
            session,
            user_id=str(test_user.id),
            title="Test"
        )
        
        # Retrieve it
        retrieved = ConversationService.get_conversation(
            session,
            conversation_id=str(conversation.id),
            user_id=str(test_user.id)
        )
        
        assert retrieved.id == conversation.id
        assert retrieved.title == "Test"
    
    def test_get_nonexistent_conversation(self, session: Session, test_user: User):
        """Test that getting nonexistent conversation raises error."""
        fake_id = str(uuid4())
        
        with pytest.raises(ConversationNotFoundError):
            ConversationService.get_conversation(
                session,
                conversation_id=fake_id,
                user_id=str(test_user.id)
            )
    
    def test_get_conversation_wrong_user(self, session: Session, test_user: User):
        """Test that user cannot access another user's conversation."""
        # Create conversation for test_user
        conversation = ConversationService.create_conversation(
            session,
            user_id=str(test_user.id)
        )
        
        # Try to access with different user_id
        other_user_id = str(uuid4())
        
        with pytest.raises(ConversationNotFoundError):
            ConversationService.get_conversation(
                session,
                conversation_id=str(conversation.id),
                user_id=other_user_id
            )


class TestGetConversationHistory:
    """Tests for get_conversation_history method."""
    
    def test_get_empty_history(self, session: Session, test_user: User):
        """Test getting history for conversation with no messages."""
        conversation = ConversationService.create_conversation(
            session,
            user_id=str(test_user.id)
        )
        
        history = ConversationService.get_conversation_history(
            session,
            conversation_id=str(conversation.id),
            user_id=str(test_user.id)
        )
        
        assert history == []
    
    def test_get_history_with_messages(self, session: Session, test_user: User):
        """Test getting history with multiple messages."""
        conversation = ConversationService.create_conversation(
            session,
            user_id=str(test_user.id)
        )
        
        # Add messages
        msg1 = Message(
            conversation_id=conversation.id,
            user_id=test_user.id,
            role="user",
            content="Hello"
        )
        msg2 = Message(
            conversation_id=conversation.id,
            user_id=test_user.id,
            role="assistant",
            content="Hi there!"
        )
        session.add(msg1)
        session.add(msg2)
        session.commit()
        
        # Get history
        history = ConversationService.get_conversation_history(
            session,
            conversation_id=str(conversation.id),
            user_id=str(test_user.id)
        )
        
        assert len(history) == 2
        assert history[0].role == "user"
        assert history[0].content == "Hello"
        assert history[1].role == "assistant"
        assert history[1].content == "Hi there!"
    
    def test_history_respects_limit(self, session: Session, test_user: User):
        """Test that history respects the limit parameter."""
        conversation = ConversationService.create_conversation(
            session,
            user_id=str(test_user.id)
        )
        
        # Add 10 messages
        for i in range(10):
            msg = Message(
                conversation_id=conversation.id,
                user_id=test_user.id,
                role="user" if i % 2 == 0 else "assistant",
                content=f"Message {i}"
            )
            session.add(msg)
        session.commit()
        
        # Get history with limit=5
        history = ConversationService.get_conversation_history(
            session,
            conversation_id=str(conversation.id),
            user_id=str(test_user.id),
            limit=5
        )
        
        assert len(history) == 5


class TestSaveMessages:
    """Tests for save_messages method."""
    
    def test_save_messages_success(self, session: Session, test_user: User):
        """Test successfully saving user and assistant messages."""
        conversation = ConversationService.create_conversation(
            session,
            user_id=str(test_user.id)
        )
        
        ConversationService.save_messages(
            session,
            conversation_id=str(conversation.id),
            user_id=str(test_user.id),
            user_message="Add a task",
            assistant_message="Done!"
        )
        
        # Verify messages were saved
        history = ConversationService.get_conversation_history(
            session,
            conversation_id=str(conversation.id),
            user_id=str(test_user.id)
        )
        
        assert len(history) == 2
        assert history[0].role == "user"
        assert history[0].content == "Add a task"
        assert history[1].role == "assistant"
        assert history[1].content == "Done!"
    
    def test_save_messages_updates_conversation_timestamp(
        self, session: Session, test_user: User
    ):
        """Test that saving messages updates conversation timestamp."""
        conversation = ConversationService.create_conversation(
            session,
            user_id=str(test_user.id)
        )
        
        original_updated_at = conversation.updated_at
        
        # Wait a moment and save messages
        import time
        time.sleep(0.1)
        
        ConversationService.save_messages(
            session,
            conversation_id=str(conversation.id),
            user_id=str(test_user.id),
            user_message="Test",
            assistant_message="Response"
        )
        
        # Refresh conversation
        session.refresh(conversation)
        
        assert conversation.updated_at > original_updated_at


class TestGetOrCreateConversation:
    """Tests for get_or_create_conversation method."""
    
    def test_get_existing_conversation(self, session: Session, test_user: User):
        """Test getting an existing conversation."""
        # Create conversation
        conversation = ConversationService.create_conversation(
            session,
            user_id=str(test_user.id),
            title="Existing"
        )
        
        # Get it
        retrieved = ConversationService.get_or_create_conversation(
            session,
            user_id=str(test_user.id),
            conversation_id=str(conversation.id)
        )
        
        assert retrieved.id == conversation.id
        assert retrieved.title == "Existing"
    
    def test_create_new_conversation(self, session: Session, test_user: User):
        """Test creating a new conversation when none exists."""
        conversation = ConversationService.get_or_create_conversation(
            session,
            user_id=str(test_user.id)
        )
        
        assert conversation.id is not None
        assert conversation.user_id == test_user.id
    
    def test_create_when_conversation_not_found(
        self, session: Session, test_user: User
    ):
        """Test creating new conversation when provided ID doesn't exist."""
        fake_id = str(uuid4())
        
        conversation = ConversationService.get_or_create_conversation(
            session,
            user_id=str(test_user.id),
            conversation_id=fake_id
        )
        
        # Should create new conversation, not use fake_id
        assert conversation.id is not None
        assert str(conversation.id) != fake_id


class TestListUserConversations:
    """Tests for list_user_conversations method."""
    
    def test_list_empty_conversations(self, session: Session, test_user: User):
        """Test listing when user has no conversations."""
        conversations = ConversationService.list_user_conversations(
            session,
            user_id=str(test_user.id)
        )
        
        assert conversations == []
    
    def test_list_multiple_conversations(self, session: Session, test_user: User):
        """Test listing multiple conversations."""
        # Create 3 conversations
        conv1 = ConversationService.create_conversation(
            session, str(test_user.id), "Chat 1"
        )
        conv2 = ConversationService.create_conversation(
            session, str(test_user.id), "Chat 2"
        )
        conv3 = ConversationService.create_conversation(
            session, str(test_user.id), "Chat 3"
        )
        
        conversations = ConversationService.list_user_conversations(
            session,
            user_id=str(test_user.id)
        )
        
        assert len(conversations) == 3
        # Should be ordered by updated_at desc (newest first)
        assert conversations[0].id == conv3.id
        assert conversations[1].id == conv2.id
        assert conversations[2].id == conv1.id

"""
Unit tests for ChatService.

Tests the complete stateless request cycle orchestration.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool

from src.services.chat_service import ChatService, ChatServiceError, process_chat
from src.schemas.chat import ChatRequest, ChatResponse
from src.models.user import User
from src.models.conversation import Conversation
from src.models.message import Message


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


class TestBuildAgentContext:
    """Tests for _build_agent_context method."""
    
    def test_build_context_with_empty_history(self):
        """Test building context with no conversation history."""
        user_id = str(uuid4())
        conv_id = str(uuid4())
        
        context = ChatService._build_agent_context(
            user_id=user_id,
            conversation_id=conv_id,
            history=[]
        )
        
        assert str(context.user_id) == user_id
        assert context.conversation_id == conv_id
        assert len(context.conversation_history) == 0
        assert context.system_instructions != ""
        assert len(context.available_tools) == 5  # 5 MCP tools
    
    def test_build_context_with_history(self):
        """Test building context with conversation history."""
        from src.schemas.chat import ConversationMessage
        from datetime import datetime
        
        user_id = str(uuid4())
        conv_id = str(uuid4())
        
        history = [
            ConversationMessage(
                role="user",
                content="Hello",
                timestamp=datetime.utcnow()
            ),
            ConversationMessage(
                role="assistant",
                content="Hi there!",
                timestamp=datetime.utcnow()
            )
        ]
        
        context = ChatService._build_agent_context(
            user_id=user_id,
            conversation_id=conv_id,
            history=history
        )
        
        assert len(context.conversation_history) == 2
        assert context.conversation_history[0]["role"] == "user"
        assert context.conversation_history[0]["content"] == "Hello"
        assert context.conversation_history[1]["role"] == "assistant"
    
    def test_build_context_invalid_user_id(self):
        """Test that invalid user_id raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            ChatService._build_agent_context(
                user_id="not-a-uuid",
                conversation_id=str(uuid4()),
                history=[]
            )
        assert "Invalid user_id format" in str(exc_info.value)


class TestProcessChatRequest:
    """Tests for process_chat_request method."""
    
    @pytest.mark.asyncio
    @patch('src.services.chat_service.create_todo_assistant')
    @patch('src.services.chat_service.create_mcp_client')
    async def test_process_new_conversation(
        self,
        mock_create_mcp,
        mock_create_assistant,
        session: Session,
        test_user: User
    ):
        """Test processing a message in a new conversation."""
        # Setup mocks
        mock_assistant = AsyncMock()
        mock_assistant.process_message.return_value = {
            "message": "Hello! How can I help?",
            "tool_calls": []
        }
        mock_create_assistant.return_value = mock_assistant
        
        mock_mcp_client = AsyncMock()
        mock_create_mcp.return_value = mock_mcp_client
        
        # Create request
        request = ChatRequest(
            message="Hello",
            conversation_id=None
        )
        
        # Process request
        response = await ChatService.process_chat_request(
            session,
            user_id=str(test_user.id),
            request=request
        )
        
        # Verify response
        assert isinstance(response, ChatResponse)
        assert response.message == "Hello! How can I help?"
        assert response.conversation_id is not None
        assert response.tool_calls == []
        
        # Verify assistant was called
        mock_assistant.process_message.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('src.services.chat_service.create_todo_assistant')
    @patch('src.services.chat_service.create_mcp_client')
    async def test_process_existing_conversation(
        self,
        mock_create_mcp,
        mock_create_assistant,
        session: Session,
        test_user: User
    ):
        """Test processing a message in an existing conversation."""
        # Create existing conversation
        conversation = Conversation(
            user_id=test_user.id,
            title="Test Chat"
        )
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        
        # Add existing messages
        msg1 = Message(
            conversation_id=conversation.id,
            user_id=test_user.id,
            role="user",
            content="Previous message"
        )
        msg2 = Message(
            conversation_id=conversation.id,
            user_id=test_user.id,
            role="assistant",
            content="Previous response"
        )
        session.add(msg1)
        session.add(msg2)
        session.commit()
        
        # Setup mocks
        mock_assistant = AsyncMock()
        mock_assistant.process_message.return_value = {
            "message": "New response",
            "tool_calls": []
        }
        mock_create_assistant.return_value = mock_assistant
        
        mock_mcp_client = AsyncMock()
        mock_create_mcp.return_value = mock_mcp_client
        
        # Create request
        request = ChatRequest(
            message="New message",
            conversation_id=str(conversation.id)
        )
        
        # Process request
        response = await ChatService.process_chat_request(
            session,
            user_id=str(test_user.id),
            request=request
        )
        
        # Verify response uses existing conversation
        assert response.conversation_id == str(conversation.id)
        assert response.message == "New response"
    
    @pytest.mark.asyncio
    @patch('src.services.chat_service.create_todo_assistant')
    @patch('src.services.chat_service.create_mcp_client')
    async def test_process_with_tool_calls(
        self,
        mock_create_mcp,
        mock_create_assistant,
        session: Session,
        test_user: User
    ):
        """Test processing a message that triggers tool calls."""
        from src.schemas.chat import ToolCall
        
        # Setup mocks
        tool_call = ToolCall(
            tool_name="add_task",
            parameters={"title": "Buy groceries"},
            result={"task_id": "550e8400-e29b-41d4-a716-446655440000"}
        )
        
        mock_assistant = AsyncMock()
        mock_assistant.process_message.return_value = {
            "message": "Done! I've added 'Buy groceries' to your list.",
            "tool_calls": [tool_call]
        }
        mock_create_assistant.return_value = mock_assistant
        
        mock_mcp_client = AsyncMock()
        mock_create_mcp.return_value = mock_mcp_client
        
        # Create request
        request = ChatRequest(
            message="Add a task to buy groceries"
        )
        
        # Process request
        response = await ChatService.process_chat_request(
            session,
            user_id=str(test_user.id),
            request=request
        )
        
        # Verify tool calls in response
        assert len(response.tool_calls) == 1
        assert response.tool_calls[0].tool_name == "add_task"
        assert "Buy groceries" in response.message
    
    @pytest.mark.asyncio
    @patch('src.services.chat_service.create_todo_assistant')
    @patch('src.services.chat_service.create_mcp_client')
    async def test_process_saves_messages_to_database(
        self,
        mock_create_mcp,
        mock_create_assistant,
        session: Session,
        test_user: User
    ):
        """Test that messages are saved to database."""
        # Setup mocks
        mock_assistant = AsyncMock()
        mock_assistant.process_message.return_value = {
            "message": "Response",
            "tool_calls": []
        }
        mock_create_assistant.return_value = mock_assistant
        
        mock_mcp_client = AsyncMock()
        mock_create_mcp.return_value = mock_mcp_client
        
        # Create request
        request = ChatRequest(message="Test message")
        
        # Process request
        response = await ChatService.process_chat_request(
            session,
            user_id=str(test_user.id),
            request=request
        )
        
        # Verify messages were saved
        from sqlmodel import select
        statement = select(Message).where(
            Message.conversation_id == response.conversation_id
        )
        messages = session.exec(statement).all()
        
        assert len(messages) == 2  # User message + assistant message
        assert messages[0].role == "user"
        assert messages[0].content == "Test message"
        assert messages[1].role == "assistant"
        assert messages[1].content == "Response"


class TestProcessChatConvenienceFunction:
    """Tests for process_chat convenience function."""
    
    @pytest.mark.asyncio
    @patch('src.services.chat_service.ChatService.process_chat_request')
    async def test_process_chat_convenience(
        self,
        mock_process,
        session: Session,
        test_user: User
    ):
        """Test convenience function calls main service method."""
        # Setup mock
        mock_response = ChatResponse(
            conversation_id=str(uuid4()),
            message="Response"
        )
        mock_process.return_value = mock_response
        
        # Call convenience function
        response = await process_chat(
            session,
            user_id=str(test_user.id),
            message="Test message"
        )
        
        # Verify it called the main method
        assert response == mock_response
        mock_process.assert_called_once()
        
        # Verify it created a ChatRequest
        call_args = mock_process.call_args
        assert call_args[0][1] == str(test_user.id)
        assert isinstance(call_args[0][2], ChatRequest)
        assert call_args[0][2].message == "Test message"

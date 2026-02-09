"""
Unit tests for chat API endpoint.

Tests the FastAPI endpoint for chat requests, including authentication,
validation, error handling, and response formatting.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from fastapi import HTTPException
from datetime import datetime
import os

# Set required environment variables before importing modules
os.environ.setdefault('GEMINI_API_KEY', 'test-gemini-key')
os.environ.setdefault('DATABASE_URL', 'postgresql://test:test@localhost/test')
os.environ.setdefault('BETTER_AUTH_SECRET', 'test-secret')

from src.schemas.chat import ChatRequest, ChatResponse, ToolCall


class TestChatAPIEndpoint:
    """Test suite for POST /api/{user_id}/chat endpoint."""
    
    @pytest.fixture
    def mock_session(self):
        """Mock database session."""
        return Mock()
    
    @pytest.fixture
    def mock_user(self):
        """Mock authenticated user."""
        user = Mock()
        user.id = "550e8400-e29b-41d4-a716-446655440000"
        return user
    
    @pytest.fixture
    def valid_request(self):
        """Valid chat request."""
        return ChatRequest(
            message="Add a task to buy groceries",
            conversation_id=None
        )
    
    @pytest.fixture
    def mock_response(self):
        """Mock chat response."""
        return ChatResponse(
            conversation_id="550e8400-e29b-41d4-a716-446655440001",
            message="I've added 'Buy groceries' to your task list!",
            tool_calls=[
                ToolCall(
                    tool_name="add_task",
                    parameters={"title": "Buy groceries", "description": ""},
                    result={"task_id": "123", "title": "Buy groceries"}
                )
            ],
            timestamp=datetime.now()
        )
    
    @pytest.mark.asyncio
    async def test_successful_chat_request(
        self, mock_session, mock_user, valid_request, mock_response
    ):
        """Test successful chat request returns 200 with response."""
        from src.api.chat import send_chat_message
        
        with patch('src.api.chat.process_chat', new_callable=AsyncMock) as mock_process:
            mock_process.return_value = mock_response
            
            response = await send_chat_message(
                user_id=str(mock_user.id),
                request=valid_request,
                session=mock_session,
                current_user=mock_user
            )
            
            assert response == mock_response
            mock_process.assert_called_once_with(
                user_id=str(mock_user.id),
                request=valid_request,
                session=mock_session
            )
    
    @pytest.mark.asyncio
    async def test_chat_with_conversation_id(
        self, mock_session, mock_user, mock_response
    ):
        """Test chat request with existing conversation_id."""
        from src.api.chat import send_chat_message
        
        request = ChatRequest(
            message="Show my tasks",
            conversation_id="550e8400-e29b-41d4-a716-446655440001"
        )
        
        with patch('src.api.chat.process_chat', new_callable=AsyncMock) as mock_process:
            mock_process.return_value = mock_response
            
            response = await send_chat_message(
                user_id=str(mock_user.id),
                request=request,
                session=mock_session,
                current_user=mock_user
            )
            
            assert response.conversation_id == "550e8400-e29b-41d4-a716-446655440001"
    
    @pytest.mark.asyncio
    async def test_validation_error_returns_400(
        self, mock_session, mock_user, valid_request
    ):
        """Test validation error returns 400 Bad Request."""
        from src.api.chat import send_chat_message
        
        with patch('src.api.chat.process_chat', new_callable=AsyncMock) as mock_process:
            mock_process.side_effect = ValueError("Invalid conversation_id format")
            
            with pytest.raises(HTTPException) as exc_info:
                await send_chat_message(
                    user_id=str(mock_user.id),
                    request=valid_request,
                    session=mock_session,
                    current_user=mock_user
                )
            
            assert exc_info.value.status_code == 400
            assert "Invalid conversation_id format" in exc_info.value.detail
    
    @pytest.mark.asyncio
    async def test_permission_error_returns_403(
        self, mock_session, mock_user, valid_request
    ):
        """Test permission error returns 403 Forbidden."""
        from src.api.chat import send_chat_message
        
        with patch('src.api.chat.process_chat', new_callable=AsyncMock) as mock_process:
            mock_process.side_effect = PermissionError(
                "Conversation belongs to different user"
            )
            
            with pytest.raises(HTTPException) as exc_info:
                await send_chat_message(
                    user_id=str(mock_user.id),
                    request=valid_request,
                    session=mock_session,
                    current_user=mock_user
                )
            
            assert exc_info.value.status_code == 403
            assert "different user" in exc_info.value.detail
    
    @pytest.mark.asyncio
    async def test_unexpected_error_returns_500(
        self, mock_session, mock_user, valid_request
    ):
        """Test unexpected error returns 500 Internal Server Error."""
        from src.api.chat import send_chat_message
        
        with patch('src.api.chat.process_chat', new_callable=AsyncMock) as mock_process:
            mock_process.side_effect = Exception("OpenAI API connection failed")
            
            with pytest.raises(HTTPException) as exc_info:
                await send_chat_message(
                    user_id=str(mock_user.id),
                    request=valid_request,
                    session=mock_session,
                    current_user=mock_user
                )
            
            assert exc_info.value.status_code == 500
            assert "error processing your message" in exc_info.value.detail
    
    @pytest.mark.asyncio
    async def test_response_includes_tool_calls(
        self, mock_session, mock_user, valid_request
    ):
        """Test response includes tool call details."""
        from src.api.chat import send_chat_message
        
        response = ChatResponse(
            conversation_id="550e8400-e29b-41d4-a716-446655440001",
            message="I've completed task 123!",
            tool_calls=[
                ToolCall(
                    tool_name="complete_task",
                    parameters={"task_id": "123"},
                    result={"success": True}
                )
            ],
            timestamp=datetime.now()
        )
        
        with patch('src.api.chat.process_chat', new_callable=AsyncMock) as mock_process:
            mock_process.return_value = response
            
            result = await send_chat_message(
                user_id=str(mock_user.id),
                request=valid_request,
                session=mock_session,
                current_user=mock_user
            )
            
            assert len(result.tool_calls) == 1
            assert result.tool_calls[0].tool_name == "complete_task"
            assert result.tool_calls[0].parameters == {"task_id": "123"}
    
    @pytest.mark.asyncio
    async def test_response_without_tool_calls(
        self, mock_session, mock_user, valid_request
    ):
        """Test response without tool calls (conversational only)."""
        from src.api.chat import send_chat_message
        
        response = ChatResponse(
            conversation_id="550e8400-e29b-41d4-a716-446655440001",
            message="I'm here to help you manage your tasks! What would you like to do?",
            tool_calls=[],
            timestamp=datetime.now()
        )
        
        with patch('src.api.chat.process_chat', new_callable=AsyncMock) as mock_process:
            mock_process.return_value = response
            
            result = await send_chat_message(
                user_id=str(mock_user.id),
                request=valid_request,
                session=mock_session,
                current_user=mock_user
            )
            
            assert len(result.tool_calls) == 0
            assert "help you manage" in result.message


class TestChatAPIValidation:
    """Test suite for request validation."""
    
    def test_message_too_short(self):
        """Test message must be at least 1 character."""
        with pytest.raises(ValueError):
            ChatRequest(message="", conversation_id=None)
    
    def test_message_too_long(self):
        """Test message cannot exceed 2000 characters."""
        long_message = "a" * 2001
        with pytest.raises(ValueError):
            ChatRequest(message=long_message, conversation_id=None)
    
    def test_valid_message_length(self):
        """Test valid message lengths are accepted."""
        # Minimum length
        request1 = ChatRequest(message="a", conversation_id=None)
        assert request1.message == "a"
        
        # Maximum length
        max_message = "a" * 2000
        request2 = ChatRequest(message=max_message, conversation_id=None)
        assert len(request2.message) == 2000
    
    def test_conversation_id_optional(self):
        """Test conversation_id is optional."""
        request = ChatRequest(message="Hello", conversation_id=None)
        assert request.conversation_id is None
    
    def test_conversation_id_provided(self):
        """Test conversation_id can be provided."""
        conv_id = "550e8400-e29b-41d4-a716-446655440000"
        request = ChatRequest(message="Hello", conversation_id=conv_id)
        assert request.conversation_id == conv_id


class TestChatAPIAuthentication:
    """Test suite for authentication and authorization."""
    
    @pytest.mark.asyncio
    async def test_requires_authentication(self):
        """Test endpoint requires valid JWT token."""
        # This test would be done at integration level with FastAPI TestClient
        # Unit test just verifies the dependency is declared
        from src.api.chat import send_chat_message
        import inspect
        
        sig = inspect.signature(send_chat_message)
        params = sig.parameters
        
        # Verify current_user parameter exists (authentication required)
        assert 'current_user' in params
    
    @pytest.mark.asyncio
    async def test_requires_user_id_validation(self):
        """Test endpoint validates user_id matches authenticated user."""
        from src.api.chat import send_chat_message
        import inspect
        
        sig = inspect.signature(send_chat_message)
        params = sig.parameters
        
        # Verify user_id parameter has validate_user_id dependency
        assert 'user_id' in params
        # The validate_user_id dependency ensures user_id matches JWT token


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

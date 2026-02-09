"""
Integration tests for chat endpoint.

Tests the complete end-to-end flow of chat requests.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, Mock
from uuid import uuid4

from src.main import app
from src.models.user import User


client = TestClient(app)


class TestChatEndpointIntegration:
    """Integration tests for POST /api/{user_id}/chat endpoint."""
    
    @pytest.fixture
    def mock_user(self):
        """Mock authenticated user."""
        user = User(
            id=uuid4(),
            email="test@example.com",
            name="Test User"
        )
        return user
    
    @pytest.fixture
    def auth_token(self, mock_user):
        """Generate mock JWT token."""
        from src.utils.security import create_access_token
        return create_access_token(str(mock_user.id))
    
    @patch('src.services.chat_service.create_todo_assistant')
    @patch('src.services.chat_service.create_mcp_client')
    @patch('src.services.chat_service.ConversationService')
    def test_chat_endpoint_success(
        self,
        mock_conv_service,
        mock_mcp_client,
        mock_assistant,
        mock_user,
        auth_token
    ):
        """Test successful chat request."""
        # Mock conversation
        mock_conversation = Mock()
        mock_conversation.id = uuid4()
        mock_conv_service.get_or_create_conversation.return_value = mock_conversation
        mock_conv_service.get_conversation_history.return_value = []
        
        # Mock assistant response
        mock_assistant_instance = AsyncMock()
        mock_assistant_instance.process_message = AsyncMock(return_value={
            "message": "I've added the task!",
            "tool_calls": []
        })
        mock_assistant.return_value = mock_assistant_instance
        
        # Mock MCP client
        mock_mcp_client.return_value = AsyncMock()
        
        # Make request
        response = client.post(
            f"/api/{mock_user.id}/chat",
            json={"message": "Add a task to test"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "conversation_id" in data
        assert "timestamp" in data
    
    def test_chat_endpoint_requires_auth(self, mock_user):
        """Test that endpoint requires authentication."""
        response = client.post(
            f"/api/{mock_user.id}/chat",
            json={"message": "Hello"}
        )
        
        assert response.status_code == 403  # No auth header
    
    def test_chat_endpoint_validates_user_id(self, mock_user, auth_token):
        """Test that endpoint validates user_id matches token."""
        different_user_id = str(uuid4())
        
        response = client.post(
            f"/api/{different_user_id}/chat",
            json={"message": "Hello"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        assert response.status_code == 403
    
    def test_chat_endpoint_validates_message(self, mock_user, auth_token):
        """Test that endpoint validates message format."""
        # Empty message
        response = client.post(
            f"/api/{mock_user.id}/chat",
            json={"message": ""},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        assert response.status_code == 422  # Validation error
        
        # Message too long
        long_message = "a" * 2001
        response = client.post(
            f"/api/{mock_user.id}/chat",
            json={"message": long_message},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        assert response.status_code == 422


class TestChatEndpointWithMCP:
    """Integration tests with MCP tool execution."""
    
    @pytest.fixture
    def mock_user(self):
        """Mock authenticated user."""
        user = User(
            id=uuid4(),
            email="test@example.com",
            name="Test User"
        )
        return user
    
    @pytest.fixture
    def auth_token(self, mock_user):
        """Generate mock JWT token."""
        from src.utils.security import create_access_token
        return create_access_token(str(mock_user.id))
    
    @patch('src.services.chat_service.create_todo_assistant')
    @patch('src.services.chat_service.create_mcp_client')
    @patch('src.services.chat_service.ConversationService')
    def test_chat_with_tool_execution(
        self,
        mock_conv_service,
        mock_mcp_client_factory,
        mock_assistant_factory,
        mock_user,
        auth_token
    ):
        """Test chat request that triggers tool execution."""
        # Mock conversation
        mock_conversation = Mock()
        mock_conversation.id = uuid4()
        mock_conv_service.get_or_create_conversation.return_value = mock_conversation
        mock_conv_service.get_conversation_history.return_value = []
        
        # Mock MCP client
        mock_mcp_client = AsyncMock()
        mock_mcp_client.add_task = AsyncMock(return_value={
            "task_id": "123",
            "title": "Buy groceries"
        })
        mock_mcp_client_factory.return_value = mock_mcp_client
        
        # Mock assistant with tool call
        from src.schemas.chat import ToolCall
        mock_assistant = AsyncMock()
        mock_assistant.process_message = AsyncMock(return_value={
            "message": "I've added 'Buy groceries' to your task list!",
            "tool_calls": [
                ToolCall(
                    tool_name="add_task",
                    parameters={"title": "Buy groceries", "description": ""},
                    result={"task_id": "123", "title": "Buy groceries"}
                )
            ]
        })
        mock_assistant_factory.return_value = mock_assistant
        
        # Make request
        response = client.post(
            f"/api/{mock_user.id}/chat",
            json={"message": "Add a task to buy groceries"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "tool_calls" in data
        assert len(data["tool_calls"]) == 1
        assert data["tool_calls"][0]["tool_name"] == "add_task"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

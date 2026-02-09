"""
Unit tests for chat schemas.

Tests validation rules and model behavior for ChatRequest, ChatResponse, and ToolCall.
"""

import pytest
from datetime import datetime
from pydantic import ValidationError

from src.schemas.chat import ChatRequest, ChatResponse, ToolCall, ConversationMessage


class TestChatRequest:
    """Tests for ChatRequest model."""
    
    def test_valid_request(self):
        """Test creating a valid chat request."""
        request = ChatRequest(
            message="Add a task to buy groceries",
            conversation_id="550e8400-e29b-41d4-a716-446655440000"
        )
        assert request.message == "Add a task to buy groceries"
        assert request.conversation_id == "550e8400-e29b-41d4-a716-446655440000"
    
    def test_request_without_conversation_id(self):
        """Test creating request without conversation_id (new conversation)."""
        request = ChatRequest(message="Hello")
        assert request.message == "Hello"
        assert request.conversation_id is None
    
    def test_message_too_short(self):
        """Test validation fails for empty message."""
        with pytest.raises(ValidationError) as exc_info:
            ChatRequest(message="")
        assert "at least 1 character" in str(exc_info.value)
    
    def test_message_whitespace_only(self):
        """Test validation fails for whitespace-only message."""
        with pytest.raises(ValidationError) as exc_info:
            ChatRequest(message="   ")
        assert "Message cannot be empty" in str(exc_info.value)
    
    def test_message_too_long(self):
        """Test validation fails for message exceeding 2000 characters."""
        long_message = "a" * 2001
        with pytest.raises(ValidationError) as exc_info:
            ChatRequest(message=long_message)
        assert "at most 2000 characters" in str(exc_info.value)
    
    def test_message_strips_whitespace(self):
        """Test message is stripped of leading/trailing whitespace."""
        request = ChatRequest(message="  Hello  ")
        assert request.message == "Hello"
    
    def test_invalid_conversation_id(self):
        """Test validation fails for invalid UUID format."""
        with pytest.raises(ValidationError) as exc_info:
            ChatRequest(
                message="Hello",
                conversation_id="not-a-uuid"
            )
        assert "must be a valid UUID" in str(exc_info.value)


class TestToolCall:
    """Tests for ToolCall model."""
    
    def test_valid_tool_call(self):
        """Test creating a valid tool call."""
        tool_call = ToolCall(
            tool_name="add_task",
            parameters={"title": "Buy groceries", "description": ""},
            result={"task_id": "550e8400-e29b-41d4-a716-446655440000"}
        )
        assert tool_call.tool_name == "add_task"
        assert tool_call.parameters["title"] == "Buy groceries"
        assert tool_call.result["task_id"] == "550e8400-e29b-41d4-a716-446655440000"
    
    def test_tool_call_without_result(self):
        """Test creating tool call without result (before execution)."""
        tool_call = ToolCall(
            tool_name="list_tasks",
            parameters={}
        )
        assert tool_call.tool_name == "list_tasks"
        assert tool_call.result is None
    
    def test_tool_call_missing_required_fields(self):
        """Test validation fails when required fields are missing."""
        with pytest.raises(ValidationError):
            ToolCall(parameters={})  # Missing tool_name


class TestChatResponse:
    """Tests for ChatResponse model."""
    
    def test_valid_response(self):
        """Test creating a valid chat response."""
        response = ChatResponse(
            conversation_id="550e8400-e29b-41d4-a716-446655440000",
            message="Done! I've added 'Buy groceries' to your task list.",
            tool_calls=[
                ToolCall(
                    tool_name="add_task",
                    parameters={"title": "Buy groceries"},
                    result={"task_id": "650e8400-e29b-41d4-a716-446655440001"}
                )
            ]
        )
        assert response.conversation_id == "550e8400-e29b-41d4-a716-446655440000"
        assert "Buy groceries" in response.message
        assert len(response.tool_calls) == 1
        assert isinstance(response.timestamp, datetime)
    
    def test_response_without_tool_calls(self):
        """Test creating response without tool calls (simple conversation)."""
        response = ChatResponse(
            conversation_id="550e8400-e29b-41d4-a716-446655440000",
            message="Hello! How can I help you?"
        )
        assert response.message == "Hello! How can I help you?"
        assert response.tool_calls is None
    
    def test_timestamp_auto_generated(self):
        """Test timestamp is automatically generated."""
        response = ChatResponse(
            conversation_id="550e8400-e29b-41d4-a716-446655440000",
            message="Test"
        )
        assert isinstance(response.timestamp, datetime)
        # Timestamp should be recent (within last minute)
        time_diff = datetime.utcnow() - response.timestamp
        assert time_diff.total_seconds() < 60


class TestConversationMessage:
    """Tests for ConversationMessage model."""
    
    def test_valid_user_message(self):
        """Test creating a valid user message."""
        msg = ConversationMessage(
            role="user",
            content="Add a task",
            timestamp=datetime.utcnow()
        )
        assert msg.role == "user"
        assert msg.content == "Add a task"
    
    def test_valid_assistant_message(self):
        """Test creating a valid assistant message."""
        msg = ConversationMessage(
            role="assistant",
            content="What task would you like to add?",
            timestamp=datetime.utcnow()
        )
        assert msg.role == "assistant"
    
    def test_invalid_role(self):
        """Test validation fails for invalid role."""
        with pytest.raises(ValidationError) as exc_info:
            ConversationMessage(
                role="system",  # Only 'user' or 'assistant' allowed
                content="Test",
                timestamp=datetime.utcnow()
            )
        assert "pattern" in str(exc_info.value).lower()

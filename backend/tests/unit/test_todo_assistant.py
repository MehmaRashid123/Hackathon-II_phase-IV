"""
Unit tests for TodoAssistant.

Tests agent initialization and message processing with mocked Gemini API.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch, Mock
from uuid import uuid4
import json
import os

# Set environment variables before imports
os.environ.setdefault('GEMINI_API_KEY', 'test-gemini-key')
os.environ.setdefault('DATABASE_URL', 'postgresql://test:test@localhost/test')
os.environ.setdefault('BETTER_AUTH_SECRET', 'test-secret')

from src.agents.todo_assistant import (
    TodoAssistant,
    create_todo_assistant,
    AgentProcessingError
)
from src.agents.context import AgentContext
from src.services.mcp_client import MCPClient
from src.schemas.chat import ToolCall


class TestTodoAssistantInitialization:
    """Tests for TodoAssistant initialization."""
    
    @patch('src.agents.todo_assistant.genai')
    def test_initialization_with_defaults(self, mock_genai):
        """Test initializing assistant with default settings."""
        mock_genai.GenerativeModel.return_value = Mock()
        
        assistant = TodoAssistant()
        
        assert assistant.model_name == "gemini-2.5-flash"
        assert assistant.max_tokens == 4000
        assert assistant.temperature == 0.7
        mock_genai.configure.assert_called_once()
    
    @patch('src.agents.todo_assistant.genai')
    def test_initialization_with_custom_settings(self, mock_genai):
        """Test initializing assistant with custom settings."""
        mock_genai.GenerativeModel.return_value = Mock()
        
        assistant = TodoAssistant(
            api_key="test-key",
            model="gemini-pro",
            max_tokens=2000,
            temperature=0.5
        )
        
        assert assistant.model_name == "gemini-pro"
        assert assistant.max_tokens == 2000
        assert assistant.temperature == 0.5
    
    @patch('src.agents.todo_assistant.genai')
    def test_create_todo_assistant_factory(self, mock_genai):
        """Test factory function creates assistant correctly."""
        mock_genai.GenerativeModel.return_value = Mock()
        
        assistant = create_todo_assistant(
            api_key="factory-key",
            model="gemini-pro"
        )
        
        assert isinstance(assistant, TodoAssistant)
        assert assistant.model_name == "gemini-pro"


class TestProcessMessage:
    """Tests for message processing."""
    
    @pytest.fixture
    def mock_mcp_client(self):
        """Mock MCP client."""
        client = AsyncMock(spec=MCPClient)
        client.user_id = str(uuid4())
        return client
    
    @pytest.fixture
    def agent_context(self):
        """Create agent context for testing."""
        context = AgentContext(
            user_id=uuid4(),
            conversation_id=str(uuid4()),
            conversation_history=[],
            system_instructions="You are a helpful assistant",
            available_tools=[]
        )
        context.add_message("user", "Hello")
        return context
    
    @pytest.mark.asyncio
    @patch('src.agents.todo_assistant.genai')
    async def test_process_simple_message_no_tools(self, mock_genai, agent_context, mock_mcp_client):
        """Test processing a simple message without tool calls."""
        # Mock Gemini response
        mock_response = Mock()
        mock_response.text = "Hello! How can I help you?"
        mock_response.candidates = [Mock()]
        mock_response.candidates[0].content.parts = []
        
        mock_chat = Mock()
        mock_chat.send_message = Mock(return_value=mock_response)
        
        mock_model = Mock()
        mock_model.start_chat = Mock(return_value=mock_chat)
        mock_genai.GenerativeModel.return_value = mock_model
        
        assistant = TodoAssistant()
        result = await assistant.process_message(
            context=agent_context,
            user_message="Hello",
            mcp_client=mock_mcp_client
        )
        
        assert result["message"] == "Hello! How can I help you?"
        assert len(result["tool_calls"]) == 0
    
    @pytest.mark.asyncio
    @patch('src.agents.todo_assistant.genai')
    async def test_process_message_with_tool_call(self, mock_genai, agent_context, mock_mcp_client):
        """Test processing a message that triggers a tool call."""
        # Mock function call
        mock_function_call = Mock()
        mock_function_call.name = "add_task"
        mock_function_call.args = {"title": "Buy groceries", "description": ""}
        
        # Mock first response with function call
        mock_part = Mock()
        mock_part.function_call = mock_function_call
        
        mock_response1 = Mock()
        mock_response1.candidates = [Mock()]
        mock_response1.candidates[0].content.parts = [mock_part]
        
        # Mock second response after tool execution
        mock_response2 = Mock()
        mock_response2.text = "I've added 'Buy groceries' to your task list!"
        mock_response2.candidates = [Mock()]
        mock_response2.candidates[0].content.parts = []
        
        mock_chat = Mock()
        mock_chat.send_message = Mock(side_effect=[mock_response1, mock_response2])
        
        mock_model = Mock()
        mock_model.start_chat = Mock(return_value=mock_chat)
        mock_genai.GenerativeModel.return_value = mock_model
        
        # Mock MCP client response
        mock_mcp_client.add_task = AsyncMock(
            return_value={"task_id": "123", "title": "Buy groceries"}
        )
        
        assistant = TodoAssistant()
        result = await assistant.process_message(
            context=agent_context,
            user_message="Add a task to buy groceries",
            mcp_client=mock_mcp_client
        )
        
        assert "added" in result["message"].lower() or "groceries" in result["message"].lower()
        assert len(result["tool_calls"]) == 1
        assert result["tool_calls"][0].tool_name == "add_task"
        assert result["tool_calls"][0].parameters["title"] == "Buy groceries"
    
    @pytest.mark.asyncio
    @patch('src.agents.todo_assistant.genai')
    async def test_process_message_adds_to_context(self, mock_genai, agent_context, mock_mcp_client):
        """Test that processed messages are added to context."""
        mock_response = Mock()
        mock_response.text = "Response message"
        mock_response.candidates = [Mock()]
        mock_response.candidates[0].content.parts = []
        
        mock_chat = Mock()
        mock_chat.send_message = Mock(return_value=mock_response)
        
        mock_model = Mock()
        mock_model.start_chat = Mock(return_value=mock_chat)
        mock_genai.GenerativeModel.return_value = mock_model
        
        initial_length = len(agent_context.conversation_history)
        
        assistant = TodoAssistant()
        await assistant.process_message(
            context=agent_context,
            user_message="Test message",
            mcp_client=mock_mcp_client
        )
        
        # Should add user message and assistant response
        assert len(agent_context.conversation_history) == initial_length + 2


class TestExecuteToolCall:
    """Tests for tool execution."""
    
    @pytest.fixture
    def mock_mcp_client(self):
        """Mock MCP client."""
        client = AsyncMock(spec=MCPClient)
        client.user_id = str(uuid4())
        return client
    
    @pytest.fixture
    def agent_context(self):
        """Create agent context for testing."""
        return AgentContext(
            user_id=uuid4(),
            conversation_id=str(uuid4()),
            conversation_history=[],
            system_instructions="You are a helpful assistant",
            available_tools=[]
        )
    
    @pytest.mark.asyncio
    @patch('src.agents.todo_assistant.genai')
    async def test_execute_add_task_tool(self, mock_genai, agent_context, mock_mcp_client):
        """Test executing add_task tool."""
        mock_genai.GenerativeModel.return_value = Mock()
        
        mock_mcp_client.add_task = AsyncMock(
            return_value={"task_id": "123", "title": "Test task"}
        )
        
        assistant = TodoAssistant()
        result = await assistant._execute_tool_call(
            "add_task",
            {"title": "Test task", "description": ""},
            mock_mcp_client
        )
        
        assert isinstance(result, ToolCall)
        assert result.tool_name == "add_task"
        assert result.result["task_id"] == "123"
    
    @pytest.mark.asyncio
    @patch('src.agents.todo_assistant.genai')
    async def test_execute_list_tasks_tool(self, mock_genai, agent_context, mock_mcp_client):
        """Test executing list_tasks tool."""
        mock_genai.GenerativeModel.return_value = Mock()
        
        mock_mcp_client.list_tasks = AsyncMock(
            return_value={"tasks": []}
        )
        
        assistant = TodoAssistant()
        result = await assistant._execute_tool_call(
            "list_tasks",
            {},
            mock_mcp_client
        )
        
        assert isinstance(result, ToolCall)
        assert result.tool_name == "list_tasks"
        assert "tasks" in result.result
    
    @pytest.mark.asyncio
    @patch('src.agents.todo_assistant.genai')
    async def test_execute_complete_task_tool(self, mock_genai, agent_context, mock_mcp_client):
        """Test executing complete_task tool."""
        mock_genai.GenerativeModel.return_value = Mock()
        
        mock_mcp_client.complete_task = AsyncMock(
            return_value={"success": True}
        )
        
        assistant = TodoAssistant()
        result = await assistant._execute_tool_call(
            "complete_task",
            {"task_id": "123"},
            mock_mcp_client
        )
        
        assert isinstance(result, ToolCall)
        assert result.tool_name == "complete_task"
        assert result.result["success"] is True
    
    @pytest.mark.asyncio
    @patch('src.agents.todo_assistant.genai')
    async def test_execute_unknown_tool_raises_error(self, mock_genai, agent_context, mock_mcp_client):
        """Test that unknown tool raises ValueError."""
        mock_genai.GenerativeModel.return_value = Mock()
        
        assistant = TodoAssistant()
        
        with pytest.raises(ValueError, match="Unknown tool"):
            await assistant._execute_tool_call(
                "unknown_tool",
                {},
                mock_mcp_client
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

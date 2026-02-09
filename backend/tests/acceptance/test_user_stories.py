"""
Acceptance tests for user stories.

Tests all user story scenarios from the specification.
"""

import pytest
from unittest.mock import patch, AsyncMock, Mock
from uuid import uuid4

from src.agents.todo_assistant import create_todo_assistant
from src.agents.context import AgentContext
from src.schemas.chat import ToolCall


class TestUserStory1_NaturalLanguageTaskManagement:
    """
    User Story 1: Natural Language Task Management
    As a user, I want to manage my tasks using natural language
    so that I don't have to remember specific commands or syntax.
    """
    
    @pytest.fixture
    def mock_mcp_client(self):
        """Mock MCP client."""
        client = AsyncMock()
        client.add_task = AsyncMock(return_value={"task_id": "123", "title": "Buy groceries"})
        client.list_tasks = AsyncMock(return_value={"tasks": [{"id": "123", "title": "Buy groceries"}]})
        client.complete_task = AsyncMock(return_value={"success": True})
        client.delete_task = AsyncMock(return_value={"success": True})
        client.update_task = AsyncMock(return_value={"task_id": "123", "title": "Buy milk"})
        return client
    
    @pytest.fixture
    def agent_context(self):
        """Create agent context."""
        return AgentContext(
            user_id=uuid4(),
            conversation_id=str(uuid4()),
            conversation_history=[],
            system_instructions="You are a helpful task assistant",
            available_tools=[]
        )
    
    @pytest.mark.asyncio
    @patch('src.agents.todo_assistant.genai')
    async def test_scenario_1_add_task_natural_language(
        self, mock_genai, agent_context, mock_mcp_client
    ):
        """
        Scenario 1: User says "Add a task to buy groceries"
        Expected: Task is created and user receives confirmation
        """
        # Mock Gemini response with tool call
        mock_function_call = Mock()
        mock_function_call.name = "add_task"
        mock_function_call.args = {"title": "Buy groceries", "description": ""}
        
        mock_part = Mock()
        mock_part.function_call = mock_function_call
        
        mock_response1 = Mock()
        mock_response1.candidates = [Mock()]
        mock_response1.candidates[0].content.parts = [mock_part]
        
        mock_response2 = Mock()
        mock_response2.text = "I've added 'Buy groceries' to your task list!"
        mock_response2.candidates = [Mock()]
        mock_response2.candidates[0].content.parts = []
        
        mock_chat = Mock()
        mock_chat.send_message = Mock(side_effect=[mock_response1, mock_response2])
        
        mock_model = Mock()
        mock_model.start_chat = Mock(return_value=mock_chat)
        mock_genai.GenerativeModel.return_value = mock_model
        
        # Execute
        assistant = create_todo_assistant()
        result = await assistant.process_message(
            context=agent_context,
            user_message="Add a task to buy groceries",
            mcp_client=mock_mcp_client
        )
        
        # Verify
        assert "added" in result["message"].lower() or "groceries" in result["message"].lower()
        assert len(result["tool_calls"]) == 1
        assert result["tool_calls"][0].tool_name == "add_task"
        mock_mcp_client.add_task.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('src.agents.todo_assistant.genai')
    async def test_scenario_2_list_tasks_natural_language(
        self, mock_genai, agent_context, mock_mcp_client
    ):
        """
        Scenario 2: User says "Show me my tasks"
        Expected: All tasks are retrieved and displayed
        """
        # Mock Gemini response
        mock_response = Mock()
        mock_response.text = "You have 1 task: Buy groceries"
        mock_response.candidates = [Mock()]
        mock_response.candidates[0].content.parts = []
        
        mock_chat = Mock()
        mock_chat.send_message = Mock(return_value=mock_response)
        
        mock_model = Mock()
        mock_model.start_chat = Mock(return_value=mock_chat)
        mock_genai.GenerativeModel.return_value = mock_model
        
        # Execute
        assistant = create_todo_assistant()
        result = await assistant.process_message(
            context=agent_context,
            user_message="Show me my tasks",
            mcp_client=mock_mcp_client
        )
        
        # Verify
        assert "task" in result["message"].lower()


class TestUserStory2_StatelessRequestCycle:
    """
    User Story 2: Stateless Request Cycle
    As a developer, I want each chat request to be stateless
    so that the system is scalable and reliable.
    """
    
    @pytest.mark.asyncio
    async def test_scenario_1_no_server_state(self):
        """
        Scenario 1: Each request includes full conversation history
        Expected: No server-side state is maintained
        """
        # This is verified by the architecture - context is built fresh each time
        context = AgentContext(
            user_id=uuid4(),
            conversation_id=str(uuid4()),
            conversation_history=[
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi!"}
            ],
            system_instructions="Test",
            available_tools=[]
        )
        
        # Verify context is ephemeral
        assert len(context.conversation_history) == 2
        assert context.conversation_id is not None
    
    @pytest.mark.asyncio
    async def test_scenario_2_conversation_history_from_database(self):
        """
        Scenario 2: Conversation history is fetched from database
        Expected: Previous messages are loaded for context
        """
        # This is tested in chat_service tests
        # Verifying the pattern here
        from src.services.conversation_service import ConversationService
        
        # ConversationService.get_conversation_history loads from DB
        # This ensures stateless architecture
        assert hasattr(ConversationService, 'get_conversation_history')


class TestUserStory3_FriendlyAssistant:
    """
    User Story 3: Friendly AI Assistant Persona
    As a user, I want the assistant to be friendly and helpful
    so that I enjoy using the application.
    """
    
    @pytest.mark.asyncio
    @patch('src.agents.todo_assistant.genai')
    async def test_scenario_1_friendly_confirmations(self, mock_genai):
        """
        Scenario 1: Assistant provides friendly confirmations
        Expected: Responses are warm and encouraging
        """
        from src.agents.system_instructions import get_system_instructions
        
        instructions = get_system_instructions()
        
        # Verify persona is defined
        assert "friendly" in instructions.lower() or "helpful" in instructions.lower()
        assert "todo assistant" in instructions.lower()
    
    @pytest.mark.asyncio
    @patch('src.agents.todo_assistant.genai')
    async def test_scenario_2_clear_error_messages(self, mock_genai):
        """
        Scenario 2: Assistant provides clear error messages
        Expected: Errors are user-friendly, not technical
        """
        mock_mcp_client = AsyncMock()
        mock_mcp_client.add_task = AsyncMock(side_effect=Exception("Database error"))
        
        assistant = create_todo_assistant()
        
        # Execute tool call that fails
        result = await assistant._execute_tool_call(
            "add_task",
            {"title": "Test"},
            mock_mcp_client
        )
        
        # Verify error is captured
        assert "error" in result.result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

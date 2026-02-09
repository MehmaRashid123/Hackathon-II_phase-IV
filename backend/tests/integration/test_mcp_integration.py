"""
Integration tests for MCP tool integration.

Tests that all MCP tools are callable and work correctly.
"""

import pytest
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from src.agents.todo_assistant import create_todo_assistant
from src.agents.context import AgentContext
from src.services.mcp_client import MCPClient
from src.schemas.chat import ToolCall


class TestMCPToolIntegration:
    """Test MCP tool integration with the assistant."""
    
    @pytest.fixture
    def mock_mcp_client(self):
        """Mock MCP client with all tools."""
        client = AsyncMock(spec=MCPClient)
        client.add_task = AsyncMock(return_value={"task_id": "123", "title": "Test"})
        client.list_tasks = AsyncMock(return_value={"tasks": []})
        client.complete_task = AsyncMock(return_value={"success": True})
        client.delete_task = AsyncMock(return_value={"success": True})
        client.update_task = AsyncMock(return_value={"task_id": "123", "title": "Updated"})
        return client
    
    @pytest.fixture
    def agent_context(self):
        """Create agent context."""
        return AgentContext(
            user_id=uuid4(),
            conversation_id=str(uuid4()),
            conversation_history=[],
            system_instructions="You are a helpful assistant",
            available_tools=[]
        )
    
    @pytest.mark.asyncio
    @patch('src.agents.todo_assistant.genai')
    async def test_add_task_tool(self, mock_genai, agent_context, mock_mcp_client):
        """Test add_task tool execution."""
        assistant = create_todo_assistant()
        
        result = await assistant._execute_tool_call(
            "add_task",
            {"title": "Test task", "description": "Test description"},
            mock_mcp_client
        )
        
        assert isinstance(result, ToolCall)
        assert result.tool_name == "add_task"
        assert result.result["task_id"] == "123"
        mock_mcp_client.add_task.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('src.agents.todo_assistant.genai')
    async def test_list_tasks_tool(self, mock_genai, agent_context, mock_mcp_client):
        """Test list_tasks tool execution."""
        assistant = create_todo_assistant()
        
        result = await assistant._execute_tool_call(
            "list_tasks",
            {},
            mock_mcp_client
        )
        
        assert isinstance(result, ToolCall)
        assert result.tool_name == "list_tasks"
        assert "tasks" in result.result
        mock_mcp_client.list_tasks.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('src.agents.todo_assistant.genai')
    async def test_complete_task_tool(self, mock_genai, agent_context, mock_mcp_client):
        """Test complete_task tool execution."""
        assistant = create_todo_assistant()
        
        result = await assistant._execute_tool_call(
            "complete_task",
            {"task_id": "123"},
            mock_mcp_client
        )
        
        assert isinstance(result, ToolCall)
        assert result.tool_name == "complete_task"
        assert result.result["success"] is True
        mock_mcp_client.complete_task.assert_called_once_with(task_id="123")
    
    @pytest.mark.asyncio
    @patch('src.agents.todo_assistant.genai')
    async def test_delete_task_tool(self, mock_genai, agent_context, mock_mcp_client):
        """Test delete_task tool execution."""
        assistant = create_todo_assistant()
        
        result = await assistant._execute_tool_call(
            "delete_task",
            {"task_id": "123"},
            mock_mcp_client
        )
        
        assert isinstance(result, ToolCall)
        assert result.tool_name == "delete_task"
        assert result.result["success"] is True
        mock_mcp_client.delete_task.assert_called_once_with(task_id="123")
    
    @pytest.mark.asyncio
    @patch('src.agents.todo_assistant.genai')
    async def test_update_task_tool(self, mock_genai, agent_context, mock_mcp_client):
        """Test update_task tool execution."""
        assistant = create_todo_assistant()
        
        result = await assistant._execute_tool_call(
            "update_task",
            {"task_id": "123", "title": "Updated title"},
            mock_mcp_client
        )
        
        assert isinstance(result, ToolCall)
        assert result.tool_name == "update_task"
        assert result.result["title"] == "Updated"
        mock_mcp_client.update_task.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

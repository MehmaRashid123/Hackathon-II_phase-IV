"""
Unit tests for tool definitions.

Tests that MCP tool schemas are properly defined for OpenAI function calling.
"""

import pytest

from src.agents.tool_definitions import (
    ADD_TASK_TOOL,
    LIST_TASKS_TOOL,
    COMPLETE_TASK_TOOL,
    DELETE_TASK_TOOL,
    UPDATE_TASK_TOOL,
    get_all_tools,
    get_tool_by_name,
    get_tool_names
)


class TestToolStructure:
    """Tests for tool definition structure."""
    
    def test_all_tools_have_correct_structure(self):
        """Test that all tools have required OpenAI function calling structure."""
        tools = get_all_tools()
        
        for tool in tools:
            # Check top-level structure
            assert "type" in tool
            assert tool["type"] == "function"
            assert "function" in tool
            
            # Check function structure
            func = tool["function"]
            assert "name" in func
            assert "description" in func
            assert "parameters" in func
            
            # Check parameters structure
            params = func["parameters"]
            assert "type" in params
            assert params["type"] == "object"
            assert "properties" in params
            assert "required" in params
    
    def test_tool_names_are_unique(self):
        """Test that all tool names are unique."""
        tools = get_all_tools()
        names = [tool["function"]["name"] for tool in tools]
        assert len(names) == len(set(names))
    
    def test_tool_descriptions_not_empty(self):
        """Test that all tools have non-empty descriptions."""
        tools = get_all_tools()
        for tool in tools:
            desc = tool["function"]["description"]
            assert desc
            assert len(desc.strip()) > 10  # Meaningful description


class TestAddTaskTool:
    """Tests for add_task tool definition."""
    
    def test_add_task_has_title_parameter(self):
        """Test that add_task requires title parameter."""
        params = ADD_TASK_TOOL["function"]["parameters"]
        assert "title" in params["properties"]
        assert "title" in params["required"]
    
    def test_add_task_has_description_parameter(self):
        """Test that add_task has optional description parameter."""
        params = ADD_TASK_TOOL["function"]["parameters"]
        assert "description" in params["properties"]
        assert "description" not in params["required"]  # Optional
    
    def test_add_task_name(self):
        """Test add_task tool name."""
        assert ADD_TASK_TOOL["function"]["name"] == "add_task"


class TestListTasksTool:
    """Tests for list_tasks tool definition."""
    
    def test_list_tasks_has_no_required_parameters(self):
        """Test that list_tasks requires no parameters."""
        params = LIST_TASKS_TOOL["function"]["parameters"]
        assert len(params["required"]) == 0
    
    def test_list_tasks_name(self):
        """Test list_tasks tool name."""
        assert LIST_TASKS_TOOL["function"]["name"] == "list_tasks"


class TestCompleteTaskTool:
    """Tests for complete_task tool definition."""
    
    def test_complete_task_requires_task_id(self):
        """Test that complete_task requires task_id parameter."""
        params = COMPLETE_TASK_TOOL["function"]["parameters"]
        assert "task_id" in params["properties"]
        assert "task_id" in params["required"]
    
    def test_complete_task_name(self):
        """Test complete_task tool name."""
        assert COMPLETE_TASK_TOOL["function"]["name"] == "complete_task"


class TestDeleteTaskTool:
    """Tests for delete_task tool definition."""
    
    def test_delete_task_requires_task_id(self):
        """Test that delete_task requires task_id parameter."""
        params = DELETE_TASK_TOOL["function"]["parameters"]
        assert "task_id" in params["properties"]
        assert "task_id" in params["required"]
    
    def test_delete_task_name(self):
        """Test delete_task tool name."""
        assert DELETE_TASK_TOOL["function"]["name"] == "delete_task"


class TestUpdateTaskTool:
    """Tests for update_task tool definition."""
    
    def test_update_task_requires_task_id(self):
        """Test that update_task requires task_id parameter."""
        params = UPDATE_TASK_TOOL["function"]["parameters"]
        assert "task_id" in params["properties"]
        assert "task_id" in params["required"]
    
    def test_update_task_has_optional_fields(self):
        """Test that update_task has optional title and description."""
        params = UPDATE_TASK_TOOL["function"]["parameters"]
        assert "title" in params["properties"]
        assert "description" in params["properties"]
        assert "title" not in params["required"]
        assert "description" not in params["required"]
    
    def test_update_task_name(self):
        """Test update_task tool name."""
        assert UPDATE_TASK_TOOL["function"]["name"] == "update_task"


class TestGetAllTools:
    """Tests for get_all_tools function."""
    
    def test_returns_list(self):
        """Test that get_all_tools returns a list."""
        tools = get_all_tools()
        assert isinstance(tools, list)
    
    def test_returns_five_tools(self):
        """Test that get_all_tools returns all 5 tools."""
        tools = get_all_tools()
        assert len(tools) == 5
    
    def test_includes_all_tool_types(self):
        """Test that all tool types are included."""
        tools = get_all_tools()
        names = [tool["function"]["name"] for tool in tools]
        
        assert "add_task" in names
        assert "list_tasks" in names
        assert "complete_task" in names
        assert "delete_task" in names
        assert "update_task" in names


class TestGetToolByName:
    """Tests for get_tool_by_name function."""
    
    def test_get_add_task(self):
        """Test getting add_task tool by name."""
        tool = get_tool_by_name("add_task")
        assert tool["function"]["name"] == "add_task"
    
    def test_get_list_tasks(self):
        """Test getting list_tasks tool by name."""
        tool = get_tool_by_name("list_tasks")
        assert tool["function"]["name"] == "list_tasks"
    
    def test_invalid_tool_name_raises_error(self):
        """Test that invalid tool name raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            get_tool_by_name("invalid_tool")
        assert "not found" in str(exc_info.value)
        assert "invalid_tool" in str(exc_info.value)


class TestGetToolNames:
    """Tests for get_tool_names function."""
    
    def test_returns_list_of_strings(self):
        """Test that get_tool_names returns list of strings."""
        names = get_tool_names()
        assert isinstance(names, list)
        assert all(isinstance(name, str) for name in names)
    
    def test_returns_five_names(self):
        """Test that get_tool_names returns 5 tool names."""
        names = get_tool_names()
        assert len(names) == 5
    
    def test_includes_all_tools(self):
        """Test that all tool names are included."""
        names = get_tool_names()
        assert "add_task" in names
        assert "list_tasks" in names
        assert "complete_task" in names
        assert "delete_task" in names
        assert "update_task" in names

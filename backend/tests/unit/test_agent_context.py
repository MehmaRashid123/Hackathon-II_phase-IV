"""
Unit tests for AgentContext.

Tests context initialization, message management, and OpenAI format conversion.
"""

import pytest
from uuid import UUID, uuid4

from src.agents.context import AgentContext


class TestAgentContextInitialization:
    """Tests for AgentContext initialization."""
    
    def test_valid_initialization(self):
        """Test creating a valid agent context."""
        user_id = uuid4()
        context = AgentContext(
            user_id=user_id,
            conversation_history=[
                {"role": "user", "content": "Hello"}
            ],
            system_instructions="You are a Todo Assistant",
            available_tools=[
                {"function": {"name": "add_task", "description": "Add a task"}}
            ],
            conversation_id=str(uuid4())
        )
        assert context.user_id == user_id
        assert len(context.conversation_history) == 1
        assert context.system_instructions == "You are a Todo Assistant"
        assert len(context.available_tools) == 1
    
    def test_minimal_initialization(self):
        """Test creating context with only required fields."""
        user_id = uuid4()
        context = AgentContext(user_id=user_id)
        assert context.user_id == user_id
        assert context.conversation_history == []
        assert context.system_instructions == ""
        assert context.available_tools == []
        assert context.conversation_id is None
    
    def test_invalid_user_id_type(self):
        """Test validation fails for non-UUID user_id."""
        with pytest.raises(ValueError) as exc_info:
            AgentContext(user_id="not-a-uuid")
        assert "must be a UUID instance" in str(exc_info.value)
    
    def test_invalid_conversation_id_format(self):
        """Test validation fails for invalid conversation_id format."""
        with pytest.raises(ValueError) as exc_info:
            AgentContext(
                user_id=uuid4(),
                conversation_id="not-a-uuid"
            )
        assert "must be a valid UUID string" in str(exc_info.value)


class TestAddMessage:
    """Tests for add_message method."""
    
    def test_add_user_message(self):
        """Test adding a user message to history."""
        context = AgentContext(user_id=uuid4())
        context.add_message("user", "Add a task")
        
        assert len(context.conversation_history) == 1
        assert context.conversation_history[0]["role"] == "user"
        assert context.conversation_history[0]["content"] == "Add a task"
    
    def test_add_assistant_message(self):
        """Test adding an assistant message to history."""
        context = AgentContext(user_id=uuid4())
        context.add_message("assistant", "What task?")
        
        assert len(context.conversation_history) == 1
        assert context.conversation_history[0]["role"] == "assistant"
    
    def test_add_multiple_messages(self):
        """Test adding multiple messages maintains order."""
        context = AgentContext(user_id=uuid4())
        context.add_message("user", "Message 1")
        context.add_message("assistant", "Message 2")
        context.add_message("user", "Message 3")
        
        assert len(context.conversation_history) == 3
        assert context.conversation_history[0]["content"] == "Message 1"
        assert context.conversation_history[1]["content"] == "Message 2"
        assert context.conversation_history[2]["content"] == "Message 3"
    
    def test_invalid_role(self):
        """Test validation fails for invalid role."""
        context = AgentContext(user_id=uuid4())
        with pytest.raises(ValueError) as exc_info:
            context.add_message("system", "Invalid")
        assert "must be 'user' or 'assistant'" in str(exc_info.value)


class TestGetMessagesForOpenAI:
    """Tests for get_messages_for_openai method."""
    
    def test_with_system_instructions(self):
        """Test messages include system instructions as first message."""
        context = AgentContext(
            user_id=uuid4(),
            system_instructions="You are a Todo Assistant"
        )
        context.add_message("user", "Hello")
        
        messages = context.get_messages_for_openai()
        
        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert messages[0]["content"] == "You are a Todo Assistant"
        assert messages[1]["role"] == "user"
        assert messages[1]["content"] == "Hello"
    
    def test_without_system_instructions(self):
        """Test messages work without system instructions."""
        context = AgentContext(user_id=uuid4())
        context.add_message("user", "Hello")
        
        messages = context.get_messages_for_openai()
        
        assert len(messages) == 1
        assert messages[0]["role"] == "user"
    
    def test_conversation_history_order(self):
        """Test conversation history maintains correct order."""
        context = AgentContext(
            user_id=uuid4(),
            system_instructions="System prompt"
        )
        context.add_message("user", "First")
        context.add_message("assistant", "Second")
        context.add_message("user", "Third")
        
        messages = context.get_messages_for_openai()
        
        assert len(messages) == 4  # system + 3 messages
        assert messages[0]["role"] == "system"
        assert messages[1]["content"] == "First"
        assert messages[2]["content"] == "Second"
        assert messages[3]["content"] == "Third"
    
    def test_empty_history(self):
        """Test with empty conversation history."""
        context = AgentContext(
            user_id=uuid4(),
            system_instructions="System prompt"
        )
        
        messages = context.get_messages_for_openai()
        
        assert len(messages) == 1
        assert messages[0]["role"] == "system"


class TestGetToolNames:
    """Tests for get_tool_names method."""
    
    def test_extract_tool_names(self):
        """Test extracting tool names from tool definitions."""
        context = AgentContext(
            user_id=uuid4(),
            available_tools=[
                {"function": {"name": "add_task", "description": "Add"}},
                {"function": {"name": "list_tasks", "description": "List"}},
                {"function": {"name": "delete_task", "description": "Delete"}}
            ]
        )
        
        tool_names = context.get_tool_names()
        
        assert len(tool_names) == 3
        assert "add_task" in tool_names
        assert "list_tasks" in tool_names
        assert "delete_task" in tool_names
    
    def test_no_tools(self):
        """Test with no tools available."""
        context = AgentContext(user_id=uuid4())
        tool_names = context.get_tool_names()
        assert tool_names == []


class TestRepr:
    """Tests for __repr__ method."""
    
    def test_repr_format(self):
        """Test string representation includes key information."""
        user_id = uuid4()
        conv_id = str(uuid4())
        context = AgentContext(
            user_id=user_id,
            conversation_id=conv_id,
            available_tools=[
                {"function": {"name": "add_task"}},
                {"function": {"name": "list_tasks"}}
            ]
        )
        context.add_message("user", "Hello")
        
        repr_str = repr(context)
        
        assert "AgentContext" in repr_str
        assert str(user_id) in repr_str
        assert conv_id in repr_str
        assert "history_length=1" in repr_str
        assert "add_task" in repr_str
        assert "list_tasks" in repr_str

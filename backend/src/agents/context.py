"""
Agent Context

Ephemeral data structure to hold agent context during request processing.
This context is built fresh for each request (stateless architecture).
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from uuid import UUID


@dataclass
class AgentContext:
    """
    Ephemeral context for agent request processing.
    
    This context is built fresh for each chat request and contains all
    information needed to process the request in a stateless manner.
    
    Attributes:
        user_id: UUID of the user making the request
        conversation_history: List of previous messages in conversation
        system_instructions: System prompt defining agent persona and behavior
        available_tools: List of MCP tool definitions for function calling
        conversation_id: ID of current conversation (new or existing)
        mcp_server_url: URL of MCP server for tool execution
    
    Example:
        context = AgentContext(
            user_id=UUID("550e8400-e29b-41d4-a716-446655440000"),
            conversation_history=[
                {"role": "user", "content": "Add a task"},
                {"role": "assistant", "content": "What task?"}
            ],
            system_instructions="You are a Todo Assistant...",
            available_tools=[...],
            conversation_id="650e8400-e29b-41d4-a716-446655440001"
        )
    """
    
    user_id: UUID
    """UUID of the user making the request (for authorization and data isolation)"""
    
    conversation_history: List[Dict[str, Any]] = field(default_factory=list)
    """
    List of previous messages in conversation.
    Format: [{"role": "user|assistant", "content": "...", "timestamp": "..."}]
    """
    
    system_instructions: str = ""
    """System prompt defining agent persona, capabilities, and behavior"""
    
    available_tools: List[Dict[str, Any]] = field(default_factory=list)
    """
    List of MCP tool definitions in OpenAI function calling format.
    Each tool includes name, description, and parameter schema.
    """
    
    conversation_id: Optional[str] = None
    """ID of current conversation (UUID string). None for new conversations."""
    
    mcp_server_url: str = "http://localhost:8000/api/mcp"
    """Base URL of MCP server for tool execution"""
    
    def __post_init__(self):
        """Validate context after initialization."""
        if not isinstance(self.user_id, UUID):
            raise ValueError("user_id must be a UUID instance")
        
        if self.conversation_id is not None:
            try:
                UUID(self.conversation_id)
            except ValueError:
                raise ValueError("conversation_id must be a valid UUID string")
    
    def add_message(self, role: str, content: str) -> None:
        """
        Add a message to conversation history.
        
        Args:
            role: Message role ('user' or 'assistant')
            content: Message content
        
        Raises:
            ValueError: If role is not 'user' or 'assistant'
        """
        if role not in ['user', 'assistant']:
            raise ValueError("role must be 'user' or 'assistant'")
        
        self.conversation_history.append({
            "role": role,
            "content": content
        })
    
    def get_messages_for_openai(self) -> List[Dict[str, str]]:
        """
        Get conversation history in OpenAI API format.
        
        Returns:
            List of messages with 'role' and 'content' keys
        
        Example:
            [
                {"role": "system", "content": "You are a Todo Assistant..."},
                {"role": "user", "content": "Add a task"},
                {"role": "assistant", "content": "What task?"}
            ]
        """
        messages = []
        
        # Add system instructions as first message
        if self.system_instructions:
            messages.append({
                "role": "system",
                "content": self.system_instructions
            })
        
        # Add conversation history
        for msg in self.conversation_history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        return messages
    
    def get_tool_names(self) -> List[str]:
        """
        Get list of available tool names.
        
        Returns:
            List of tool names (e.g., ['add_task', 'list_tasks', ...])
        """
        return [tool.get("function", {}).get("name", "") for tool in self.available_tools]
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"AgentContext("
            f"user_id={self.user_id}, "
            f"conversation_id={self.conversation_id}, "
            f"history_length={len(self.conversation_history)}, "
            f"tools={self.get_tool_names()})"
        )

"""
AI Agent Module

Contains OpenAI agent integration, system instructions, and tool definitions.
"""

from .context import AgentContext
from .todo_assistant import TodoAssistant, create_todo_assistant

__all__ = ['AgentContext', 'TodoAssistant', 'create_todo_assistant']

"""
Todo Assistant implementation using Google Gemini.

This module provides the TodoAssistant class that processes user messages
through Google's Gemini API with function calling capabilities for MCP tools.
"""

import logging
import json
from typing import List, Dict, Any
import google.generativeai as genai

from src.config import settings
from src.agents.context import AgentContext
from src.agents.system_instructions import get_system_instructions
from src.agents.tool_definitions import get_all_tools, get_tool_by_name
from src.schemas.chat import ToolCall


logger = logging.getLogger(__name__)


class AgentError(Exception):
    """Base exception for agent errors."""
    pass


class AgentProcessingError(AgentError):
    """Raised when agent fails to process a message."""
    pass


class TodoAssistant:
    """
    Todo Assistant powered by Google Gemini.
    
    This class handles natural language interactions with users, processes
    their requests through Gemini's function calling, and executes MCP tools
    to manage tasks.
    
    The assistant maintains conversation context and can handle multi-turn
    conversations with tool execution.
    """
    
    def __init__(
        self,
        api_key: str = None,
        model: str = None,
        max_tokens: int = None,
        temperature: float = None
    ):
        """
        Initialize the Todo Assistant with Gemini configuration.
        
        Args:
            api_key: Gemini API key (defaults to settings.GEMINI_API_KEY)
            model: Gemini model name (defaults to settings.GEMINI_MODEL)
            max_tokens: Maximum tokens in response (defaults to settings.GEMINI_MAX_TOKENS)
            temperature: Sampling temperature (defaults to settings.GEMINI_TEMPERATURE)
        """
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model_name = model or settings.GEMINI_MODEL
        self.max_tokens = max_tokens or settings.GEMINI_MAX_TOKENS
        self.temperature = temperature or settings.GEMINI_TEMPERATURE
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Convert OpenAI-style tool definitions to Gemini format
        self.tools = self._convert_tools_to_gemini_format(get_all_tools())
        
        # Initialize model with tools
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            tools=self.tools,
            system_instruction=get_system_instructions()
        )
        
        logger.info(
            f"Initialized TodoAssistant with model={self.model_name}, "
            f"max_tokens={self.max_tokens}, temperature={self.temperature}"
        )
    
    def _convert_tools_to_gemini_format(self, openai_tools: List[Dict]) -> List[Dict]:
        """
        Convert OpenAI function calling format to Gemini function declarations.
        
        Gemini expects a simpler format without nested "type" fields and "default" values.
        
        Args:
            openai_tools: List of OpenAI-style tool definitions
            
        Returns:
            List of Gemini-style function declarations
        """
        gemini_tools = []
        
        for tool in openai_tools:
            function = tool["function"]
            
            # Build Gemini-compatible parameters
            gemini_params = {
                "type": "OBJECT",
                "properties": {},
                "required": function["parameters"].get("required", [])
            }
            
            # Convert each property
            for prop_name, prop_def in function["parameters"].get("properties", {}).items():
                gemini_prop = {
                    "type": prop_def.get("type", "string").upper(),
                    "description": prop_def.get("description", "")
                }
                gemini_params["properties"][prop_name] = gemini_prop
            
            gemini_tool = {
                "name": function["name"],
                "description": function["description"],
                "parameters": gemini_params
            }
            gemini_tools.append(gemini_tool)
        
        return gemini_tools
    
    async def process_message(
        self,
        context: AgentContext,
        user_message: str,
        mcp_client
    ) -> Dict[str, Any]:
        """
        Process a user message through Gemini with tool execution.
        
        This method:
        1. Builds conversation history from context
        2. Sends message to Gemini
        3. Detects and executes any tool calls via MCP client
        4. Returns final agent response and tool call details
        
        Args:
            context: Agent context with conversation history
            user_message: The user's message to process
            mcp_client: MCP client for executing tool calls
            
        Returns:
            Dict with 'message' and 'tool_calls' keys
            
        Raises:
            AgentProcessingError: If message processing fails
        """
        try:
            logger.info(
                f"Processing message for user {context.user_id} "
                f"with {len(context.conversation_history)} messages and "
                f"{len(context.available_tools)} tools"
            )
            
            # Build conversation history for Gemini
            history = self._build_gemini_history(context)
            
            # Start chat session with history
            chat = self.model.start_chat(history=history)
            
            # Send message and get response
            response = chat.send_message(
                user_message,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=self.max_tokens,
                    temperature=self.temperature
                )
            )
            
            tool_calls_executed = []
            
            # Check if Gemini wants to call functions
            if response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'function_call') and part.function_call:
                        # Execute the function call
                        function_call = part.function_call
                        tool_call = await self._execute_tool_call(
                            function_call.name,
                            dict(function_call.args),
                            mcp_client
                        )
                        tool_calls_executed.append(tool_call)
                        
                        # Send function response back to Gemini
                        # In newer Gemini SDK, we send the response directly
                        function_response_part = genai.protos.Part(
                            function_response=genai.protos.FunctionResponse(
                                name=function_call.name,
                                response=tool_call.result  # Send result directly, not wrapped
                            )
                        )
                        
                        # Get final response after tool execution
                        response = chat.send_message(
                            function_response_part,
                            generation_config=genai.types.GenerationConfig(
                                max_output_tokens=self.max_tokens,
                                temperature=self.temperature
                            )
                        )
            
            # Extract final text response
            # Handle cases where response might not have text
            try:
                agent_message = response.text
            except ValueError:
                # Response doesn't have text (might be blocked or only function calls)
                if tool_calls_executed:
                    # If we executed tools, generate a default response
                    agent_message = "I've processed your request."
                else:
                    # No tools and no text - something went wrong
                    logger.warning(f"Response has no text. Finish reason: {response.candidates[0].finish_reason}")
                    agent_message = "I'm sorry, I couldn't generate a response. Could you try rephrasing your request?"
            
            # Add messages to context
            context.add_message("user", user_message)
            context.add_message("assistant", agent_message)
            
            logger.info(
                f"Successfully processed message. "
                f"Tool calls: {len(tool_calls_executed)}, "
                f"Response length: {len(agent_message)}"
            )
            
            return {
                "message": agent_message,
                "tool_calls": tool_calls_executed
            }
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}", exc_info=True)
            raise AgentProcessingError(f"Failed to process message: {str(e)}") from e
    
    def _build_gemini_history(self, context: AgentContext) -> List[Dict]:
        """
        Build conversation history in Gemini format.
        
        Args:
            context: Agent context with conversation history
            
        Returns:
            List of Gemini-formatted messages
        """
        history = []
        
        # Convert conversation history to Gemini format
        for msg in context.conversation_history:
            role = "user" if msg["role"] == "user" else "model"
            history.append({
                "role": role,
                "parts": [msg["content"]]
            })
        
        return history
    
    async def _execute_tool_call(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
        mcp_client
    ) -> ToolCall:
        """
        Execute a tool call via the MCP client.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Tool arguments from Gemini
            mcp_client: MCP client for executing tools
            
        Returns:
            ToolCall object with execution results
            
        Raises:
            ValueError: If tool name is unknown
        """
        logger.info(f"Executing tool: {tool_name} with args: {arguments}")
        
        # Validate tool exists
        try:
            get_tool_by_name(tool_name)
        except ValueError as e:
            logger.error(f"Unknown tool: {tool_name}")
            raise ValueError(f"Unknown tool: {tool_name}") from e
        
        # Execute tool via MCP client
        try:
            if tool_name == "add_task":
                result = await mcp_client.add_task(
                    title=arguments["title"],
                    description=arguments.get("description", "")
                )
            elif tool_name == "list_tasks":
                result = await mcp_client.list_tasks()
            elif tool_name == "complete_task":
                result = await mcp_client.complete_task(
                    task_id=arguments["task_id"]
                )
            elif tool_name == "delete_task":
                result = await mcp_client.delete_task(
                    task_id=arguments["task_id"]
                )
            elif tool_name == "update_task":
                result = await mcp_client.update_task(
                    task_id=arguments["task_id"],
                    title=arguments.get("title"),
                    description=arguments.get("description")
                )
            else:
                raise ValueError(f"Tool {tool_name} not implemented")
            
            logger.info(f"Tool {tool_name} executed successfully")
            
            return ToolCall(
                tool_name=tool_name,
                parameters=arguments,
                result=result
            )
            
        except Exception as e:
            logger.error(f"Tool execution failed: {str(e)}", exc_info=True)
            # Return error as result
            return ToolCall(
                tool_name=tool_name,
                parameters=arguments,
                result={"error": str(e)}
            )


def create_todo_assistant(
    api_key: str = None,
    model: str = None,
    max_tokens: int = None,
    temperature: float = None
) -> TodoAssistant:
    """
    Factory function to create a TodoAssistant instance.
    
    Args:
        api_key: Gemini API key (optional, uses settings default)
        model: Gemini model name (optional, uses settings default)
        max_tokens: Maximum tokens (optional, uses settings default)
        temperature: Sampling temperature (optional, uses settings default)
        
    Returns:
        Configured TodoAssistant instance
    """
    return TodoAssistant(
        api_key=api_key,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature
    )

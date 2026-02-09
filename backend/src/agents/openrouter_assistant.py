"""
Todo Assistant implementation using OpenRouter API.

OpenRouter provides access to multiple AI models through OpenAI-compatible API.
"""

import logging
import json
import re
from typing import List, Dict, Any
import httpx

from src.config import settings
from src.agents.context import AgentContext
from src.agents.system_instructions import get_system_instructions
from src.agents.tool_definitions import get_all_tools
from src.agents.tool_executors import get_tool_function
from src.schemas.chat import ToolCall


logger = logging.getLogger(__name__)


class AgentError(Exception):
    """Base exception for agent errors."""
    pass


class AgentProcessingError(AgentError):
    """Raised when agent fails to process a message."""
    pass


def parse_xml_tool_calls(content: str) -> List[Dict[str, Any]]:
    """
    Parse XML-style tool calls from model response.
    
    Handles multiple formats:
    1. <tool_call><function=name></function></tool_call>
    2. <tool_call><function=name><parameter=key>value</parameter></function></tool_call>
    
    Returns: [{"name": "add_task", "arguments": {"title": "sleep"}}]
    """
    tool_calls = []
    
    # Pattern to extract tool_call blocks
    tool_call_pattern = r'<tool_call>(.*?)</tool_call>'
    tool_call_matches = re.findall(tool_call_pattern, content, re.DOTALL)
    
    for tool_call_content in tool_call_matches:
        # Extract function name
        function_match = re.search(r'<function=([^>]+)>', tool_call_content)
        if not function_match:
            continue
        
        function_name = function_match.group(1).strip()
        
        # Extract all parameters
        param_pattern = r'<parameter=([^>]+)>\s*(.*?)\s*</parameter>'
        param_matches = re.findall(param_pattern, tool_call_content, re.DOTALL)
        
        arguments = {}
        for param_name, param_value in param_matches:
            param_name = param_name.strip()
            param_value = param_value.strip()
            
            # Try to parse as JSON if it looks like JSON
            if param_value.startswith('{') or param_value.startswith('['):
                try:
                    arguments[param_name] = json.loads(param_value)
                except json.JSONDecodeError:
                    arguments[param_name] = param_value
            else:
                arguments[param_name] = param_value
        
        tool_calls.append({
            "name": function_name,
            "arguments": arguments
        })
    
    return tool_calls


class OpenRouterAssistant:
    """
    Todo Assistant powered by OpenRouter API.
    
    Uses OpenAI-compatible API to access various models through OpenRouter.
    """
    
    def __init__(
        self,
        api_key: str = None,
        model: str = None,
        max_tokens: int = None,
        temperature: float = None
    ):
        """
        Initialize the Todo Assistant with OpenRouter configuration.
        
        Args:
            api_key: OpenRouter API key
            model: Model name (e.g., "google/gemini-2.0-flash-exp:free")
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
        """
        self.api_key = api_key or settings.GEMINI_API_KEY  # Reusing GEMINI_API_KEY for OpenRouter
        self.model_name = model or "nvidia/nemotron-3-nano-30b-a3b:free"  # Model we tested successfully
        self.max_tokens = max_tokens or 1000  # Reduced for faster responses
        self.temperature = temperature or settings.GEMINI_TEMPERATURE
        self.base_url = "https://openrouter.ai/api/v1"
        
        # Get tools
        self.tools = get_all_tools()
        
        logger.info(
            f"Initialized OpenRouterAssistant with model={self.model_name}, "
            f"max_tokens={self.max_tokens}, temperature={self.temperature}"
        )
    
    async def process_message(
        self,
        message: str,
        context: AgentContext,
        conversation_history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Process a user message and return AI response with tool execution.
        
        Args:
            message: User's message
            context: Agent context with database session and user info
            conversation_history: Previous messages in conversation
            
        Returns:
            Dict with 'message' and optional 'tool_calls'
        """
        try:
            # Build messages
            messages = []
            
            # Add system message
            messages.append({
                "role": "system",
                "content": get_system_instructions()
            })
            
            # Add conversation history
            if conversation_history:
                messages.extend(conversation_history[-10:])  # Last 10 messages
            
            # Add current message
            messages.append({
                "role": "user",
                "content": message
            })
            
            # Call OpenRouter API
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "http://localhost:3000",  # Optional
                        "X-Title": "Todo App"  # Optional
                    },
                    json={
                        "model": self.model_name,
                        "messages": messages,
                        "temperature": self.temperature,
                        "max_tokens": self.max_tokens,
                        "tools": self.tools,
                        "tool_choice": "auto"
                    },
                    timeout=30.0
                )
                
                if response.status_code != 200:
                    error_text = response.text
                    logger.error(f"OpenRouter API error: {response.status_code} - {error_text}")
                    raise AgentProcessingError(f"OpenRouter API error: {response.status_code}")
                
                result = response.json()
            
            # Extract response
            choice = result["choices"][0]
            ai_message = choice["message"]
            content = ai_message.get("content", "")
            
            logger.info(f"AI response - has tool_calls: {'tool_calls' in ai_message}, content length: {len(content)}, has <tool_call>: {'<tool_call>' in content}")
            
            # Check for tool calls (both JSON and XML formats)
            tool_calls_data = []
            
            # First check for standard OpenAI-style tool calls
            if "tool_calls" in ai_message and ai_message["tool_calls"]:
                # Execute tools (OpenAI format)
                for tool_call in ai_message["tool_calls"]:
                    function_name = tool_call["function"]["name"]
                    function_args = json.loads(tool_call["function"]["arguments"])
                    
                    logger.info(f"Executing tool: {function_name} with args: {function_args}")
                    
                    # Get tool function and execute
                    tool_func = get_tool_function(function_name)
                    if tool_func:
                        try:
                            result = await tool_func(context, **function_args)
                            tool_calls_data.append({
                                "tool_name": function_name,
                                "parameters": function_args,
                                "result": result
                            })
                        except Exception as e:
                            logger.error(f"Tool execution error: {e}")
                            tool_calls_data.append({
                                "tool_name": function_name,
                                "parameters": function_args,
                                "result": {"error": str(e)}
                            })
                
                # If tools were called, get final response
                if tool_calls_data:
                    # Add tool results to messages
                    messages.append(ai_message)
                    for i, tool_call in enumerate(ai_message["tool_calls"]):
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call["id"],
                            "content": json.dumps(tool_calls_data[i]["result"])
                        })
                    
                    # Get final response
                    async with httpx.AsyncClient() as client:
                        response = await client.post(
                            f"{self.base_url}/chat/completions",
                            headers={
                                "Authorization": f"Bearer {self.api_key}",
                                "Content-Type": "application/json"
                            },
                            json={
                                "model": self.model_name,
                                "messages": messages,
                                "temperature": self.temperature,
                                "max_tokens": self.max_tokens
                            },
                            timeout=30.0
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            final_message = result["choices"][0]["message"]["content"]
                        else:
                            final_message = "I've completed the task."
            
            # Check for XML-style tool calls (for models like nvidia that don't support OpenAI format)
            elif content and "<tool_call>" in content:
                logger.info(f"Detected XML-style tool calls in response: {content[:200]}")
                xml_tool_calls = parse_xml_tool_calls(content)
                logger.info(f"Parsed {len(xml_tool_calls)} XML tool calls: {xml_tool_calls}")
                
                if xml_tool_calls:
                    # Execute XML-style tools
                    for tool_call in xml_tool_calls:
                        function_name = tool_call["name"]
                        function_args = tool_call["arguments"]
                        
                        logger.info(f"Executing XML tool: {function_name} with args: {function_args}")
                        
                        # Get tool function and execute
                        tool_func = get_tool_function(function_name)
                        if tool_func:
                            try:
                                result = await tool_func(context, **function_args)
                                tool_calls_data.append({
                                    "tool_name": function_name,
                                    "parameters": function_args,
                                    "result": result
                                })
                            except Exception as e:
                                logger.error(f"Tool execution error: {e}")
                                tool_calls_data.append({
                                    "tool_name": function_name,
                                    "parameters": function_args,
                                    "result": {"error": str(e)}
                                })
                    
                    # Get final response after tool execution
                    if tool_calls_data:
                        # Build summary of tool results
                        tool_results_summary = "\n".join([
                            f"Tool {tc['tool_name']}: {json.dumps(tc['result'])}"
                            for tc in tool_calls_data
                        ])
                        
                        # Ask model to generate final response based on tool results
                        messages.append({
                            "role": "assistant",
                            "content": content
                        })
                        messages.append({
                            "role": "user",
                            "content": f"Tool execution results:\n{tool_results_summary}\n\nPlease provide a natural response to the user based on these results."
                        })
                        
                        async with httpx.AsyncClient() as client:
                            response = await client.post(
                                f"{self.base_url}/chat/completions",
                                headers={
                                    "Authorization": f"Bearer {self.api_key}",
                                    "Content-Type": "application/json"
                                },
                                json={
                                    "model": self.model_name,
                                    "messages": messages,
                                    "temperature": self.temperature,
                                    "max_tokens": self.max_tokens
                                },
                                timeout=30.0
                            )
                            
                            if response.status_code == 200:
                                result = response.json()
                                final_message = result["choices"][0]["message"]["content"]
                            else:
                                final_message = "I've completed the task."
                else:
                    # No tool calls found, but XML present - strip it
                    final_message = re.sub(r'<tool_call>.*?</tool_call>', '', content, flags=re.DOTALL).strip()
                    if not final_message:
                        final_message = "I'm working on that for you."
            else:
                final_message = content or "I'm here to help!"
            
            # Final cleanup: remove any remaining XML tags
            final_message = re.sub(r'<tool_call>.*?</tool_call>', '', final_message, flags=re.DOTALL).strip()
            if not final_message:
                final_message = "Done!"
            
            return {
                "message": final_message,
                "tool_calls": tool_calls_data if tool_calls_data else None
            }
            
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            raise AgentProcessingError(f"Failed to process message: {str(e)}") from e

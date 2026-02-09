"""
Chat API endpoint for OpenAI Agents SDK integration.

This module provides the stateless chat API endpoint that allows users
to interact with the Todo Assistant using natural language.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Annotated

from src.database import get_session
from src.middleware.auth import get_current_user, validate_user_id
from src.models.user import User
from src.schemas.chat import ChatRequest, ChatResponse
from src.services.chat_service import process_chat


router = APIRouter(
    prefix="/api/{user_id}/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Send a chat message to the Todo Assistant",
    description="""
    Send a natural language message to the Todo Assistant and receive a response.
    
    The assistant can help you:
    - Add new tasks: "Add a task to buy groceries"
    - List tasks: "Show me my tasks"
    - Complete tasks: "Mark task 123 as done"
    - Delete tasks: "Delete the grocery task"
    - Update tasks: "Change the title of task 123 to 'Buy milk'"
    
    The conversation is stateless - each request includes the full conversation history
    from the database, and the response is saved back to the database.
    
    **Authentication**: Requires valid JWT token in Authorization header.
    
    **User Isolation**: The user_id in the URL must match the authenticated user's ID.
    """,
    responses={
        200: {
            "description": "Successful response from Todo Assistant",
            "content": {
                "application/json": {
                    "example": {
                        "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
                        "message": "I've added 'Buy groceries' to your task list!",
                        "tool_calls": [
                            {
                                "tool_name": "add_task",
                                "parameters": {"title": "Buy groceries", "description": ""},
                                "result": {"task_id": "123", "title": "Buy groceries"}
                            }
                        ],
                        "timestamp": "2026-02-09T10:30:00Z"
                    }
                }
            }
        },
        400: {"description": "Invalid request (message too long, invalid format)"},
        401: {"description": "Missing or invalid authentication token"},
        403: {"description": "User ID in URL does not match authenticated user"},
        500: {"description": "Internal server error (OpenAI API failure, database error, etc.)"}
    }
)
async def send_chat_message(
    user_id: Annotated[str, Depends(validate_user_id)],
    request: ChatRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> ChatResponse:
    """
    Process a chat message through the Todo Assistant.
    
    This endpoint orchestrates the complete stateless request cycle:
    1. Validates authentication and user_id
    2. Fetches conversation history from database
    3. Processes message through OpenAI agent with MCP tools
    4. Saves user message and agent response to database
    5. Returns agent response with tool call details
    
    Args:
        user_id: User ID from URL path (validated against JWT token)
        request: Chat request with message and optional conversation_id
        session: Database session (injected)
        current_user: Authenticated user (injected)
    
    Returns:
        ChatResponse with agent message, conversation_id, tool calls, and timestamp
    
    Raises:
        HTTPException 400: Invalid request format
        HTTPException 401: Authentication failure
        HTTPException 403: User ID mismatch
        HTTPException 500: Internal server error
    """
    try:
        # Process chat request through the stateless service
        response = await process_chat(
            user_id=user_id,
            request=request,
            session=session
        )
        return response
    
    except ValueError as e:
        # Validation errors (invalid conversation_id, etc.)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    except PermissionError as e:
        # Authorization errors (conversation belongs to different user)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    
    except Exception as e:
        # Unexpected errors (OpenAI API failure, database error, etc.)
        # Log the full error for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Chat request failed for user {user_id}: {str(e)}", exc_info=True)
        
        # Print to console for immediate debugging
        print(f"❌ CHAT ERROR for user {user_id}:")
        print(f"   Error type: {type(e).__name__}")
        print(f"   Error message: {str(e)}")
        import traceback
        traceback.print_exc()
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Sorry, I encountered an error processing your message. Please try again."
        )

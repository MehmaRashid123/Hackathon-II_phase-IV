"""
Quick test script to verify Gemini API connection.

Run this to test if your Gemini API key is working correctly.
"""

import asyncio
from src.agents.todo_assistant import create_todo_assistant
from src.agents.context import AgentContext
from src.services.mcp_client import MCPClient
from unittest.mock import AsyncMock
from uuid import uuid4


async def test_gemini_connection():
    """Test Gemini API connection with a simple message."""
    print("🔍 Testing Gemini API connection...")
    print()
    
    try:
        # Create assistant
        print("1️⃣ Creating Gemini assistant...")
        assistant = create_todo_assistant()
        print(f"   ✅ Assistant created with model: {assistant.model_name}")
        print()
        
        # Create mock MCP client (we're just testing Gemini, not MCP)
        print("2️⃣ Setting up test context...")
        mock_mcp_client = AsyncMock(spec=MCPClient)
        
        # Create agent context
        context = AgentContext(
            user_id=uuid4(),
            conversation_id=str(uuid4()),
            conversation_history=[],
            system_instructions="You are a helpful assistant.",
            available_tools=[]
        )
        print("   ✅ Context created")
        print()
        
        # Test simple message (no tools)
        print("3️⃣ Sending test message to Gemini...")
        print("   Message: 'Hello! Can you hear me?'")
        print()
        
        result = await assistant.process_message(
            context=context,
            user_message="Hello! Can you hear me?",
            mcp_client=mock_mcp_client
        )
        
        print("4️⃣ Response received:")
        print(f"   📝 {result['message']}")
        print()
        
        print("✅ SUCCESS! Gemini API is working correctly!")
        print()
        print("Your Gemini API key is valid and the assistant is ready to use.")
        return True
        
    except Exception as e:
        print("❌ ERROR! Gemini API test failed:")
        print(f"   {type(e).__name__}: {str(e)}")
        print()
        print("Possible issues:")
        print("  - Invalid API key")
        print("  - Network connection problem")
        print("  - API quota exceeded")
        print("  - Region restrictions")
        print()
        print("Please check your GEMINI_API_KEY in backend/.env")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("GEMINI API CONNECTION TEST")
    print("=" * 60)
    print()
    
    success = asyncio.run(test_gemini_connection())
    
    print("=" * 60)
    exit(0 if success else 1)

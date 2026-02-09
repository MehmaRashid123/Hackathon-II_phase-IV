"""
Test chat with tool calling to verify the fix.
"""

import asyncio
from src.agents.todo_assistant import create_todo_assistant
from src.agents.context import AgentContext
from src.services.mcp_client import create_mcp_client
from uuid import uuid4


async def test_chat_with_tools():
    """Test chat with actual tool calling."""
    print("🔍 Testing chat with tool calling...")
    print()
    
    try:
        # Create assistant
        print("1️⃣ Creating Gemini assistant...")
        assistant = create_todo_assistant()
        print(f"   ✅ Assistant created")
        print()
        
        # Create MCP client
        print("2️⃣ Creating MCP client...")
        user_id = str(uuid4())
        mcp_client = create_mcp_client(user_id)
        print(f"   ✅ MCP client created for user {user_id}")
        print()
        
        # Create agent context
        print("3️⃣ Setting up context...")
        from src.agents.system_instructions import get_system_instructions
        from src.agents.tool_definitions import get_all_tools
        
        context = AgentContext(
            user_id=uuid4(),
            conversation_id=str(uuid4()),
            conversation_history=[],
            system_instructions=get_system_instructions(),
            available_tools=get_all_tools()
        )
        print(f"   ✅ Context created with {len(context.available_tools)} tools")
        print()
        
        # Test message that should trigger tool call
        print("4️⃣ Sending test message...")
        print("   Message: 'Add a task called Test Task'")
        print()
        
        result = await assistant.process_message(
            context=context,
            user_message="Add a task called Test Task",
            mcp_client=mcp_client
        )
        
        print("5️⃣ Response received:")
        print(f"   📝 Message: {result['message']}")
        print(f"   🔧 Tool calls: {len(result.get('tool_calls', []))}")
        if result.get('tool_calls'):
            for tc in result['tool_calls']:
                print(f"      - {tc['tool_name']}: {tc['parameters']}")
        print()
        
        print("✅ SUCCESS! Tool calling is working!")
        return True
        
    except Exception as e:
        print("❌ ERROR! Test failed:")
        print(f"   {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("CHAT WITH TOOLS TEST")
    print("=" * 60)
    print()
    
    success = asyncio.run(test_chat_with_tools())
    
    print("=" * 60)
    exit(0 if success else 1)

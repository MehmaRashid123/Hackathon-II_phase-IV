"""
Integration test for MCP tools.

Tests all 5 MCP tools to ensure they are properly registered and functional.
"""
import sys
from pathlib import Path
from uuid import uuid4

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.mcp.server import list_registered_tools, get_tool
from src.core.database import engine, Session
from src.models.task import Task


def test_tool_registration():
    """Test that all 5 tools are registered."""
    print("\n" + "=" * 60)
    print("TEST: Tool Registration")
    print("=" * 60)
    
    # Import tools to trigger registration
    from src.mcp.tools import add_task, list_tasks, complete_task, delete_task, update_task
    
    registered_tools = list_registered_tools()
    expected_tools = ["add_task", "list_tasks", "complete_task", "delete_task", "update_task"]
    
    print(f"\nExpected tools: {expected_tools}")
    print(f"Registered tools: {registered_tools}")
    
    for tool_name in expected_tools:
        if tool_name in registered_tools:
            print(f"  ✓ {tool_name} is registered")
        else:
            print(f"  ✗ {tool_name} is NOT registered")
            return False
    
    print("\n✓ All tools are registered successfully!")
    return True


def test_tool_metadata():
    """Test that all tools have proper metadata."""
    print("\n" + "=" * 60)
    print("TEST: Tool Metadata")
    print("=" * 60)
    
    from src.mcp.tools import add_task, list_tasks, complete_task, delete_task, update_task
    
    tools = [
        ("add_task", add_task.add_task),
        ("list_tasks", list_tasks.list_tasks),
        ("complete_task", complete_task.complete_task),
        ("delete_task", delete_task.delete_task),
        ("update_task", update_task.update_task),
    ]
    
    for tool_name, tool_func in tools:
        if hasattr(tool_func, 'metadata'):
            metadata = tool_func.metadata
            print(f"\n✓ {tool_name} has metadata:")
            print(f"  - Name: {metadata.get('name')}")
            print(f"  - Description: {metadata.get('description')}")
            print(f"  - Required params: {metadata.get('parameters', {}).get('required', [])}")
        else:
            print(f"\n✗ {tool_name} is missing metadata")
            return False
    
    print("\n✓ All tools have proper metadata!")
    return True


def test_add_task_tool():
    """Test add_task tool with a real database call."""
    print("\n" + "=" * 60)
    print("TEST: add_task Tool")
    print("=" * 60)
    
    from src.mcp.tools.add_task import add_task
    import asyncio
    
    # Create a test user_id
    test_user_id = str(uuid4())
    
    # Test arguments
    arguments = {
        "user_id": test_user_id,
        "title": "Test Task from MCP",
        "description": "This is a test task created via MCP tool"
    }
    
    print(f"\nCalling add_task with:")
    print(f"  user_id: {test_user_id}")
    print(f"  title: {arguments['title']}")
    print(f"  description: {arguments['description']}")
    
    try:
        # Call the tool
        result = asyncio.run(add_task("add_task", arguments))
        
        if result and len(result) > 0:
            task_data = result[0]
            if "error" in task_data:
                print(f"\n✗ Tool returned error: {task_data['error']}")
                return False
            else:
                print(f"\n✓ Task created successfully!")
                print(f"  task_id: {task_data.get('task_id')}")
                print(f"  title: {task_data.get('title')}")
                print(f"  completed: {task_data.get('completed')}")
                print(f"  created_at: {task_data.get('created_at')}")
                return True
        else:
            print("\n✗ Tool returned empty result")
            return False
            
    except Exception as e:
        print(f"\n✗ Error calling tool: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_list_tasks_tool():
    """Test list_tasks tool."""
    print("\n" + "=" * 60)
    print("TEST: list_tasks Tool")
    print("=" * 60)
    
    from src.mcp.tools.list_tasks import list_tasks
    import asyncio
    
    # Create a test user_id
    test_user_id = str(uuid4())
    
    arguments = {
        "user_id": test_user_id,
        "completed": None
    }
    
    print(f"\nCalling list_tasks with:")
    print(f"  user_id: {test_user_id}")
    
    try:
        result = asyncio.run(list_tasks("list_tasks", arguments))
        
        if result and len(result) > 0:
            data = result[0]
            if "error" in data:
                print(f"\n✗ Tool returned error: {data['error']}")
                return False
            else:
                print(f"\n✓ Tasks listed successfully!")
                print(f"  count: {data.get('count')}")
                print(f"  tasks: {len(data.get('tasks', []))} items")
                return True
        else:
            print("\n✗ Tool returned empty result")
            return False
            
    except Exception as e:
        print(f"\n✗ Error calling tool: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("MCP TOOLS INTEGRATION TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Tool Registration", test_tool_registration),
        ("Tool Metadata", test_tool_metadata),
        ("add_task Tool", test_add_task_tool),
        ("list_tasks Tool", test_list_tasks_tool),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"\n✗ Test '{test_name}' crashed: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"  Passed: {passed}/{len(tests)}")
    print(f"  Failed: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())

"""
Quick test script to verify services work correctly.

This script tests the basic functionality of Task, Conversation, and Message services.
Run after migrations to ensure everything is set up correctly.

Usage:
    python test_services.py
"""
import sys
from pathlib import Path
from uuid import uuid4

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.database import engine, Session
from src.services import TaskService, ConversationService, MessageService


def test_services():
    """Test all services with basic operations."""
    
    print("=" * 60)
    print("Testing Services")
    print("=" * 60)
    
    # Use a test user ID (you'll need to replace this with a real user ID from your database)
    test_user_id = uuid4()
    print(f"\nUsing test user ID: {test_user_id}")
    print("Note: Replace with a real user ID from your database for actual testing")
    
    with Session(engine) as session:
        # Test Task Service
        print("\n" + "-" * 60)
        print("Testing Task Service")
        print("-" * 60)
        
        task_service = TaskService(session)
        
        # Create task
        task = task_service.create_task(
            user_id=test_user_id,
            title="Test Task",
            description="This is a test task"
        )
        print(f"✓ Created task: {task.title} (ID: {task.id})")
        
        # List tasks
        tasks = task_service.get_tasks(user_id=test_user_id)
        print(f"✓ Listed {len(tasks)} task(s)")
        
        # Update task
        updated_task = task_service.update_task(
            user_id=test_user_id,
            task_id=task.id,
            title="Updated Test Task"
        )
        if updated_task:
            print(f"✓ Updated task: {updated_task.title}")
        
        # Complete task
        completed_task = task_service.complete_task(
            user_id=test_user_id,
            task_id=task.id
        )
        if completed_task:
            print(f"✓ Completed task: {completed_task.completed}")
        
        # Test Conversation Service
        print("\n" + "-" * 60)
        print("Testing Conversation Service")
        print("-" * 60)
        
        conv_service = ConversationService(session)
        
        # Create conversation
        conversation = conv_service.create_conversation(
            user_id=test_user_id,
            title="Test Conversation"
        )
        print(f"✓ Created conversation: {conversation.title} (ID: {conversation.id})")
        
        # List conversations
        conversations = conv_service.list_conversations(user_id=test_user_id)
        print(f"✓ Listed {len(conversations)} conversation(s)")
        
        # Test Message Service
        print("\n" + "-" * 60)
        print("Testing Message Service")
        print("-" * 60)
        
        msg_service = MessageService(session)
        
        # Add user message
        user_msg = msg_service.add_message(
            conversation_id=conversation.id,
            user_id=test_user_id,
            role="user",
            content="Hello, this is a test message"
        )
        print(f"✓ Added user message: {user_msg.content[:50]}...")
        
        # Add assistant message
        assistant_msg = msg_service.add_message(
            conversation_id=conversation.id,
            user_id=test_user_id,
            role="assistant",
            content="Hello! I'm the assistant. How can I help?"
        )
        print(f"✓ Added assistant message: {assistant_msg.content[:50]}...")
        
        # Get messages
        messages = msg_service.get_messages(
            user_id=test_user_id,
            conversation_id=conversation.id
        )
        print(f"✓ Retrieved {len(messages)} message(s)")
        
        # Count messages
        count = msg_service.count_messages(
            user_id=test_user_id,
            conversation_id=conversation.id
        )
        print(f"✓ Message count: {count}")
        
        # Cleanup (delete test data)
        print("\n" + "-" * 60)
        print("Cleaning up test data")
        print("-" * 60)
        
        task_service.delete_task(user_id=test_user_id, task_id=task.id)
        print("✓ Deleted test task")
        
        conv_service.delete_conversation(user_id=test_user_id, conversation_id=conversation.id)
        print("✓ Deleted test conversation (and messages)")
    
    print("\n" + "=" * 60)
    print("All service tests completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        test_services()
    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

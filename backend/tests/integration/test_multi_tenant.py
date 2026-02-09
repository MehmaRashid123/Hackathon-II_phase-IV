"""
Multi-tenant isolation tests.

Verifies that users cannot access or modify each other's data.
Tests the security boundary between different users.
"""
import pytest
import asyncio
from uuid import uuid4

from src.mcp.tools.add_task import add_task
from src.mcp.tools.list_tasks import list_tasks
from src.mcp.tools.complete_task import complete_task
from src.mcp.tools.delete_task import delete_task
from src.mcp.tools.update_task import update_task


@pytest.fixture
def user1_id():
    """Generate user 1 ID."""
    return str(uuid4())


@pytest.fixture
def user2_id():
    """Generate user 2 ID."""
    return str(uuid4())


class TestDataIsolation:
    """Tests for data isolation between users."""
    
    @pytest.mark.asyncio
    async def test_users_cannot_see_each_others_tasks(self, user1_id, user2_id):
        """Test that users can only see their own tasks."""
        # Arrange - User 1 creates tasks
        await add_task("add_task", {
            "user_id": user1_id,
            "title": "User 1 Task 1"
        })
        await add_task("add_task", {
            "user_id": user1_id,
            "title": "User 1 Task 2"
        })
        
        # User 2 creates tasks
        await add_task("add_task", {
            "user_id": user2_id,
            "title": "User 2 Task 1"
        })
        
        # Act - List tasks for each user
        user1_tasks = await list_tasks("list_tasks", {"user_id": user1_id})
        user2_tasks = await list_tasks("list_tasks", {"user_id": user2_id})
        
        # Assert
        assert user1_tasks[0]["count"] == 2
        assert user2_tasks[0]["count"] == 1
        
        # Verify task titles
        user1_titles = [t["title"] for t in user1_tasks[0]["tasks"]]
        user2_titles = [t["title"] for t in user2_tasks[0]["tasks"]]
        
        assert "User 1 Task 1" in user1_titles
        assert "User 1 Task 2" in user1_titles
        assert "User 2 Task 1" not in user1_titles
        
        assert "User 2 Task 1" in user2_titles
        assert "User 1 Task 1" not in user2_titles
    
    @pytest.mark.asyncio
    async def test_user_cannot_complete_another_users_task(self, user1_id, user2_id):
        """Test that users cannot complete tasks belonging to other users."""
        # Arrange - User 1 creates a task
        add_result = await add_task("add_task", {
            "user_id": user1_id,
            "title": "User 1 Private Task"
        })
        user1_task_id = add_result[0]["task_id"]
        
        # Act - User 2 tries to complete User 1's task
        result = await complete_task("complete_task", {
            "user_id": user2_id,
            "task_id": user1_task_id
        })
        
        # Assert - Should fail with not found error
        assert "error" in result[0]
        assert "not found" in result[0]["error"].lower()
        
        # Verify User 1's task is still incomplete
        user1_tasks = await list_tasks("list_tasks", {"user_id": user1_id})
        user1_task = next(t for t in user1_tasks[0]["tasks"] if t["task_id"] == user1_task_id)
        assert user1_task["completed"] is False
    
    @pytest.mark.asyncio
    async def test_user_cannot_update_another_users_task(self, user1_id, user2_id):
        """Test that users cannot update tasks belonging to other users."""
        # Arrange - User 1 creates a task
        add_result = await add_task("add_task", {
            "user_id": user1_id,
            "title": "User 1 Original Title"
        })
        user1_task_id = add_result[0]["task_id"]
        
        # Act - User 2 tries to update User 1's task
        result = await update_task("update_task", {
            "user_id": user2_id,
            "task_id": user1_task_id,
            "title": "Malicious Update"
        })
        
        # Assert - Should fail with not found error
        assert "error" in result[0]
        assert "not found" in result[0]["error"].lower()
        
        # Verify User 1's task is unchanged
        user1_tasks = await list_tasks("list_tasks", {"user_id": user1_id})
        user1_task = next(t for t in user1_tasks[0]["tasks"] if t["task_id"] == user1_task_id)
        assert user1_task["title"] == "User 1 Original Title"
    
    @pytest.mark.asyncio
    async def test_user_cannot_delete_another_users_task(self, user1_id, user2_id):
        """Test that users cannot delete tasks belonging to other users."""
        # Arrange - User 1 creates a task
        add_result = await add_task("add_task", {
            "user_id": user1_id,
            "title": "User 1 Protected Task"
        })
        user1_task_id = add_result[0]["task_id"]
        
        # Act - User 2 tries to delete User 1's task
        result = await delete_task("delete_task", {
            "user_id": user2_id,
            "task_id": user1_task_id
        })
        
        # Assert - Should fail with not found error
        assert "error" in result[0]
        assert "not found" in result[0]["error"].lower()
        
        # Verify User 1's task still exists
        user1_tasks = await list_tasks("list_tasks", {"user_id": user1_id})
        task_ids = [t["task_id"] for t in user1_tasks[0]["tasks"]]
        assert user1_task_id in task_ids


class TestCrossUserOperations:
    """Tests for operations across multiple users."""
    
    @pytest.mark.asyncio
    async def test_multiple_users_can_have_same_task_title(self, user1_id, user2_id):
        """Test that multiple users can have tasks with the same title."""
        # Arrange & Act
        same_title = "Buy groceries"
        
        user1_result = await add_task("add_task", {
            "user_id": user1_id,
            "title": same_title
        })
        
        user2_result = await add_task("add_task", {
            "user_id": user2_id,
            "title": same_title
        })
        
        # Assert
        assert "error" not in user1_result[0]
        assert "error" not in user2_result[0]
        assert user1_result[0]["task_id"] != user2_result[0]["task_id"]
        
        # Verify both users have their own task
        user1_tasks = await list_tasks("list_tasks", {"user_id": user1_id})
        user2_tasks = await list_tasks("list_tasks", {"user_id": user2_id})
        
        assert any(t["title"] == same_title for t in user1_tasks[0]["tasks"])
        assert any(t["title"] == same_title for t in user2_tasks[0]["tasks"])
    
    @pytest.mark.asyncio
    async def test_user_operations_do_not_affect_other_users(self, user1_id, user2_id):
        """Test that operations by one user don't affect another user's data."""
        # Arrange - Both users create tasks
        user1_add = await add_task("add_task", {
            "user_id": user1_id,
            "title": "User 1 Task"
        })
        user1_task_id = user1_add[0]["task_id"]
        
        user2_add = await add_task("add_task", {
            "user_id": user2_id,
            "title": "User 2 Task"
        })
        user2_task_id = user2_add[0]["task_id"]
        
        # Get initial counts
        user1_initial = await list_tasks("list_tasks", {"user_id": user1_id})
        user2_initial = await list_tasks("list_tasks", {"user_id": user2_id})
        user1_initial_count = user1_initial[0]["count"]
        user2_initial_count = user2_initial[0]["count"]
        
        # Act - User 1 completes and deletes their task
        await complete_task("complete_task", {
            "user_id": user1_id,
            "task_id": user1_task_id
        })
        await delete_task("delete_task", {
            "user_id": user1_id,
            "task_id": user1_task_id
        })
        
        # Assert - User 2's data is unchanged
        user2_after = await list_tasks("list_tasks", {"user_id": user2_id})
        assert user2_after[0]["count"] == user2_initial_count
        
        # User 2's task is still incomplete
        user2_task = next(t for t in user2_after[0]["tasks"] if t["task_id"] == user2_task_id)
        assert user2_task["completed"] is False


class TestUserIdValidation:
    """Tests for user_id validation and security."""
    
    @pytest.mark.asyncio
    async def test_empty_user_id_fails(self):
        """Test that empty user_id is rejected."""
        # Act
        result = await add_task("add_task", {
            "user_id": "",
            "title": "Test Task"
        })
        
        # Assert
        assert "error" in result[0]
    
    @pytest.mark.asyncio
    async def test_invalid_uuid_format_fails(self):
        """Test that invalid UUID format is rejected."""
        # Act
        result = await add_task("add_task", {
            "user_id": "not-a-valid-uuid",
            "title": "Test Task"
        })
        
        # Assert
        assert "error" in result[0]
    
    @pytest.mark.asyncio
    async def test_sql_injection_in_user_id_fails(self):
        """Test that SQL injection attempts in user_id are rejected."""
        # Act
        result = await add_task("add_task", {
            "user_id": "'; DROP TABLE tasks; --",
            "title": "Test Task"
        })
        
        # Assert
        assert "error" in result[0]


class TestConcurrentUserOperations:
    """Tests for concurrent operations by multiple users."""
    
    @pytest.mark.asyncio
    async def test_concurrent_task_creation_by_different_users(self, user1_id, user2_id):
        """Test that multiple users can create tasks concurrently."""
        # Arrange
        user1_tasks = [
            add_task("add_task", {"user_id": user1_id, "title": f"User 1 Task {i}"})
            for i in range(5)
        ]
        
        user2_tasks = [
            add_task("add_task", {"user_id": user2_id, "title": f"User 2 Task {i}"})
            for i in range(5)
        ]
        
        # Act - Execute concurrently
        results = await asyncio.gather(*user1_tasks, *user2_tasks)
        
        # Assert - All tasks created successfully
        for result in results:
            assert "error" not in result[0]
        
        # Verify correct counts
        user1_list = await list_tasks("list_tasks", {"user_id": user1_id})
        user2_list = await list_tasks("list_tasks", {"user_id": user2_id})
        
        assert user1_list[0]["count"] >= 5
        assert user2_list[0]["count"] >= 5
    
    @pytest.mark.asyncio
    async def test_concurrent_operations_maintain_isolation(self, user1_id, user2_id):
        """Test that concurrent operations maintain data isolation."""
        # Arrange - Create initial tasks
        user1_add = await add_task("add_task", {
            "user_id": user1_id,
            "title": "User 1 Task"
        })
        user1_task_id = user1_add[0]["task_id"]
        
        user2_add = await add_task("add_task", {
            "user_id": user2_id,
            "title": "User 2 Task"
        })
        user2_task_id = user2_add[0]["task_id"]
        
        # Act - Perform concurrent operations
        operations = [
            complete_task("complete_task", {"user_id": user1_id, "task_id": user1_task_id}),
            update_task("update_task", {"user_id": user2_id, "task_id": user2_task_id, "title": "Updated"}),
            list_tasks("list_tasks", {"user_id": user1_id}),
            list_tasks("list_tasks", {"user_id": user2_id}),
        ]
        
        results = await asyncio.gather(*operations)
        
        # Assert - All operations succeeded
        for result in results:
            assert "error" not in result[0]
        
        # Verify final state
        user1_final = await list_tasks("list_tasks", {"user_id": user1_id})
        user2_final = await list_tasks("list_tasks", {"user_id": user2_id})
        
        user1_task = next(t for t in user1_final[0]["tasks"] if t["task_id"] == user1_task_id)
        user2_task = next(t for t in user2_final[0]["tasks"] if t["task_id"] == user2_task_id)
        
        assert user1_task["completed"] is True
        assert user2_task["title"] == "Updated"

"""
Integration tests for all MCP tools.

Tests end-to-end functionality of add_task, list_tasks, complete_task,
delete_task, and update_task tools with real database interactions.
"""
import pytest
import asyncio
from uuid import uuid4
from datetime import datetime

from src.mcp.tools.add_task import add_task
from src.mcp.tools.list_tasks import list_tasks
from src.mcp.tools.complete_task import complete_task
from src.mcp.tools.delete_task import delete_task
from src.mcp.tools.update_task import update_task
from src.core.database import engine, Session
from src.models.task import Task


@pytest.fixture
def test_user_id():
    """Generate a unique user ID for testing."""
    return str(uuid4())


@pytest.fixture
def cleanup_tasks():
    """Cleanup tasks after each test."""
    yield
    # Cleanup logic would go here if needed
    # For now, we rely on test database isolation


class TestAddTaskTool:
    """Integration tests for add_task tool."""
    
    @pytest.mark.asyncio
    async def test_add_task_success(self, test_user_id):
        """Test successfully adding a task."""
        # Arrange
        arguments = {
            "user_id": test_user_id,
            "title": "Integration Test Task",
            "description": "This is a test task"
        }
        
        # Act
        result = await add_task("add_task", arguments)
        
        # Assert
        assert len(result) == 1
        task_data = result[0]
        assert "error" not in task_data
        assert task_data["title"] == "Integration Test Task"
        assert task_data["description"] == "This is a test task"
        assert task_data["completed"] is False
        assert "task_id" in task_data
        assert "created_at" in task_data
    
    @pytest.mark.asyncio
    async def test_add_task_without_description(self, test_user_id):
        """Test adding a task without description."""
        # Arrange
        arguments = {
            "user_id": test_user_id,
            "title": "Task without description"
        }
        
        # Act
        result = await add_task("add_task", arguments)
        
        # Assert
        assert len(result) == 1
        task_data = result[0]
        assert "error" not in task_data
        assert task_data["title"] == "Task without description"
        assert task_data["description"] is None or task_data["description"] == ""
    
    @pytest.mark.asyncio
    async def test_add_task_empty_title_fails(self, test_user_id):
        """Test that empty title returns error."""
        # Arrange
        arguments = {
            "user_id": test_user_id,
            "title": "",
            "description": "Description"
        }
        
        # Act
        result = await add_task("add_task", arguments)
        
        # Assert
        assert len(result) == 1
        assert "error" in result[0]
    
    @pytest.mark.asyncio
    async def test_add_task_invalid_user_id_fails(self):
        """Test that invalid user_id returns error."""
        # Arrange
        arguments = {
            "user_id": "invalid-uuid",
            "title": "Test Task"
        }
        
        # Act
        result = await add_task("add_task", arguments)
        
        # Assert
        assert len(result) == 1
        assert "error" in result[0]


class TestListTasksTool:
    """Integration tests for list_tasks tool."""
    
    @pytest.mark.asyncio
    async def test_list_tasks_empty(self, test_user_id):
        """Test listing tasks when user has no tasks."""
        # Arrange
        arguments = {"user_id": test_user_id}
        
        # Act
        result = await list_tasks("list_tasks", arguments)
        
        # Assert
        assert len(result) == 1
        data = result[0]
        assert "error" not in data
        assert data["count"] == 0
        assert data["tasks"] == []
    
    @pytest.mark.asyncio
    async def test_list_tasks_after_adding(self, test_user_id):
        """Test listing tasks after adding some."""
        # Arrange - Add tasks first
        await add_task("add_task", {
            "user_id": test_user_id,
            "title": "Task 1"
        })
        await add_task("add_task", {
            "user_id": test_user_id,
            "title": "Task 2"
        })
        
        # Act
        result = await list_tasks("list_tasks", {"user_id": test_user_id})
        
        # Assert
        assert len(result) == 1
        data = result[0]
        assert "error" not in data
        assert data["count"] == 2
        assert len(data["tasks"]) == 2
    
    @pytest.mark.asyncio
    async def test_list_tasks_filter_completed(self, test_user_id):
        """Test filtering tasks by completion status."""
        # Arrange - Add and complete a task
        add_result = await add_task("add_task", {
            "user_id": test_user_id,
            "title": "Task to complete"
        })
        task_id = add_result[0]["task_id"]
        
        await complete_task("complete_task", {
            "user_id": test_user_id,
            "task_id": task_id
        })
        
        # Add another incomplete task
        await add_task("add_task", {
            "user_id": test_user_id,
            "title": "Incomplete task"
        })
        
        # Act - List only completed tasks
        result = await list_tasks("list_tasks", {
            "user_id": test_user_id,
            "completed": True
        })
        
        # Assert
        assert len(result) == 1
        data = result[0]
        assert data["count"] == 1
        assert data["tasks"][0]["completed"] is True


class TestCompleteTaskTool:
    """Integration tests for complete_task tool."""
    
    @pytest.mark.asyncio
    async def test_complete_task_success(self, test_user_id):
        """Test successfully completing a task."""
        # Arrange - Add a task first
        add_result = await add_task("add_task", {
            "user_id": test_user_id,
            "title": "Task to complete"
        })
        task_id = add_result[0]["task_id"]
        
        # Act
        result = await complete_task("complete_task", {
            "user_id": test_user_id,
            "task_id": task_id
        })
        
        # Assert
        assert len(result) == 1
        task_data = result[0]
        assert "error" not in task_data
        assert task_data["completed"] is True
        assert task_data["completed_at"] is not None
    
    @pytest.mark.asyncio
    async def test_complete_task_not_found(self, test_user_id):
        """Test completing non-existent task returns error."""
        # Arrange
        fake_task_id = str(uuid4())
        
        # Act
        result = await complete_task("complete_task", {
            "user_id": test_user_id,
            "task_id": fake_task_id
        })
        
        # Assert
        assert len(result) == 1
        assert "error" in result[0]
        assert "not found" in result[0]["error"].lower()


class TestDeleteTaskTool:
    """Integration tests for delete_task tool."""
    
    @pytest.mark.asyncio
    async def test_delete_task_success(self, test_user_id):
        """Test successfully deleting a task."""
        # Arrange - Add a task first
        add_result = await add_task("add_task", {
            "user_id": test_user_id,
            "title": "Task to delete"
        })
        task_id = add_result[0]["task_id"]
        
        # Act
        result = await delete_task("delete_task", {
            "user_id": test_user_id,
            "task_id": task_id
        })
        
        # Assert
        assert len(result) == 1
        data = result[0]
        assert "error" not in data
        assert data["success"] is True
        
        # Verify task is deleted
        list_result = await list_tasks("list_tasks", {"user_id": test_user_id})
        assert list_result[0]["count"] == 0
    
    @pytest.mark.asyncio
    async def test_delete_task_not_found(self, test_user_id):
        """Test deleting non-existent task returns error."""
        # Arrange
        fake_task_id = str(uuid4())
        
        # Act
        result = await delete_task("delete_task", {
            "user_id": test_user_id,
            "task_id": fake_task_id
        })
        
        # Assert
        assert len(result) == 1
        assert "error" in result[0]


class TestUpdateTaskTool:
    """Integration tests for update_task tool."""
    
    @pytest.mark.asyncio
    async def test_update_task_title(self, test_user_id):
        """Test updating task title."""
        # Arrange - Add a task first
        add_result = await add_task("add_task", {
            "user_id": test_user_id,
            "title": "Original Title",
            "description": "Original Description"
        })
        task_id = add_result[0]["task_id"]
        
        # Act
        result = await update_task("update_task", {
            "user_id": test_user_id,
            "task_id": task_id,
            "title": "Updated Title"
        })
        
        # Assert
        assert len(result) == 1
        task_data = result[0]
        assert "error" not in task_data
        assert task_data["title"] == "Updated Title"
        assert task_data["description"] == "Original Description"
    
    @pytest.mark.asyncio
    async def test_update_task_description(self, test_user_id):
        """Test updating task description."""
        # Arrange - Add a task first
        add_result = await add_task("add_task", {
            "user_id": test_user_id,
            "title": "Title",
            "description": "Original Description"
        })
        task_id = add_result[0]["task_id"]
        
        # Act
        result = await update_task("update_task", {
            "user_id": test_user_id,
            "task_id": task_id,
            "description": "Updated Description"
        })
        
        # Assert
        assert len(result) == 1
        task_data = result[0]
        assert "error" not in task_data
        assert task_data["title"] == "Title"
        assert task_data["description"] == "Updated Description"
    
    @pytest.mark.asyncio
    async def test_update_task_both_fields(self, test_user_id):
        """Test updating both title and description."""
        # Arrange - Add a task first
        add_result = await add_task("add_task", {
            "user_id": test_user_id,
            "title": "Original Title",
            "description": "Original Description"
        })
        task_id = add_result[0]["task_id"]
        
        # Act
        result = await update_task("update_task", {
            "user_id": test_user_id,
            "task_id": task_id,
            "title": "New Title",
            "description": "New Description"
        })
        
        # Assert
        assert len(result) == 1
        task_data = result[0]
        assert "error" not in task_data
        assert task_data["title"] == "New Title"
        assert task_data["description"] == "New Description"
    
    @pytest.mark.asyncio
    async def test_update_task_not_found(self, test_user_id):
        """Test updating non-existent task returns error."""
        # Arrange
        fake_task_id = str(uuid4())
        
        # Act
        result = await update_task("update_task", {
            "user_id": test_user_id,
            "task_id": fake_task_id,
            "title": "New Title"
        })
        
        # Assert
        assert len(result) == 1
        assert "error" in result[0]


class TestToolWorkflow:
    """Integration tests for complete workflows."""
    
    @pytest.mark.asyncio
    async def test_complete_task_workflow(self, test_user_id):
        """Test complete workflow: add, list, complete, update, delete."""
        # Step 1: Add a task
        add_result = await add_task("add_task", {
            "user_id": test_user_id,
            "title": "Workflow Task",
            "description": "Test workflow"
        })
        assert "error" not in add_result[0]
        task_id = add_result[0]["task_id"]
        
        # Step 2: List tasks
        list_result = await list_tasks("list_tasks", {"user_id": test_user_id})
        assert list_result[0]["count"] >= 1
        
        # Step 3: Update task
        update_result = await update_task("update_task", {
            "user_id": test_user_id,
            "task_id": task_id,
            "title": "Updated Workflow Task"
        })
        assert update_result[0]["title"] == "Updated Workflow Task"
        
        # Step 4: Complete task
        complete_result = await complete_task("complete_task", {
            "user_id": test_user_id,
            "task_id": task_id
        })
        assert complete_result[0]["completed"] is True
        
        # Step 5: Delete task
        delete_result = await delete_task("delete_task", {
            "user_id": test_user_id,
            "task_id": task_id
        })
        assert delete_result[0]["success"] is True
        
        # Step 6: Verify deletion
        list_result_after = await list_tasks("list_tasks", {"user_id": test_user_id})
        # Task should be gone
        task_ids = [t["task_id"] for t in list_result_after[0]["tasks"]]
        assert task_id not in task_ids

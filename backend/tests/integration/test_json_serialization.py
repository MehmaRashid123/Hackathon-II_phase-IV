"""
JSON serialization tests.

Verifies that all tool outputs are properly JSON-serializable and
that datetime/UUID objects are correctly converted to strings.
"""
import pytest
import json
import asyncio
from uuid import uuid4
from datetime import datetime

from src.mcp.tools.add_task import add_task
from src.mcp.tools.list_tasks import list_tasks
from src.mcp.tools.complete_task import complete_task
from src.mcp.tools.update_task import update_task
from src.mcp.utils.serialization import (
    serialize_datetime,
    serialize_uuid,
    serialize_task,
)
from src.models.task import Task


@pytest.fixture
def test_user_id():
    """Generate a test user ID."""
    return str(uuid4())


class TestSerializationFunctions:
    """Tests for serialization utility functions."""
    
    def test_serialize_datetime_with_value(self):
        """Test datetime serialization with a valid datetime."""
        # Arrange
        dt = datetime(2026, 2, 9, 10, 30, 45)
        
        # Act
        result = serialize_datetime(dt)
        
        # Assert
        assert isinstance(result, str)
        assert result == "2026-02-09T10:30:45"
        # Verify it's JSON serializable
        json.dumps({"datetime": result})
    
    def test_serialize_datetime_with_none(self):
        """Test datetime serialization with None."""
        # Act
        result = serialize_datetime(None)
        
        # Assert
        assert result is None
        # Verify it's JSON serializable
        json.dumps({"datetime": result})
    
    def test_serialize_uuid(self):
        """Test UUID serialization."""
        # Arrange
        uuid_obj = uuid4()
        
        # Act
        result = serialize_uuid(uuid_obj)
        
        # Assert
        assert isinstance(result, str)
        assert len(result) == 36  # UUID string length
        assert result == str(uuid_obj)
        # Verify it's JSON serializable
        json.dumps({"uuid": result})
    
    def test_serialize_task_complete(self):
        """Test task serialization with all fields."""
        # Arrange
        task = Task(
            id=uuid4(),
            user_id=uuid4(),
            title="Test Task",
            description="Test Description",
            completed=True,
            created_at=datetime(2026, 2, 9, 10, 0, 0),
            updated_at=datetime(2026, 2, 9, 11, 0, 0),
            completed_at=datetime(2026, 2, 9, 11, 0, 0)
        )
        
        # Act
        result = serialize_task(task)
        
        # Assert
        assert isinstance(result, dict)
        assert isinstance(result["task_id"], str)
        assert isinstance(result["created_at"], str)
        assert isinstance(result["updated_at"], str)
        assert isinstance(result["completed_at"], str)
        assert result["title"] == "Test Task"
        assert result["description"] == "Test Description"
        assert result["completed"] is True
        
        # Verify it's JSON serializable
        json.dumps(result)
    
    def test_serialize_task_incomplete(self):
        """Test task serialization with None completed_at."""
        # Arrange
        task = Task(
            id=uuid4(),
            user_id=uuid4(),
            title="Incomplete Task",
            description=None,
            completed=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            completed_at=None
        )
        
        # Act
        result = serialize_task(task)
        
        # Assert
        assert result["completed_at"] is None
        assert result["description"] is None
        
        # Verify it's JSON serializable
        json.dumps(result)


class TestToolOutputSerialization:
    """Tests for JSON serialization of tool outputs."""
    
    @pytest.mark.asyncio
    async def test_add_task_output_is_json_serializable(self, test_user_id):
        """Test that add_task output can be serialized to JSON."""
        # Arrange
        arguments = {
            "user_id": test_user_id,
            "title": "Serialization Test",
            "description": "Testing JSON output"
        }
        
        # Act
        result = await add_task("add_task", arguments)
        
        # Assert
        assert len(result) == 1
        # Should not raise exception
        json_str = json.dumps(result[0])
        assert isinstance(json_str, str)
        
        # Verify we can parse it back
        parsed = json.loads(json_str)
        assert parsed["title"] == "Serialization Test"
    
    @pytest.mark.asyncio
    async def test_list_tasks_output_is_json_serializable(self, test_user_id):
        """Test that list_tasks output can be serialized to JSON."""
        # Arrange - Add some tasks first
        await add_task("add_task", {"user_id": test_user_id, "title": "Task 1"})
        await add_task("add_task", {"user_id": test_user_id, "title": "Task 2"})
        
        # Act
        result = await list_tasks("list_tasks", {"user_id": test_user_id})
        
        # Assert
        assert len(result) == 1
        # Should not raise exception
        json_str = json.dumps(result[0])
        assert isinstance(json_str, str)
        
        # Verify we can parse it back
        parsed = json.loads(json_str)
        assert "tasks" in parsed
        assert "count" in parsed
        assert isinstance(parsed["tasks"], list)
    
    @pytest.mark.asyncio
    async def test_complete_task_output_is_json_serializable(self, test_user_id):
        """Test that complete_task output can be serialized to JSON."""
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
        # Should not raise exception
        json_str = json.dumps(result[0])
        assert isinstance(json_str, str)
        
        # Verify completed_at is a string
        parsed = json.loads(json_str)
        assert isinstance(parsed["completed_at"], str)
    
    @pytest.mark.asyncio
    async def test_update_task_output_is_json_serializable(self, test_user_id):
        """Test that update_task output can be serialized to JSON."""
        # Arrange - Add a task first
        add_result = await add_task("add_task", {
            "user_id": test_user_id,
            "title": "Original"
        })
        task_id = add_result[0]["task_id"]
        
        # Act
        result = await update_task("update_task", {
            "user_id": test_user_id,
            "task_id": task_id,
            "title": "Updated"
        })
        
        # Assert
        assert len(result) == 1
        # Should not raise exception
        json_str = json.dumps(result[0])
        assert isinstance(json_str, str)
    
    @pytest.mark.asyncio
    async def test_delete_task_output_is_json_serializable(self, test_user_id):
        """Test that delete_task output can be serialized to JSON."""
        # Arrange - Add a task first
        add_result = await add_task("add_task", {
            "user_id": test_user_id,
            "title": "Task to delete"
        })
        task_id = add_result[0]["task_id"]
        
        # Act
        from src.mcp.tools.delete_task import delete_task
        result = await delete_task("delete_task", {
            "user_id": test_user_id,
            "task_id": task_id
        })
        
        # Assert
        assert len(result) == 1
        # Should not raise exception
        json_str = json.dumps(result[0])
        assert isinstance(json_str, str)


class TestErrorOutputSerialization:
    """Tests for JSON serialization of error outputs."""
    
    @pytest.mark.asyncio
    async def test_error_output_is_json_serializable(self, test_user_id):
        """Test that error responses are JSON serializable."""
        # Arrange - Try to complete non-existent task
        fake_task_id = str(uuid4())
        
        # Act
        result = await complete_task("complete_task", {
            "user_id": test_user_id,
            "task_id": fake_task_id
        })
        
        # Assert
        assert len(result) == 1
        assert "error" in result[0]
        
        # Should not raise exception
        json_str = json.dumps(result[0])
        assert isinstance(json_str, str)
        
        # Verify we can parse it back
        parsed = json.loads(json_str)
        assert "error" in parsed


class TestDateTimeFormats:
    """Tests for datetime format consistency."""
    
    @pytest.mark.asyncio
    async def test_datetime_fields_are_iso8601_format(self, test_user_id):
        """Test that all datetime fields use ISO 8601 format."""
        # Arrange & Act
        result = await add_task("add_task", {
            "user_id": test_user_id,
            "title": "DateTime Test"
        })
        
        # Assert
        task_data = result[0]
        created_at = task_data["created_at"]
        updated_at = task_data["updated_at"]
        
        # Verify ISO 8601 format (YYYY-MM-DDTHH:MM:SS)
        assert "T" in created_at
        assert "T" in updated_at
        
        # Verify we can parse them back to datetime
        datetime.fromisoformat(created_at)
        datetime.fromisoformat(updated_at)
    
    @pytest.mark.asyncio
    async def test_completed_at_format_after_completion(self, test_user_id):
        """Test that completed_at uses ISO 8601 format."""
        # Arrange - Add and complete a task
        add_result = await add_task("add_task", {
            "user_id": test_user_id,
            "title": "Task"
        })
        task_id = add_result[0]["task_id"]
        
        # Act
        result = await complete_task("complete_task", {
            "user_id": test_user_id,
            "task_id": task_id
        })
        
        # Assert
        task_data = result[0]
        completed_at = task_data["completed_at"]
        
        assert completed_at is not None
        assert isinstance(completed_at, str)
        assert "T" in completed_at
        
        # Verify we can parse it back to datetime
        datetime.fromisoformat(completed_at)


class TestUUIDFormats:
    """Tests for UUID format consistency."""
    
    @pytest.mark.asyncio
    async def test_task_id_is_valid_uuid_string(self, test_user_id):
        """Test that task_id is a valid UUID string."""
        # Arrange & Act
        result = await add_task("add_task", {
            "user_id": test_user_id,
            "title": "UUID Test"
        })
        
        # Assert
        task_id = result[0]["task_id"]
        assert isinstance(task_id, str)
        assert len(task_id) == 36  # UUID string length with hyphens
        
        # Verify we can parse it back to UUID
        from uuid import UUID
        UUID(task_id)
    
    @pytest.mark.asyncio
    async def test_all_task_ids_are_unique(self, test_user_id):
        """Test that each task gets a unique ID."""
        # Arrange & Act - Create multiple tasks
        results = []
        for i in range(5):
            result = await add_task("add_task", {
                "user_id": test_user_id,
                "title": f"Task {i}"
            })
            results.append(result[0]["task_id"])
        
        # Assert - All IDs are unique
        assert len(results) == len(set(results))


class TestComplexSerialization:
    """Tests for complex serialization scenarios."""
    
    @pytest.mark.asyncio
    async def test_task_with_special_characters_serializes(self, test_user_id):
        """Test that tasks with special characters serialize correctly."""
        # Arrange
        special_chars = "Task with 'quotes', \"double quotes\", and émojis 🎉"
        
        # Act
        result = await add_task("add_task", {
            "user_id": test_user_id,
            "title": special_chars
        })
        
        # Assert
        assert len(result) == 1
        # Should not raise exception
        json_str = json.dumps(result[0])
        
        # Verify we can parse it back
        parsed = json.loads(json_str)
        assert parsed["title"] == special_chars
    
    @pytest.mark.asyncio
    async def test_task_with_unicode_serializes(self, test_user_id):
        """Test that tasks with Unicode characters serialize correctly."""
        # Arrange
        unicode_text = "Task with 中文, العربية, and Русский"
        
        # Act
        result = await add_task("add_task", {
            "user_id": test_user_id,
            "title": unicode_text
        })
        
        # Assert
        assert len(result) == 1
        # Should not raise exception
        json_str = json.dumps(result[0], ensure_ascii=False)
        
        # Verify we can parse it back
        parsed = json.loads(json_str)
        assert parsed["title"] == unicode_text
    
    @pytest.mark.asyncio
    async def test_list_with_many_tasks_serializes(self, test_user_id):
        """Test that large lists of tasks serialize correctly."""
        # Arrange - Create many tasks
        for i in range(50):
            await add_task("add_task", {
                "user_id": test_user_id,
                "title": f"Task {i}"
            })
        
        # Act
        result = await list_tasks("list_tasks", {"user_id": test_user_id})
        
        # Assert
        assert len(result) == 1
        # Should not raise exception even with large list
        json_str = json.dumps(result[0])
        assert isinstance(json_str, str)
        
        # Verify we can parse it back
        parsed = json.loads(json_str)
        assert parsed["count"] >= 50

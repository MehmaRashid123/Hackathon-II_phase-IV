"""
Unit tests for TaskService.

Tests CRUD operations on tasks with proper user isolation.
"""
import pytest
from datetime import datetime
from uuid import uuid4, UUID
from unittest.mock import Mock, MagicMock, patch
from sqlmodel import Session

from src.services.task_service import TaskService
from src.models.task import Task


@pytest.fixture
def mock_session():
    """Create a mock database session."""
    session = Mock(spec=Session)
    return session


@pytest.fixture
def task_service(mock_session):
    """Create a TaskService instance with mocked session."""
    return TaskService(mock_session)


@pytest.fixture
def sample_user_id():
    """Generate a sample user ID."""
    return uuid4()


@pytest.fixture
def sample_task_id():
    """Generate a sample task ID."""
    return uuid4()


@pytest.fixture
def sample_task(sample_user_id, sample_task_id):
    """Create a sample task for testing."""
    return Task(
        id=sample_task_id,
        user_id=sample_user_id,
        title="Test Task",
        description="Test Description",
        completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        completed_at=None
    )


class TestCreateTask:
    """Tests for create_task method."""
    
    def test_create_task_success(self, task_service, mock_session, sample_user_id):
        """Test successful task creation."""
        # Arrange
        title = "Buy groceries"
        description = "Milk, eggs, bread"
        
        # Mock the session methods
        mock_session.add = Mock()
        mock_session.commit = Mock()
        mock_session.refresh = Mock()
        
        # Act
        task = task_service.create_task(sample_user_id, title, description)
        
        # Assert
        assert task.title == title
        assert task.description == description
        assert task.user_id == sample_user_id
        assert task.completed is False
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()
    
    def test_create_task_empty_title_raises_error(self, task_service, sample_user_id):
        """Test that empty title raises ValueError."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            task_service.create_task(sample_user_id, "", "Description")
    
    def test_create_task_whitespace_title_raises_error(self, task_service, sample_user_id):
        """Test that whitespace-only title raises ValueError."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            task_service.create_task(sample_user_id, "   ", "Description")
    
    def test_create_task_title_too_long_raises_error(self, task_service, sample_user_id):
        """Test that title exceeding 255 chars raises ValueError."""
        long_title = "a" * 256
        with pytest.raises(ValueError, match="Task title cannot exceed 255 characters"):
            task_service.create_task(sample_user_id, long_title, "Description")
    
    def test_create_task_description_too_long_raises_error(self, task_service, sample_user_id):
        """Test that description exceeding 2000 chars raises ValueError."""
        long_description = "a" * 2001
        with pytest.raises(ValueError, match="Task description cannot exceed 2000 characters"):
            task_service.create_task(sample_user_id, "Title", long_description)
    
    def test_create_task_strips_whitespace(self, task_service, mock_session, sample_user_id):
        """Test that title and description are stripped of whitespace."""
        # Arrange
        mock_session.add = Mock()
        mock_session.commit = Mock()
        mock_session.refresh = Mock()
        
        # Act
        task = task_service.create_task(sample_user_id, "  Title  ", "  Description  ")
        
        # Assert
        assert task.title == "Title"
        assert task.description == "Description"
    
    def test_create_task_empty_description_becomes_none(self, task_service, mock_session, sample_user_id):
        """Test that empty description is stored as None."""
        # Arrange
        mock_session.add = Mock()
        mock_session.commit = Mock()
        mock_session.refresh = Mock()
        
        # Act
        task = task_service.create_task(sample_user_id, "Title", "")
        
        # Assert
        assert task.description is None


class TestGetTasks:
    """Tests for get_tasks method."""
    
    def test_get_tasks_returns_all_user_tasks(self, task_service, mock_session, sample_user_id):
        """Test getting all tasks for a user."""
        # Arrange
        mock_result = Mock()
        mock_result.all.return_value = [Mock(), Mock(), Mock()]
        mock_session.exec.return_value = mock_result
        
        # Act
        tasks = task_service.get_tasks(sample_user_id)
        
        # Assert
        assert len(tasks) == 3
        mock_session.exec.assert_called_once()
    
    def test_get_tasks_filters_by_completed(self, task_service, mock_session, sample_user_id):
        """Test filtering tasks by completion status."""
        # Arrange
        mock_result = Mock()
        mock_result.all.return_value = [Mock()]
        mock_session.exec.return_value = mock_result
        
        # Act
        tasks = task_service.get_tasks(sample_user_id, completed=True)
        
        # Assert
        assert len(tasks) == 1
        mock_session.exec.assert_called_once()
    
    def test_get_tasks_returns_empty_list_for_no_tasks(self, task_service, mock_session, sample_user_id):
        """Test that empty list is returned when user has no tasks."""
        # Arrange
        mock_result = Mock()
        mock_result.all.return_value = []
        mock_session.exec.return_value = mock_result
        
        # Act
        tasks = task_service.get_tasks(sample_user_id)
        
        # Assert
        assert tasks == []


class TestGetTaskById:
    """Tests for get_task_by_id method."""
    
    def test_get_task_by_id_success(self, task_service, mock_session, sample_user_id, sample_task_id, sample_task):
        """Test successfully retrieving a task by ID."""
        # Arrange
        mock_result = Mock()
        mock_result.first.return_value = sample_task
        mock_session.exec.return_value = mock_result
        
        # Act
        task = task_service.get_task_by_id(sample_user_id, sample_task_id)
        
        # Assert
        assert task == sample_task
        mock_session.exec.assert_called_once()
    
    def test_get_task_by_id_not_found(self, task_service, mock_session, sample_user_id, sample_task_id):
        """Test that None is returned when task is not found."""
        # Arrange
        mock_result = Mock()
        mock_result.first.return_value = None
        mock_session.exec.return_value = mock_result
        
        # Act
        task = task_service.get_task_by_id(sample_user_id, sample_task_id)
        
        # Assert
        assert task is None
    
    def test_get_task_by_id_wrong_user(self, task_service, mock_session, sample_task_id):
        """Test that task is not returned for wrong user."""
        # Arrange
        wrong_user_id = uuid4()
        mock_result = Mock()
        mock_result.first.return_value = None
        mock_session.exec.return_value = mock_result
        
        # Act
        task = task_service.get_task_by_id(wrong_user_id, sample_task_id)
        
        # Assert
        assert task is None


class TestUpdateTask:
    """Tests for update_task method."""
    
    def test_update_task_title_only(self, task_service, mock_session, sample_user_id, sample_task_id, sample_task):
        """Test updating only the title."""
        # Arrange
        mock_result = Mock()
        mock_result.first.return_value = sample_task
        mock_session.exec.return_value = mock_result
        mock_session.add = Mock()
        mock_session.commit = Mock()
        mock_session.refresh = Mock()
        
        # Act
        updated_task = task_service.update_task(sample_user_id, sample_task_id, title="New Title")
        
        # Assert
        assert updated_task.title == "New Title"
        mock_session.commit.assert_called_once()
    
    def test_update_task_description_only(self, task_service, mock_session, sample_user_id, sample_task_id, sample_task):
        """Test updating only the description."""
        # Arrange
        mock_result = Mock()
        mock_result.first.return_value = sample_task
        mock_session.exec.return_value = mock_result
        mock_session.add = Mock()
        mock_session.commit = Mock()
        mock_session.refresh = Mock()
        
        # Act
        updated_task = task_service.update_task(sample_user_id, sample_task_id, description="New Description")
        
        # Assert
        assert updated_task.description == "New Description"
        mock_session.commit.assert_called_once()
    
    def test_update_task_both_fields(self, task_service, mock_session, sample_user_id, sample_task_id, sample_task):
        """Test updating both title and description."""
        # Arrange
        mock_result = Mock()
        mock_result.first.return_value = sample_task
        mock_session.exec.return_value = mock_result
        mock_session.add = Mock()
        mock_session.commit = Mock()
        mock_session.refresh = Mock()
        
        # Act
        updated_task = task_service.update_task(
            sample_user_id, sample_task_id,
            title="New Title",
            description="New Description"
        )
        
        # Assert
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"
    
    def test_update_task_not_found(self, task_service, mock_session, sample_user_id, sample_task_id):
        """Test updating non-existent task returns None."""
        # Arrange
        mock_result = Mock()
        mock_result.first.return_value = None
        mock_session.exec.return_value = mock_result
        
        # Act
        result = task_service.update_task(sample_user_id, sample_task_id, title="New Title")
        
        # Assert
        assert result is None
    
    def test_update_task_no_fields_raises_error(self, task_service, sample_user_id, sample_task_id):
        """Test that updating with no fields raises ValueError."""
        with pytest.raises(ValueError, match="At least one field"):
            task_service.update_task(sample_user_id, sample_task_id)
    
    def test_update_task_empty_title_raises_error(self, task_service, mock_session, sample_user_id, sample_task_id, sample_task):
        """Test that empty title raises ValueError."""
        # Arrange
        mock_result = Mock()
        mock_result.first.return_value = sample_task
        mock_session.exec.return_value = mock_result
        
        # Act & Assert
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            task_service.update_task(sample_user_id, sample_task_id, title="")


class TestCompleteTask:
    """Tests for complete_task method."""
    
    def test_complete_task_success(self, task_service, mock_session, sample_user_id, sample_task_id, sample_task):
        """Test successfully completing a task."""
        # Arrange
        mock_result = Mock()
        mock_result.first.return_value = sample_task
        mock_session.exec.return_value = mock_result
        mock_session.add = Mock()
        mock_session.commit = Mock()
        mock_session.refresh = Mock()
        
        # Act
        completed_task = task_service.complete_task(sample_user_id, sample_task_id)
        
        # Assert
        assert completed_task.completed is True
        assert completed_task.completed_at is not None
        mock_session.commit.assert_called_once()
    
    def test_complete_task_not_found(self, task_service, mock_session, sample_user_id, sample_task_id):
        """Test completing non-existent task returns None."""
        # Arrange
        mock_result = Mock()
        mock_result.first.return_value = None
        mock_session.exec.return_value = mock_result
        
        # Act
        result = task_service.complete_task(sample_user_id, sample_task_id)
        
        # Assert
        assert result is None


class TestDeleteTask:
    """Tests for delete_task method."""
    
    def test_delete_task_success(self, task_service, mock_session, sample_user_id, sample_task_id, sample_task):
        """Test successfully deleting a task."""
        # Arrange
        mock_result = Mock()
        mock_result.first.return_value = sample_task
        mock_session.exec.return_value = mock_result
        mock_session.delete = Mock()
        mock_session.commit = Mock()
        
        # Act
        result = task_service.delete_task(sample_user_id, sample_task_id)
        
        # Assert
        assert result is True
        mock_session.delete.assert_called_once_with(sample_task)
        mock_session.commit.assert_called_once()
    
    def test_delete_task_not_found(self, task_service, mock_session, sample_user_id, sample_task_id):
        """Test deleting non-existent task returns False."""
        # Arrange
        mock_result = Mock()
        mock_result.first.return_value = None
        mock_session.exec.return_value = mock_result
        
        # Act
        result = task_service.delete_task(sample_user_id, sample_task_id)
        
        # Assert
        assert result is False
        mock_session.delete.assert_not_called()

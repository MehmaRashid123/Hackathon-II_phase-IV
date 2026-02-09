"""
Shared pytest fixtures and configuration.

This file contains fixtures that are available to all tests.
"""
import pytest
import sys
from pathlib import Path

# Add src to path for imports
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))


@pytest.fixture(scope="session")
def test_database_url():
    """
    Provide test database URL.
    
    In a real environment, this would point to a test database.
    For now, it uses the same database as development.
    """
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    return os.getenv("DATABASE_URL")


@pytest.fixture(scope="function")
def clean_database():
    """
    Clean database before each test.
    
    This fixture would typically:
    1. Create a transaction
    2. Run the test
    3. Rollback the transaction
    
    For now, it's a placeholder for future implementation.
    """
    yield
    # Cleanup logic would go here


@pytest.fixture
def sample_user_ids():
    """Generate multiple test user IDs."""
    from uuid import uuid4
    return [str(uuid4()) for _ in range(5)]


# Pytest configuration hooks

def pytest_configure(config):
    """Configure pytest with custom settings."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically."""
    for item in items:
        # Auto-mark tests based on their location
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        
        # Auto-mark async tests
        if asyncio.iscoroutinefunction(item.function):
            item.add_marker(pytest.mark.asyncio)


# Import asyncio for async test detection
import asyncio

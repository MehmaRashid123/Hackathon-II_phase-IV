# MCP Server Quickstart Guide

**Spec**: 010-mcp-server-chatbot  
**Version**: 1.0.0  
**Last Updated**: 2026-02-09

## Overview

This guide will help you set up and test the MCP (Model Context Protocol) server with its 5 task management tools. The MCP server enables AI agents to interact with the task management system through a standardized protocol.

---

## Prerequisites

- Python 3.11 or higher
- PostgreSQL 14 or higher
- Virtual environment tool (venv or virtualenv)
- Git

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>/backend
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Key Dependencies**:
- `fastapi` - Web framework
- `sqlmodel` - ORM for database operations
- `mcp-sdk` - Model Context Protocol SDK
- `pydantic` - Data validation
- `psycopg2-binary` - PostgreSQL adapter
- `alembic` - Database migrations
- `pytest` - Testing framework

### 4. Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# JWT Configuration (for authentication)
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# MCP Server Configuration
MCP_SERVER_PORT=8001
MCP_SERVER_HOST=0.0.0.0

# Application Configuration
ENVIRONMENT=development
DEBUG=true
```

**Important**: Replace the placeholder values with your actual configuration.

### 5. Run Database Migrations

```bash
# Run all migrations
python run_migrations.py

# Or use Alembic directly
alembic upgrade head
```

This will create the following tables:
- `conversations` - Chat sessions
- `messages` - Individual messages
- `tasks` - Todo items

### 6. Verify Database Setup

```bash
# Check tables were created
python check_tables.py

# Expected output:
# ✓ conversations table exists
# ✓ messages table exists
# ✓ tasks table exists
```

---

## Running the MCP Server

### Start the Server

```bash
# Using the startup script
python start_mcp_server.py

# Or directly with uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload
```

**Expected Output**:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     MCP Server initialized with 5 tools
INFO:     - add_task
INFO:     - list_tasks
INFO:     - complete_task
INFO:     - delete_task
INFO:     - update_task
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001
```

### Verify Server is Running

```bash
# Check health endpoint
curl http://localhost:8001/health

# Expected response:
# {"status": "healthy", "mcp_tools": 5}
```

---

## Testing the MCP Tools

### Option 1: Run Automated Tests

```bash
# Run all tests
python run_tests.py

# Run specific test suites
pytest tests/unit/test_task_service.py -v
pytest tests/integration/test_mcp_tools.py -v
pytest tests/integration/test_multi_tenant.py -v
pytest tests/integration/test_json_serialization.py -v

# Run with coverage
pytest --cov=src --cov-report=html
```

**Expected Results**:
- 67 tests total
- All tests passing
- Coverage > 80%

### Option 2: Manual Testing with MCP Client

#### 1. Add a Task

```python
import asyncio
from mcp_client import MCPClient

async def test_add_task():
    client = MCPClient("http://localhost:8001")
    
    result = await client.call_tool(
        name="add_task",
        arguments={
            "user_id": "123e4567-e89b-12d3-a456-426614174000",
            "title": "Buy groceries",
            "description": "Milk, eggs, bread"
        }
    )
    
    print(f"Created task: {result['task_id']}")
    return result

asyncio.run(test_add_task())
```

**Expected Output**:
```json
{
  "task_id": "770e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-02-09T10:30:00",
  "updated_at": "2026-02-09T10:30:00",
  "completed_at": null
}
```

#### 2. List Tasks

```python
async def test_list_tasks():
    client = MCPClient("http://localhost:8001")
    
    result = await client.call_tool(
        name="list_tasks",
        arguments={
            "user_id": "123e4567-e89b-12d3-a456-426614174000",
            "completed": false  # Optional: filter by completion status
        }
    )
    
    print(f"Found {result['count']} tasks")
    for task in result['tasks']:
        print(f"- {task['title']}")

asyncio.run(test_list_tasks())
```

#### 3. Complete a Task

```python
async def test_complete_task():
    client = MCPClient("http://localhost:8001")
    
    result = await client.call_tool(
        name="complete_task",
        arguments={
            "user_id": "123e4567-e89b-12d3-a456-426614174000",
            "task_id": "770e8400-e29b-41d4-a716-446655440000"
        }
    )
    
    print(f"Task completed: {result['completed']}")

asyncio.run(test_complete_task())
```

#### 4. Update a Task

```python
async def test_update_task():
    client = MCPClient("http://localhost:8001")
    
    result = await client.call_tool(
        name="update_task",
        arguments={
            "user_id": "123e4567-e89b-12d3-a456-426614174000",
            "task_id": "770e8400-e29b-41d4-a716-446655440000",
            "title": "Buy groceries and milk",
            "description": "Milk, eggs, bread, butter"
        }
    )
    
    print(f"Task updated: {result['title']}")

asyncio.run(test_update_task())
```

#### 5. Delete a Task

```python
async def test_delete_task():
    client = MCPClient("http://localhost:8001")
    
    result = await client.call_tool(
        name="delete_task",
        arguments={
            "user_id": "123e4567-e89b-12d3-a456-426614174000",
            "task_id": "770e8400-e29b-41d4-a716-446655440000"
        }
    )
    
    print(f"Task deleted: {result['success']}")

asyncio.run(test_delete_task())
```

---

## Tool Reference

### Available Tools

1. **add_task** - Create a new task
2. **list_tasks** - List all tasks with optional filtering
3. **complete_task** - Mark a task as complete
4. **delete_task** - Delete a task
5. **update_task** - Update task details

### Tool Contracts

Detailed API specifications for each tool are available in the [contracts](./contracts/) directory:

- [add_task.yaml](./contracts/add_task.yaml)
- [list_tasks.yaml](./contracts/list_tasks.yaml)
- [complete_task.yaml](./contracts/complete_task.yaml)
- [delete_task.yaml](./contracts/delete_task.yaml)
- [update_task.yaml](./contracts/update_task.yaml)

---

## Troubleshooting

### Database Connection Issues

**Problem**: `psycopg2.OperationalError: could not connect to server`

**Solution**:
1. Verify PostgreSQL is running: `pg_isready`
2. Check DATABASE_URL in `.env` file
3. Verify database exists: `psql -l`
4. Check firewall settings

### Migration Errors

**Problem**: `alembic.util.exc.CommandError: Can't locate revision identified by 'xyz'`

**Solution**:
```bash
# Reset migrations (WARNING: drops all data)
alembic downgrade base
alembic upgrade head
```

### MCP Server Not Starting

**Problem**: `ModuleNotFoundError: No module named 'mcp'`

**Solution**:
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Test Failures

**Problem**: Tests fail with database errors

**Solution**:
```bash
# Use test database
export DATABASE_URL=postgresql://user:password@localhost:5432/test_db
pytest
```

---

## Development Workflow

### 1. Make Code Changes

Edit files in `backend/src/`:
- `src/mcp/tools/` - MCP tool implementations
- `src/services/` - Business logic
- `src/models/` - Database models

### 2. Run Tests

```bash
# Run tests after changes
pytest tests/ -v

# Run specific test file
pytest tests/unit/test_task_service.py -v
```

### 3. Check Code Quality

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

### 4. Create Migration (if schema changed)

```bash
# Auto-generate migration
alembic revision --autogenerate -m "Description of changes"

# Review generated migration in migrations/versions/

# Apply migration
alembic upgrade head
```

---

## Next Steps

1. **Explore Tool Contracts**: Review [contracts](./contracts/) for detailed API specs
2. **Read Data Model**: Understand the [data model](./data-model.md) documentation
3. **Run Tests**: Execute the full test suite to verify everything works
4. **Integrate with AI Agent**: Connect your AI agent to the MCP server
5. **Monitor Performance**: Use logging and metrics to track usage

---

## Additional Resources

- [MCP Protocol Specification](https://modelcontextprotocol.io/docs)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Pytest Documentation](https://docs.pytest.org/)

---

## Support

For issues or questions:
1. Check the [troubleshooting section](#troubleshooting)
2. Review test files in `tests/` for usage examples
3. Consult tool contracts in `contracts/` for API details
4. Check backend logs in `backend/server.log`

---

## Summary

You now have a fully functional MCP server with 5 task management tools:
- ✅ Database configured and migrated
- ✅ MCP server running on port 8001
- ✅ All 5 tools registered and tested
- ✅ Multi-tenant isolation enabled
- ✅ JSON serialization working

Start building your AI-powered task management chatbot!

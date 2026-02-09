# Implementation Plan: MCP Server and Database Persistence for AI Chatbot

**Branch**: `010-mcp-server-chatbot` | **Date**: 2026-02-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/010-mcp-server-chatbot/spec.md`

## Summary

Establish the MCP (Model Context Protocol) server infrastructure with database persistence for AI chatbot task management. This foundational feature implements 5 stateless MCP tools (add_task, list_tasks, complete_task, delete_task, update_task) that enable AI agents to perform CRUD operations on user tasks. The system includes database schema for Conversation, Message, and Task entities with strict multi-tenant isolation via user_id. All tools are JSON-serializable and stateless, requiring user_id in every call for secure data access.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Official MCP SDK (Python), SQLModel, Neon PostgreSQL, FastAPI (for MCP server hosting)
**Storage**: Neon Serverless PostgreSQL with SQLModel ORM
**Testing**: pytest (unit, integration), MCP tool testing framework, multi-tenant isolation tests
**Target Platform**: Linux/macOS server (backend MCP server)
**Project Type**: Backend MCP server (tool provider for AI agents)
**Performance Goals**:
- Tool execution < 500ms per call
- Database query < 200ms for list operations
- 99.9% availability for database persistence
- Support 100+ concurrent tool calls
- JSON serialization < 50ms per response

**Constraints**:
- Stateless tools (no server-side state between calls)
- user_id required in every tool call
- All tables must include user_id for multi-tenant isolation
- Tool parameters must match MCP SDK specifications
- JSON-serializable outputs only
- No AI agent logic (tools only)
- No frontend UI components
- Uses existing authentication from Phase I/II

**Scale/Scope**: Foundation for AI-powered task management, designed for 100-1000 concurrent users

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Spec-Driven Development ✅
- **Status**: PASS
- **Evidence**: Specification created in `specs/010-mcp-server-chatbot/spec.md` with 3 user stories, 8 functional requirements, and 5 success criteria before any implementation.

### Principle II: Agentic Workflow ✅
- **Status**: PASS
- **Evidence**: Implementation will be delegated to:
  - `neon-db-manager`: Database schema (Conversation, Message, Task tables), migrations, indexes
  - `fastapi-backend-architect`: MCP server setup, tool endpoint hosting
  - `mcp-tools-specialist`: MCP tool implementations (5 tools), JSON serialization
  - `spec-driven-architect`: Cross-stack coordination with future Spec 011 (AI Agent)

### Principle III: Security First ✅
- **Status**: PASS
- **Evidence**:
  - user_id required in every tool call for data isolation
  - Multi-tenant isolation via user_id filtering in all queries
  - No cross-user data access (verified through testing)
  - Input validation on all tool parameters
  - Error messages don't leak sensitive information
  - Database constraints enforce user_id presence
  - Existing JWT authentication from Phase I/II

### Principle IV: Modern Stack with Strong Typing ✅
- **Status**: PASS
- **Evidence**:
  - Python 3.11+ with type hints throughout
  - SQLModel for type-safe database models
  - Pydantic for tool parameter validation
  - MCP SDK with typed tool definitions
  - Type-checked tool inputs and outputs

### Principle V: User Isolation ✅
- **Status**: PASS
- **Evidence**:
  - All tables include user_id column
  - All queries filter by user_id
  - Tools require user_id parameter
  - No shared data between users
  - Database indexes on user_id for performance
  - Foreign key constraints maintain referential integrity

### Principle VI: Responsive Design ⚠️
- **Status**: NOT APPLICABLE
- **Evidence**: This is a backend MCP server with no UI components. Responsive design will be addressed in Spec 012 (Conversational UI).

### Principle VII: Data Persistence ✅
- **Status**: PASS
- **Evidence**:
  - Neon Serverless PostgreSQL for all data
  - SQLModel ORM for type-safe persistence
  - Conversation, Message, and Task tables
  - Database migrations for schema versioning
  - Indexes for query performance
  - Foreign key constraints for data integrity
  - 99.9% availability target

**Gate Decision**: ✅ PASS (Principle VI not applicable to backend MCP server)

## Project Structure

### Documentation (this feature)

```text
specs/010-mcp-server-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification
├── research.md          # Phase 0 output (MCP SDK best practices)
├── data-model.md        # Phase 1 output (Conversation, Message, Task schemas)
├── quickstart.md        # Phase 1 output (MCP server setup instructions)
├── contracts/           # Phase 1 output (MCP tool contracts)
│   ├── add_task.yaml    # add_task tool specification
│   ├── list_tasks.yaml  # list_tasks tool specification
│   ├── complete_task.yaml  # complete_task tool specification
│   ├── delete_task.yaml    # delete_task tool specification
│   └── update_task.yaml    # update_task tool specification
└── checklists/
    └── requirements.md  # Specification quality checklist
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── mcp/
│   │   ├── __init__.py
│   │   ├── server.py              # MCP server initialization
│   │   ├── tools/
│   │   │   ├── __init__.py
│   │   │   ├── add_task.py        # add_task tool implementation
│   │   │   ├── list_tasks.py      # list_tasks tool implementation
│   │   │   ├── complete_task.py   # complete_task tool implementation
│   │   │   ├── delete_task.py     # delete_task tool implementation
│   │   │   └── update_task.py     # update_task tool implementation
│   │   └── schemas/
│   │       ├── __init__.py
│   │       └── tool_params.py     # Pydantic schemas for tool parameters
│   ├── models/
│   │   ├── __init__.py
│   │   ├── conversation.py        # Conversation SQLModel
│   │   ├── message.py             # Message SQLModel
│   │   └── task.py                # Task SQLModel
│   ├── services/
│   │   ├── __init__.py
│   │   ├── task_service.py        # Task CRUD business logic
│   │   ├── conversation_service.py  # Conversation management
│   │   └── message_service.py     # Message persistence
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py              # Configuration (env vars)
│   │   └── database.py            # Database connection
│   └── main.py                    # FastAPI app with MCP server
├── migrations/
│   └── versions/
│       ├── 001_create_conversations_table.py
│       ├── 002_create_messages_table.py
│       └── 003_create_tasks_table.py
├── tests/
│   ├── unit/
│   │   ├── test_task_service.py
│   │   ├── test_conversation_service.py
│   │   └── test_message_service.py
│   ├── integration/
│   │   ├── test_mcp_tools.py      # Test all 5 MCP tools
│   │   ├── test_multi_tenant.py   # Test user isolation
│   │   └── test_json_serialization.py
│   └── fixtures/
│       ├── sample_tasks.json
│       ├── sample_conversations.json
│       └── sample_messages.json
├── requirements.txt               # Add: mcp-sdk, sqlmodel
└── README.md                      # Updated with MCP server documentation
```

**Structure Decision**: Backend MCP server structure (Option 1) selected. This is a pure backend feature providing tools for AI agents. No frontend components. MCP server hosted within existing FastAPI application.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | All applicable principles pass | N/A |

## Phase 0: Research & Technology Best Practices

### Official MCP SDK (Python)
- **Decision**: Use Official MCP SDK for tool implementation
- **Rationale**: Standardized protocol for AI agent tool calling, ensures compatibility with OpenAI Agents SDK and other agent frameworks. Official SDK provides robust tool registration, parameter validation, and JSON serialization.
- **Alternatives Considered**:
  - Custom tool protocol: More control but no standardization, compatibility issues
  - REST API endpoints: Simpler but doesn't follow MCP standard, less efficient
  - gRPC: More performant but adds complexity, not standard for AI agents
- **Best Practices**:
  - Define tools with clear descriptions and parameter schemas
  - Use Pydantic for parameter validation
  - Return JSON-serializable outputs only
  - Include error handling with descriptive messages
  - Log all tool calls for debugging and monitoring
  - Implement tool versioning for future updates

### Stateless Tool Design
- **Decision**: All tools are stateless, requiring user_id in every call
- **Rationale**: Enables horizontal scaling, simplifies deployment, prevents state synchronization issues. Each tool call is independent and can be processed by any server instance.
- **Alternatives Considered**:
  - Session-based tools: Requires state management, doesn't scale horizontally
  - Context injection: More complex, requires middleware coordination
  - Implicit user context: Security risk, harder to audit
- **Best Practices**:
  - Require user_id as first parameter in all tools
  - Validate user_id on every call
  - No server-side state between calls
  - Each tool call is atomic and independent
  - Database connection pooling for performance
  - Idempotent operations where possible

### Database Schema Design
- **Decision**: Three tables (Conversation, Message, Task) with user_id in all
- **Rationale**: Supports conversation history, message persistence, and task management with strict multi-tenant isolation. Normalized schema prevents data duplication.
- **Alternatives Considered**:
  - Single table with JSON columns: Simpler but loses query performance and type safety
  - Separate databases per user: Better isolation but operational complexity
  - NoSQL document store: More flexible but loses relational integrity
- **Best Practices**:
  - user_id in all tables for multi-tenant isolation
  - Foreign key constraints for referential integrity
  - Indexes on user_id and frequently queried columns
  - Timestamps (created_at, updated_at) for audit trail
  - UUID primary keys for better distribution
  - Soft deletes for data recovery (optional)

### Multi-Tenant Data Isolation
- **Decision**: Filter all queries by user_id, enforce at database and application level
- **Rationale**: Prevents cross-user data leakage, ensures privacy compliance, enables secure multi-user system.
- **Alternatives Considered**:
  - Row-level security (RLS) in PostgreSQL: More secure but adds complexity
  - Separate schemas per user: Better isolation but operational overhead
  - Application-level only: Easier but less secure
- **Best Practices**:
  - WHERE user_id = ? in all SELECT queries
  - Validate user_id before INSERT/UPDATE/DELETE
  - Database indexes on user_id for performance
  - Test cross-user access attempts
  - Log all data access for audit trail
  - Consider RLS for additional security layer (future)

### JSON Serialization for AI Agents
- **Decision**: All tool outputs must be JSON-serializable
- **Rationale**: AI agents consume tool outputs as JSON. Non-serializable types (datetime, UUID) must be converted to strings.
- **Alternatives Considered**:
  - Custom serialization format: More control but compatibility issues
  - Protobuf: More efficient but not standard for AI agents
  - Plain text: Simpler but loses structure
- **Best Practices**:
  - Convert datetime to ISO 8601 strings
  - Convert UUID to strings
  - Use Pydantic models with json() method
  - Test serialization in unit tests
  - Document output schemas clearly
  - Handle None values explicitly

### Error Handling in Tools
- **Decision**: Return clear error strings, don't raise exceptions
- **Rationale**: AI agents need descriptive error messages to communicate issues to users. Exceptions break tool execution flow.
- **Best Practices**:
  - Return error objects with "error" field
  - Include descriptive error messages
  - Don't leak sensitive information in errors
  - Log full error details server-side
  - Use consistent error format across tools
  - Test error scenarios explicitly

## Phase 1: Data Models & API Contracts

### Data Models

See [data-model.md](./data-model.md) for complete entity definitions.

**Conversation Entity** (SQLModel):
```python
class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
    title: Optional[str] = Field(None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    messages: List["Message"] = Relationship(back_populates="conversation")
```

**Message Entity** (SQLModel):
```python
class Message(SQLModel, table=True):
    __tablename__ = "messages"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", nullable=False, index=True)
    user_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
    role: str = Field(..., max_length=20)  # "user", "assistant", "tool"
    content: str = Field(..., max_length=10000)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    conversation: Conversation = Relationship(back_populates="messages")
```

**Task Entity** (SQLModel):
```python
class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
    title: str = Field(..., max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = Field(None)
```

**Database Constraints**:
- Foreign keys: conversation_id → conversations.id, user_id → users.id
- Indexes: user_id (all tables), conversation_id (messages), completed (tasks)
- Unique constraints: None (allow duplicate titles)
- Check constraints: role IN ('user', 'assistant', 'tool')

### MCP Tool Contracts

See [contracts/](./contracts/) for complete MCP tool specifications.

**Tool 1: add_task**
```python
@mcp_tool
def add_task(user_id: str, title: str, description: str = "") -> dict:
    """
    Create a new task for the user.
    
    Args:
        user_id: UUID of the user (required)
        title: Task title (required, max 255 chars)
        description: Task description (optional, max 2000 chars)
    
    Returns:
        {
            "task_id": "550e8400-e29b-41d4-a716-446655440000",
            "title": "Buy groceries",
            "description": "",
            "completed": false,
            "created_at": "2026-02-09T10:30:00Z"
        }
    
    Errors:
        {"error": "Invalid user_id"}
        {"error": "Title cannot be empty"}
    """
```

**Tool 2: list_tasks**
```python
@mcp_tool
def list_tasks(user_id: str, completed: Optional[bool] = None) -> dict:
    """
    List all tasks for the user.
    
    Args:
        user_id: UUID of the user (required)
        completed: Filter by completion status (optional)
    
    Returns:
        {
            "tasks": [
                {
                    "task_id": "550e8400-e29b-41d4-a716-446655440000",
                    "title": "Buy groceries",
                    "description": "",
                    "completed": false,
                    "created_at": "2026-02-09T10:30:00Z"
                },
                ...
            ],
            "count": 5
        }
    
    Errors:
        {"error": "Invalid user_id"}
    """
```

**Tool 3: complete_task**
```python
@mcp_tool
def complete_task(user_id: str, task_id: str) -> dict:
    """
    Mark a task as complete.
    
    Args:
        user_id: UUID of the user (required)
        task_id: UUID of the task (required)
    
    Returns:
        {
            "task_id": "550e8400-e29b-41d4-a716-446655440000",
            "title": "Buy groceries",
            "completed": true,
            "completed_at": "2026-02-09T11:00:00Z"
        }
    
    Errors:
        {"error": "Task not found"}
        {"error": "Invalid user_id or task_id"}
    """
```

**Tool 4: delete_task**
```python
@mcp_tool
def delete_task(user_id: str, task_id: str) -> dict:
    """
    Delete a task.
    
    Args:
        user_id: UUID of the user (required)
        task_id: UUID of the task (required)
    
    Returns:
        {
            "success": true,
            "message": "Task deleted successfully"
        }
    
    Errors:
        {"error": "Task not found"}
        {"error": "Invalid user_id or task_id"}
    """
```

**Tool 5: update_task**
```python
@mcp_tool
def update_task(user_id: str, task_id: str, title: Optional[str] = None, description: Optional[str] = None) -> dict:
    """
    Update task details.
    
    Args:
        user_id: UUID of the user (required)
        task_id: UUID of the task (required)
        title: New title (optional, max 255 chars)
        description: New description (optional, max 2000 chars)
    
    Returns:
        {
            "task_id": "550e8400-e29b-41d4-a716-446655440000",
            "title": "Buy groceries and milk",
            "description": "Don't forget organic milk",
            "completed": false,
            "updated_at": "2026-02-09T11:30:00Z"
        }
    
    Errors:
        {"error": "Task not found"}
        {"error": "Invalid user_id or task_id"}
        {"error": "At least one field (title or description) must be provided"}
    """
```

### Quickstart

See [quickstart.md](./quickstart.md) for complete setup instructions.

**Summary**:
1. Ensure database from Phase I/II is running (Neon PostgreSQL)
2. Set up environment variables in `.env`:
   - `DATABASE_URL`: Neon PostgreSQL connection string
   - `MCP_SERVER_PORT`: Port for MCP server (default: 8001)
3. Install dependencies:
   - `pip install mcp-sdk sqlmodel`
4. Run database migrations:
   - `alembic upgrade head` (creates Conversation, Message, Task tables)
5. Start MCP server:
   - `python -m src.mcp.server`
6. Test MCP tools:
   - Use MCP testing framework or manual tool calls
   - Verify JSON serialization
   - Test multi-tenant isolation

## Architectural Decisions Requiring Documentation

### ADR 1: MCP SDK vs. Custom Tool Protocol
- **Context**: Need standardized tool interface for AI agents
- **Decision**: Use Official MCP SDK for tool implementation
- **Alternatives**:
  - Custom tool protocol: More control but no standardization
  - REST API: Simpler but not MCP-compliant
  - gRPC: More performant but adds complexity
- **Consequences**:
  - ✅ Standardized protocol for AI agent compatibility
  - ✅ Official SDK support and updates
  - ✅ JSON serialization built-in
  - ⚠️ Dependency on MCP SDK updates
  - ⚠️ Learning curve for MCP-specific patterns
- **Status**: Approved
- **Suggest ADR**: 📋 Architectural decision detected: MCP SDK for tool implementation. Document? Run `/sp.adr mcp-sdk-choice`

### ADR 2: Stateless Tools with user_id Parameter
- **Context**: Need scalable, secure tool architecture
- **Decision**: All tools are stateless, requiring user_id in every call
- **Alternatives**:
  - Session-based tools: Requires state management
  - Context injection: More complex middleware
  - Implicit user context: Security risk
- **Consequences**:
  - ✅ Horizontal scaling without state synchronization
  - ✅ Clear security model (explicit user_id)
  - ✅ Simplified deployment and testing
  - ⚠️ user_id in every tool call (slight verbosity)
  - ⚠️ No implicit context (must pass explicitly)
- **Status**: Approved
- **Suggest ADR**: 📋 Architectural decision detected: Stateless tools with explicit user_id. Document? Run `/sp.adr stateless-mcp-tools`

### ADR 3: Three-Table Schema (Conversation, Message, Task)
- **Context**: Need to support conversation history and task management
- **Decision**: Separate tables for Conversation, Message, and Task with user_id in all
- **Alternatives**:
  - Single table with JSON: Simpler but loses query performance
  - Separate databases per user: Better isolation but operational complexity
  - NoSQL: More flexible but loses relational integrity
- **Consequences**:
  - ✅ Normalized schema prevents duplication
  - ✅ Efficient queries with proper indexes
  - ✅ Type-safe with SQLModel
  - ✅ Foreign key constraints ensure integrity
  - ⚠️ More complex migrations
  - ⚠️ Joins required for related data
- **Status**: Approved
- **Suggest ADR**: 📋 Architectural decision detected: Three-table normalized schema. Document? Run `/sp.adr database-schema-design`

## Testing Strategy

### Unit Tests
- **Task Service**: Test CRUD operations with mocked database
- **Conversation Service**: Test conversation creation and retrieval
- **Message Service**: Test message persistence with role validation
- **Tool Parameter Validation**: Test Pydantic schemas with invalid inputs
- **JSON Serialization**: Test datetime and UUID conversion

### Integration Tests
- **MCP Tool Execution**: Test all 5 tools end-to-end with real database
- **Multi-Tenant Isolation**: Create data for multiple users, verify no cross-access
- **JSON Serialization**: Verify all tool outputs are JSON-serializable
- **Error Handling**: Test error scenarios (invalid user_id, missing task, etc.)
- **Database Constraints**: Test foreign key and check constraints

### Performance Tests
- **Tool Execution Time**: Verify < 500ms per tool call
- **Database Query Performance**: Verify < 200ms for list operations
- **Concurrent Tool Calls**: Test 100+ concurrent calls
- **Connection Pooling**: Verify efficient database connection usage

### Acceptance Tests
- **Tool Integration**: AI agent successfully calls all 5 tools
- **Data Persistence**: Verify 99.9% availability
- **User Isolation**: 100% effective (no cross-user data leakage)
- **JSON Serialization**: 100% success rate
- **CRUD Operations**: 95% success rate under normal conditions

## Next Steps

This plan will be followed by:
1. **Phase 2: Task Generation** (`/sp.tasks`) - Break down this plan into actionable, ordered tasks
2. **Phase 3: Implementation** (`/sp.implement`) - Execute tasks via specialized agents
3. **Phase 4: Testing & Validation** - Verify all acceptance scenarios pass
4. **Phase 5: Documentation** - Complete MCP server documentation and quickstart guide
5. **Phase 6: Commit & PR** (`/sp.git.commit_pr`) - Create pull request for review

**Implementation Sequence**:
1. Database schema (Conversation, Message, Task tables with migrations)
2. SQLModel models with relationships and constraints
3. Database indexes on user_id and frequently queried columns
4. MCP server initialization and tool registration
5. Implement 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)
6. Task service with CRUD business logic
7. Conversation and message services
8. JSON serialization helpers
9. Error handling and validation
10. Unit tests for each component
11. Integration tests for MCP tools
12. Multi-tenant isolation tests
13. Performance and load tests

**Critical Path**:
- Database schema must be created before models
- SQLModel models must be defined before services
- Services must be implemented before MCP tools
- MCP server must be initialized before tool registration
- All tools must be tested for JSON serialization
- Multi-tenant isolation must be verified before production

**Agent Assignments**:
- `neon-db-manager`: Database schema, migrations, indexes, SQLModel models
- `fastapi-backend-architect`: MCP server setup, tool hosting, FastAPI integration
- `mcp-tools-specialist`: 5 MCP tool implementations, JSON serialization, error handling
- `spec-driven-architect`: Cross-stack coordination with Spec 011 (AI Agent)

**Estimated Complexity**: Medium-High (MCP SDK integration, multi-tenant isolation, 5 tools, 3 database tables)

**Dependencies**:
- **Phase I/II Authentication**: Uses existing Better Auth and JWT
- **Neon PostgreSQL**: Database must be provisioned and accessible
- **User table**: Must exist from Phase I (foreign key reference)

**Risk Mitigation**:
- MCP SDK learning curve: Study official documentation and examples
- Multi-tenant isolation: Comprehensive testing with multiple users
- JSON serialization: Test all data types (datetime, UUID, None)
- Database performance: Proper indexes and connection pooling
- Tool error handling: Clear error messages without sensitive data leakage


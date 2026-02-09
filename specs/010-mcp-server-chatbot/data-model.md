# Data Model Documentation

**Spec**: 010-mcp-server-chatbot  
**Version**: 1.0.0  
**Last Updated**: 2026-02-09

## Overview

This document describes the database schema and data models for the MCP server chatbot implementation. The system uses three primary entities: Conversations, Messages, and Tasks, all designed with multi-tenant isolation in mind.

---

## Entity Relationship Diagram

```
┌─────────────┐
│    User     │
│  (External) │
└──────┬──────┘
       │
       │ 1:N
       │
       ├──────────────────┬──────────────────┐
       │                  │                  │
       ▼                  ▼                  ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ Conversation │   │   Message    │   │     Task     │
└──────┬───────┘   └──────────────┘   └──────────────┘
       │
       │ 1:N
       │
       ▼
┌──────────────┐
│   Message    │
└──────────────┘
```

---

## Entities

### 1. Conversation

Represents a chat session between a user and the AI assistant.

**Table Name**: `conversations`

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique conversation identifier |
| `user_id` | UUID | FOREIGN KEY (users.id), NOT NULL, INDEXED | Owner of the conversation |
| `title` | VARCHAR(255) | NULLABLE | Optional conversation title |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation timestamp (UTC) |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp (UTC) |

**Relationships**:
- **User**: Many-to-One (conversation belongs to one user)
- **Messages**: One-to-Many (conversation has many messages)

**Indexes**:
- Primary key on `id`
- Index on `user_id` for efficient user-based queries

**Example**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Task Management Chat",
  "created_at": "2026-02-09T10:00:00Z",
  "updated_at": "2026-02-09T10:30:00Z"
}
```

---

### 2. Message

Represents individual messages within a conversation (user inputs, assistant responses, tool results).

**Table Name**: `messages`

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique message identifier |
| `conversation_id` | UUID | FOREIGN KEY (conversations.id), NOT NULL, INDEXED | Parent conversation |
| `user_id` | UUID | FOREIGN KEY (users.id), NOT NULL, INDEXED | Message owner (for isolation) |
| `role` | VARCHAR(20) | NOT NULL, CHECK IN ('user', 'assistant', 'tool') | Message role |
| `content` | VARCHAR(10000) | NOT NULL | Message text content |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation timestamp (UTC) |

**Relationships**:
- **Conversation**: Many-to-One (message belongs to one conversation)
- **User**: Many-to-One (message belongs to one user)

**Indexes**:
- Primary key on `id`
- Index on `conversation_id` for efficient conversation queries
- Index on `user_id` for multi-tenant isolation

**Constraints**:
- `role` must be one of: `'user'`, `'assistant'`, `'tool'`

**Example**:
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440000",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "role": "user",
  "content": "Add a task to buy groceries",
  "created_at": "2026-02-09T10:00:00Z"
}
```

---

### 3. Task

Represents a todo item created and managed through the MCP tools.

**Table Name**: `tasks`

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique task identifier |
| `created_by` | UUID | FOREIGN KEY (users.id), NOT NULL, INDEXED | Task creator/owner |
| `title` | VARCHAR(500) | NOT NULL | Task title (1-500 characters) |
| `description` | VARCHAR(5000) | NULLABLE | Optional task description |
| `priority` | ENUM | NOT NULL, DEFAULT 'MEDIUM' | Task priority (LOW, MEDIUM, HIGH, URGENT) |
| `status` | ENUM | NOT NULL, DEFAULT 'TO_DO' | Task status (TO_DO, IN_PROGRESS, REVIEW, DONE) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation timestamp (UTC) |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp (UTC) |
| `completed_at` | TIMESTAMP | NULLABLE | Completion timestamp (UTC) |
| `due_date` | TIMESTAMP | NULLABLE | Optional due date |
| `workspace_id` | UUID | FOREIGN KEY (workspace.id), NULLABLE, INDEXED | Optional workspace association |
| `project_id` | UUID | FOREIGN KEY (project.id), NULLABLE, INDEXED | Optional project association |
| `section_id` | UUID | FOREIGN KEY (sections.id), NULLABLE, INDEXED | Optional section association |
| `parent_id` | UUID | FOREIGN KEY (tasks.id), NULLABLE, INDEXED | Parent task for subtasks |
| `assigned_to` | UUID | FOREIGN KEY (users.id), NULLABLE, INDEXED | Optional task assignee |
| `recurrence_rule` | VARCHAR | NULLABLE | Recurrence pattern string |

**Relationships**:
- **User (Creator)**: Many-to-One (task created by one user)
- **User (Assignee)**: Many-to-One (task assigned to one user)
- **Workspace**: Many-to-One (task belongs to one workspace, optional)
- **Project**: Many-to-One (task belongs to one project, optional)
- **Section**: Many-to-One (task belongs to one section, optional)
- **Parent Task**: Many-to-One (task can have one parent)
- **Subtasks**: One-to-Many (task can have many subtasks)

**Indexes**:
- Primary key on `id`
- Index on `created_by` for efficient user-based queries
- Index on `assigned_to` for assignee queries
- Index on `workspace_id` for workspace filtering
- Index on `project_id` for project filtering
- Index on `section_id` for section filtering
- Index on `parent_id` for subtask queries
- Composite index on `(created_by, created_at)` for sorted queries

**Enums**:

**TaskPriority**:
- `LOW`
- `MEDIUM` (default)
- `HIGH`
- `URGENT`

**TaskStatus**:
- `TO_DO` (default)
- `IN_PROGRESS`
- `REVIEW`
- `DONE`

**Example**:
```json
{
  "id": "770e8400-e29b-41d4-a716-446655440000",
  "created_by": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": "MEDIUM",
  "status": "TO_DO",
  "created_at": "2026-02-09T10:30:00Z",
  "updated_at": "2026-02-09T10:30:00Z",
  "completed_at": null,
  "due_date": null,
  "workspace_id": null,
  "project_id": null,
  "section_id": null,
  "parent_id": null,
  "assigned_to": null,
  "recurrence_rule": null
}
```

---

## Multi-Tenant Isolation

All entities implement multi-tenant isolation through the `user_id` foreign key:

1. **Conversations**: Filtered by `user_id`
2. **Messages**: Filtered by `user_id` (even though they belong to conversations)
3. **Tasks**: Filtered by `created_by` (which maps to `user_id`)

**Security Guarantees**:
- Users can only access their own data
- All MCP tools require `user_id` parameter
- All database queries include `user_id` filter
- Foreign key constraints ensure referential integrity

---

## Database Migrations

Migrations are managed using Alembic and located in `backend/migrations/versions/`:

1. **001_create_conversations_table.py**: Creates conversations table
2. **002_create_messages_table.py**: Creates messages table with role constraint
3. **003_create_tasks_table.py**: Creates tasks table with enums and indexes

---

## JSON Serialization

All entities are serialized to JSON for MCP tool responses:

**Serialization Rules**:
- `UUID` → `string` (e.g., "770e8400-e29b-41d4-a716-446655440000")
- `datetime` → `ISO 8601 string` (e.g., "2026-02-09T10:30:00")
- `None` → `null`
- `Enum` → `string` (e.g., TaskPriority.MEDIUM → "MEDIUM")

**Utility Functions** (in `backend/src/mcp/utils/serialization.py`):
- `serialize_datetime(dt: datetime) -> str`
- `serialize_uuid(uuid: UUID) -> str`
- `serialize_task(task: Task) -> dict`
- `serialize_model(model: SQLModel) -> dict`

---

## Performance Considerations

**Indexes**:
- All foreign keys are indexed for efficient joins
- Composite index on `(created_by, created_at)` for sorted task queries
- Single indexes on frequently filtered columns

**Query Optimization**:
- Use `SELECT` with specific columns instead of `SELECT *`
- Limit result sets with pagination (future enhancement)
- Use connection pooling for concurrent requests

**Scalability**:
- All MCP tools are stateless (horizontal scaling)
- Database connection pooling configured
- Indexes support efficient filtering and sorting

---

## Future Enhancements

1. **Soft Deletes**: Add `deleted_at` column for data recovery
2. **Pagination**: Add limit/offset parameters to list operations
3. **Full-Text Search**: Add search indexes for task titles/descriptions
4. **Audit Logging**: Track all data modifications
5. **Caching**: Add Redis cache for frequently accessed data
6. **Archiving**: Move old completed tasks to archive tables

---

## Related Documentation

- [Tool Contracts](./contracts/) - API specifications for all MCP tools
- [Quickstart Guide](./quickstart.md) - Setup and testing instructions
- [Backend README](../../backend/README.md) - Development guide

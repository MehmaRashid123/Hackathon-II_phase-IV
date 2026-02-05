# Data Model: Backend Task Management API

**Feature**: 002-task-api
**Date**: 2026-02-05
**Phase**: Phase 1 - Data Model & Contracts

## Overview

This document defines the data model for the Task Management API, including database schema, relationships, validation rules, and state transitions.

---

## Entity: Task

### Description

Represents a single task item owned by a user. Tasks support CRUD operations and can be marked as completed or incomplete.

### Database Schema

**Table Name**: `tasks`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique task identifier |
| title | VARCHAR(500) | NOT NULL, INDEX | Task title (max 500 characters) |
| description | VARCHAR(5000) | NOT NULL, DEFAULT '' | Task description (optional, max 5000 chars) |
| is_completed | BOOLEAN | NOT NULL, DEFAULT FALSE | Completion status |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Creation timestamp (UTC) |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP | Last update timestamp (UTC) |
| user_id | INTEGER | NOT NULL, FOREIGN KEY → users.id, INDEX, ON DELETE CASCADE | Owner user reference |

### Indexes

1. **Primary Key**: `id` (automatic)
2. **Foreign Key Index**: `user_id` (optimizes `WHERE user_id = X` queries)
3. **Sort Index**: `created_at` (optimizes `ORDER BY created_at DESC`)
4. **Search Index**: `title` (optional, for future search functionality)

**Composite Index**: Consider `(user_id, created_at)` for optimal list endpoint performance

### Relationships

#### Task → User (Many-to-One)

- **Foreign Key**: `tasks.user_id → users.id`
- **Cascade Rule**: `ON DELETE CASCADE` (delete user → delete all their tasks)
- **Cardinality**: Each task belongs to exactly one user; each user can have many tasks
- **Nullability**: NOT NULL (tasks must have an owner)

**Rationale for ON DELETE CASCADE**:
- Tasks are meaningless without an owning user
- Prevents orphaned task records
- Simplifies user deletion logic

### SQLModel Definition

```python
# backend/src/models/task.py
from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    """
    Task database model with user ownership.
    Combines Pydantic validation with SQLAlchemy ORM.
    """
    __tablename__ = "tasks"

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Task content
    title: str = Field(
        max_length=500,
        min_length=1,
        index=True,
        description="Task title (1-500 characters)"
    )
    description: str = Field(
        default="",
        max_length=5000,
        description="Task description (0-5000 characters, optional)"
    )

    # Status
    is_completed: bool = Field(
        default=False,
        description="Task completion status"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC)"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC)"
    )

    # Foreign key to user
    user_id: int = Field(
        foreign_key="users.id",
        index=True,
        ondelete="CASCADE",
        description="Owner user ID"
    )

    # Optional: ORM relationship (for lazy loading user)
    # user: Optional["User"] = Relationship(back_populates="tasks")

    def __repr__(self):
        return f"Task(id={self.id}, title='{self.title}', user_id={self.user_id}, completed={self.is_completed})"
```

### Validation Rules

#### Title Validation

- **Required**: Yes
- **Min Length**: 1 character (after stripping whitespace)
- **Max Length**: 500 characters
- **Pattern**: Any Unicode characters allowed
- **Normalization**: Trim leading/trailing whitespace on save

**Validation Example**:
```python
title = title.strip()
if not title or len(title) > 500:
    raise ValueError("Title must be 1-500 characters")
```

#### Description Validation

- **Required**: No (default: empty string)
- **Min Length**: 0 characters
- **Max Length**: 5000 characters
- **Pattern**: Any Unicode characters allowed

#### is_completed Validation

- **Type**: Boolean
- **Allowed Values**: `True` (completed) or `False` (incomplete)
- **Default**: `False` (new tasks are incomplete)

#### user_id Validation

- **Type**: Integer
- **Required**: Yes
- **Must Match**: Authenticated user ID from JWT token
- **Foreign Key**: Must reference existing user in `users` table

**Security Validation**:
```python
# In API endpoint
if task.user_id != authenticated_user_id:
    raise HTTPException(status_code=403, detail="Access denied")
```

### State Transitions

#### Completion Status Lifecycle

```
[New Task]
    ↓
is_completed = False (default)
    ↓
[User marks complete via PATCH /complete]
    ↓
is_completed = True
    ↓
[User marks incomplete via PATCH /complete]
    ↓
is_completed = False
```

**Transition Rules**:
- Toggle operation: `is_completed = not is_completed`
- Idempotent: Calling PATCH /complete twice with same state is safe
- No validation needed: Boolean toggle is always valid

**State Diagram**:
```
    ┌─────────────┐
    │  Incomplete │ ←──────┐
    │  (False)    │        │
    └─────────────┘        │
          │                │
          │ PATCH          │ PATCH
          │ /complete      │ /complete
          ↓                │
    ┌─────────────┐        │
    │  Completed  │ ───────┘
    │  (True)     │
    └─────────────┘
```

### Timestamp Management

#### created_at

- **Set On**: Task creation (INSERT)
- **Updated On**: Never (immutable)
- **Value**: UTC timestamp at creation time
- **Implementation**: `default_factory=datetime.utcnow`

#### updated_at

- **Set On**: Task creation (INSERT) and every update (UPDATE)
- **Updated On**: PUT (update task), PATCH (toggle completion)
- **Value**: UTC timestamp at last modification
- **Implementation**: Manual update in service layer

**Update Pattern**:
```python
# In service layer before save
task.updated_at = datetime.utcnow()
db.commit()
```

### Query Patterns

#### List User Tasks (Paginated)

```python
# Most common query pattern
tasks = db.exec(
    select(Task)
    .where(Task.user_id == user_id)
    .order_by(Task.created_at.desc())
    .limit(limit)
    .offset(offset)
).all()
```

**Index Used**: `(user_id, created_at)` composite index (optimal)

#### Get Single Task

```python
# Get task with ownership validation
task = db.exec(
    select(Task)
    .where(Task.id == task_id)
    .where(Task.user_id == user_id)  # Ensures user owns task
).first()
```

**Index Used**: Primary key `id` + foreign key `user_id`

#### Toggle Completion

```python
# Atomic update
task.is_completed = not task.is_completed
task.updated_at = datetime.utcnow()
db.add(task)
db.commit()
db.refresh(task)
```

### Migration Script

**File**: `backend/alembic/versions/002_add_tasks_table.py`

```python
"""Add tasks table

Revision ID: 002
Revises: 001
Create Date: 2026-02-05

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '002'
down_revision = '001'  # Depends on users table from auth feature
branch_labels = None
depends_on = None

def upgrade():
    """Create tasks table with indexes and foreign key."""
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('description', sa.String(length=5000), nullable=False, server_default=''),
        sa.Column('is_completed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )

    # Indexes
    op.create_index('ix_tasks_user_id', 'tasks', ['user_id'], unique=False)
    op.create_index('ix_tasks_created_at', 'tasks', ['created_at'], unique=False)
    op.create_index('ix_tasks_title', 'tasks', ['title'], unique=False)

    # Composite index for optimal list queries
    op.create_index('ix_tasks_user_created', 'tasks', ['user_id', 'created_at'], unique=False)

def downgrade():
    """Drop tasks table and all indexes."""
    op.drop_index('ix_tasks_user_created', table_name='tasks')
    op.drop_index('ix_tasks_title', table_name='tasks')
    op.drop_index('ix_tasks_created_at', table_name='tasks')
    op.drop_index('ix_tasks_user_id', table_name='tasks')
    op.drop_table('tasks')
```

---

## Entity: User (Reference)

**Note**: User model is defined in the auth feature (001-auth-db-foundation). Tasks reference this existing table.

**Required User Schema**:
- `id`: INTEGER PRIMARY KEY (referenced by tasks.user_id)
- Other fields (email, password_hash, etc.) not relevant to task API

**Relationship**: User has many Tasks (one-to-many)

---

## Data Integrity Constraints

### Foreign Key Constraints

- **tasks.user_id → users.id**: Ensures every task belongs to a valid user
- **ON DELETE CASCADE**: Automatically delete tasks when user is deleted
- **ON UPDATE CASCADE**: Update task.user_id if user.id changes (unlikely)

### Check Constraints (Optional Future Enhancement)

```sql
-- Ensure title is not empty after trim
ALTER TABLE tasks ADD CONSTRAINT chk_title_not_empty
    CHECK (LENGTH(TRIM(title)) > 0);

-- Ensure created_at <= updated_at
ALTER TABLE tasks ADD CONSTRAINT chk_created_before_updated
    CHECK (created_at <= updated_at);
```

### Unique Constraints

**None**: Multiple users can have tasks with the same title (no global uniqueness required)

---

## Performance Considerations

### Query Optimization

1. **List Endpoint**: Index on `(user_id, created_at)` ensures fast pagination
2. **Single Task Lookup**: Primary key index makes `WHERE id = X` instant
3. **User Deletion**: CASCADE rule uses foreign key index for efficient cleanup

### Expected Query Volumes

- **List Tasks**: Most frequent (every page load)
- **Create Task**: Moderate (user action)
- **Update/Delete/Toggle**: Low (user action)

### Scalability Notes

- **Current design**: Handles 10,000 tasks per user efficiently
- **Index size**: ~100KB per 1,000 tasks (negligible)
- **Future optimization**: Partition by user_id if single user exceeds 100,000 tasks

---

## Security Notes

### User Isolation

- **Database Level**: Foreign key ensures task ownership
- **Application Level**: All queries MUST include `WHERE user_id = authenticated_user_id`
- **API Level**: Path parameter validation prevents cross-user access

### SQL Injection Prevention

- **SQLModel ORM**: Parameterized queries prevent injection
- **No raw SQL**: All queries use SQLModel select() API

### Data Retention

- **Cascade Delete**: Tasks deleted when user is deleted
- **No soft delete**: Tasks are permanently removed (simplifies compliance)
- **Audit logging**: Consider separate audit table for regulatory requirements

---

## Summary

| Aspect | Decision |
|--------|----------|
| Primary Key | Auto-increment integer `id` |
| Timestamps | UTC `created_at` and `updated_at` |
| User Relationship | Foreign key with ON DELETE CASCADE |
| Indexes | Primary key, user_id, created_at, composite (user_id, created_at) |
| Validation | Pydantic via SQLModel (title 1-500 chars, description 0-5000 chars) |
| State Management | Boolean toggle for completion status |
| ORM | SQLModel (Pydantic + SQLAlchemy) |

**Next**: Define API contracts (OpenAPI schema) in `contracts/task-api.openapi.yaml`

# Research: Backend Task Management API

**Feature**: 002-task-api
**Date**: 2026-02-05
**Phase**: Phase 0 - Research & Discovery

## Overview

This document consolidates research findings for implementing a secure FastAPI task management API with JWT authentication, SQLModel ORM, and user isolation patterns.

---

## 1. JWT Verification Best Practices in FastAPI

### Decision: Dependency Injection with python-jose

**Research Question**: How to implement secure JWT verification middleware using python-jose?

**Findings**:

FastAPI's dependency injection system provides a clean pattern for JWT verification:

```python
# middleware/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime
from typing import Optional

security = HTTPBearer()

JWT_SECRET = os.getenv("BETTER_AUTH_SECRET")
JWT_ALGORITHM = "HS256"  # Better Auth default

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Verify JWT token and extract claims.
    Raises HTTPException(401) if token is invalid or expired.
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        # Check expiration
        exp = payload.get("exp")
        if exp and datetime.utcnow().timestamp() > exp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user_id(token_payload: dict = Depends(verify_token)) -> int:
    """
    Extract user_id from JWT payload.
    Better Auth uses 'sub' claim for user ID by default.
    """
    user_id = token_payload.get("sub") or token_payload.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing user identifier",
        )

    return int(user_id)
```

**Rationale**:
- Dependency injection allows reusability across all endpoints
- FastAPI handles exception translation to proper HTTP responses
- Separation of concerns: token verification vs. user extraction
- Type hints provide IDE autocomplete and validation

**Alternatives Considered**:
- **Middleware**: Would apply to all routes globally, harder to exclude specific endpoints
- **Manual verification in each endpoint**: DRY violation, error-prone

**Dependencies**:
```bash
pip install python-jose[cryptography] python-multipart
```

---

## 2. SQLModel Foreign Key Relationships

### Decision: Explicit Foreign Key with ON DELETE CASCADE

**Research Question**: How to define Task → User foreign key with ON DELETE CASCADE using SQLModel?

**Findings**:

SQLModel combines Pydantic validation with SQLAlchemy ORM:

```python
# models/task.py
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=500, index=True)
    description: str = Field(default="", max_length=5000)
    is_completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Foreign key with cascade delete
    user_id: int = Field(foreign_key="users.id", index=True, ondelete="CASCADE")

    # Optional: Relationship for ORM navigation
    # user: Optional["User"] = Relationship(back_populates="tasks")
```

**Alembic Migration**:

```python
# alembic/versions/002_add_tasks_table.py
def upgrade():
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('description', sa.String(length=5000), nullable=False),
        sa.Column('is_completed', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    op.create_index(op.f('ix_tasks_title'), 'tasks', ['title'], unique=False)
    op.create_index(op.f('ix_tasks_user_id'), 'tasks', ['user_id'], unique=False)
    op.create_index(op.f('ix_tasks_created_at'), 'tasks', ['created_at'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_tasks_created_at'), table_name='tasks')
    op.drop_index(op.f('ix_tasks_user_id'), table_name='tasks')
    op.drop_index(op.f('ix_tasks_title'), table_name='tasks')
    op.drop_table('tasks')
```

**Rationale**:
- `ON DELETE CASCADE` ensures orphaned tasks are cleaned up when user is deleted
- Indexes on `user_id` and `created_at` optimize queries (WHERE user_id = X ORDER BY created_at)
- `default_factory` ensures fresh datetime objects (not shared across instances)
- SQLModel provides both Pydantic validation and SQLAlchemy ORM

**Alternatives Considered**:
- **No cascade**: Would require manual cleanup, risk orphaned records
- **ON DELETE SET NULL**: Not applicable, tasks must belong to a user

---

## 3. FastAPI User Isolation Patterns

### Decision: Path Parameter Validation Dependency

**Research Question**: How to enforce user_id path parameter matches JWT user_id?

**Findings**:

Create a reusable dependency that validates path parameter against JWT claim:

```python
# middleware/auth.py (continued)

async def verify_user_access(
    user_id: int,  # From path parameter
    current_user_id: int = Depends(get_current_user_id)
) -> int:
    """
    Verify that the user_id in the path matches the authenticated user.
    Returns user_id if valid, raises 403 if mismatch.
    """
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: cannot access resources of other users",
        )

    return user_id
```

**Usage in Endpoints**:

```python
# api/tasks.py
from fastapi import APIRouter, Depends
from middleware.auth import verify_user_access

router = APIRouter()

@router.get("/api/{user_id}/tasks")
async def list_tasks(
    validated_user_id: int = Depends(verify_user_access),
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    # validated_user_id guaranteed to match JWT user_id
    tasks = db.query(Task).filter(
        Task.user_id == validated_user_id
    ).limit(limit).offset(offset).all()

    return tasks
```

**Rationale**:
- Single source of truth for user isolation enforcement
- Dependency chain: HTTP Auth → JWT Verify → User Extract → Path Validate
- FastAPI handles dependency injection and error propagation
- Type-safe with IDE support

**Alternatives Considered**:
- **Manual validation in each endpoint**: DRY violation, easy to forget
- **Middleware**: Can't access path parameters easily
- **Query-only filtering**: Doesn't prevent users from guessing other user IDs in URL

---

## 4. Pagination Best Practices for Task Lists

### Decision: Limit/Offset with Total Count

**Research Question**: How to implement limit/offset pagination with SQLModel?

**Findings**:

```python
# api/tasks.py
from sqlmodel import select, func

@router.get("/api/{user_id}/tasks")
async def list_tasks(
    validated_user_id: int = Depends(verify_user_access),
    limit: int = Query(default=50, le=100),  # Max 100 items per page
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    # Count total tasks for pagination metadata
    total_count = db.scalar(
        select(func.count()).select_from(Task).where(Task.user_id == validated_user_id)
    )

    # Fetch paginated tasks
    tasks = db.exec(
        select(Task)
        .where(Task.user_id == validated_user_id)
        .order_by(Task.created_at.desc())
        .limit(limit)
        .offset(offset)
    ).all()

    return {
        "tasks": tasks,
        "total": total_count,
        "limit": limit,
        "offset": offset,
        "has_more": (offset + limit) < total_count
    }
```

**Rationale**:
- Limit/offset is simple and works well for small-to-medium datasets
- Query parameter validation via FastAPI's `Query`
- Total count enables UI to show "Page X of Y"
- `has_more` flag simplifies infinite scroll implementation

**Alternatives Considered**:
- **Cursor-based pagination**: More complex, better for very large datasets with concurrent writes
- **No pagination**: Would fail performance goals for users with 1000+ tasks

**Performance Considerations**:
- Indexes on `user_id` and `created_at` make ORDER BY + LIMIT efficient
- For 1000 tasks, offset queries remain fast (<50ms)
- Consider cursor pagination if dataset grows beyond 10,000 tasks per user

---

## 5. Neon PostgreSQL Connection Pooling

### Decision: Standard SQLModel Engine with Moderate Pool Size

**Research Question**: Optimal connection pool settings for serverless PostgreSQL?

**Findings**:

```python
# core/database.py
from sqlmodel import create_engine, Session
from sqlalchemy.pool import QueuePool
import os

DATABASE_URL = os.getenv("DATABASE_URL")

# Neon-optimized connection pool
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL logging in dev
    poolclass=QueuePool,
    pool_size=10,          # Neon recommends 5-10 for serverless
    max_overflow=20,       # Burst capacity for concurrent requests
    pool_timeout=30,       # Wait 30s for available connection
    pool_recycle=3600,     # Recycle connections after 1 hour
    pool_pre_ping=True,    # Verify connections before use
)

def get_db():
    """Dependency for database session injection."""
    with Session(engine) as session:
        yield session
```

**Rationale**:
- **pool_size=10**: Neon serverless scales automatically, moderate pool prevents over-connection
- **max_overflow=20**: Handles traffic spikes (100 concurrent requests with avg 10 active connections)
- **pool_pre_ping=True**: Detects stale connections (important for serverless with dynamic IPs)
- **pool_recycle=3600**: Prevents long-lived connections from accumulating state

**Neon-Specific Considerations**:
- Neon automatically scales compute based on load
- Connection pooling on application side reduces overhead
- Use PgBouncer for very high concurrency (1000+ concurrent users)

**Alternatives Considered**:
- **NullPool**: No pooling, new connection per request (high latency)
- **Large pool_size (50+)**: Wastes resources on Neon's serverless model

---

## Summary of Decisions

| Research Area | Decision | Key Technology |
|---------------|----------|----------------|
| JWT Verification | Dependency injection pattern | python-jose, FastAPI Depends |
| Foreign Keys | ON DELETE CASCADE with indexes | SQLModel, Alembic |
| User Isolation | Path parameter validation dependency | FastAPI Depends |
| Pagination | Limit/offset with total count | SQLModel select() |
| Connection Pool | Moderate pool size (10+20) | SQLAlchemy QueuePool |

---

## Dependencies to Install

```bash
# Add to backend/requirements.txt
python-jose[cryptography]==3.3.0
python-multipart==0.0.6
psycopg2-binary==2.9.9
```

---

## Next Phase

**Phase 1**: Generate data-model.md, contracts/task-api.openapi.yaml, and quickstart.md based on these research findings.

**Validation**: Research findings align with constitution principles (Security First, Modern Stack, User Isolation).

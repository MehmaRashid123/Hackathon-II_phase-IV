# Implementation Plan: Backend Task Management API

**Branch**: `002-task-api` | **Date**: 2026-02-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-task-api/spec.md`

## Summary

Build a secure REST API for task management using FastAPI, SQLModel ORM, and Neon PostgreSQL. The API provides 6 user stories implementing CRUD operations on tasks with JWT-based authentication and user isolation. Each endpoint enforces that users can only access their own tasks by validating the URL `user_id` parameter against the JWT token's user ID claim.

**Technical Approach**: Implement FastAPI dependency injection for JWT verification, SQLModel for database operations with automatic timestamps, and strict user isolation at the query level. All endpoints follow RESTful conventions with proper HTTP status codes and OpenAPI documentation.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**:
- FastAPI 0.104+ (async web framework, OpenAPI docs)
- SQLModel 0.0.14+ (Pydantic + SQLAlchemy ORM)
- python-jose[cryptography] (JWT verification)
- psycopg2-binary (PostgreSQL driver)
- uvicorn (ASGI server)

**Storage**: Neon Serverless PostgreSQL (configured via DATABASE_URL env variable)
**Testing**: pytest, httpx (async test client), pytest-asyncio
**Target Platform**: Linux server (Docker container or cloud VM)
**Project Type**: Web API (backend only)
**Performance Goals**:
- List tasks endpoint: < 200ms p95 latency for 1000 tasks
- CRUD operations: < 100ms p95 latency
- Support 100 concurrent requests without degradation
- Database connection pooling configured

**Constraints**:
- Must verify JWT signature on every request
- Must validate URL user_id matches JWT token user_id
- Must return standard HTTP status codes (200, 201, 204, 401, 403, 404, 422, 503)
- Must auto-generate unique task IDs
- Must auto-set timestamps (created_at, updated_at)
- Must use SQLModel (no raw SQL)

**Scale/Scope**:
- 6 user stories (2 P1, 2 P2, 2 P3)
- 6 API endpoints (GET list, POST create, GET single, PUT update, PATCH toggle, DELETE)
- 1 database table (tasks) with 7 columns
- User isolation enforced at database query level

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Spec-Driven Development
✅ **PASS** - Feature has complete specification in `specs/002-task-api/spec.md` with user stories, functional requirements, and success criteria.

### Principle II: Agentic Workflow
✅ **PASS** - Implementation will delegate to `fastapi-backend-architect` agent for all backend code.

### Principle III: Security First
✅ **PASS** - JWT verification on every request via dependency injection. User ID validation enforced. PostgreSQL parameterized queries via SQLModel ORM prevent SQL injection.

### Principle IV: Modern Stack with Strong Typing
✅ **PASS** - Python 3.11+ with type hints. FastAPI + Pydantic for request/response validation. SQLModel for type-safe database operations.

### Principle V: User Isolation
✅ **PASS** - All database queries filtered by `WHERE user_id = {authenticated_user_id}`. URL user_id validated against JWT token user_id with 403 Forbidden on mismatch.

### Principle VI: Responsive Design
✅ **PASS** - N/A (backend API only, no frontend)

### Principle VII: Data Persistence
✅ **PASS** - All task data persisted to Neon PostgreSQL. SQLModel handles migrations. Foreign key constraints ensure referential integrity.

**Overall Gate Status**: ✅ **PASS** - All applicable constitutional principles satisfied.

## Project Structure

### Documentation (this feature)

```text
specs/002-task-api/
├── spec.md              # Feature specification
├── plan.md              # This file (/sp.plan output)
├── research.md          # JWT verification, SQLModel patterns (already created)
├── data-model.md        # Task entity schema, relationships (already created)
├── quickstart.md        # API testing guide (already created)
├── contracts/           # API endpoint contracts (already created)
│   └── openapi.yaml     # OpenAPI 3.0 specification
└── checklists/
    └── requirements.md  # Specification quality checklist
```

### Source Code (repository root)

```text
backend/                            # FastAPI application
├── src/
│   ├── models/                     # SQLModel database models
│   │   ├── __init__.py
│   │   ├── user.py                 # User model (from Spec 001)
│   │   └── task.py                 # Task model with user_id FK
│   │
│   ├── schemas/                    # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   └── task_schemas.py         # TaskCreate, TaskUpdate, TaskResponse
│   │
│   ├── api/                        # API route handlers
│   │   ├── __init__.py
│   │   └── tasks.py                # Task CRUD endpoints
│   │
│   ├── middleware/                 # Authentication middleware
│   │   ├── __init__.py
│   │   └── auth.py                 # JWT verification, get_current_user_id
│   │
│   ├── services/                   # Business logic layer
│   │   ├── __init__.py
│   │   └── task_service.py         # Task CRUD operations with user isolation
│   │
│   ├── database.py                 # Database connection and session management
│   ├── config.py                   # Environment configuration
│   └── main.py                     # FastAPI app entry point, routers
│
├── tests/
│   ├── conftest.py                 # Pytest fixtures (test DB, auth tokens)
│   ├── contract/                   # API contract tests
│   │   └── test_task_endpoints.py # Test each endpoint spec compliance
│   ├── integration/                # Integration tests
│   │   └── test_task_isolation.py # Test user isolation across endpoints
│   └── unit/                       # Unit tests
│       └── test_task_service.py   # Test service layer logic
│
├── alembic/                        # Database migrations
│   ├── versions/                   # Migration scripts
│   │   └── 001_create_tasks_table.py
│   └── env.py                      # Alembic configuration
│
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Container image definition
└── .env.example                    # Environment template
```

**Structure Decision**: Backend monolith using FastAPI best practices. Services layer separates business logic from route handlers. Middleware handles cross-cutting concerns (auth). Alembic manages database migrations.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No constitutional violations. This section is intentionally left empty.

## Phase 0: Research & Analysis

### Research Completed ✅

All research documented in `research.md` (already created):

1. ✅ **JWT Verification** - python-jose implementation with dependency injection
2. ✅ **User ID Validation** - Extract from JWT payload, validate against URL parameter
3. ✅ **SQLModel Patterns** - ORM setup, relationship definitions, automatic timestamps
4. ✅ **User Isolation** - Query filtering, service layer patterns
5. ✅ **Error Handling** - HTTP status codes, Pydantic validation errors

## Phase 1: Design & Contracts

### Data Model ✅ Completed

Documented in `data-model.md`:

**Task Entity**:
- `id`: INTEGER PRIMARY KEY (auto-increment)
- `title`: VARCHAR(500) NOT NULL (indexed)
- `description`: VARCHAR(5000) DEFAULT ''
- `is_completed`: BOOLEAN DEFAULT FALSE
- `created_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- `updated_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- `user_id`: INTEGER NOT NULL FK → users.id (indexed, ON DELETE CASCADE)

**Indexes**:
- Primary: `id`
- Foreign Key: `user_id`
- Composite: `(user_id, created_at)` for optimal list queries

### API Contracts ✅ Completed

Documented in `contracts/openapi.yaml`:

| Endpoint | Method | Request | Response | Auth |
|----------|--------|---------|----------|------|
| `/api/{user_id}/tasks` | GET | - | TaskList (200) | JWT Required |
| `/api/{user_id}/tasks` | POST | TaskCreate | Task (201) | JWT Required |
| `/api/{user_id}/tasks/{id}` | GET | - | Task (200) | JWT Required |
| `/api/{user_id}/tasks/{id}` | PUT | TaskUpdate | Task (200) | JWT Required |
| `/api/{user_id}/tasks/{id}` | DELETE | - | 204 No Content | JWT Required |
| `/api/{user_id}/tasks/{id}/complete` | PATCH | - | Task (200) | JWT Required |

**Common Error Responses**:
- `401 Unauthorized`: Missing/invalid JWT token
- `403 Forbidden`: URL user_id doesn't match JWT user_id
- `404 Not Found`: Task doesn't exist
- `422 Validation Error`: Invalid request data

### Pydantic Schemas

```python
# schemas/task_schemas.py
from pydantic import BaseModel, Field
from datetime import datetime

class TaskCreate(BaseModel):
    """Request schema for creating a task"""
    title: str = Field(..., min_length=1, max_length=500)
    description: str = Field(default="", max_length=5000)

class TaskUpdate(BaseModel):
    """Request schema for updating a task"""
    title: str | None = Field(None, min_length=1, max_length=500)
    description: str | None = Field(None, max_length=5000)

class TaskResponse(BaseModel):
    """Response schema for task data"""
    id: int
    title: str
    description: str
    is_completed: bool
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        from_attributes = True  # Allow SQLModel → Pydantic conversion
```

### Quickstart Guide ✅ Completed

Documented in `quickstart.md`:
1. Prerequisites: Python 3.11+, PostgreSQL (Neon), Better Auth JWT secret
2. Environment setup: `.env` with DATABASE_URL and BETTER_AUTH_SECRET
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `alembic upgrade head`
5. Start server: `uvicorn src.main:app --reload`
6. Access docs: `http://localhost:8000/docs`
7. Test endpoints with valid JWT token

### Agent Context Update

After completing Phase 1 design:
```bash
.specify/scripts/bash/update-agent-context.sh claude
```

This will update `.claude/context` with:
- FastAPI dependency injection patterns
- SQLModel relationships and queries
- JWT verification middleware
- User isolation service patterns
- OpenAPI documentation structure

## Phase 2: Implementation Workflow

**Note**: Actual task breakdown will be created by `/sp.tasks` command (not part of this plan).

### High-Level Implementation Sequence

1. **Database Models** (P1 - Critical)
   - Implement Task model in `models/task.py`
   - Create Alembic migration for tasks table
   - Run migration against Neon database

2. **Authentication Middleware** (P1 - Critical)
   - Implement JWT verification in `middleware/auth.py`
   - Create `verify_token` dependency
   - Create `get_current_user_id` dependency
   - Create `validate_user_id` dependency for URL parameter checking

3. **Pydantic Schemas** (P1 - Critical)
   - Implement TaskCreate, TaskUpdate, TaskResponse in `schemas/task_schemas.py`

4. **Service Layer** (P1 - Critical)
   - Implement TaskService in `services/task_service.py`
   - All CRUD methods with user isolation filters
   - Error handling for not found, forbidden cases

5. **API Endpoints - User Story 1** (P1 - MVP Core)
   - Implement GET `/api/{user_id}/tasks` in `api/tasks.py`
   - List all tasks for authenticated user

6. **API Endpoints - User Story 2** (P1 - MVP Core)
   - Implement POST `/api/{user_id}/tasks`
   - Create new task for authenticated user

7. **API Endpoints - User Story 3** (P2 - Enhancement)
   - Implement PUT `/api/{user_id}/tasks/{id}`
   - Update existing task

8. **API Endpoints - User Story 4** (P2 - Enhancement)
   - Implement PATCH `/api/{user_id}/tasks/{id}/complete`
   - Toggle task completion status

9. **API Endpoints - User Story 5** (P3 - Nice-to-Have)
   - Implement GET `/api/{user_id}/tasks/{id}`
   - Get single task details

10. **API Endpoints - User Story 6** (P3 - Nice-to-Have)
    - Implement DELETE `/api/{user_id}/tasks/{id}`
    - Delete task permanently

11. **Testing** (All Priorities)
    - Write contract tests for each endpoint
    - Write integration tests for user isolation
    - Write unit tests for service layer

### Agent Delegation Strategy

All implementation tasks will be delegated to:
- **`fastapi-backend-architect` agent**: All Python FastAPI code, SQLModel models, endpoints, middleware

### Dependencies

**Internal** (Must be complete before implementation):
- ✅ Spec 001: Better Auth implementation with JWT token issuance
- ✅ Spec 001: User model in database
- ✅ Spec 001: Neon database connection configured

**External** (Required packages):
- FastAPI 0.104+
- SQLModel 0.0.14+
- python-jose[cryptography]
- psycopg2-binary
- uvicorn
- alembic

**Environment Variables**:
```bash
# .env (backend)
DATABASE_URL=postgresql://user:pass@host/db  # Neon connection string
BETTER_AUTH_SECRET=<shared-jwt-secret>        # JWT verification key (shared with frontend)
API_HOST=0.0.0.0                              # Server host
API_PORT=8000                                 # Server port
CORS_ORIGINS=http://localhost:3000            # Allowed frontend origins
```

## Risk Analysis

### Technical Risks

1. **JWT Secret Mismatch**
   - Risk: Frontend (Better Auth) and backend use different secrets
   - Mitigation: Share BETTER_AUTH_SECRET environment variable between services
   - Contingency: Document secret synchronization in deployment guide

2. **Database Connection Pool Exhaustion**
   - Risk: High concurrent requests exhaust database connections
   - Mitigation: Configure SQLModel connection pooling (max 20 connections)
   - Contingency: Add connection timeout and retry logic

3. **User ID Type Mismatch**
   - Risk: JWT payload uses string ID, database expects integer
   - Mitigation: Explicit type conversion in `get_current_user_id`
   - Contingency: Add validation and clear error messages

4. **Timestamp Timezone Issues**
   - Risk: Inconsistent timezone handling (UTC vs local time)
   - Mitigation: Force UTC everywhere (`datetime.utcnow()`)
   - Contingency: Add timezone conversion utilities if needed

### Implementation Risks

1. **Incomplete User Isolation**
   - Risk: Missing user_id filter in some queries exposes other users' data
   - Mitigation: Service layer enforces user_id filter on all operations
   - Contingency: Integration tests verify isolation across all endpoints

2. **Migration Failures**
   - Risk: Alembic migration fails on production database
   - Mitigation: Test migrations on staging Neon branch first
   - Contingency: Keep rollback migration ready

## Success Criteria

Implementation will be considered complete when:

1. ✅ All functional requirements (FR-001 through FR-020) are implemented
2. ✅ All user stories (P1, P2, P3) pass acceptance scenarios
3. ✅ OpenAPI documentation accessible at `/docs` with all 6 endpoints
4. ✅ JWT verification works correctly (valid tokens accepted, invalid rejected)
5. ✅ User isolation verified (users cannot access other users' tasks)
6. ✅ Database migrations run successfully on Neon PostgreSQL
7. ✅ List endpoint returns results in < 200ms for 1000 tasks
8. ✅ CRUD operations complete in < 100ms
9. ✅ All endpoints return correct HTTP status codes
10. ✅ No SQL injection vulnerabilities (verified by using SQLModel ORM)

## Next Steps

1. ✅ Complete this plan document
2. ✅ Verify Phase 0 research is complete (`research.md`)
3. ✅ Verify Phase 1 design is complete (`data-model.md`, `contracts/`, `quickstart.md`)
4. Run `/sp.tasks` to generate actionable task breakdown → `tasks.md`
5. Run `/sp.implement` to execute tasks via `fastapi-backend-architect` agent
6. Run `/sp.git.commit_pr` to commit changes and create pull request
7. Consider ADR for JWT verification strategy (if significant)

# Implementation Plan: Authentication and Database Foundation

**Branch**: `001-auth-db-foundation` | **Date**: 2026-02-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/mnt/c/Users/HP/specs/001-auth-db-foundation/spec.md`

## Summary

Establish the monorepo infrastructure, database connectivity, and JWT-based authentication bridge between Next.js frontend and FastAPI backend. This foundational feature enables user registration, sign-in with JWT token issuance, backend JWT verification middleware, and Neon PostgreSQL connection with SQLModel migrations. The system will support secure, stateless authentication using Better Auth on the frontend and shared secret verification on the backend, with a health check endpoint to validate the JWT bridge.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript 5+ (frontend)
**Primary Dependencies**: FastAPI (backend), Next.js 16+ App Router (frontend), Better Auth (auth), SQLModel (ORM), Neon PostgreSQL (database)
**Storage**: Neon Serverless PostgreSQL with SQLModel ORM
**Testing**: pytest (backend), Jest/Vitest (frontend), manual API testing for JWT verification
**Target Platform**: Linux/macOS server (backend), Modern browsers (frontend)
**Project Type**: Web application (monorepo with frontend/ and backend/ directories)
**Performance Goals**:
- Registration/signin < 5 seconds
- JWT verification < 100ms per request
- Database connection < 3 seconds on startup
- Health check endpoint < 50ms response time

**Constraints**:
- No Task CRUD implementation (auth/DB foundation only)
- Minimal UI styling (functional forms, no sophisticated design)
- httpOnly cookies for JWT storage (XSS prevention)
- Shared BETTER_AUTH_SECRET between services
- PostgreSQL-specific features (Neon Serverless)

**Scale/Scope**: Foundation for multi-user todo app, designed for <1000 concurrent users initially

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Spec-Driven Development ✅
- **Status**: PASS
- **Evidence**: Specification created in `specs/001-auth-db-foundation/spec.md` with 4 user stories, 20 functional requirements, and 10 success criteria before any implementation.

### Principle II: Agentic Workflow ✅
- **Status**: PASS
- **Evidence**: Implementation will be delegated to:
  - `auth-security-specialist`: Better Auth config, JWT middleware, password hashing
  - `nextjs-ui-builder`: Signup/signin UI pages
  - `fastapi-backend-architect`: Health check endpoint, JWT verification middleware
  - `neon-db-manager`: User schema, migrations, database connection

### Principle III: Security First ✅
- **Status**: PASS
- **Evidence**:
  - JWT authentication with BETTER_AUTH_SECRET signing
  - Password hashing (bcrypt/argon2) before storage
  - httpOnly cookies prevent XSS attacks
  - JWT verification middleware on all `/api/*` endpoints
  - 401 Unauthorized responses for missing/invalid tokens
  - Environment variables for secrets (no hardcoding)

### Principle IV: Modern Stack with Strong Typing ✅
- **Status**: PASS
- **Evidence**:
  - TypeScript 5+ for all frontend code
  - Python 3.11+ with type hints for backend
  - Pydantic models for request/response validation
  - SQLModel for database models (combines Pydantic + SQLAlchemy)
  - Next.js 16+ App Router conventions

### Principle V: User Isolation ✅
- **Status**: PASS
- **Evidence**:
  - User schema includes `id` field (UUID primary key)
  - JWT contains user ID for identity extraction
  - Future task queries will filter by `user_id` (foundation established here)
  - Health check endpoint demonstrates user ID extraction from token

### Principle VI: Responsive Design ⚠️
- **Status**: DEFERRED
- **Evidence**: Minimal UI in this feature (basic signup/signin forms). Full responsive design will be implemented in future task management UI feature. Forms will use basic Tailwind CSS for mobile compatibility.

### Principle VII: Data Persistence ✅
- **Status**: PASS
- **Evidence**:
  - Neon Serverless PostgreSQL configured via DATABASE_URL
  - SQLModel User schema with proper fields (id, email, hashed_password, timestamps)
  - Migration mechanism for schema creation
  - Database connection verification on startup
  - Unique constraint on email column

**Gate Decision**: ✅ PASS with minor deferral (Principle VI responsive design will be fully addressed in task management UI feature)

## Project Structure

### Documentation (this feature)

```text
specs/001-auth-db-foundation/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification
├── research.md          # Phase 0 output (technology best practices)
├── data-model.md        # Phase 1 output (User entity schema)
├── quickstart.md        # Phase 1 output (setup instructions)
├── contracts/           # Phase 1 output (API contracts)
│   └── health-check.yaml  # /api/health endpoint OpenAPI spec
└── checklists/
    └── requirements.md  # Specification quality checklist
```

### Source Code (repository root)

```text
phase-II/
├── frontend/                       # Next.js 16+ application
│   ├── app/                        # App Router directory
│   │   ├── (auth)/                 # Route group for authentication
│   │   │   ├── signup/
│   │   │   │   └── page.tsx        # Signup page component
│   │   │   └── signin/
│   │   │       └── page.tsx        # Signin page component
│   │   ├── layout.tsx              # Root layout with Better Auth provider
│   │   └── page.tsx                # Landing/home page
│   ├── components/
│   │   ├── SignupForm.tsx          # Signup form with validation
│   │   └── SigninForm.tsx          # Signin form with validation
│   ├── lib/
│   │   └── auth.ts                 # Better Auth configuration (JWT plugin)
│   ├── public/                     # Static assets
│   ├── package.json                # Dependencies (Next.js, Better Auth, Tailwind)
│   ├── tsconfig.json               # TypeScript configuration
│   ├── tailwind.config.js          # Tailwind CSS configuration
│   └── next.config.js              # Next.js configuration (CORS, env vars)
│
├── backend/                        # FastAPI application
│   ├── src/
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── user.py             # SQLModel User schema
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── auth.py             # Pydantic request/response schemas
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── health.py           # Health check endpoint
│   │   ├── middleware/
│   │   │   ├── __init__.py
│   │   │   └── jwt_auth.py         # JWT verification middleware
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py           # Configuration (env vars)
│   │   │   └── database.py         # Database connection setup
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── auth_service.py     # Authentication business logic
│   │   └── main.py                 # FastAPI app entry point
│   ├── migrations/
│   │   └── versions/
│   │       └── 001_create_users_table.py  # Alembic migration
│   ├── tests/
│   │   ├── contract/
│   │   │   └── test_health_check.py
│   │   ├── integration/
│   │   │   └── test_jwt_verification.py
│   │   └── unit/
│   │       └── test_user_model.py
│   ├── requirements.txt            # Python dependencies
│   ├── pyproject.toml              # Project metadata and tool config
│   └── pytest.ini                  # Pytest configuration
│
├── .env.example                    # Example environment variables
├── .env                            # Environment variables (gitignored)
├── .gitignore                      # Git ignore patterns
├── docker-compose.yml              # Optional: local Neon PostgreSQL for dev
└── README.md                       # Project setup instructions
```

**Structure Decision**: Web application monorepo structure (Option 2) selected due to frontend (Next.js) + backend (FastAPI) architecture. Frontend and backend are separate services communicating via REST API with JWT authentication. Monorepo enables shared environment variables (BETTER_AUTH_SECRET) and coordinated development.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | All principles pass or deferred with justification | N/A |

**Note**: Principle VI (Responsive Design) deferred to future task management UI feature is not a violation. Current feature provides minimal functional forms that work on mobile using basic Tailwind CSS utilities.

## Phase 0: Research & Technology Best Practices

This phase is complete based on the constitution and specification requirements. Key decisions have been made:

### Better Auth JWT Configuration
- **Decision**: Use Better Auth with JWT plugin enabled
- **Rationale**: Better Auth provides modern, secure authentication with JWT support out of the box. Configurable token expiration and automatic httpOnly cookie handling.
- **Alternatives Considered**:
  - NextAuth.js: More established but heavier, session-based by default
  - Custom JWT implementation: More control but higher security risk
- **Best Practices**:
  - Store BETTER_AUTH_SECRET in environment variable
  - Configure JWT expiration to 24 hours (adjustable)
  - Use httpOnly cookies to prevent XSS attacks
  - Include user ID and email in JWT payload

### FastAPI JWT Verification Middleware
- **Decision**: Implement custom middleware using PyJWT library
- **Rationale**: Lightweight, standard JWT verification with shared secret. Integrates cleanly with FastAPI dependency injection.
- **Alternatives Considered**:
  - FastAPI-Users: Full-featured but unnecessary for simple JWT verification
  - Authlib: More comprehensive but adds complexity
- **Best Practices**:
  - Extract JWT from Authorization header (Bearer token)
  - Verify signature using BETTER_AUTH_SECRET
  - Decode user ID and email from payload
  - Inject authenticated user into request context
  - Return 401 for missing/invalid tokens
  - Log verification failures for security monitoring

### Neon PostgreSQL with SQLModel
- **Decision**: Use Neon Serverless PostgreSQL with SQLModel ORM
- **Rationale**: Neon provides serverless PostgreSQL with automatic scaling, branching, and backups. SQLModel combines Pydantic validation with SQLAlchemy ORM for type-safe database operations.
- **Alternatives Considered**:
  - SQLAlchemy alone: More verbose, loses Pydantic validation benefits
  - Raw SQL: More control but higher risk, no type safety
  - Prisma: TypeScript-focused, doesn't integrate with Python backend
- **Best Practices**:
  - Use connection pooling (asyncpg driver for async support)
  - Define schema with SQLModel classes (type hints)
  - Use Alembic for migrations (version control schema changes)
  - Create indexes on email and id columns
  - Enable foreign key constraints
  - Use UUID for primary keys (better distribution than sequential IDs)

### Password Hashing
- **Decision**: Use bcrypt with cost factor 10
- **Rationale**: Industry standard, well-vetted, configurable cost factor balances security and performance.
- **Alternatives Considered**:
  - Argon2: More modern, slightly slower but more secure against GPU attacks
  - PBKDF2: Older standard, less resistant to brute force
- **Best Practices**:
  - Never store plain-text passwords
  - Hash on registration before database insert
  - Verify on signin by comparing hash
  - Use bcrypt library with salt generation
  - Cost factor 10 provides ~100ms hashing time (acceptable UX)

### CORS Configuration
- **Decision**: Configure FastAPI CORS middleware to allow Next.js frontend origin
- **Rationale**: Frontend and backend run on different ports (localhost:3000 and localhost:8000), requiring CORS headers.
- **Best Practices**:
  - Allow specific origin (http://localhost:3000 in dev)
  - Allow credentials (for httpOnly cookies)
  - Allow Authorization header
  - Restrict allowed methods to actual API methods (GET, POST, PUT, DELETE, PATCH)

## Phase 1: Data Models & API Contracts

### Data Model

See [data-model.md](./data-model.md) for complete entity definitions.

**User Entity**:
- `id`: UUID (primary key, auto-generated)
- `email`: String (unique, not null, max 255 characters)
- `hashed_password`: String (not null, bcrypt hash)
- `created_at`: Timestamp (auto-generated on insert)
- `updated_at`: Timestamp (auto-updated on modification)

**Constraints**:
- Unique index on `email`
- Primary key index on `id`
- No foreign keys in this feature (will add Task entity with `user_id` foreign key in future feature)

### API Contracts

See [contracts/](./contracts/) for OpenAPI specifications.

**Health Check Endpoint**: `/api/health`
- **Method**: GET
- **Authentication**: Required (JWT Bearer token)
- **Request Headers**:
  - `Authorization: Bearer <jwt_token>` (required)
- **Responses**:
  - **200 OK** (valid JWT):
    ```json
    {
      "status": "healthy",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "user@example.com"
    }
    ```
  - **401 Unauthorized** (missing token):
    ```json
    {
      "detail": "Missing authentication token"
    }
    ```
  - **401 Unauthorized** (invalid/expired token):
    ```json
    {
      "detail": "Invalid or expired token"
    }
    ```

### Quickstart

See [quickstart.md](./quickstart.md) for complete setup instructions.

**Summary**:
1. Clone repository and checkout `001-auth-db-foundation` branch
2. Set up environment variables in `.env`:
   - `DATABASE_URL`: Neon PostgreSQL connection string
   - `BETTER_AUTH_SECRET`: Shared secret for JWT signing/verification
3. Backend setup:
   - Create Python virtual environment
   - Install dependencies (`pip install -r backend/requirements.txt`)
   - Run migrations (`alembic upgrade head`)
   - Start server (`uvicorn src.main:app --reload`)
4. Frontend setup:
   - Install dependencies (`npm install` in frontend/)
   - Configure Better Auth with BETTER_AUTH_SECRET
   - Start development server (`npm run dev`)
5. Test authentication flow:
   - Visit signup page, create account
   - Sign in with credentials
   - Access health check endpoint with JWT token

## Next Steps

This plan will be followed by:
1. **Phase 2: Task Generation** (`/sp.tasks`) - Break down this plan into actionable, ordered tasks
2. **Phase 3: Implementation** (`/sp.implement`) - Execute tasks via specialized agents
3. **Phase 4: Testing & Validation** - Verify all acceptance scenarios pass
4. **Phase 5: Documentation** - Complete README and quickstart guide
5. **Phase 6: Commit & PR** (`/sp.git.commit_pr`) - Create pull request for review

**Implementation Sequence**:
1. Monorepo initialization (frontend/, backend/, .env setup)
2. Database foundation (Neon connection, SQLModel User schema, migrations)
3. Backend JWT middleware (verification, 401 responses)
4. Health check endpoint (demonstrates JWT bridge)
5. Better Auth configuration (JWT plugin, httpOnly cookies)
6. Signup/signin UI (minimal forms, validation)
7. End-to-end testing (registration → signin → health check with JWT)

**Critical Path**:
- Database connection must work before migrations
- User schema migration must complete before registration
- JWT middleware must be implemented before health check endpoint
- Better Auth config must be complete before signup/signin pages
- All components must integrate for end-to-end test

**Agent Assignments**:
- `neon-db-manager`: Database connection, User schema, migrations
- `fastapi-backend-architect`: JWT middleware, health check endpoint, CORS config
- `auth-security-specialist`: Password hashing, Better Auth config, JWT signing
- `nextjs-ui-builder`: Signup/signin pages, Better Auth UI integration

**Estimated Complexity**: Medium (foundational infrastructure, multiple moving parts, cross-service integration)

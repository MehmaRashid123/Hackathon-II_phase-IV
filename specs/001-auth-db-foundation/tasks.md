# Tasks: Foundation & Secure Authentication

**Input**: Design documents from `/specs/001-auth-db-foundation/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Tests**: Not explicitly requested - focusing on implementation tasks only.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Monorepo structure**: `backend/` (FastAPI) and `frontend/` (Next.js)
- All paths relative to repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize monorepo structure and configure foundational tooling

- [X] T001 Create monorepo directory structure with `backend/` and `frontend/` at repository root
- [X] T002 [P] Initialize FastAPI project in `backend/` with Python 3.11+ and create `backend/requirements.txt`
- [X] T003 [P] Initialize Next.js 16+ project in `frontend/` with TypeScript and Tailwind CSS
- [X] T004 [P] Create environment configuration template `backend/.env.example` with DATABASE_URL, BETTER_AUTH_SECRET, CORS_ORIGINS
- [X] T005 [P] Create environment configuration template `frontend/.env.local.example` with NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core database and authentication infrastructure that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Foundation

- [X] T006 Install and configure SQLModel in `backend/requirements.txt` (version 0.0.14+)
- [X] T007 Create database configuration in `backend/src/database.py` with Neon PostgreSQL connection using DATABASE_URL from environment
- [X] T008 Configure SQLModel engine with connection pooling (max 20 connections) in `backend/src/database.py`
- [X] T009 Create database session dependency for FastAPI in `backend/src/database.py`
- [X] T010 Initialize Alembic for database migrations in `backend/alembic/` directory

### Authentication Infrastructure

- [X] T011 Install Better Auth in `frontend/` (npm install better-auth)
- [X] T012 Install python-jose[cryptography] in `backend/requirements.txt` for JWT verification
- [X] T013 [P] Create FastAPI configuration in `backend/src/config.py` to load environment variables (DATABASE_URL, BETTER_AUTH_SECRET, CORS_ORIGINS)
- [X] T014 [P] Configure CORS middleware in `backend/src/main.py` to allow frontend origin

### Base Project Structure

- [X] T015 [P] Create directory structure: `backend/src/models/`, `backend/src/schemas/`, `backend/src/api/`, `backend/src/middleware/`
- [X] T016 [P] Create FastAPI app instance in `backend/src/main.py` with title, version, and OpenAPI docs

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 4 - Database Connection and Migrations (Priority: P1) 🎯 MVP Foundation

**Goal**: Establish Neon PostgreSQL connection and create User table schema via migrations

**Independent Test**: Run `alembic upgrade head` → Verify users table exists in Neon → Connect to database successfully

### Implementation for User Story 4

- [X] T017 [P] [US4] Create User model in `backend/src/models/user.py` with SQLModel (id, email, hashed_password, created_at)
- [X] T018 [US4] Add unique constraint and index on email column in User model
- [X] T019 [US4] Generate Alembic migration for User table: `alembic revision --autogenerate -m "create users table"`
- [X] T020 [US4] Review generated migration in `backend/alembic/versions/` and verify schema correctness
- [X] T021 [US4] Apply migration to Neon database: `alembic upgrade head`
- [X] T022 [US4] Verify User table exists in Neon PostgreSQL database using database client or query
- [X] T023 [US4] Test database connection by creating a test query in FastAPI startup event

**Checkpoint**: Database schema ready - user authentication features can now be implemented

---

## Phase 4: User Story 1 - User Registration (Priority: P1)

**Goal**: Enable new users to create accounts with email and password

**Independent Test**: POST `/api/auth/signup` with email and password → Verify 201 response → Check user exists in database

### Implementation for User Story 1

- [X] T024 [P] [US1] Create Pydantic schema `UserCreate` in `backend/src/schemas/auth_schemas.py` (email: EmailStr, password: str with min 8 chars)
- [X] T025 [P] [US1] Create Pydantic schema `UserResponse` in `backend/src/schemas/auth_schemas.py` (id, email, created_at)
- [X] T026 [P] [US1] Install passlib[bcrypt] in `backend/requirements.txt` for password hashing
- [X] T027 [US1] Create password hashing utility in `backend/src/utils/security.py` (hash_password, verify_password functions using bcrypt)
- [X] T028 [US1] Create UserService in `backend/src/services/user_service.py` with create_user method (check email uniqueness, hash password, save to DB)
- [X] T029 [US1] Implement POST `/api/auth/signup` endpoint in `backend/src/api/auth.py` that calls UserService.create_user
- [X] T030 [US1] Add email validation to prevent duplicate registrations (return HTTP 400 if email exists)
- [X] T031 [US1] Add password strength validation (min 8 characters, at least one letter and number)
- [X] T032 [US1] Return UserResponse with HTTP 201 status on successful registration

**Checkpoint**: Users can register - next implement signin with JWT tokens

---

## Phase 5: User Story 2 - User Sign-In with JWT Issuance (Priority: P1)

**Goal**: Authenticated users receive JWT tokens to access protected resources

**Independent Test**: POST `/api/auth/signin` with valid credentials → Receive JWT token → Decode token and verify claims

### Implementation for User Story 2

- [X] T033 [P] [US2] Configure Better Auth in `frontend/lib/auth.ts` with email/password provider
- [X] T034 [P] [US2] Create JWT token generation utility in `backend/src/utils/security.py` (create_access_token function using python-jose)
- [X] T035 [US2] Configure JWT settings in `backend/src/config.py` (SECRET_KEY from BETTER_AUTH_SECRET, ALGORITHM="HS256", TOKEN_EXPIRE_MINUTES=60)
- [X] T036 [US2] Create Pydantic schema `UserSignIn` in `backend/src/schemas/auth_schemas.py` (email, password)
- [X] T037 [US2] Create Pydantic schema `TokenResponse` in `backend/src/schemas/auth_schemas.py` (access_token, token_type="bearer")
- [X] T038 [US2] Implement authenticate_user method in `backend/src/services/user_service.py` (find user by email, verify password)
- [X] T039 [US2] Implement POST `/api/auth/signin` endpoint in `backend/src/api/auth.py` that authenticates and returns JWT token
- [X] T040 [US2] Add error handling for invalid credentials (return HTTP 401 Unauthorized)
- [X] T041 [US2] Include user ID and email in JWT token payload (sub: user_id, email: user_email)
- [X] T042 [US2] Set JWT token expiration to 60 minutes
- [X] T043 [US2] Create Better Auth configuration in `frontend/lib/auth.ts` to use backend JWT tokens
- [X] T044 [US2] Create login page in `frontend/app/(auth)/login/page.tsx` with email/password form
- [X] T045 [US2] Create signup page in `frontend/app/(auth)/signup/page.tsx` with email/password form

**Checkpoint**: Users can register and sign in - JWT tokens issued successfully

---

## Phase 6: User Story 3 - Backend JWT Verification (Priority: P1)

**Goal**: Protect backend endpoints by verifying JWT tokens on every request

**Independent Test**: Call protected endpoint with valid JWT → Access granted (200) → Call with invalid/missing JWT → Access denied (401)

### Implementation for User Story 3

- [X] T046 [P] [US3] Create JWT verification dependency in `backend/src/middleware/auth.py` (verify_token function using python-jose)
- [X] T047 [US3] Implement get_current_user dependency in `backend/src/middleware/auth.py` that extracts user from JWT token
- [X] T048 [US3] Add HTTPBearer security scheme to FastAPI in `backend/src/middleware/auth.py`
- [X] T049 [US3] Implement token expiration check in verify_token function (raise HTTP 401 if expired)
- [X] T050 [US3] Implement token signature validation in verify_token function (raise HTTP 401 if invalid)
- [X] T051 [US3] Extract user_id from JWT "sub" claim in get_current_user dependency
- [X] T052 [US3] Create test protected endpoint GET `/api/auth/me` in `backend/src/api/auth.py` that returns current user info
- [X] T053 [US3] Apply get_current_user dependency to `/api/auth/me` endpoint to test JWT verification
- [X] T054 [US3] Test JWT verification with valid token (should return user info with HTTP 200)
- [ ] T055 [US3] Test JWT verification with expired token (should return HTTP 401 Unauthorized)
- [ ] T056 [US3] Test JWT verification with invalid signature (should return HTTP 401 Unauthorized)
- [ ] T057 [US3] Test JWT verification with missing Authorization header (should return HTTP 401 Unauthorized)

**Checkpoint**: All P1 user stories complete - authentication system fully functional

---

## Phase 7: Polish & Integration

**Purpose**: Final touches, documentation, and end-to-end validation

### Integration Testing

- [ ] T058 [P] Manual test: Register new user via signup endpoint → Verify user created in database
- [ ] T059 [P] Manual test: Sign in with registered user → Verify JWT token received
- [ ] T060 [P] Manual test: Call protected endpoint with JWT → Verify access granted
- [ ] T061 [P] Manual test: Call protected endpoint without JWT → Verify HTTP 401 returned
- [ ] T062 Manual test: Test full flow - signup → signin → access protected resource

### Documentation & Developer Experience

- [ ] T063 [P] Add API documentation in `backend/src/main.py` OpenAPI description
- [ ] T064 [P] Document environment variables in `backend/README.md`
- [ ] T065 [P] Create quickstart guide in `backend/QUICKSTART.md` with setup steps
- [ ] T066 [P] Add example requests/responses to API docs using FastAPI examples parameter

### Error Handling

- [ ] T067 [P] Add global exception handler in `backend/src/main.py` for consistent error responses
- [ ] T068 [P] Add validation error handler for Pydantic validation failures
- [ ] T069 [P] Add database connection error handler (return HTTP 503 if database unavailable)

### Security Hardening

- [ ] T070 [P] Verify BETTER_AUTH_SECRET is strong (minimum 32 characters) in configuration
- [ ] T071 [P] Ensure password hashing uses bcrypt with appropriate cost factor (12 rounds minimum)
- [ ] T072 [P] Verify CORS configuration only allows intended frontend origin
- [ ] T073 [P] Add rate limiting to authentication endpoints (optional, for production)

---

## Dependencies & Execution Strategy

### User Story Dependencies

**Sequential Dependencies** (must complete in order):
1. Phase 1: Setup (BLOCKING - foundation)
2. Phase 2: Foundational (BLOCKING - database and auth infrastructure)
3. Phase 3: US4 (Database Connection) - BLOCKING for US1, US2, US3
4. Phase 4: US1 (Registration) - Independent after US4
5. Phase 5: US2 (Sign-In) - Depends on US1 (needs registered users)
6. Phase 6: US3 (JWT Verification) - Depends on US2 (needs JWT tokens)
7. Phase 7: Polish - After all user stories

**Parallel Opportunities**:
- After US4 complete: US1 can be implemented
- After US1 complete: US2 can be implemented  
- After US2 complete: US3 can be implemented

### Parallel Execution Opportunities

**Within Setup (Phase 1)**:
- T002, T003, T004, T005 can run in parallel (different projects)

**Within Foundation (Phase 2)**:
- T013, T014, T015, T016 can run in parallel (different concerns)

**Within User Story 1 (Phase 4)**:
- T024, T025, T026 can run in parallel (schemas and dependencies)

**Within User Story 2 (Phase 5)**:
- T033, T034, T036, T037 can run in parallel (frontend and backend schemas)

**Within User Story 3 (Phase 6)**:
- T046, T047, T048 can run in parallel (different middleware functions)

**Within Polish (Phase 7)**:
- T058-T073 can mostly run in parallel (testing, docs, error handling are independent)

### MVP Scope (Minimum Viable Product)

**Suggested MVP**: Phase 1 + Phase 2 + Phase 3 (US4 only)

This delivers:
- ✅ Monorepo structure set up
- ✅ Database connection to Neon PostgreSQL
- ✅ User table schema migrated
- ✅ Foundation ready for authentication features

**Next increment**: Add Phase 4 (US1 - Registration)
**Next increment**: Add Phase 5 (US2 - Sign-In with JWT)
**Next increment**: Add Phase 6 (US3 - JWT Verification)
**Full feature**: Complete all phases including Polish

---

## Task Summary

**Total Tasks**: 73
- Setup (Phase 1): 5 tasks
- Foundation (Phase 2): 11 tasks (BLOCKING)
- User Story 4 - Database (Phase 3): 7 tasks
- User Story 1 - Registration (Phase 4): 9 tasks
- User Story 2 - Sign-In (Phase 5): 13 tasks
- User Story 3 - JWT Verification (Phase 6): 12 tasks
- Polish (Phase 7): 16 tasks

**Parallel Opportunities**: 32 tasks marked with [P] can run in parallel

**Agent Delegation**:
- Backend tasks → `fastapi-backend-architect` agent
- Frontend tasks → `nextjs-ui-builder` agent  
- Database tasks → `neon-db-manager` agent
- Auth tasks → `auth-security-specialist` agent

**Estimated Completion**:
- MVP (US4 only): 23 tasks (Setup + Foundation + US4)
- With Registration (US1): 32 tasks
- With Sign-In (US2): 45 tasks
- With JWT Verification (US3): 57 tasks
- Full Feature with Polish: 73 tasks

---

## Implementation Notes

### File Organization

**Backend Structure**:
```
backend/
├── src/
│   ├── models/user.py          # SQLModel User entity
│   ├── schemas/auth_schemas.py # Pydantic request/response models
│   ├── api/auth.py             # Auth endpoints (signup, signin, me)
│   ├── services/user_service.py # User business logic
│   ├── middleware/auth.py      # JWT verification dependencies
│   ├── utils/security.py       # Password hashing, JWT utilities
│   ├── database.py             # Database connection
│   ├── config.py               # Environment configuration
│   └── main.py                 # FastAPI app entry point
├── alembic/                    # Database migrations
│   └── versions/
└── requirements.txt
```

**Frontend Structure**:
```
frontend/
├── app/
│   └── (auth)/
│       ├── login/page.tsx      # Login form
│       └── signup/page.tsx     # Signup form
└── lib/
    └── auth.ts                 # Better Auth configuration
```

### Key Dependencies

**Backend**:
- FastAPI 0.104+
- SQLModel 0.0.14+
- python-jose[cryptography]
- passlib[bcrypt]
- psycopg2-binary
- alembic
- uvicorn

**Frontend**:
- Next.js 16+
- Better Auth
- TypeScript 5+
- Tailwind CSS 3+

### Environment Variables

**Backend** (`.env`):
```bash
DATABASE_URL=postgresql://user:pass@host/db
BETTER_AUTH_SECRET=<32-char-secret>
CORS_ORIGINS=http://localhost:3000
API_HOST=0.0.0.0
API_PORT=8000
```

**Frontend** (`.env.local`):
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=<same-32-char-secret>
```

### Testing Strategy

**Manual Testing Checklist**:
1. Database migration runs successfully
2. User registration creates record in database
3. Password is hashed (not stored in plaintext)
4. Sign-in with valid credentials returns JWT
5. Sign-in with invalid credentials returns 401
6. Protected endpoint accepts valid JWT
7. Protected endpoint rejects invalid/missing JWT
8. JWT token expires after configured time

### Security Checklist

- [ ] Passwords hashed with bcrypt (cost factor >= 12)
- [ ] JWT secret is strong (32+ characters)
- [ ] CORS configured to allow only trusted origins
- [ ] SQL injection prevented (using SQLModel ORM)
- [ ] Email validation prevents duplicate registrations
- [ ] JWT tokens have expiration time
- [ ] Sensitive data not logged or exposed in errors

---

## Next Steps

1. ✅ Review this task list for completeness
2. Run `/sp.implement` to begin execution via specialized agents
3. Execute tasks in phase order (Setup → Foundation → User Stories → Polish)
4. Mark tasks complete as you progress
5. Test each user story checkpoint independently
6. Create pull request after all tasks complete

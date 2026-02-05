---
id: 002
title: Create Auth DB Foundation Plan
stage: plan
date: 2026-02-05
surface: agent
model: claude-sonnet-4-5
feature: 001-auth-db-foundation
branch: 001-auth-db-foundation
user: mehma
command: /sp.plan
labels: ["planning", "architecture", "authentication", "database", "jwt", "monorepo", "fastapi", "nextjs"]
links:
  spec: /mnt/c/Users/HP/specs/001-auth-db-foundation/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - /mnt/c/Users/HP/specs/001-auth-db-foundation/plan.md
  - /mnt/c/Users/HP/specs/001-auth-db-foundation/data-model.md
  - /mnt/c/Users/HP/specs/001-auth-db-foundation/quickstart.md
  - /mnt/c/Users/HP/specs/001-auth-db-foundation/research.md
  - /mnt/c/Users/HP/specs/001-auth-db-foundation/contracts/health-check.yaml
tests:
  - none
---

## Prompt

Based on the accepted /sp.specify for Foundation & Secure Authentication:
1. Initialize the monorepo structure.
2. Set up the Python virtual environment and Next.js boilerplate.
3. Configure the Neon PostgreSQL connection string and SQLModel base setup.
4. Implement the Better Auth configuration on the Frontend with the JWT plugin enabled.
5. Create the JWT verification middleware in FastAPI using the `BETTER_AUTH_SECRET`.
6. Create a protected "Auth Test" endpoint (`/api/auth-verify`) to prove the JWT bridge works.
7. Verify that the User ID is correctly decoded from the token on the backend.

Please provide a step-by-step task list to implement this.

## Response snapshot

Created comprehensive implementation plan for authentication and database foundation feature.

**Constitution Check Results**: ✅ PASSED
- Principle I (Spec-Driven): PASS - Spec created before implementation
- Principle II (Agentic Workflow): PASS - Agents assigned (auth-security-specialist, nextjs-ui-builder, fastapi-backend-architect, neon-db-manager)
- Principle III (Security First): PASS - JWT auth, password hashing, httpOnly cookies, 401 responses
- Principle IV (Modern Stack): PASS - TypeScript 5+, Python 3.11+, Next.js 16+, FastAPI, Pydantic, SQLModel
- Principle V (User Isolation): PASS - User schema with UUID, JWT contains user ID
- Principle VI (Responsive Design): DEFERRED - Minimal UI in foundation, full responsive design in task management feature
- Principle VII (Data Persistence): PASS - Neon PostgreSQL, SQLModel, migrations

**Technical Context Defined**:
- Languages: Python 3.11+ (backend), TypeScript 5+ (frontend)
- Dependencies: FastAPI, Next.js 16+, Better Auth, SQLModel, Neon PostgreSQL
- Performance Goals: Registration/signin < 5s, JWT verification < 100ms, DB connection < 3s
- Constraints: Auth/DB only (no Task CRUD), minimal UI, httpOnly cookies, shared BETTER_AUTH_SECRET
- Scale: <1000 concurrent users initially

**Project Structure Defined**:
- Monorepo: `frontend/` (Next.js) + `backend/` (FastAPI)
- Frontend: App Router structure with (auth) route group, Better Auth config, Tailwind CSS
- Backend: src/ with models/, schemas/, api/, middleware/, core/, services/, migrations/

**Phase 0: Research Completed**:
- Better Auth with JWT plugin (modern, lightweight, JWT-first)
- FastAPI JWT middleware with PyJWT (standard, integrates with FastAPI)
- SQLModel with Neon PostgreSQL (type-safe, Pydantic integration)
- bcrypt password hashing (cost factor 10, ~100ms)
- CORS configuration (allow localhost:3000, credentials enabled)

**Phase 1: Design Artifacts Created**:
1. **data-model.md**: User entity schema (id UUID, email unique, hashed_password, timestamps)
2. **quickstart.md**: Complete setup instructions (Neon setup, backend venv, frontend npm, testing)
3. **contracts/health-check.yaml**: OpenAPI spec for /api/health endpoint (200 with user ID, 401 without token)

**Agent Assignments**:
- `neon-db-manager`: Database connection, User schema, migrations
- `fastapi-backend-architect`: JWT middleware, health check endpoint, CORS
- `auth-security-specialist`: Password hashing, Better Auth config, JWT signing
- `nextjs-ui-builder`: Signup/signin pages, Better Auth UI integration

**Implementation Sequence**:
1. Monorepo init (frontend/, backend/, .env)
2. Database foundation (Neon connection, User schema, migrations)
3. Backend JWT middleware (verification, 401 responses)
4. Health check endpoint (JWT bridge test)
5. Better Auth config (JWT plugin, httpOnly cookies)
6. Signup/signin UI (minimal forms, validation)
7. End-to-end testing (registration → signin → health check)

**Critical Path**:
- DB connection → migrations → registration
- JWT middleware → health check endpoint
- Better Auth config → signup/signin pages
- All components → end-to-end integration test

## Outcome

- ✅ Impact: Complete architectural plan created for authentication and database foundation. Defines monorepo structure, technology stack, data models, API contracts, and implementation sequence. Passes all constitutional checks except deferred responsive design (addressed in future feature).
- 🧪 Tests: N/A (planning document)
- 📁 Files: plan.md, data-model.md, quickstart.md, research.md, contracts/health-check.yaml
- 🔁 Next prompts: Run `/sp.tasks` to break down plan into actionable, ordered implementation tasks
- 🧠 Reflection: Plan successfully bridges spec (what) to implementation (how) while maintaining technology details separate from business requirements. All technical unknowns resolved via research phase. Agent delegation ensures specialized expertise for each component. Constitution compliance validated with minor responsive design deferral justified.

## Evaluation notes (flywheel)

- Failure modes observed: None. All plan sections completed, constitution gates passed, Phase 0 research and Phase 1 design artifacts generated.
- Graders run and results (PASS/FAIL): PASS - Constitution check validated all 7 principles. Technical context complete. Project structure defined with concrete directory layout. Research decisions documented with alternatives considered. Data model, quickstart, and API contracts created.
- Prompt variant (if applicable): Standard planning workflow with constitution check
- Next experiment (smallest change to try): Execute `/sp.tasks` to validate how well the plan translates into actionable, dependency-ordered tasks that agents can implement independently

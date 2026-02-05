<!--
SYNC IMPACT REPORT
==================
Version Change: 0.0.0 → 1.0.0 (INITIAL)
Rationale: Initial constitution for Hackathon Phase II - Full-Stack Todo Web Application

Modified Principles:
- N/A (new constitution)

Added Sections:
- Core Principles (7 principles)
- Technology Stack Standards
- Development Workflow
- Governance

Removed Sections:
- N/A (new constitution)

Templates Requiring Updates:
- ✅ plan-template.md: Constitution Check section will reference these principles
- ✅ spec-template.md: Requirements must align with tech stack and security constraints
- ✅ tasks-template.md: Task categories reflect agentic workflow and security principles

Follow-up TODOs:
- None (all placeholders filled)

Date: 2026-02-05
-->

# Hackathon Phase II - Full-Stack Todo Web Application Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

Implementation MUST strictly follow written specifications. No manual coding is permitted outside the defined spec → plan → tasks → implement workflow.

**Rules:**
- Every feature MUST have a specification in `specs/<feature>/spec.md` before implementation begins
- Every implementation MUST have an architectural plan in `specs/<feature>/plan.md`
- Every plan MUST be broken down into actionable tasks in `specs/<feature>/tasks.md`
- Code changes without corresponding spec/plan/task documentation are prohibited
- All work MUST be trackable through the spec-driven artifact chain

**Rationale:** Ensures predictable, reviewable, and traceable development process that can be validated at every stage. Eliminates ad-hoc changes that bypass architectural review.

### II. Agentic Workflow (NON-NEGOTIABLE)

All implementation work MUST be delegated to specialized agents. Direct manual coding is prohibited.

**Agent Delegation Rules:**
- **Authentication tasks** → `auth-security-specialist` agent (Better Auth, JWT, password hashing, session management)
- **Frontend tasks** → `nextjs-ui-builder` agent (Next.js pages, React components, responsive UI)
- **Backend API tasks** → `fastapi-backend-architect` agent (FastAPI routes, Pydantic models, middleware)
- **Database tasks** → `neon-db-manager` agent (Schema design, migrations, SQLModel, queries)
- **Cross-stack coordination** → `spec-driven-architect` agent (Feature planning, task orchestration)

**Rationale:** Leverages specialized expertise for each technology domain, ensures consistency in patterns, and maintains separation of concerns. Agents enforce best practices specific to their domain.

### III. Security First

Client-server separation MUST be strict, with stateless JWT authentication enforcing user isolation.

**Security Requirements:**
- All API endpoints under `/api/` MUST require `Authorization: Bearer <token>` header
- JWT tokens MUST be issued by Better Auth on successful login
- FastAPI backend MUST verify JWT signature using shared secret (`BETTER_AUTH_SECRET`)
- User ID in request URL MUST match authenticated user ID from JWT token
- Database queries MUST filter by authenticated user ID - no cross-user data access
- Secrets and tokens MUST be stored in `.env` files, never hardcoded
- CORS configuration MUST explicitly allow only the Next.js frontend origin
- Password hashing MUST use industry-standard algorithms (bcrypt/argon2)

**Rationale:** Prevents unauthorized access, data leakage between users, and common web vulnerabilities (injection, XSS, CSRF). Stateless JWT enables horizontal scaling.

### IV. Modern Stack with Strong Typing

Utilize Next.js 16+ with App Router and Python FastAPI with comprehensive type validation.

**Frontend Standards:**
- TypeScript MUST be used for all frontend code
- Next.js App Router conventions MUST be followed (app directory, server/client components)
- React Server Components MUST be preferred where applicable
- Client-side state management MUST be minimal and explicit

**Backend Standards:**
- Python 3.11+ MUST be used
- All request/response models MUST use Pydantic for validation
- All database models MUST use SQLModel for ORM and validation
- Type hints MUST be provided for all function signatures
- FastAPI automatic OpenAPI documentation MUST be accessible

**Rationale:** Strong typing catches errors at development time, provides IDE autocomplete, generates automatic documentation, and reduces runtime failures.

### V. User Isolation (NON-NEGOTIABLE)

Data access MUST be strictly filtered by authenticated user ID at the database query level.

**Isolation Rules:**
- Every task record MUST have a `user_id` foreign key to the users table
- Database queries MUST include `WHERE user_id = <authenticated_user_id>` filter
- API endpoints MUST validate that `{user_id}` path parameter matches JWT token user ID
- Unauthorized access attempts MUST return HTTP 403 Forbidden
- Unit and integration tests MUST verify user isolation

**Rationale:** Prevents data leakage, ensures privacy, and is a fundamental security requirement for multi-user applications. Violating this principle risks exposing sensitive user data.

### VI. Responsive Design

Mobile-first UI MUST work seamlessly on all device sizes using Tailwind CSS.

**Design Requirements:**
- Mobile breakpoint (< 640px) MUST be the primary design target
- Tablet (640px - 1024px) and desktop (> 1024px) MUST progressively enhance
- Touch targets MUST be minimum 44x44px for mobile accessibility
- Tailwind CSS utility classes MUST be used for responsive styling
- No horizontal scrolling on any viewport size
- Loading states and error messages MUST be user-friendly and visible

**Rationale:** Majority of users access web applications on mobile devices. Mobile-first ensures core functionality works on constrained devices, with enhancement for larger screens.

### VII. Data Persistence

All user data MUST be stored in Neon Serverless PostgreSQL with proper schema design.

**Persistence Requirements:**
- Neon connection string MUST be stored in `DATABASE_URL` environment variable
- SQLModel MUST be used for all database models and queries
- Database migrations MUST be versioned and reversible
- Foreign key relationships MUST enforce referential integrity
- Indexes MUST be created on frequently queried columns (`user_id`, `created_at`)
- Connection pooling MUST be configured for performance
- Database transactions MUST be used for multi-step operations

**Rationale:** Neon provides serverless PostgreSQL with automatic scaling, backups, and branching for development. Proper schema design ensures data integrity and query performance.

## Technology Stack Standards

**Mandatory Stack Components:**

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Frontend Framework | Next.js (App Router) | 16+ | Server-side rendering, routing, React framework |
| Backend Framework | FastAPI | Latest | RESTful API, async support, automatic docs |
| ORM | SQLModel | Latest | Type-safe database models, Pydantic integration |
| Database | Neon Serverless PostgreSQL | Latest | Persistent storage, serverless scalability |
| Authentication | Better Auth | Latest | User signup/signin, JWT token issuance |
| Styling | Tailwind CSS | Latest | Responsive utility-first CSS |
| Language (Frontend) | TypeScript | 5+ | Type safety for frontend code |
| Language (Backend) | Python | 3.11+ | Type hints, performance, async support |

**Prohibited:**
- Manual SQL queries without SQLModel (except for complex optimizations with justification)
- Session-based authentication (JWT only)
- Client-side only routing (must use Next.js App Router)
- Untyped JavaScript (TypeScript required)
- Storing sensitive data in localStorage (use secure httpOnly cookies for tokens)

## Development Workflow

**Mandatory Workflow Stages:**

1. **Specification (`/sp.specify`)**
   - Create `specs/<feature>/spec.md` with user stories, acceptance criteria, functional requirements
   - Prioritize user stories (P1, P2, P3) for incremental delivery
   - Define success criteria and edge cases

2. **Planning (`/sp.plan`)**
   - Generate `specs/<feature>/plan.md` with architectural decisions
   - Document technical context, dependencies, and constraints
   - Create constitution check to verify compliance
   - Define project structure (monorepo: `frontend/`, `backend/`)
   - Document data models, API contracts, and integration points

3. **Task Breakdown (`/sp.tasks`)**
   - Generate `specs/<feature>/tasks.md` with actionable, ordered tasks
   - Organize tasks by user story for independent implementation
   - Mark parallel tasks with `[P]` prefix
   - Include exact file paths and dependencies

4. **Implementation (`/sp.implement`)**
   - Execute tasks via specialized agents (auth, frontend, backend, database)
   - Create Prompt History Records (PHRs) for all work in `history/prompts/`
   - Commit after each logical task or group

5. **Git Workflow (`/sp.git.commit_pr`)**
   - Commit changes with descriptive messages
   - Create pull requests with test plans
   - Link PRs to specs and tasks

6. **Architecture Decision Records (ADRs)**
   - Suggest ADRs for significant architectural decisions
   - Document in `history/adr/` with context, decision, and consequences
   - Require user consent before creating ADR

**Required API Endpoints:**

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/api/{user_id}/tasks` | List all tasks for user | Required (JWT) |
| POST | `/api/{user_id}/tasks` | Create a new task | Required (JWT) |
| GET | `/api/{user_id}/tasks/{id}` | Get task details | Required (JWT) |
| PUT | `/api/{user_id}/tasks/{id}` | Update a task | Required (JWT) |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete a task | Required (JWT) |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion status | Required (JWT) |

**Monorepo Structure:**

```
phase-II/
├── frontend/                 # Next.js 16+ application
│   ├── app/                  # App Router directory
│   │   ├── (auth)/           # Authentication routes (signup, signin)
│   │   ├── (dashboard)/      # Protected routes (task list, task form)
│   │   ├── api/              # API route handlers (optional, proxy to backend)
│   │   └── layout.tsx        # Root layout
│   ├── components/           # Reusable React components
│   ├── lib/                  # Utility functions, Better Auth config
│   └── public/               # Static assets
│
├── backend/                  # FastAPI application
│   ├── src/
│   │   ├── models/           # SQLModel database models
│   │   ├── schemas/          # Pydantic request/response schemas
│   │   ├── api/              # API route handlers
│   │   ├── middleware/       # JWT authentication middleware
│   │   ├── services/         # Business logic
│   │   └── main.py           # FastAPI app entry point
│   └── tests/
│       ├── contract/         # API contract tests
│       ├── integration/      # Integration tests
│       └── unit/             # Unit tests
│
├── .env                      # Environment variables (DATABASE_URL, JWT_SECRET)
├── specs/                    # Feature specifications
├── history/                  # PHRs and ADRs
└── .specify/                 # Spec-Kit Plus templates and scripts
```

## Governance

**Constitution Authority:**
- This constitution supersedes all other development practices and preferences
- All pull requests MUST verify compliance with constitutional principles
- Agents MUST enforce constitution rules and refuse non-compliant requests
- Complexity and deviations MUST be justified in `specs/<feature>/plan.md` Complexity Tracking table

**Amendment Process:**
1. Propose amendment with rationale and impact analysis
2. Update constitution with version bump (MAJOR for breaking changes, MINOR for additions, PATCH for clarifications)
3. Synchronize all dependent templates (spec, plan, tasks)
4. Create ADR documenting the governance change
5. Update runtime guidance (README, CLAUDE.md)
6. Commit with message: `docs: amend constitution to vX.Y.Z (description)`

**Version Bump Rules:**
- **MAJOR**: Backward incompatible governance changes, principle removals, or redefinitions
- **MINOR**: New principles added, sections materially expanded, new requirements added
- **PATCH**: Clarifications, wording improvements, typo fixes, non-semantic refinements

**Compliance Review:**
- Every spec MUST include constitution check in plan.md
- Every task MUST reference the principle it serves
- Every PHR MUST document adherence to agentic workflow
- Every PR MUST verify no hardcoded secrets, proper user isolation, and type safety

**Complexity Justification:**
- Any deviation from constitutional principles MUST be documented in plan.md Complexity Tracking table
- Justification MUST include: specific violation, why needed, and why simpler alternatives were rejected
- Unapproved deviations will be rejected in code review

**Version**: 1.0.0 | **Ratified**: 2026-02-05 | **Last Amended**: 2026-02-05

---
id: 001
title: Create Project Constitution
stage: constitution
date: 2026-02-05
surface: agent
model: claude-sonnet-4-5
feature: none
branch: 001-console-todo-mvp
user: mehma
command: /sp.constitution
labels: ["constitution", "governance", "spec-driven-development", "agentic-workflow"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

Project: Hackathon Phase II - Full-Stack Todo Web Application

Core principles:
- **Spec-Driven Development:** Implementation must strictly follow the written specs; no manual coding.
- **Agentic Workflow:** Use the Plan → Task → Execute loop via Claude Code.
- **Security First:** Strict separation of client/server using JWT tokens for stateless authentication.
- **Modern Stack:** Utilization of Next.js 16+ (App Router) and Python FastAPI with strong typing.
- **User Isolation:** Data access must be strictly filtered by the authenticated user ID.

Key standards:
- **Monorepo Structure:** Frontend and Backend live in the same repo but run as distinct services.
- **Code Quality:** TypeScript for Frontend, Python (with Pydantic/SQLModel) for Backend.
- **Database:** Neon Serverless PostgreSQL for all persistent storage.
- **Authentication:** Better Auth (Frontend) issuing JWTs -> Verified by FastAPI Middleware (Backend) using a shared secret.
- **Responsive Design:** Mobile-first UI using Tailwind CSS.

Constraints:
- **Tech Stack:** Next.js 16+, FastAPI, SQLModel, Neon DB, Better Auth.
- **API Protocol:** RESTful endpoints (GET, POST, PUT, DELETE, PATCH).
- **Authorization:** All `/api/` endpoints must require `Authorization: Bearer <token>` header.
- **Shared Secret:** Frontend and Backend must share `BETTER_AUTH_SECRET` for token validation.
- **Functionality:** Must implement all 5 Basic Level features (List, Create, Get, Update, Delete/Toggle).

Success criteria:
- **End-to-End Auth:** User can sign up/login and session persists securely.
- **Data Persistence:** Tasks are saved to Neon DB and survive server restarts.
- **Privacy:** User A cannot see or modify User B's tasks.
- **Responsiveness:** UI works seamlessly on mobile and desktop.
- **Zero Manual Code:** All features implemented via Agentic prompting.

## Response snapshot

Created comprehensive project constitution (v1.0.0) with 7 core principles:

1. **Spec-Driven Development (NON-NEGOTIABLE)** - Mandatory spec → plan → tasks → implement workflow
2. **Agentic Workflow (NON-NEGOTIABLE)** - All work delegated to specialized agents (auth, frontend, backend, database, architect)
3. **Security First** - JWT authentication, user isolation, CORS, no hardcoded secrets
4. **Modern Stack with Strong Typing** - TypeScript + Next.js 16, Python 3.11+ + FastAPI, Pydantic + SQLModel
5. **User Isolation (NON-NEGOTIABLE)** - Database queries filtered by authenticated user ID
6. **Responsive Design** - Mobile-first with Tailwind CSS
7. **Data Persistence** - Neon Serverless PostgreSQL with proper schema and migrations

Additional sections:
- **Technology Stack Standards** - Mandatory components and prohibited practices
- **Development Workflow** - 6 mandatory stages from specification to ADR creation
- **Required API Endpoints** - All 6 REST endpoints defined with authentication requirements
- **Monorepo Structure** - Detailed directory layout for frontend/ and backend/
- **Governance** - Amendment process, version bump rules, compliance review, complexity justification

Constitution includes Sync Impact Report documenting version change and template updates required.

## Outcome

- ✅ Impact: Initial project constitution establishes governance framework for entire hackathon project. All future specs, plans, and tasks must comply with these principles.
- 🧪 Tests: N/A (governance document)
- 📁 Files: .specify/memory/constitution.md (created, v1.0.0)
- 🔁 Next prompts: Run `/sp.specify` to create first feature specification for multi-user todo web application
- 🧠 Reflection: Constitution successfully captures all hackathon requirements (Better Auth, JWT, Next.js 16+, FastAPI, SQLModel, Neon DB, user isolation, responsive design). Agentic workflow principle ensures all implementation delegated to specialized agents. Three NON-NEGOTIABLE principles enforce critical constraints (spec-driven, agentic, user isolation).

## Evaluation notes (flywheel)

- Failure modes observed: None. All placeholders filled, no unresolved tokens, version and dates properly set.
- Graders run and results (PASS/FAIL): PASS - Constitution complete with 7 principles, all required sections, proper governance, sync impact report included.
- Prompt variant (if applicable): Standard constitution creation workflow
- Next experiment (smallest change to try): Create first feature specification to validate constitution principles in practice

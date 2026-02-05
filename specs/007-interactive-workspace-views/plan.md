# Implementation Plan: Interactive Views & Workspace Management

**Branch**: `007-interactive-workspace-views` | **Date**: 2026-02-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/007-interactive-workspace-views/spec.md`

## Summary

This feature adds advanced interactive visualization and workspace management capabilities to the task management application. The primary requirements include:

1. **Kanban Board**: Drag-and-drop interface for visual task organization across status columns (To Do, In Progress, Review, Done)
2. **Analytics Dashboard**: Data visualization with charts showing status distribution (pie chart), priority workload (bar chart), and productivity trends
3. **Workspace Management**: Switcher component for multi-workspace context management with project-level filtering
4. **Billing UI**: Presentational subscription plan interface (Free, Pro, Business tiers)
5. **Activity Feed**: Real-time activity log showing workspace changes

**Technical Approach**: Leverage recharts for data visualization and @hello-pangea/dnd (or dnd-kit) for drag-and-drop functionality. Integrate with existing Task API and authentication system. Build frontend components in Next.js with responsive design, and extend backend with workspace/project filtering and status update endpoints.

## Technical Context

**Language/Version**:
- Frontend: TypeScript 5+
- Backend: Python 3.11+

**Primary Dependencies**:
- Frontend: Next.js 16+ (App Router), React 18+, recharts, @hello-pangea/dnd or dnd-kit, Tailwind CSS, Better Auth
- Backend: FastAPI, SQLModel, Pydantic, JWT libraries (python-jose, passlib)

**Storage**: Neon Serverless PostgreSQL with SQLModel ORM

**Testing**:
- Frontend: Jest, React Testing Library
- Backend: pytest, httpx (FastAPI test client)

**Target Platform**:
- Frontend: Web browsers (mobile-first responsive, 320px-1920px)
- Backend: Linux server (containerized deployment)

**Project Type**: Web application (monorepo with frontend/ and backend/ directories)

**Performance Goals**:
- Drag-and-drop operations: < 1 second backend update
- Analytics charts: < 2 seconds render time
- Activity feed updates: < 5 seconds latency
- API responses: < 200ms p95 latency
- Chart data aggregation: handle 1000+ tasks efficiently

**Constraints**:
- MUST use recharts library for all data visualizations
- MUST use @hello-pangea/dnd or dnd-kit for drag-and-drop functionality
- MUST maintain existing JWT security and user isolation patterns
- MUST work within Next.js App Router architecture
- Billing UI is presentational only (no actual payment processing)
- Performance: Drag operations < 1s, chart render < 2s, activity updates < 5s

**Scale/Scope**:
- Support multiple workspaces per user
- Handle 100+ tasks per workspace efficiently
- Display charts with up to 1000 data points
- Activity feed: show last 100 events with pagination

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ I. Spec-Driven Development (NON-NEGOTIABLE)
- [x] Feature has specification at `specs/007-interactive-workspace-views/spec.md`
- [x] Implementation plan being created at `specs/007-interactive-workspace-views/plan.md`
- [x] Will generate tasks at `specs/007-interactive-workspace-views/tasks.md` in next phase
- [x] All work traceable through spec-driven artifact chain

**Status**: PASS

### ✅ II. Agentic Workflow (NON-NEGOTIABLE)
**Planned Agent Delegation:**
- `nextjs-ui-builder`: Kanban board components (KanbanBoard.tsx, KanbanColumn.tsx, KanbanCard.tsx), Analytics dashboard (ProductivityChart.tsx, StatusPieChart.tsx), Workspace switcher, Billing page, Activity feed components
- `fastapi-backend-architect`: Extend task status PATCH endpoint, workspace/project filtering, activity logging endpoints, analytics aggregation service
- `neon-db-manager`: Extend Task model with status enum, add Activity model for feed, add Workspace and Project models if not existing, create indexes for filtering
- `spec-driven-architect`: Coordinate cross-stack implementation, validate consistency between frontend and backend

**Status**: PASS - Clear agent delegation strategy defined

### ✅ III. Security First
- [x] All API endpoints require JWT authentication (existing pattern maintained)
- [x] User ID validation: URL user_id must match JWT token user_id
- [x] Database queries filtered by authenticated user ID
- [x] Workspace/Project access validated against user permissions
- [x] No secrets hardcoded (use .env for JWT_SECRET, DATABASE_URL)
- [x] CORS limited to Next.js frontend origin

**Status**: PASS - Existing security architecture maintained

### ✅ IV. Modern Stack with Strong Typing
- [x] Frontend: TypeScript with Next.js 16+ App Router
- [x] Backend: Python 3.11+ with FastAPI and Pydantic models
- [x] SQLModel for type-safe database models
- [x] All request/response validated with Pydantic schemas
- [x] Type hints for all functions

**Status**: PASS - Adheres to stack requirements

### ✅ V. User Isolation (NON-NEGOTIABLE)
- [x] Task queries filtered by user_id (existing)
- [x] Workspace queries filtered by user access permissions
- [x] Activity feed filtered by workspace user has access to
- [x] Project filtering validates user ownership
- [x] Unauthorized access returns 403 Forbidden

**Status**: PASS - User isolation enforced at query level

### ✅ VI. Responsive Design
- [x] Mobile-first design (320px minimum)
- [x] Tailwind CSS for responsive utilities
- [x] Kanban board adapts to mobile (stacked columns or horizontal scroll)
- [x] Charts responsive with recharts built-in responsiveness
- [x] Billing cards stack on mobile, grid on desktop
- [x] Touch targets >= 44x44px for drag-and-drop

**Status**: PASS - Mobile-first responsive approach

### ✅ VII. Data Persistence
- [x] Neon PostgreSQL via DATABASE_URL
- [x] SQLModel for all models (Task, Workspace, Project, Activity)
- [x] Foreign keys enforce referential integrity (task.workspace_id -> workspace.id)
- [x] Indexes on user_id, workspace_id, created_at for performance
- [x] Connection pooling configured

**Status**: PASS - Proper database design with indexes

### Constitution Check Summary
**Overall Status**: ✅ PASS - All constitutional requirements satisfied

No violations requiring justification in Complexity Tracking table.

## Project Structure

### Documentation (this feature)

```text
specs/007-interactive-workspace-views/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification (already created)
├── checklists/
│   └── requirements.md  # Specification quality checklist (already created)
├── research.md          # Phase 0 output (to be created)
├── data-model.md        # Phase 1 output (to be created)
├── quickstart.md        # Phase 1 output (to be created)
├── contracts/           # Phase 1 output (to be created)
│   ├── analytics-api.openapi.yaml
│   ├── workspace-api.openapi.yaml
│   └── activity-api.openapi.yaml
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Web application structure (monorepo)
backend/
├── src/
│   ├── models/
│   │   ├── task.py          # Extend with status enum, workspace_id, project_id
│   │   ├── user.py          # Existing user model
│   │   ├── workspace.py     # NEW: Workspace model
│   │   ├── project.py       # NEW: Project model
│   │   └── activity.py      # NEW: Activity log model
│   ├── schemas/
│   │   ├── task.py          # Extend with status update schema
│   │   ├── workspace.py     # NEW: Workspace request/response schemas
│   │   ├── project.py       # NEW: Project request/response schemas
│   │   ├── activity.py      # NEW: Activity request/response schemas
│   │   └── analytics.py     # NEW: Analytics aggregation schemas
│   ├── api/
│   │   ├── tasks.py         # Extend with PATCH status endpoint, workspace/project filtering
│   │   ├── workspaces.py    # NEW: Workspace endpoints
│   │   ├── projects.py      # NEW: Project endpoints
│   │   ├── activities.py    # NEW: Activity feed endpoints
│   │   └── analytics.py     # NEW: Analytics data endpoints
│   ├── services/
│   │   ├── task_service.py  # Existing task business logic
│   │   ├── analytics_service.py  # NEW: Chart data aggregation (StatsService)
│   │   └── activity_service.py   # NEW: Activity logging
│   ├── middleware/
│   │   └── auth.py          # Existing JWT authentication middleware
│   └── main.py              # FastAPI app entry point
└── tests/
    ├── contract/            # API contract tests for new endpoints
    ├── integration/         # Integration tests for workspace/project filtering
    └── unit/                # Unit tests for analytics aggregation

frontend/
├── app/
│   ├── (auth)/
│   │   └── ...              # Existing authentication routes
│   ├── (dashboard)/
│   │   ├── layout.tsx       # Extend with WorkspaceSwitcher in sidebar
│   │   ├── page.tsx         # Main dashboard (extend with tabs: List vs Kanban)
│   │   ├── kanban/
│   │   │   └── page.tsx     # NEW: Kanban board page
│   │   ├── analytics/
│   │   │   └── page.tsx     # NEW: Analytics dashboard page (Insights tab)
│   │   └── billing/
│   │       └── page.tsx     # NEW: Billing subscription page
│   └── layout.tsx           # Root layout
├── components/
│   ├── kanban/
│   │   ├── KanbanBoard.tsx       # NEW: Main Kanban board container
│   │   ├── KanbanColumn.tsx      # NEW: Status column component
│   │   └── KanbanCard.tsx        # NEW: Task card with drag functionality
│   ├── analytics/
│   │   ├── ProductivityChart.tsx # NEW: Tasks completed vs created chart
│   │   ├── StatusPieChart.tsx    # NEW: Status distribution pie chart
│   │   └── PriorityBarChart.tsx  # NEW: Priority workload bar chart
│   ├── workspace/
│   │   ├── WorkspaceSwitcher.tsx # NEW: Sidebar workspace dropdown
│   │   └── ProjectFilter.tsx     # NEW: Project filter component
│   ├── billing/
│   │   ├── PricingCard.tsx       # NEW: Subscription plan card
│   │   └── PaymentHistory.tsx    # NEW: Mock payment history table
│   ├── activity/
│   │   ├── ActivityFeed.tsx      # NEW: Live activity feed component
│   │   └── ActivityItem.tsx      # NEW: Single activity entry
│   └── ui/
│       └── ...                   # Existing UI components (Button, Card, etc.)
├── lib/
│   ├── services/
│   │   ├── task-service.ts       # Extend with status update, workspace filtering
│   │   ├── analytics-service.ts  # NEW: Analytics data fetching (StatsService.ts)
│   │   ├── workspace-service.ts  # NEW: Workspace API calls
│   │   └── activity-service.ts   # NEW: Activity feed API calls
│   ├── hooks/
│   │   ├── use-workspace.ts      # NEW: Workspace context hook
│   │   └── use-analytics.ts      # NEW: Analytics data hook
│   └── utils/
│       └── confetti.ts           # NEW: Celebration effect for task completion
└── tests/
```

**Structure Decision**: Web application monorepo with separate `backend/` and `frontend/` directories. This structure supports the full-stack nature of the feature with clear separation between API services (backend) and user interface (frontend). The existing directory structure is extended with new modules for Kanban, analytics, workspace management, and billing.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**No violations detected** - All constitutional requirements are satisfied. The feature adheres to:
- Spec-driven workflow with clear artifacts
- Agentic delegation to specialized agents
- Security-first design with JWT and user isolation
- Modern typed stack (TypeScript + Python)
- Responsive mobile-first design
- Persistent storage with proper indexing

No complexity justifications needed.

---

## Phase 0: Research & Technology Validation

### Research Tasks

The following research tasks resolve unknowns from Technical Context and validate technology choices:

#### R1: Drag-and-Drop Library Selection
**Question**: Should we use @hello-pangea/dnd or dnd-kit for Kanban board?

**Research Focus**:
- Compare API complexity and bundle size
- Evaluate Next.js 16 App Router compatibility
- Assess mobile/touch support quality
- Check React 18+ concurrent features support
- Review accessibility features (keyboard navigation)

**Deliverable**: Library recommendation with rationale in research.md

#### R2: Recharts Integration Patterns
**Question**: How to integrate recharts with Next.js App Router server/client components?

**Research Focus**:
- Server vs client component boundaries for charts
- Data fetching patterns (server-side vs client-side)
- Responsive chart configuration best practices
- Performance optimization for large datasets (1000+ tasks)
- Empty state handling patterns

**Deliverable**: Integration approach in research.md

#### R3: Workspace Data Model Design
**Question**: How should workspaces relate to users, tasks, and projects?

**Research Focus**:
- User-workspace relationship (many-to-many with roles?)
- Task-workspace-project hierarchy
- Permission model (owner, admin, member)
- Default workspace behavior for new users
- Database schema design patterns for multi-tenancy

**Deliverable**: Entity relationship diagram and schema decisions in research.md

#### R4: Activity Logging Strategy
**Question**: How to implement efficient activity logging without performance impact?

**Research Focus**:
- Event sourcing vs simple audit log approach
- Database write optimization (async logging, batching)
- Query patterns for activity feed (pagination, filtering)
- Storage considerations (retention policy, archiving)
- Performance impact on task CRUD operations

**Deliverable**: Activity logging architecture in research.md

#### R5: Analytics Aggregation Performance
**Question**: How to efficiently aggregate task data for charts?

**Research Focus**:
- Database query optimization (indexes, joins)
- Caching strategy for analytics data (Redis, in-memory)
- Incremental aggregation vs full scan
- SQL window functions for time-based queries
- SQLModel/SQLAlchemy query patterns for aggregation

**Deliverable**: Analytics service design in research.md

#### R6: Confetti/Celebration Effect Implementation
**Question**: What library or approach for task completion celebration?

**Research Focus**:
- Lightweight confetti libraries (canvas-confetti, react-confetti)
- Performance impact and bundle size
- Accessibility considerations (reduced motion preference)
- Trigger patterns (optimistic vs confirmed completion)

**Deliverable**: Celebration effect recommendation in research.md

### Research Status: ✅ COMPLETE

All research tasks have been completed and findings documented in [research.md](./research.md).

**Key Decisions Made:**
- **Drag-and-Drop**: dnd-kit (15KB, transform-based, mobile-optimized)
- **Charts**: recharts with hybrid data fetching (server initial + client refresh)
- **Workspace Model**: Many-to-many with WorkspaceMember association table and RBAC
- **Activity Logging**: Async audit log with background tasks
- **Analytics**: Database-level aggregation (reduces 1000 tasks to 10-30 data points)
- **Celebration Effect**: canvas-confetti (6KB, accessible)

**Next Phase**: Phase 1 - Design & Contracts

---

## Phase 1: Design & Contracts

### Data Model Design

**Deliverable**: `data-model.md` with complete entity schemas including:
- Workspace model with relationships
- WorkspaceMember association table with roles (OWNER, ADMIN, MEMBER, VIEWER)
- Updated Task model with workspace_id, created_by, assigned_to
- Project model with workspace association
- Section model for task organization
- Activity model for audit logging

### API Contracts

**Deliverables**: OpenAPI specifications in `contracts/` directory:

#### `contracts/workspace-api.openapi.yaml`
```yaml
# Workspace Management Endpoints
GET    /api/workspaces                        # List user's workspaces
POST   /api/workspaces                        # Create workspace
GET    /api/workspaces/{workspace_id}         # Get workspace details
PUT    /api/workspaces/{workspace_id}         # Update workspace
DELETE /api/workspaces/{workspace_id}         # Delete workspace (OWNER only)

# Workspace Member Management
GET    /api/workspaces/{workspace_id}/members           # List members
POST   /api/workspaces/{workspace_id}/members           # Invite member
DELETE /api/workspaces/{workspace_id}/members/{user_id} # Remove member
PATCH  /api/workspaces/{workspace_id}/members/{user_id} # Update member role
```

#### `contracts/task-api-v2.openapi.yaml`
```yaml
# Updated Task Endpoints (Workspace-Aware)
GET    /api/workspaces/{workspace_id}/tasks             # List tasks (filtered by workspace)
POST   /api/workspaces/{workspace_id}/tasks             # Create task in workspace
GET    /api/workspaces/{workspace_id}/tasks/{task_id}   # Get task details
PUT    /api/workspaces/{workspace_id}/tasks/{task_id}   # Update task
DELETE /api/workspaces/{workspace_id}/tasks/{task_id}   # Delete task
PATCH  /api/workspaces/{workspace_id}/tasks/{task_id}/status  # Update task status (Kanban drag)
```

#### `contracts/analytics-api.openapi.yaml`
```yaml
# Analytics Data Endpoints
GET /api/workspaces/{workspace_id}/analytics                    # All analytics data
GET /api/workspaces/{workspace_id}/analytics/status             # Status distribution
GET /api/workspaces/{workspace_id}/analytics/priority           # Priority breakdown
GET /api/workspaces/{workspace_id}/analytics/completion-trend   # Completion trend (30 days)
```

#### `contracts/activity-api.openapi.yaml`
```yaml
# Activity Feed Endpoints
GET /api/workspaces/{workspace_id}/activities  # List recent activities (paginated)
```

### Quickstart Guide

**Deliverable**: `quickstart.md` with:
- Development environment setup
- Install dependencies (dnd-kit, recharts, canvas-confetti)
- Database migration commands
- Running frontend and backend servers
- Testing the Kanban board and analytics dashboard

### Agent Context Update

**Action**: Run `.specify/scripts/bash/update-agent-context.sh claude` to add:
- dnd-kit (@dnd-kit/core, @dnd-kit/sortable, @dnd-kit/utilities)
- recharts
- canvas-confetti
- Workspace multi-tenancy architecture
- Activity logging patterns

---

## Phase 2: Constitution Re-Check (After Design)

After completing Phase 1 design artifacts, re-verify constitutional compliance:

### ✅ I. Spec-Driven Development
- [x] Spec created at `specs/007-interactive-workspace-views/spec.md`
- [x] Plan created at `specs/007-interactive-workspace-views/plan.md`
- [x] Research documented at `specs/007-interactive-workspace-views/research.md`
- [ ] Data model documented (Phase 1 deliverable)
- [ ] API contracts defined (Phase 1 deliverable)
- [ ] Tasks will be generated via `/sp.tasks` (next command)

**Status**: ON TRACK

### ✅ II. Agentic Workflow
- [x] Research completed by general-purpose agents
- [ ] Database schema → `neon-db-manager` agent
- [ ] Backend APIs → `fastapi-backend-architect` agent
- [ ] Frontend components → `nextjs-ui-builder` agent
- [ ] Cross-stack coordination → `spec-driven-architect` agent

**Status**: READY FOR IMPLEMENTATION

### ✅ III-VII. All Other Principles
No changes to security, typing, isolation, responsive design, or persistence requirements.

**Overall Status**: ✅ PASS - Constitution compliance maintained

---

## Implementation Readiness

**Branch**: `007-interactive-workspace-views`
**Specification**: [spec.md](./spec.md) ✅ Complete
**Research**: [research.md](./research.md) ✅ Complete
**Plan**: [plan.md](./plan.md) ✅ In Progress

**Next Steps**:
1. Complete Phase 1 (data-model.md, contracts/, quickstart.md)
2. Run `/sp.tasks` to generate task breakdown
3. Execute `/sp.implement` to delegate to specialized agents
4. Create PHR for planning phase
5. Run `/sp.git.commit_pr` when ready to commit

**Blocked By**: None - All research complete, ready for Phase 1 design work.


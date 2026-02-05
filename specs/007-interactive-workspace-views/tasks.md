# Tasks: Interactive Views & Workspace Management

**Input**: Design documents from `/specs/007-interactive-workspace-views/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅

**Tests**: Not explicitly requested in specification - tests marked as OPTIONAL

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4, US5)
- Include exact file paths in descriptions

## Path Conventions

- **Web app (monorepo)**: `backend/src/`, `frontend/`
- Paths follow plan.md structure with separate frontend and backend directories

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Install dependencies and configure development environment

- [ ] T001 [P] Install frontend dependencies: dnd-kit (@dnd-kit/core, @dnd-kit/sortable, @dnd-kit/utilities) in frontend/package.json
- [ ] T002 [P] Install recharts library for data visualization in frontend/package.json
- [ ] T003 [P] Install canvas-confetti for celebration effects in frontend/package.json
- [ ] T004 [P] Verify Next.js 16+ App Router configuration in frontend/next.config.js
- [ ] T005 [P] Verify FastAPI dependencies (SQLModel, Pydantic, python-jose) in backend/requirements.txt

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core database models and infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Models (Backend)

- [ ] T006 [P] Create Workspace model with relationships in backend/src/models/workspace.py
- [ ] T007 [P] Create WorkspaceMember association table with roles (OWNER, ADMIN, MEMBER, VIEWER) in backend/src/models/workspace_member.py
- [ ] T008 [P] Create Project model with workspace_id foreign key in backend/src/models/project.py
- [ ] T009 [P] Create Section model with project_id foreign key in backend/src/models/section.py
- [ ] T010 [P] Create Activity model for audit logging in backend/src/models/activity.py
- [ ] T011 Update Task model to add workspace_id, created_by, assigned_to fields in backend/src/models/task.py
- [ ] T012 Update Task model to add status enum (To Do, In Progress, Review, Done) in backend/src/models/task.py
- [ ] T013 Create database migration for new models and Task model updates in backend/alembic/versions/

### Database Indexes

- [ ] T014 Create composite index on workspace_members(user_id, workspace_id) for permission checks
- [ ] T015 Create composite index on tasks(workspace_id, created_at) for performance
- [ ] T016 Create composite index on tasks(workspace_id, status) for analytics aggregation
- [ ] T017 Create index on activities(workspace_id, created_at) for activity feed queries

### Backend Services

- [ ] T018 [P] Create permissions service with check_workspace_access() in backend/src/services/permissions.py
- [ ] T019 [P] Create activity logging service with log_activity_async() in backend/src/services/activity_service.py
- [ ] T020 [P] Create analytics service with aggregation queries in backend/src/services/analytics_service.py

### Pydantic Schemas

- [ ] T021 [P] Create Workspace request/response schemas in backend/src/schemas/workspace.py
- [ ] T022 [P] Create WorkspaceMember schemas in backend/src/schemas/workspace_member.py
- [ ] T023 [P] Create Project schemas in backend/src/schemas/project.py
- [ ] T024 [P] Create Activity schemas in backend/src/schemas/activity.py
- [ ] T025 [P] Create Analytics aggregation schemas in backend/src/schemas/analytics.py
- [ ] T026 Update Task schemas to include workspace_id and status update in backend/src/schemas/task.py

### Frontend Services & Hooks

- [ ] T027 [P] Create workspace service for API calls in frontend/lib/services/workspace-service.ts
- [ ] T028 [P] Create analytics service for data fetching in frontend/lib/services/analytics-service.ts
- [ ] T029 [P] Create activity service for feed API calls in frontend/lib/services/activity-service.ts
- [ ] T030 [P] Create use-workspace hook for context management in frontend/lib/hooks/use-workspace.ts
- [ ] T031 [P] Create use-analytics hook for data loading in frontend/lib/hooks/use-analytics.ts

### Shared UI Components

- [ ] T032 [P] Create EmptyChartState component for no-data handling in frontend/components/analytics/EmptyChartState.tsx
- [ ] T033 [P] Create ChartSkeleton loading component in frontend/components/analytics/ChartSkeleton.tsx
- [ ] T034 [P] Create confetti celebration utility in frontend/lib/utils/confetti.ts

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Kanban Board Task Management (Priority: P1) 🎯 MVP

**Goal**: Enable users to organize and manage tasks using a visual Kanban board with drag-and-drop between status columns (To Do, In Progress, Review, Done)

**Independent Test**: Create a task, drag it from "To Do" to "In Progress", and verify the task status updates in the database. Kanban board displays all tasks in correct status columns.

### Backend API for User Story 1

- [ ] T035 [US1] Create PATCH endpoint for task status update in backend/src/api/tasks.py
- [ ] T036 [US1] Add workspace_id filtering to existing GET /tasks endpoint in backend/src/api/tasks.py
- [ ] T037 [US1] Add error handling and reversion logic for failed status updates in backend/src/api/tasks.py
- [ ] T038 [US1] Integrate activity logging on task status changes in backend/src/api/tasks.py

### Frontend Kanban Components for User Story 1

- [ ] T039 [P] [US1] Create KanbanBoard container component with dnd-kit DndContext in frontend/components/kanban/KanbanBoard.tsx
- [ ] T040 [P] [US1] Create KanbanColumn component for status columns in frontend/components/kanban/KanbanColumn.tsx
- [ ] T041 [P] [US1] Create KanbanCard component with drag functionality in frontend/components/kanban/KanbanCard.tsx
- [ ] T042 [US1] Implement onDragEnd handler with API call to update task status in frontend/components/kanban/KanbanBoard.tsx
- [ ] T043 [US1] Add error handling and task reversion on API failure in frontend/components/kanban/KanbanBoard.tsx
- [ ] T044 [US1] Add visual feedback during drag operations (drag overlay, drop zone highlighting) in frontend/components/kanban/KanbanBoard.tsx
- [ ] T045 [US1] Integrate confetti celebration effect on task move to "Done" column in frontend/components/kanban/KanbanCard.tsx

### Frontend Kanban Page for User Story 1

- [ ] T046 [US1] Create Kanban board page with data fetching in frontend/app/(dashboard)/kanban/page.tsx
- [ ] T047 [US1] Add loading and error states to Kanban page in frontend/app/(dashboard)/kanban/page.tsx
- [ ] T048 [US1] Add mobile-responsive layout (stacked or horizontal scroll) in frontend/app/(dashboard)/kanban/page.tsx
- [ ] T049 [US1] Update dashboard layout to add Kanban tab/navigation link in frontend/app/(dashboard)/layout.tsx

**Checkpoint**: At this point, User Story 1 (Kanban Board) should be fully functional and testable independently. Users can drag tasks between columns and see status updates persist.

---

## Phase 4: User Story 2 - Analytics Dashboard Visualization (Priority: P2)

**Goal**: Provide visual analytics of task data through charts showing status distribution (pie chart), priority workload (bar chart), and productivity trends

**Independent Test**: Create tasks with different statuses and priorities, then verify that charts correctly display aggregated data from the Task API

### Backend Analytics API for User Story 2

- [ ] T050 [US2] Create GET /analytics endpoint returning all chart data in backend/src/api/analytics.py
- [ ] T051 [US2] Create GET /analytics/status endpoint for status distribution in backend/src/api/analytics.py
- [ ] T052 [US2] Create GET /analytics/priority endpoint for priority breakdown in backend/src/api/analytics.py
- [ ] T053 [US2] Create GET /analytics/completion-trend endpoint for 30-day trends in backend/src/api/analytics.py
- [ ] T054 [US2] Implement database aggregation queries in analytics service in backend/src/services/analytics_service.py
- [ ] T055 [US2] Add workspace_id filtering to all analytics queries in backend/src/services/analytics_service.py
- [ ] T056 [US2] Add project_id filtering support for project-specific analytics in backend/src/services/analytics_service.py

### Frontend Analytics Components for User Story 2

- [ ] T057 [P] [US2] Create StatusPieChart component with recharts in frontend/components/analytics/StatusPieChart.tsx
- [ ] T058 [P] [US2] Create PriorityBarChart component with recharts in frontend/components/analytics/PriorityBarChart.tsx
- [ ] T059 [P] [US2] Create ProductivityChart (completion trend) with recharts in frontend/components/analytics/ProductivityChart.tsx
- [ ] T060 [US2] Create TaskAnalyticsCharts wrapper component (client component) in frontend/components/analytics/TaskAnalyticsCharts.tsx
- [ ] T061 [US2] Add responsive chart configuration (mobile vs desktop sizing) in all chart components
- [ ] T062 [US2] Add empty state handling for charts with no data in frontend/components/analytics/TaskAnalyticsCharts.tsx

### Frontend Analytics Page for User Story 2

- [ ] T063 [US2] Create analytics dashboard page with server-side data fetching in frontend/app/(dashboard)/analytics/page.tsx
- [ ] T064 [US2] Add loading.tsx for analytics page skeleton in frontend/app/(dashboard)/analytics/loading.tsx
- [ ] T065 [US2] Add error handling and retry logic for analytics data in frontend/app/(dashboard)/analytics/page.tsx
- [ ] T066 [US2] Update dashboard navigation to add Analytics/Insights tab in frontend/app/(dashboard)/layout.tsx

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Users can view Kanban board AND analytics dashboard separately.

---

## Phase 5: User Story 3 - Workspace Switcher and Context Management (Priority: P2)

**Goal**: Enable users to switch between different workspaces from the sidebar and filter all views (Kanban, analytics) by workspace and project context

**Independent Test**: Create multiple workspaces, switch between them, and verify that task lists and analytics update to show only workspace-specific data

### Backend Workspace API for User Story 3

- [ ] T067 [US3] Create GET /workspaces endpoint to list user's workspaces in backend/src/api/workspaces.py
- [ ] T068 [US3] Create POST /workspaces endpoint to create workspace in backend/src/api/workspaces.py
- [ ] T069 [US3] Create GET /workspaces/{workspace_id} endpoint in backend/src/api/workspaces.py
- [ ] T070 [US3] Create PUT /workspaces/{workspace_id} endpoint in backend/src/api/workspaces.py
- [ ] T071 [US3] Create DELETE /workspaces/{workspace_id} endpoint (OWNER only) in backend/src/api/workspaces.py
- [ ] T072 [US3] Create GET /workspaces/{workspace_id}/members endpoint in backend/src/api/workspaces.py
- [ ] T073 [US3] Add workspace access validation using permissions service in backend/src/api/workspaces.py

### Backend Project API for User Story 3

- [ ] T074 [P] [US3] Create GET /workspaces/{workspace_id}/projects endpoint in backend/src/api/projects.py
- [ ] T075 [P] [US3] Create POST /workspaces/{workspace_id}/projects endpoint in backend/src/api/projects.py
- [ ] T076 [P] [US3] Create GET /projects/{project_id} endpoint in backend/src/api/projects.py

### Frontend Workspace Components for User Story 3

- [ ] T077 [P] [US3] Create WorkspaceSwitcher dropdown component in frontend/components/workspace/WorkspaceSwitcher.tsx
- [ ] T078 [P] [US3] Create ProjectFilter component for project-based filtering in frontend/components/workspace/ProjectFilter.tsx
- [ ] T079 [US3] Integrate WorkspaceSwitcher into dashboard sidebar in frontend/app/(dashboard)/layout.tsx
- [ ] T080 [US3] Add workspace context state management using use-workspace hook in frontend/app/(dashboard)/layout.tsx
- [ ] T081 [US3] Update Kanban board to filter tasks by current workspace in frontend/app/(dashboard)/kanban/page.tsx
- [ ] T082 [US3] Update analytics dashboard to filter by current workspace in frontend/app/(dashboard)/analytics/page.tsx
- [ ] T083 [US3] Add project filter UI to dashboard pages in frontend/components/workspace/ProjectFilter.tsx
- [ ] T084 [US3] Implement URL-based project filtering (query parameter ?project=uuid) in frontend/app/(dashboard)/page.tsx

**Checkpoint**: All three user stories (Kanban, Analytics, Workspace Switcher) should now work together. Users can switch workspaces and see filtered data across all views.

---

## Phase 6: User Story 4 - Billing and Subscription Management (Priority: P3)

**Goal**: Display subscription plan options (Free, Pro, Business) with features and pricing in a responsive billing page

**Independent Test**: Navigate to the billing page and verify that plan cards display correctly with pricing and features, and that the UI is responsive across devices (320px-1920px)

### Frontend Billing Components for User Story 4

- [ ] T085 [P] [US4] Create PricingCard component for subscription tiers in frontend/components/billing/PricingCard.tsx
- [ ] T086 [P] [US4] Create PaymentHistory mock table component in frontend/components/billing/PaymentHistory.tsx
- [ ] T087 [US4] Create billing page with plan cards (Free, Pro, Business) in frontend/app/(dashboard)/billing/page.tsx
- [ ] T088 [US4] Add responsive grid layout for plan cards (mobile: stack, desktop: grid) in frontend/app/(dashboard)/billing/page.tsx
- [ ] T089 [US4] Add current plan highlighting logic in frontend/app/(dashboard)/billing/page.tsx
- [ ] T090 [US4] Add "coming soon" message for upgrade button clicks in frontend/app/(dashboard)/billing/page.tsx
- [ ] T091 [US4] Update dashboard navigation to add Billing link in frontend/app/(dashboard)/layout.tsx

**Checkpoint**: User Story 4 (Billing UI) should be fully functional. Users can view subscription plans and the page is responsive.

---

## Phase 7: User Story 5 - Live Activity Feed (Priority: P3)

**Goal**: Display a live activity feed showing recent workspace changes (task created, status changed, completed) in chronological order

**Independent Test**: Make changes to tasks (create, update status, complete) and verify that these activities appear in the activity feed in reverse chronological order

### Backend Activity API for User Story 5

- [ ] T092 [US5] Create GET /workspaces/{workspace_id}/activities endpoint with pagination in backend/src/api/activities.py
- [ ] T093 [US5] Integrate background task logging for task creation in backend/src/api/tasks.py
- [ ] T094 [US5] Integrate background task logging for task status changes in backend/src/api/tasks.py
- [ ] T095 [US5] Integrate background task logging for task completion in backend/src/api/tasks.py
- [ ] T096 [US5] Add limit/offset pagination support to activity endpoint in backend/src/api/activities.py

### Frontend Activity Feed Components for User Story 5

- [ ] T097 [P] [US5] Create ActivityItem component for single activity entry in frontend/components/activity/ActivityItem.tsx
- [ ] T098 [P] [US5] Create ActivityFeed container component with pagination in frontend/components/activity/ActivityFeed.tsx
- [ ] T099 [US5] Add activity feed to dashboard sidebar or main page in frontend/app/(dashboard)/page.tsx
- [ ] T100 [US5] Implement auto-refresh or polling for activity feed updates in frontend/components/activity/ActivityFeed.tsx
- [ ] T101 [US5] Add empty state for activity feed with no activities in frontend/components/activity/ActivityFeed.tsx
- [ ] T102 [US5] Add workspace filtering to activity feed in frontend/components/activity/ActivityFeed.tsx

**Checkpoint**: All user stories (Kanban, Analytics, Workspace Switcher, Billing, Activity Feed) should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final quality checks

- [ ] T103 [P] Add error boundary components for Kanban and Analytics pages in frontend/components/
- [ ] T104 [P] Add toast notifications for drag-and-drop errors in frontend/components/kanban/KanbanBoard.tsx
- [ ] T105 [P] Optimize chart performance with memoization and code-splitting in frontend/components/analytics/
- [ ] T106 [P] Add keyboard accessibility announcements for drag-and-drop in frontend/components/kanban/KanbanBoard.tsx
- [ ] T107 [P] Verify mobile responsiveness across all pages (320px-1920px) in frontend/app/(dashboard)/
- [ ] T108 [P] Add database connection pooling configuration in backend/src/database.py
- [ ] T109 [P] Add API rate limiting for analytics endpoints in backend/src/middleware/
- [ ] T110 [P] Run security audit on workspace permission checks in backend/src/services/permissions.py
- [ ] T111 Code cleanup and removal of console.log statements across frontend
- [ ] T112 Update documentation with setup instructions for new dependencies
- [ ] T113 Verify all empty states display correctly (no tasks, no data, no activities)
- [ ] T114 Performance testing with 1000+ tasks to verify chart aggregation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P2 → P3 → P3)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 - Kanban (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 - Analytics (P2)**: Can start after Foundational (Phase 2) - Independent, but benefits from US1 for test data
- **User Story 3 - Workspace Switcher (P2)**: Can start after Foundational (Phase 2) - Enhances US1 and US2 when integrated
- **User Story 4 - Billing (P3)**: Can start after Foundational (Phase 2) - Completely independent of other stories
- **User Story 5 - Activity Feed (P3)**: Can start after Foundational (Phase 2) - Benefits from US1/US3 for activity generation

### Within Each User Story

- Backend API endpoints before frontend components that consume them
- Models before services (Foundational phase)
- Services before endpoints (Foundational phase)
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

**Phase 1 (Setup)**: T001-T005 can all run in parallel (different package.json files)

**Phase 2 (Foundational)**:
- Database Models: T006-T010 can run in parallel (different model files)
- Schemas: T021-T026 can run in parallel (different schema files)
- Services: T018-T020 can run in parallel (different service files)
- Frontend Services: T027-T031 can run in parallel (different service files)
- Shared Components: T032-T034 can run in parallel (different component files)

**Phase 3 (US1 - Kanban)**:
- T039-T041 (Kanban components) can run in parallel (different component files)

**Phase 4 (US2 - Analytics)**:
- T051-T053 (Analytics endpoints) can run in parallel if using different query functions
- T057-T059 (Chart components) can run in parallel (different component files)

**Phase 5 (US3 - Workspace)**:
- T074-T076 (Project API endpoints) can run in parallel
- T077-T078 (Workspace components) can run in parallel

**Phase 6 (US4 - Billing)**:
- T085-T086 (Billing components) can run in parallel

**Phase 7 (US5 - Activity)**:
- T097-T098 (Activity components) can run in parallel

**Phase 8 (Polish)**: T103-T110 can all run in parallel (different files/concerns)

**Cross-Phase Parallelism**: After Foundational (Phase 2) completes, User Stories 1-5 can ALL proceed in parallel if team capacity allows

---

## Parallel Example: User Story 1 (Kanban Board)

```bash
# Launch all Kanban components together (different files):
Task: "Create KanbanBoard container component with dnd-kit DndContext in frontend/components/kanban/KanbanBoard.tsx"
Task: "Create KanbanColumn component for status columns in frontend/components/kanban/KanbanColumn.tsx"
Task: "Create KanbanCard component with drag functionality in frontend/components/kanban/KanbanCard.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T034) - CRITICAL - blocks all stories
3. Complete Phase 3: User Story 1 - Kanban Board (T035-T049)
4. **STOP and VALIDATE**: Test Kanban board independently
   - Create tasks and drag between columns
   - Verify status updates persist
   - Test error handling and task reversion
   - Test mobile responsiveness
5. Deploy/demo Kanban board MVP if ready

### Incremental Delivery

1. Complete Setup + Foundational (T001-T034) → Foundation ready
2. Add User Story 1 - Kanban (T035-T049) → Test independently → **Deploy/Demo (MVP!)**
3. Add User Story 2 - Analytics (T050-T066) → Test independently → Deploy/Demo
4. Add User Story 3 - Workspace Switcher (T067-T084) → Test independently → Deploy/Demo
5. Add User Story 4 - Billing (T085-T091) → Test independently → Deploy/Demo
6. Add User Story 5 - Activity Feed (T092-T102) → Test independently → Deploy/Demo
7. Complete Polish (T103-T114) → Final quality pass → Deploy

Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers (recommended after Foundational phase):

1. Team completes Setup + Foundational together (T001-T034)
2. Once Foundational is done, assign in parallel:
   - **Developer A**: User Story 1 - Kanban Board (T035-T049)
   - **Developer B**: User Story 2 - Analytics Dashboard (T050-T066)
   - **Developer C**: User Story 3 - Workspace Switcher (T067-T084)
3. After P1 and P2 stories complete:
   - **Developer A or B**: User Story 4 - Billing (T085-T091)
   - **Developer C**: User Story 5 - Activity Feed (T092-T102)
4. All developers: Polish phase together (T103-T114)

Stories complete and integrate independently, allowing for continuous deployment.

---

## Task Count Summary

- **Phase 1 (Setup)**: 5 tasks
- **Phase 2 (Foundational)**: 29 tasks (BLOCKS all user stories)
- **Phase 3 (US1 - Kanban)**: 15 tasks
- **Phase 4 (US2 - Analytics)**: 17 tasks
- **Phase 5 (US3 - Workspace Switcher)**: 18 tasks
- **Phase 6 (US4 - Billing)**: 7 tasks
- **Phase 7 (US5 - Activity Feed)**: 11 tasks
- **Phase 8 (Polish)**: 12 tasks

**Total**: 114 tasks

**Parallel Opportunities**: 45+ tasks marked with [P] can run in parallel within their phases

**Independent Test Criteria**:
- **US1**: Drag task between columns, verify status persists
- **US2**: Create diverse tasks, verify charts display aggregated data
- **US3**: Switch workspaces, verify data filtering works
- **US4**: View billing page on mobile and desktop, verify responsiveness
- **US5**: Create/update tasks, verify activities appear in feed

**Suggested MVP Scope**: Phase 1-3 (Setup + Foundational + Kanban Board) = 49 tasks for core functionality

---

## Notes

- **[P]** tasks = different files, no dependencies within phase
- **[Story]** label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- **Foundational phase (Phase 2) is CRITICAL** - all user stories depend on it
- Use specialized agents as outlined in plan.md:
  - `neon-db-manager`: Database models and migrations (T006-T017)
  - `fastapi-backend-architect`: Backend APIs and services (T018-T026, T035-T038, T050-T056, T067-T076, T092-T096)
  - `nextjs-ui-builder`: Frontend components and pages (T027-T034, T039-T049, T057-T066, T077-T084, T085-T091, T097-T102)

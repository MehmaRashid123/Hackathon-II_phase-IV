---
description: "Task list for Frontend Dashboard & Task Management UI implementation"
---

# Tasks: Frontend Dashboard & Task Management UI

**Input**: Design documents from `/specs/003-frontend-dashboard/`
**Prerequisites**: plan.md (complete), spec.md (complete)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Frontend**: `frontend/` directory at repository root
- All paths relative to project root: `/mnt/c/Users/HP/Desktop/Hackathon-II/phase-II/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create frontend directory structure per plan.md (app/, components/, lib/)
- [ ] T002 Initialize Next.js 16+ TypeScript project with Better Auth dependencies in frontend/
- [ ] T003 [P] Configure Tailwind CSS 3+ in frontend/tailwind.config.ts
- [ ] T004 [P] Setup TypeScript configuration in frontend/tsconfig.json with strict mode
- [ ] T005 [P] Create environment template frontend/.env.local.example with NEXT_PUBLIC_API_URL

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T006 Create TypeScript type definitions for Task entity in frontend/lib/types/task.ts
- [ ] T007 [P] Create TypeScript type definitions for API contracts in frontend/lib/types/api.ts
- [ ] T008 [P] Create TypeScript type definitions for User entity in frontend/lib/types/user.ts
- [ ] T009 Implement centralized API client with JWT injection in frontend/lib/api/client.ts
- [ ] T010 Implement Better Auth integration helpers in frontend/lib/api/auth.ts
- [ ] T011 Implement task API methods (CRUD) in frontend/lib/api/tasks.ts
- [ ] T012 [P] Create useAuth custom hook in frontend/lib/hooks/useAuth.ts
- [ ] T013 [P] Create useToast custom hook in frontend/lib/hooks/useToast.ts
- [ ] T014 [P] Create client-side validation utilities in frontend/lib/utils/validation.ts
- [ ] T015 [P] Create error message formatting utilities in frontend/lib/utils/errors.ts
- [ ] T016 [P] Create base Button component in frontend/components/ui/Button.tsx
- [ ] T017 [P] Create base Input component in frontend/components/ui/Input.tsx
- [ ] T018 [P] Create base Modal component in frontend/components/ui/Modal.tsx
- [ ] T019 [P] Create base Spinner component in frontend/components/ui/Spinner.tsx
- [ ] T020 [P] Create base Toast component in frontend/components/ui/Toast.tsx
- [ ] T021 [P] Create responsive Container component in frontend/components/layout/Container.tsx
- [ ] T022 Create root layout with Tailwind imports in frontend/app/layout.tsx
- [ ] T023 Create global error boundary in frontend/app/error.tsx
- [ ] T024 [P] Create Navbar component with user info and logout in frontend/components/layout/Navbar.tsx

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Authenticated Task List View (Priority: P1) 🎯 MVP

**Goal**: Display all user's tasks immediately after login with empty state handling

**Independent Test**: Log in with valid credentials, verify task list displays correctly. Create tasks via API, refresh page, verify tasks persist and display.

### Implementation for User Story 1

- [ ] T025 [P] [US1] Create EmptyState component in frontend/components/tasks/EmptyState.tsx
- [ ] T026 [P] [US1] Create TaskItem component with completion checkbox in frontend/components/tasks/TaskItem.tsx
- [ ] T027 [US1] Create TaskList container component with data fetching in frontend/components/tasks/TaskList.tsx
- [ ] T028 [US1] Create useTasks custom hook with list fetching in frontend/lib/hooks/useTasks.ts
- [ ] T029 [US1] Create dashboard layout with Navbar in frontend/app/(dashboard)/layout.tsx
- [ ] T030 [US1] Create main dashboard page with TaskList in frontend/app/(dashboard)/page.tsx
- [ ] T031 [US1] Implement authentication guard middleware to redirect unauthenticated users in frontend/middleware.ts
- [ ] T032 [US1] Add loading states and error handling to TaskList component
- [ ] T033 [US1] Apply responsive Tailwind CSS styling for mobile/tablet/desktop breakpoints

**Checkpoint**: At this point, User Story 1 should be fully functional - users can log in and see their task list

---

## Phase 4: User Story 2 - Create New Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to quickly add new tasks with title and description

**Independent Test**: Submit task creation form with valid data, verify new task appears in list and persists after page refresh. Test validation errors for empty title.

### Implementation for User Story 2

- [ ] T034 [P] [US2] Create TaskForm component for add/edit with validation in frontend/components/tasks/TaskForm.tsx
- [ ] T035 [US2] Add createTask mutation to useTasks hook with optimistic update in frontend/lib/hooks/useTasks.ts
- [ ] T036 [US2] Integrate TaskForm into dashboard page for task creation in frontend/app/(dashboard)/page.tsx
- [ ] T037 [US2] Implement client-side form validation (title required, max lengths) in TaskForm
- [ ] T038 [US2] Add error handling with toast notifications for API failures
- [ ] T039 [US2] Implement optimistic UI update - show task immediately before API confirms
- [ ] T040 [US2] Add success toast notification after task creation
- [ ] T041 [US2] Clear form inputs after successful task creation

**Checkpoint**: At this point, User Stories 1 AND 2 should both work - users can view and create tasks

---

## Phase 5: User Story 3 - Toggle Task Completion (Priority: P1) 🎯 MVP

**Goal**: Allow users to mark tasks complete/incomplete with single click

**Independent Test**: Click checkbox on incomplete task, verify it toggles to complete visually and persists. Click again to toggle back to incomplete.

### Implementation for User Story 3

- [ ] T042 [US3] Add toggleComplete mutation to useTasks hook in frontend/lib/hooks/useTasks.ts
- [ ] T043 [US3] Implement checkbox click handler in TaskItem component
- [ ] T044 [US3] Add optimistic UI update for instant completion toggle feedback
- [ ] T045 [US3] Implement rollback mechanism if API request fails
- [ ] T046 [US3] Add visual styling for completed tasks (strikethrough, opacity) in TaskItem
- [ ] T047 [US3] Add error toast notification if toggle fails
- [ ] T048 [US3] Ensure completion status persists after page refresh

**Checkpoint**: MVP complete - users can view, create, and toggle task completion

---

## Phase 6: User Story 4 - Edit Existing Tasks (Priority: P2)

**Goal**: Enable users to modify task title and description

**Independent Test**: Click edit button on existing task, modify title, save, verify changes persist. Test cancel functionality and validation errors.

### Implementation for User Story 4

- [ ] T049 [US4] Add edit mode support to TaskForm component (pre-populate fields)
- [ ] T050 [US4] Add updateTask mutation to useTasks hook in frontend/lib/hooks/useTasks.ts
- [ ] T051 [US4] Add edit button to TaskItem component
- [ ] T052 [US4] Implement modal or inline edit UI for task editing
- [ ] T053 [US4] Add cancel functionality to discard changes
- [ ] T054 [US4] Implement save handler with optimistic update
- [ ] T055 [US4] Add validation to prevent empty title on update
- [ ] T056 [US4] Add success/error toast notifications for edit operations

**Checkpoint**: Users can now view, create, toggle, and edit tasks

---

## Phase 7: User Story 5 - Delete Tasks (Priority: P2)

**Goal**: Allow users to permanently remove tasks with confirmation

**Independent Test**: Click delete button, verify confirmation dialog appears. Confirm deletion, verify task is removed from UI and database. Test cancel functionality.

### Implementation for User Story 5

- [ ] T057 [P] [US5] Create TaskDeleteConfirm modal component in frontend/components/tasks/TaskDeleteConfirm.tsx
- [ ] T058 [US5] Add deleteTask mutation to useTasks hook in frontend/lib/hooks/useTasks.ts
- [ ] T059 [US5] Add delete button to TaskItem component
- [ ] T060 [US5] Implement confirmation dialog flow (show modal on delete click)
- [ ] T061 [US5] Add confirm handler to execute deletion with optimistic update
- [ ] T062 [US5] Add cancel handler to close modal without deleting
- [ ] T063 [US5] Implement rollback if API deletion fails
- [ ] T064 [US5] Add success/error toast notifications for delete operations
- [ ] T065 [US5] Remove task from UI immediately on successful deletion

**Checkpoint**: All CRUD operations now functional - users can view, create, toggle, edit, and delete tasks

---

## Phase 8: User Story 6 - Responsive Mobile Experience (Priority: P2)

**Goal**: Ensure dashboard works seamlessly on mobile devices

**Independent Test**: Access dashboard on mobile device or browser dev tools. Verify layout adapts to screen width, all controls are touch-friendly (44px minimum), no horizontal scrolling.

### Implementation for User Story 6

- [ ] T066 [P] [US6] Apply mobile-first Tailwind breakpoints to TaskList component (sm:, md:, lg:)
- [ ] T067 [P] [US6] Apply mobile-first Tailwind breakpoints to TaskItem component
- [ ] T068 [P] [US6] Apply mobile-first Tailwind breakpoints to TaskForm component
- [ ] T069 [P] [US6] Apply mobile-first Tailwind breakpoints to Navbar component
- [ ] T070 [P] [US6] Ensure all buttons and controls have minimum 44px touch targets
- [ ] T071 [US6] Test TaskDeleteConfirm modal on mobile (full-screen or bottom sheet)
- [ ] T072 [US6] Test responsive layout at 320px (mobile), 768px (tablet), 1024px (desktop), 1920px (wide)
- [ ] T073 [US6] Fix any horizontal scrolling issues on mobile
- [ ] T074 [US6] Ensure form inputs are properly sized and accessible on mobile keyboards

**Checkpoint**: Application is now fully responsive across all device sizes

---

## Phase 9: Authentication Pages (Foundation Dependency)

**Goal**: Provide login and signup pages for Better Auth integration

**Independent Test**: Navigate to /login and /signup, verify forms render. Submit valid credentials, verify redirect to dashboard on success.

### Implementation for Authentication

- [ ] T075 [P] Create login page in frontend/app/(auth)/login/page.tsx
- [ ] T076 [P] Create signup page in frontend/app/(auth)/signup/page.tsx
- [ ] T077 Integrate Better Auth signin flow in login page
- [ ] T078 Integrate Better Auth signup flow in signup page
- [ ] T079 Add form validation for email and password fields
- [ ] T080 Add loading states during authentication
- [ ] T081 Add error handling for invalid credentials or network failures
- [ ] T082 Implement redirect to dashboard after successful authentication
- [ ] T083 Add "Remember me" functionality if supported by Better Auth

**Checkpoint**: Complete authentication flow - users can sign up, log in, and access dashboard

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T084 [P] Add keyboard shortcuts for common actions (Enter to submit forms, Escape to close modals)
- [ ] T085 [P] Add ARIA labels and accessibility attributes for screen readers
- [ ] T086 [P] Implement focus management for modals and forms
- [ ] T087 Performance optimization - memoize TaskItem components with React.memo
- [ ] T088 Performance optimization - implement virtual scrolling for 1000+ tasks if needed
- [ ] T089 [P] Add loading skeleton for task list initial load
- [ ] T090 [P] Improve error messages with more specific context
- [ ] T091 Security review - ensure no XSS vulnerabilities in user input rendering
- [ ] T092 Test JWT token expiration handling - verify redirect to login on 401
- [ ] T093 Test user isolation - create multiple users, verify data separation
- [ ] T094 Cross-browser testing on Chrome, Firefox, Safari
- [ ] T095 Network throttling tests for slow connections (3G simulation)
- [ ] T096 [P] Create README.md with setup instructions in frontend/
- [ ] T097 Validate against quickstart.md requirements (when created)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - US1 (Task List) - No dependencies on other stories
  - US2 (Create Tasks) - Depends on US1 (needs TaskList to display created tasks)
  - US3 (Toggle Complete) - Depends on US1 (needs TaskItem component)
  - US4 (Edit Tasks) - Depends on US1 and US2 (needs TaskItem and TaskForm)
  - US5 (Delete Tasks) - Depends on US1 (needs TaskItem component)
  - US6 (Responsive) - Depends on US1-5 (styles all components)
- **Authentication (Phase 9)**: Depends on Foundational - Can run in parallel with user stories
- **Polish (Phase 10)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - Foundation for all other stories
- **User Story 2 (P1)**: Depends on US1 completion (uses TaskList to display created tasks)
- **User Story 3 (P1)**: Depends on US1 completion (uses TaskItem component)
- **User Story 4 (P2)**: Depends on US1 and US2 (uses TaskItem and TaskForm)
- **User Story 5 (P2)**: Depends on US1 completion (uses TaskItem component)
- **User Story 6 (P2)**: Depends on US1-5 (applies responsive styling to all components)

### Within Each User Story

- UI components before hooks
- Hooks before page integration
- Core implementation before optimistic updates
- Error handling after core functionality
- Responsive styling can be added incrementally or as dedicated phase

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (5 tasks)
- Most Foundational tasks marked [P] can run in parallel (15 tasks)
- Within User Story 1: T025, T026 can run in parallel (2 tasks)
- Within User Story 2: T034 runs independently
- Within User Story 5: T057 runs independently
- Within User Story 6: T066-T070 can run in parallel (5 tasks)
- Within Authentication: T075, T076 can run in parallel (2 tasks)
- Within Polish: T084-T086, T089, T090, T096 can run in parallel (6 tasks)

**Total parallel opportunities**: ~35 tasks can potentially run concurrently if team capacity allows

---

## Parallel Example: Foundational Phase

```bash
# Launch all UI component tasks together:
Task: "Create base Button component in frontend/components/ui/Button.tsx"
Task: "Create base Input component in frontend/components/ui/Input.tsx"
Task: "Create base Modal component in frontend/components/ui/Modal.tsx"
Task: "Create base Spinner component in frontend/components/ui/Spinner.tsx"
Task: "Create base Toast component in frontend/components/ui/Toast.tsx"

# Launch all TypeScript type definition tasks together:
Task: "Create TypeScript type definitions for API contracts in frontend/lib/types/api.ts"
Task: "Create TypeScript type definitions for User entity in frontend/lib/types/user.ts"

# Launch all utility tasks together:
Task: "Create client-side validation utilities in frontend/lib/utils/validation.ts"
Task: "Create error message formatting utilities in frontend/lib/utils/errors.ts"
```

---

## Implementation Strategy

### MVP First (User Stories 1, 2, 3 Only)

1. Complete Phase 1: Setup (5 tasks)
2. Complete Phase 2: Foundational (19 tasks) - CRITICAL
3. Complete Phase 9: Authentication (9 tasks)
4. Complete Phase 3: User Story 1 - Task List View (9 tasks)
5. Complete Phase 4: User Story 2 - Create Tasks (8 tasks)
6. Complete Phase 5: User Story 3 - Toggle Complete (7 tasks)
7. **STOP and VALIDATE**: Test MVP independently (view, create, toggle)
8. Deploy/demo if ready

**MVP Total**: 57 tasks

### Incremental Delivery

1. Complete Setup + Foundational + Authentication → Foundation ready (33 tasks)
2. Add User Story 1 → Test independently → Deploy/Demo (9 tasks)
3. Add User Story 2 → Test independently → Deploy/Demo (8 tasks)
4. Add User Story 3 → Test independently → Deploy/Demo (7 tasks) **[MVP COMPLETE]**
5. Add User Story 4 → Test independently → Deploy/Demo (8 tasks)
6. Add User Story 5 → Test independently → Deploy/Demo (9 tasks)
7. Add User Story 6 → Test independently → Deploy/Demo (9 tasks)
8. Polish Phase → Final release (14 tasks)

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (24 tasks)
2. Once Foundational is done:
   - Developer A: Authentication pages (9 tasks)
   - Developer B: User Story 1 (9 tasks)
3. After US1 complete:
   - Developer A: User Story 2 (8 tasks)
   - Developer B: User Story 3 (7 tasks)
4. Continue with remaining stories
5. Final polish together

---

## Task Summary

**Total Tasks**: 97 tasks

**Tasks by Phase**:
- Phase 1 (Setup): 5 tasks
- Phase 2 (Foundational): 19 tasks
- Phase 3 (US1 - Task List): 9 tasks
- Phase 4 (US2 - Create Tasks): 8 tasks
- Phase 5 (US3 - Toggle Complete): 7 tasks
- Phase 6 (US4 - Edit Tasks): 8 tasks
- Phase 7 (US5 - Delete Tasks): 9 tasks
- Phase 8 (US6 - Responsive): 9 tasks
- Phase 9 (Authentication): 9 tasks
- Phase 10 (Polish): 14 tasks

**Tasks by Priority**:
- P1 (MVP): 57 tasks (Phases 1, 2, 3, 4, 5, 9)
- P2 (Enhancements): 26 tasks (Phases 6, 7, 8)
- Polish: 14 tasks (Phase 10)

**Parallel Opportunities**: 35 tasks marked [P] can run concurrently

**Suggested MVP Scope**: Phases 1, 2, 3, 4, 5, 9 (57 tasks total)

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- MVP includes core functionality: view tasks, create tasks, toggle completion
- Enhancements add editing, deletion, and responsive mobile experience
- Authentication is required foundation for all user stories

# Tasks: Backend Task Management API

**Input**: Design documents from `/specs/002-task-api/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Tests**: Not explicitly requested - focusing on implementation tasks only.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4, US5, US6)
- Include exact file paths in descriptions

## Path Conventions

- **Backend structure**: `backend/src/` (FastAPI application)
- All paths relative to repository root

---

## Phase 1: Setup (Task API Infrastructure)

**Purpose**: Initialize Task API module structure

- [ ] T001 Create Task API directory structure in `backend/src/`: `models/`, `schemas/`, `api/`, `services/`
- [ ] T002 [P] Verify JWT authentication middleware exists from Spec 001 in `backend/src/middleware/auth.py`
- [ ] T003 [P] Verify database connection configured from Spec 001 in `backend/src/database.py`

---

## Phase 2: Foundational (Task Model & Schemas)

**Purpose**: Core Task entity and request/response schemas that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Task Data Model

- [ ] T004 Create Task SQLModel in `backend/src/models/task.py` with fields (id, title, description, is_completed, created_at, updated_at, user_id)
- [ ] T005 Add foreign key constraint `user_id` → `users.id` with ON DELETE CASCADE in Task model
- [ ] T006 Add unique constraint and indexes on Task model (user_id index, composite user_id+created_at index)
- [ ] T007 Generate Alembic migration for Task table: `alembic revision --autogenerate -m "create tasks table"`
- [ ] T008 Review and apply migration: `alembic upgrade head`

### Pydantic Schemas

- [ ] T009 [P] Create TaskCreate schema in `backend/src/schemas/task_schemas.py` (title: str 1-500 chars, description: str 0-5000 chars optional)
- [ ] T010 [P] Create TaskUpdate schema in `backend/src/schemas/task_schemas.py` (title: Optional[str], description: Optional[str])
- [ ] T011 [P] Create TaskResponse schema in `backend/src/schemas/task_schemas.py` (id, title, description, is_completed, created_at, updated_at, user_id)

### Authentication Dependencies

- [ ] T012 Create `validate_user_id` dependency in `backend/src/middleware/auth.py` to verify URL user_id matches JWT token user_id (raise HTTP 403 if mismatch)

### Service Layer

- [ ] T013 Create TaskService class in `backend/src/services/task_service.py` with user isolation pattern
- [ ] T014 Implement `get_user_tasks` method in TaskService (filter by user_id, order by created_at DESC)
- [ ] T015 Implement `create_task` method in TaskService (validate user_id, set defaults, save to DB)
- [ ] T016 Implement `get_task_by_id` method in TaskService (filter by id AND user_id, raise 404 if not found)
- [ ] T017 Implement `update_task` method in TaskService (verify ownership, update fields, raise 403/404 on errors)
- [ ] T018 Implement `delete_task` method in TaskService (verify ownership, delete from DB, raise 403/404 on errors)
- [ ] T019 Implement `toggle_task_completion` method in TaskService (flip is_completed boolean, update updated_at)

**Checkpoint**: Foundation ready - all 6 user stories can now be implemented in parallel

---

## Phase 3: User Story 1 - Retrieve Task List (Priority: P1) 🎯 MVP

**Goal**: Users can fetch all their tasks via GET `/api/{user_id}/tasks`

**Independent Test**: Authenticate → GET `/api/{user_id}/tasks` → Verify all user's tasks returned with HTTP 200

### Implementation for User Story 1

- [ ] T020 [US1] Create tasks router in `backend/src/api/tasks.py` and register with FastAPI app
- [ ] T021 [US1] Implement GET `/api/{user_id}/tasks` endpoint in `backend/src/api/tasks.py`
- [ ] T022 [US1] Apply `get_current_user_id` and `validate_user_id` dependencies to endpoint
- [ ] T023 [US1] Call `TaskService.get_user_tasks(user_id)` in endpoint handler
- [ ] T024 [US1] Return list of TaskResponse objects with HTTP 200 status
- [ ] T025 [US1] Handle empty list case (return empty array with HTTP 200)
- [ ] T026 [US1] Add endpoint to FastAPI OpenAPI documentation with description and examples

**Checkpoint**: MVP complete - users can view their task list

---

## Phase 4: User Story 2 - Create New Task (Priority: P1)

**Goal**: Users can create new tasks via POST `/api/{user_id}/tasks`

**Independent Test**: Authenticate → POST `/api/{user_id}/tasks` with title → Verify task created with HTTP 201

### Implementation for User Story 2

- [ ] T027 [US2] Implement POST `/api/{user_id}/tasks` endpoint in `backend/src/api/tasks.py`
- [ ] T028 [US2] Apply `get_current_user_id` and `validate_user_id` dependencies
- [ ] T029 [US2] Accept TaskCreate schema as request body with Pydantic validation
- [ ] T030 [US2] Call `TaskService.create_task(user_id, task_data)` in handler
- [ ] T031 [US2] Return TaskResponse with HTTP 201 Created status
- [ ] T032 [US2] Handle validation errors (return HTTP 422 with error details)
- [ ] T033 [US2] Add endpoint to OpenAPI docs with request/response examples

**Checkpoint**: Users can create and list tasks

---

## Phase 5: User Story 3 - Update Task (Priority: P2)

**Goal**: Users can update task details via PUT `/api/{user_id}/tasks/{id}`

**Independent Test**: Create task → PUT `/api/{user_id}/tasks/{id}` with new data → Verify task updated with HTTP 200

### Implementation for User Story 3

- [ ] T034 [US3] Implement PUT `/api/{user_id}/tasks/{id}` endpoint in `backend/src/api/tasks.py`
- [ ] T035 [US3] Apply `get_current_user_id` and `validate_user_id` dependencies
- [ ] T036 [US3] Accept TaskUpdate schema as request body
- [ ] T037 [US3] Call `TaskService.update_task(user_id, task_id, update_data)` in handler
- [ ] T038 [US3] Return updated TaskResponse with HTTP 200 status
- [ ] T039 [US3] Handle task not found (return HTTP 404)
- [ ] T040 [US3] Handle ownership violation (return HTTP 403)
- [ ] T041 [US3] Add endpoint to OpenAPI docs

**Checkpoint**: Full task editing works

---

## Phase 6: User Story 4 - Toggle Task Completion (Priority: P2)

**Goal**: Users can mark tasks complete/incomplete via PATCH `/api/{user_id}/tasks/{id}/complete`

**Independent Test**: Create task → PATCH `/api/{user_id}/tasks/{id}/complete` → Verify is_completed toggled

### Implementation for User Story 4

- [ ] T042 [US4] Implement PATCH `/api/{user_id}/tasks/{id}/complete` endpoint in `backend/src/api/tasks.py`
- [ ] T043 [US4] Apply `get_current_user_id` and `validate_user_id` dependencies
- [ ] T044 [US4] Call `TaskService.toggle_task_completion(user_id, task_id)` in handler
- [ ] T045 [US4] Return updated TaskResponse with HTTP 200 status
- [ ] T046 [US4] Handle task not found (return HTTP 404)
- [ ] T047 [US4] Handle ownership violation (return HTTP 403)
- [ ] T048 [US4] Add endpoint to OpenAPI docs

**Checkpoint**: Task completion toggle functional

---

## Phase 7: User Story 5 - Get Single Task (Priority: P3)

**Goal**: Users can fetch specific task details via GET `/api/{user_id}/tasks/{id}`

**Independent Test**: Create task → GET `/api/{user_id}/tasks/{id}` → Verify task details returned

### Implementation for User Story 5

- [ ] T049 [US5] Implement GET `/api/{user_id}/tasks/{id}` endpoint in `backend/src/api/tasks.py`
- [ ] T050 [US5] Apply `get_current_user_id` and `validate_user_id` dependencies
- [ ] T051 [US5] Call `TaskService.get_task_by_id(user_id, task_id)` in handler
- [ ] T052 [US5] Return TaskResponse with HTTP 200 status
- [ ] T053 [US5] Handle task not found (return HTTP 404)
- [ ] T054 [US5] Handle ownership violation (return HTTP 403)
- [ ] T055 [US5] Add endpoint to OpenAPI docs

**Checkpoint**: Single task retrieval works

---

## Phase 8: User Story 6 - Delete Task (Priority: P3)

**Goal**: Users can permanently delete tasks via DELETE `/api/{user_id}/tasks/{id}`

**Independent Test**: Create task → DELETE `/api/{user_id}/tasks/{id}` → Verify task deleted with HTTP 204

### Implementation for User Story 6

- [ ] T056 [US6] Implement DELETE `/api/{user_id}/tasks/{id}` endpoint in `backend/src/api/tasks.py`
- [ ] T057 [US6] Apply `get_current_user_id` and `validate_user_id` dependencies
- [ ] T058 [US6] Call `TaskService.delete_task(user_id, task_id)` in handler
- [ ] T059 [US6] Return HTTP 204 No Content on successful deletion
- [ ] T060 [US6] Handle task not found (return HTTP 404)
- [ ] T061 [US6] Handle ownership violation (return HTTP 403)
- [ ] T062 [US6] Add endpoint to OpenAPI docs

**Checkpoint**: All CRUD operations complete

---

## Phase 9: Polish & Validation

**Purpose**: Error handling, validation, and final testing

### Error Handling

- [ ] T063 [P] Add global exception handler for database errors in `backend/src/main.py` (return HTTP 503 if DB unavailable)
- [ ] T064 [P] Add error response models to OpenAPI schema for consistency
- [ ] T065 [P] Verify all endpoints return correct HTTP status codes per spec

### Data Validation

- [ ] T066 [P] Test TaskCreate validation: empty title returns HTTP 422
- [ ] T067 [P] Test TaskCreate validation: title > 500 chars returns HTTP 422
- [ ] T068 [P] Test TaskCreate validation: description > 5000 chars returns HTTP 422
- [ ] T069 [P] Test user isolation: user A cannot access user B's tasks (HTTP 403)

### Integration Testing

- [ ] T070 Manual test: Create task → Verify in database
- [ ] T071 Manual test: List tasks → Verify all user's tasks returned
- [ ] T072 Manual test: Update task → Verify changes persist
- [ ] T073 Manual test: Toggle completion → Verify status changes
- [ ] T074 Manual test: Delete task → Verify removed from database
- [ ] T075 Manual test: Access another user's task → Verify HTTP 403 returned

### Documentation

- [ ] T076 [P] Update OpenAPI docs with all 6 endpoints
- [ ] T077 [P] Add example requests/responses to OpenAPI schema
- [ ] T078 [P] Document error responses in OpenAPI schema

---

## Dependencies & Execution Strategy

### User Story Dependencies

**After Foundation (Phase 2) completes, ALL user stories are INDEPENDENT**:
- US1 (List Tasks) - Can implement immediately
- US2 (Create Task) - Can implement immediately
- US3 (Update Task) - Can implement immediately
- US4 (Toggle Complete) - Can implement immediately
- US5 (Get Single Task) - Can implement immediately
- US6 (Delete Task) - Can implement immediately

**Recommended Order** (by priority):
1. Phase 1: Setup (3 tasks)
2. Phase 2: Foundation (16 tasks) - BLOCKING
3. Phase 3: US1 - List (7 tasks) - MVP
4. Phase 4: US2 - Create (7 tasks) - MVP
5. Phase 5: US3 - Update (8 tasks)
6. Phase 6: US4 - Toggle (7 tasks)
7. Phase 7: US5 - Get Single (7 tasks)
8. Phase 8: US6 - Delete (7 tasks)
9. Phase 9: Polish (16 tasks)

### Parallel Execution Opportunities

**Within Foundation (Phase 2)**:
- T009, T010, T011 (all schemas) can run in parallel

**After Foundation Complete**:
- ALL user story phases (3-8) can run in PARALLEL since they're independent

**Within Polish (Phase 9)**:
- T063-T078 (all polish tasks) can run in parallel

### MVP Scope (Minimum Viable Product)

**Suggested MVP**: Phase 1 + Phase 2 + Phase 3 + Phase 4

This delivers:
- ✅ Task model and database schema
- ✅ List all tasks (GET endpoint)
- ✅ Create new tasks (POST endpoint)
- ✅ Full authentication and user isolation
- ✅ OpenAPI documentation

**Total MVP Tasks**: 33 tasks (3 + 16 + 7 + 7)

**Next increment**: Add US3 (Update) + US4 (Toggle) = +15 tasks
**Next increment**: Add US5 (Get) + US6 (Delete) = +14 tasks
**Full feature**: Complete all phases = 78 tasks

---

## Task Summary

**Total Tasks**: 78
- Setup (Phase 1): 3 tasks
- Foundation (Phase 2): 16 tasks (BLOCKING)
- User Story 1 - List (Phase 3): 7 tasks - **MVP**
- User Story 2 - Create (Phase 4): 7 tasks - **MVP**
- User Story 3 - Update (Phase 5): 8 tasks
- User Story 4 - Toggle (Phase 6): 7 tasks
- User Story 5 - Get Single (Phase 7): 7 tasks
- User Story 6 - Delete (Phase 8): 7 tasks
- Polish (Phase 9): 16 tasks

**Parallel Opportunities**: All 6 user stories can be implemented in parallel after Foundation

**Agent Delegation**: All tasks → `fastapi-backend-architect` agent

**Estimated Completion**:
- MVP (US1+US2): 33 tasks
- With US3+US4: 48 tasks
- Full CRUD: 62 tasks
- With Polish: 78 tasks

---

## Implementation Notes

### File Organization

```
backend/
├── src/
│   ├── models/
│   │   └── task.py              # Task SQLModel
│   ├── schemas/
│   │   └── task_schemas.py      # TaskCreate, TaskUpdate, TaskResponse
│   ├── api/
│   │   └── tasks.py             # All 6 task endpoints
│   ├── services/
│   │   └── task_service.py      # Task business logic with user isolation
│   ├── middleware/
│   │   └── auth.py              # JWT verification + validate_user_id
│   └── main.py                  # Register tasks router
└── alembic/
    └── versions/
        └── ###_create_tasks_table.py
```

### API Endpoints Summary

| Endpoint | Method | Handler | User Story |
|----------|--------|---------|------------|
| `/api/{user_id}/tasks` | GET | List all user's tasks | US1 |
| `/api/{user_id}/tasks` | POST | Create new task | US2 |
| `/api/{user_id}/tasks/{id}` | PUT | Update task | US3 |
| `/api/{user_id}/tasks/{id}/complete` | PATCH | Toggle completion | US4 |
| `/api/{user_id}/tasks/{id}` | GET | Get single task | US5 |
| `/api/{user_id}/tasks/{id}` | DELETE | Delete task | US6 |

### Testing Checklist

- [ ] Database migration creates tasks table
- [ ] Task has user_id foreign key with CASCADE delete
- [ ] User A can create tasks
- [ ] User A can list only their own tasks
- [ ] User A cannot access User B's tasks (403)
- [ ] Update task with valid data succeeds
- [ ] Update non-existent task returns 404
- [ ] Toggle completion flips boolean
- [ ] Delete task removes from database
- [ ] All endpoints return correct status codes
- [ ] OpenAPI docs accessible at `/docs`

---

## Next Steps

1. ✅ Review this task list for completeness
2. Run `/sp.implement` to begin execution via `fastapi-backend-architect` agent
3. Execute tasks in phase order
4. Test each user story independently after completion
5. Verify OpenAPI documentation
6. Create pull request

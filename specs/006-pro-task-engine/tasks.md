# Tasks: Pro Task Engine Implementation

## Feature Branch: `006-pro-task-engine`
## Created: 2026-02-05
## Status: Pending
## Feature Spec: [./spec.md](specs/006-pro-task-engine/spec.md)
## Implementation Plan: [./plan.md](specs/006-pro-task-engine/plan.md)

## Overview

This document outlines the tasks required to implement the "Pro Task Engine" feature, transforming the basic todo app into an advanced task management system with subtasks, rich metadata, dependencies, and collaboration features. Tasks are organized by user story to enable independent implementation and testing.

## Phase 1: Setup

This phase focuses on initial environment configuration and basic setup.

- [ ] T001 Ensure `DATABASE_URL`, `JWT_SECRET`, and `ALLOWED_ORIGINS` are configured in `.env` (manual check).
- [ ] T002 Run `alembic upgrade head` in `backend/` to apply schema changes after model definitions.

## Phase 2: Foundational Data Models and Enumerations

This phase involves defining the core data models and enumerations that are prerequisites for all user stories.

- [x] T003 Implement `PriorityEnum` and `StatusEnum` in `backend/src/models/task.py`.
- [x] T004 Update `backend/src/models/task.py` to include `parent_id: Optional[UUID]`, `priority: PriorityEnum`, `status: StatusEnum`, `due_date: Optional[datetime]`, `recurrence_rule: Optional[str]`, `section_id: Optional[UUID]`, `project_id: Optional[UUID]`.
- [x] T005 [P] Create `Project` model in `backend/src/models/project.py`.
- [ ] T006 [P] Create `Section` model in `backend/src/models/section.py`.
- [ ] T007 [P] Create `Comment` model in `backend/src/models/comment.py`.
- [ ] T008 [P] Create `Tag` model and `TaskTagLink` association model in `backend/src/models/tag.py`.
- [ ] T009 [P] Create `ActivityLog` model in `backend/src/models/activity_log.py`.
- [ ] T010 [P] Create `Dependency` model in `backend/src/models/dependency.py`.
- [ ] T011 [P] Create `FileAttachment` model in `backend/src/models/file_attachment.py`.
- [ ] T012 Generate Alembic migration for all new and updated models.

## Phase 3: User Story 1 - Manage Subtasks (P1)

**Goal**: As a user, I want to break down a main task into multiple subtasks, allowing for infinite nesting, so that I can organize complex work more granularly. I also want to see all subtasks associated with a parent task and easily navigate through the task hierarchy.

**Independent Test**: Create a parent task, add multiple levels of subtasks, and verify correct nesting and display of the task hierarchy via API and UI.

- [ ] T013 [US1] Implement recursive fetching for subtasks in `backend/src/services/task_service.py`.
- [ ] T014 [US1] Update `POST /api/{user_id}/tasks` to handle `parent_id` for subtask creation in `backend/src/api/tasks.py`.
- [ ] T015 [US1] Update `GET /api/{user_id}/tasks` to support `parent_id` and `include_subtasks` query parameters in `backend/src/api/tasks.py`.
- [ ] T016 [US1] Update `GET /api/{user_id}/tasks/{task_id}` to potentially include nested subtasks in `backend/src/api/tasks.py`.
- [ ] T017 [US1] Update `DELETE /api/{user_id}/tasks/{task_id}` to delete all associated subtasks in `backend/src/api/tasks.py`.
- [ ] T018 [US1] Create `SubtaskManager.tsx` component in `frontend/components/SubtaskManager.tsx`.
- [ ] T019 [US1] Integrate `SubtaskManager` into `frontend/app/dashboard/task/[id]/page.tsx`.

## Phase 4: User Story 2 - Prioritize and Categorize Tasks (P1)

**Goal**: As a user, I want to assign a priority (Low, Medium, High, Urgent), a status (To Do, In Progress, Review, Blocked, Done), and multiple labels/tags to my tasks and subtasks, so that I can easily organize, filter, and understand the urgency and progress of my work.

**Independent Test**: Create tasks with various priorities, statuses, and tags, then apply filters to verify correct display via API and UI.

- [ ] T020 [US2] Update `TaskCreateSchema` and `TaskUpdateSchema` in `backend/src/schemas/task_schemas.py` to include `priority`, `status`, `due_date`, `recurrence_rule`, `section_id`, `project_id`.
- [ ] T021 [US2] Update `POST /api/{user_id}/tasks` and `PUT /api/{user_id}/tasks/{task_id}` to handle new fields in `backend/src/api/tasks.py`.
- [ ] T022 [US2] Enhance `GET /api/{user_id}/tasks` to support filtering by `priority` and `status` via query parameters in `backend/src/api/tasks.py`.
- [ ] T023 [US2] Implement new API endpoints for Tags (`/api/{user_id}/tags`) in `backend/src/api/tags.py`.
- [ ] T024 [US2] Create `PriorityBadge.tsx` component in `frontend/components/PriorityBadge.tsx`.
- [ ] T025 [US2] Create `StatusDropdown.tsx` component in `frontend/components/StatusDropdown.tsx`.
- [ ] T026 [US2] Create `TagCloud.tsx` component in `frontend/components/TagCloud.tsx`.
- [ ] T027 [US2] Create `DueDateInput.tsx` component in `frontend/components/DueDateInput.tsx`.
- [ ] T028 [US2] Integrate `PriorityBadge`, `StatusDropdown`, `TagCloud`, `DueDateInput` into `frontend/app/dashboard/task/[id]/page.tsx`.

## Phase 5: User Story 3 - Track Task Progress and Collaboration (P2)

**Goal**: As a user, I want to see an activity log for each task, including status changes, comments, and other important events, so that I can track its history. I also want to prevent a task from starting if its dependent tasks are not complete, and add comments to tasks for collaboration.

**Independent Test**: Create tasks with dependencies, add comments, observe activity log via API and UI, and attempt to complete dependent tasks out of order to verify dependency logic.

- [ ] T029 [US3] Implement "Dependency Check" mechanism in `backend/src/services/task_service.py` before allowing status change.
- [ ] T030 [US3] Implement recurrence calculator in `backend/src/services/task_service.py`.
- [ ] T031 [US3] Implement `PATCH /api/{user_id}/tasks/{task_id}/complete` endpoint to handle subtask completion/uncompletion and dependency checks in `backend/src/api/tasks.py`.
- [ ] T032 [US3] Implement `POST /api/{user_id}/tasks/{task_id}/comments` and `GET /api/{user_id}/tasks/{task_id}/comments` endpoints in `backend/src/api/comments.py`.
- [ ] T033 [US3] Implement `GET /api/{user_id}/tasks/{task_id}/activity` endpoint in `backend/src/api/activity_logs.py`.
- [ ] T034 [US3] Implement `POST /api/{user_id}/tasks/{task_id}/dependencies` and `DELETE /api/{user_id}/tasks/{task_id}/dependencies/{dependency_id}` endpoints in `backend/src/api/dependencies.py`.
- [ ] T035 [US3] Create `ActivityLogView.tsx` component in `frontend/components/ActivityLogView.tsx`.
- [ ] T036 [US3] Create `CommentSection.tsx` component in `frontend/components/CommentSection.tsx`.
- [ ] T037 [US3] Integrate `ActivityLogView` and `CommentSection` into `frontend/app/dashboard/task/[id]/page.tsx`.

## Final Phase: Polish & Cross-Cutting Concerns

- [ ] T038 Review and refine Pydantic schemas for all new models and API responses in `backend/src/schemas/`.
- [ ] T039 Ensure robust user isolation for all new API endpoints and models.
- [ ] T040 Update `backend/src/main.py` to include new API routers.
- [ ] T041 Update OpenAPI documentation (`/docs`) for all new and updated endpoints.

## Dependencies

- Phase 1 must be completed before Phase 2.
- Phase 2 must be completed before Phase 3, Phase 4, and Phase 5.
- Phases 3, 4, and 5 can be worked on in parallel once Phase 2 is complete, but are listed in priority order.

## Parallel Execution Examples

- After Phase 2 is complete, T013, T014, T015, T020, T021, T022, T029, T030, T031 can be worked on in parallel as they primarily involve distinct backend files or logic.
- Frontend component tasks like T018, T024, T025, T026, T027, T035, T036 can often be developed in parallel once their respective API endpoints and data models are defined.

## Implementation Strategy

The implementation will follow an MVP-first approach, delivering each user story as a complete, independently testable increment. The core data model changes in Phase 2 are foundational and will be completed before moving to specific user stories.

## Summary

- Total task count: 41
- Tasks per user story:
    - US1: 7 tasks
    - US2: 9 tasks
    - US3: 9 tasks
- Parallel opportunities identified: Many tasks are marked with [P] within phases, indicating potential for parallel development.
- Independent test criteria for each story are outlined in their respective sections.
- Suggested MVP scope: Completion of Phase 1, Phase 2, and Phase 3 (User Story 1: Manage Subtasks).

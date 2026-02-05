# Implementation Plan: Pro Task Engine Implementation

**Feature Branch**: `001-pro-task-engine`
**Created**: 2026-02-05
**Status**: Draft
**Feature Spec**: [./spec.md](specs/001-pro-task-engine/spec.md)

## 1. Technical Context

This plan outlines the implementation strategy for the "Pro Task Engine" feature, which aims to transform the basic todo app into an advanced task management system. The core focus is on expanding the task data model to support subtasks, various metadata (priority, status, tags, recurrence, etc.), task dependencies, collaboration features (comments, activity logs), and an enhanced API to expose these capabilities. The frontend will consume these new APIs and introduce components for managing this rich task data.

**Key Technical Considerations:**
-   **Database Schema Evolution**: Significant changes to the `Task` model and introduction of several new models (`Comment`, `Tag`, `ActivityLog`, `Dependency`, `Section`, `Project`, `FileAttachment`). This requires careful Alembic migrations to avoid data loss.
-   **Recursive Relationships**: Handling self-referencing `parent_id` for subtasks in both database models and API responses.
-   **Complex Querying**: Implementing efficient filtering for tasks based on multiple criteria (priority, status, tags).
-   **Dependency Management**: Ensuring task progression respects defined dependencies.
-   **Recurrence Logic**: Designing a flexible and robust recurrence engine.
-   **User Isolation**: Maintaining strict data segregation for all new entities.

## 2. Constitution Check

This plan aligns with the project's constitution.

### II. Agentic Workflow
-   **Compliance**: Fully compliant. All implementation steps are delegated to specialized agents as per the constitution.
-   **Justification**: Each task is assigned to the most appropriate agent (`neon-db-manager`, `fastapi-backend-architect`, `nextjs-ui-builder`).

### III. Security First
-   **Compliance**: Fully compliant. User isolation, JWT verification, and secure handling of sensitive data (e.g., `user_id` in API paths) are central to the plan.
-   **Justification**: All new API endpoints and data models will enforce user isolation at the API and database levels.

### IV. Modern Stack with Strong Typing
-   **Compliance**: Fully compliant. SQLModel, Pydantic, FastAPI, and Next.js/TypeScript will be used throughout.
-   **Justification**: Leveraging the chosen stack's features for type safety and robust development.

### V. User Isolation
-   **Compliance**: Fully compliant. Explicit measures to filter data by authenticated user ID are integrated into the database and API design.
-   **Justification**: All new models will include `user_id` where applicable, and queries will enforce this.

### VII. Data Persistence
-   **Compliance**: Fully compliant. Neon Serverless PostgreSQL and SQLModel are central to the data management strategy, including Alembic migrations.
-   **Justification**: Ensuring data integrity and efficient storage for the expanded data model.

## 3. Architectural Decisions

### 3.1 Database Migration & Data Model Expansion

-   **Decision**: Update `backend/src/models/task.py` to include `parent_id` (ForeignKey to self, nullable for top-level tasks), `priority` (Enum), `status` (Enum), `due_date` (Optional DateTime), and `recurrence_rule` (String/JSONB to store recurrence patterns, NEEDS CLARIFICATION: exact format of recurrence_rule).
-   **Decision**: Create new SQLModel models for `Comment`, `Tag`, `ActivityLog`, `Dependency`, `Section`, `Project`, and `FileAttachment`. Each will include a `user_id` foreign key where applicable to maintain user isolation.
-   **Decision**: Utilize Alembic for generating and applying database migrations. Manual SQL will be avoided except for complex data transformations if absolutely necessary, which will be documented.
-   **Rationale**: SQLModel provides type safety and simplifies ORM operations. Alembic ensures controlled and reversible schema evolution. Foreign keys and `user_id` fields are critical for data integrity and user isolation.
-   **Alternatives Considered**:
    -   Using raw SQL for migrations: Rejected due to increased complexity and error proneness compared to Alembic.
    -   Storing recurrence rules as separate fields: Rejected in favor of a single rule string/JSONB for flexibility, to be parsed by application logic.

### 3.2 Service Layer Logic

-   **Decision**: Implement recursive fetching for subtasks within `backend/src/services/task_service.py` to efficiently retrieve full task hierarchies. This will likely involve a CTE (Common Table Expression) or multiple queries.
-   **Decision**: Introduce a "Dependency Check" mechanism in `task_service.py` before allowing a task's status to change to "In Progress" or "Done". This will query the `Dependency` model.
-   **Decision**: Develop a recurrence calculator within `task_service.py` that, upon completion of a recurring task, generates the next instance based on `recurrence_rule`.
-   **Rationale**: Centralizing business logic in the service layer promotes reusability and testability. Efficient subtask fetching is crucial for performance. Dependency checks and recurrence logic are core to the feature's advanced capabilities.
-   **Alternatives Considered**:
    -   Client-side subtask recursion: Rejected to avoid unnecessary data transfer and complexity on the frontend.
    -   Database-level triggers for dependencies/recurrence: Rejected to keep business logic in the application layer for flexibility and easier debugging.

### 3.3 Enhanced API

-   **Decision**: Update `backend/src/api/tasks.py` to accommodate new fields (priority, status, due_date, recurrence_rule) in existing Task CRUD operations.
-   **Decision**: Implement new API endpoints for `Comment` (`/api/{user_id}/tasks/{id}/comments`), `Tag` (`/api/{user_id}/tags`), `ActivityLog` (`/api/{user_id}/tasks/{id}/activity`), `Dependency` (`/api/{user_id}/tasks/{id}/dependencies`), `Section` (`/api/{user_id}/projects/{project_id}/sections`), `Project` (`/api/{user_id}/projects`), and `FileAttachment` (`/api/{user_id}/tasks/{id}/attachments`).
-   **Decision**: Enhance `GET /api/{user_id}/tasks` to support complex filtering by `priority`, `status`, and `tags` via query parameters.
-   **Decision**: Implement nested response schemas (Pydantic) to return subtasks alongside parent tasks where appropriate.
-   **Rationale**: Provides a clear and consistent interface for the frontend. Filtering and nested schemas are essential for the advanced UI.
-   **Alternatives Considered**:
    -   GraphQL API: Rejected due to project constraints and existing REST architecture.
    -   Separate microservices for each entity: Overkill for the current project scope.

### 3.4 Frontend Metadata Components

-   **Decision**: Create `frontend/components/PriorityBadge.tsx` to visually display task priority.
-   **Decision**: Create `frontend/components/StatusDropdown.tsx` to allow users to change task status, potentially with color-coding.
-   **Decision**: Create `frontend/components/TagCloud.tsx` or similar component to manage and display tags associated with a task, allowing add/remove.
-   **Decision**: Build `frontend/components/SubtaskManager.tsx` for displaying, adding, and managing subtasks within a task detail view.
-   **Decision**: Create `frontend/components/DueDateInput.tsx` for selecting a due date, potentially integrated with a reminder toggle.
-   **Decision**: Create `frontend/components/ActivityLogView.tsx` component to display the chronological activity log for a task.
-   **Decision**: Create `frontend/app/dashboard/task/[id]/page.tsx` for the task detail view, integrating the new components.
-   **Rationale**: Modular components promote reusability and maintainability, ensuring a rich and interactive user experience.

## 4. Data Model

**(This section will inform `specs/001-pro-task-engine/data-model.md`)**

### Existing `Task` Model (`backend/src/models/task.py`)
-   `id: Optional[UUID]` (Primary Key)
-   `user_id: UUID` (Foreign Key to `User.id`)
-   `title: str`
-   `description: Optional[str]`
-   `is_completed: bool`
-   `created_at: DateTime`
-   `updated_at: DateTime`
-   **NEW**: `parent_id: Optional[UUID]` (Foreign Key to `Task.id` for subtasks, `nullable=True`)
-   **NEW**: `priority: PriorityEnum` (Enum: Low, Medium, High, Urgent)
-   **NEW**: `status: StatusEnum` (Enum: To Do, In Progress, Review, Blocked, Done)
-   **NEW**: `due_date: Optional[datetime]`
-   **NEW**: `recurrence_rule: Optional[str]` (JSON string or specific format, e.g., "DAILY", "WEEKLY:MON,FRI")
-   **NEW**: `section_id: Optional[UUID]` (Foreign Key to `Section.id`)
-   **NEW**: `project_id: Optional[UUID]` (Foreign Key to `Project.id`)

### New Models (`backend/src/models/`)

-   **`PriorityEnum`**: Python Enum for task priorities (Low, Medium, High, Urgent).
-   **`StatusEnum`**: Python Enum for task statuses (To Do, In Progress, Review, Blocked, Done).

-   **`Project`**:
    -   `id: Optional[UUID]` (PK)
    -   `user_id: UUID` (FK to `User.id`)
    -   `name: str`
    -   `created_at: DateTime`
    -   `updated_at: DateTime`
    -   Relationships: `sections: List[Section]`, `tasks: List[Task]`

-   **`Section`**:
    -   `id: Optional[UUID]` (PK)
    -   `project_id: UUID` (FK to `Project.id`)
    -   `name: str`
    -   `order: int`
    -   Relationships: `tasks: List[Task]`

-   **`Comment`**:
    -   `id: Optional[UUID]` (PK)
    -   `task_id: UUID` (FK to `Task.id`)
    -   `user_id: UUID` (FK to `User.id`)
    -   `content: str`
    -   `created_at: DateTime`

-   **`Tag`**:
    -   `id: Optional[UUID]` (PK)
    -   `user_id: UUID` (FK to `User.id`)
    -   `name: str` (Unique per user)
    -   Relationships: Many-to-many with `Task`

-   **`TaskTagLink`**: (Association table for Many-to-Many `Task`-`Tag`)
    -   `task_id: UUID` (FK)
    -   `tag_id: UUID` (FK)

-   **`ActivityLog`**:
    -   `id: Optional[UUID]` (PK)
    -   `task_id: UUID` (FK to `Task.id`)
    -   `user_id: Optional[UUID]` (FK to `User.id`, nullable for system events)
    -   `event_type: str` (e.g., "status_changed", "comment_added", "priority_updated")
    -   `details: JSONB` (Stores event-specific data, e.g., `{"old_status": "To Do", "new_status": "In Progress"}`)
    -   `created_at: DateTime`

-   **`Dependency`**:
    -   `id: Optional[UUID]` (PK)
    -   `task_id: UUID` (FK to `Task.id`, the dependent task)
    -   `depends_on_task_id: UUID` (FK to `Task.id`, the prerequisite task)
    -   `user_id: UUID` (FK to `User.id`, for isolation)
    -   Unique constraint on (`task_id`, `depends_on_task_id`)

-   **`FileAttachment`**:
    -   `id: Optional[UUID]` (PK)
    -   `task_id: UUID` (FK to `Task.id`)
    -   `user_id: UUID` (FK to `User.id`)
    -   `filename: str`
    -   `file_type: str` (e.g., "image/png", "application/pdf")
    -   `url: str` (URL to storage, e.g., S3)
    -   `uploaded_at: DateTime`

## 5. API Contracts

**(This section will inform `specs/001-pro-task-engine/contracts/task-api-v2.openapi.yaml` and other contract files)**

### Updated Existing Endpoints (`backend/src/api/tasks.py`)

-   **`POST /api/{user_id}/tasks`**:
    -   **Request Body**: `TaskCreateSchema` (Pydantic model) - expanded to include `parent_id`, `priority`, `status`, `due_date`, `recurrence_rule`, `section_id`, `project_id`.
    -   **Response**: `TaskSchema` (Pydantic model) - expanded to reflect new fields.
-   **`GET /api/{user_id}/tasks`**:
    -   **Query Params**:
        -   `status: Optional[StatusEnum]`
        -   `priority: Optional[PriorityEnum]`
        -   `tag: Optional[str]` (filter by tag name)
        -   `parent_id: Optional[UUID]` (filter for top-level tasks or direct subtasks)
        -   `include_subtasks: Optional[bool]` (defaults to `False`, if `True` returns full hierarchy)
    -   **Response**: `List[TaskSchema]` (may include nested subtasks if `include_subtasks` is true).
-   **`GET /api/{user_id}/tasks/{task_id}`**:
    -   **Response**: `TaskSchema` (Pydantic model), potentially including nested subtasks.
-   **`PUT /api/{user_id}/tasks/{task_id}`**:
    -   **Request Body**: `TaskUpdateSchema` (Pydantic model) - expanded to include new updatable fields.
    -   **Response**: `TaskSchema`.
-   **`DELETE /api/{user_id}/tasks/{task_id}`**:
    -   **Response**: `{"message": "Task and all subtasks deleted"}`.
-   **`PATCH /api/{user_id}/tasks/{task_id}/complete`**:
    -   **Request Body**: `{"is_completed": bool}`
    -   **Behavior**:
        -   If setting to `True`, implicitly completes all subtasks.
        -   If setting to `False`, implicitly uncompletes all parent tasks up the hierarchy.
        -   Before completing, check dependencies. If `is_completed=True` and unfulfilled dependencies exist, return 400 Bad Request.
    -   **Response**: `TaskSchema`.

### New Endpoints

-   **`POST /api/{user_id}/tasks/{task_id}/comments`**:
    -   **Request Body**: `CommentCreateSchema` (Pydantic model: `content: str`)
    -   **Response**: `CommentSchema`
-   **`GET /api/{user_id}/tasks/{task_id}/comments`**:
    -   **Response**: `List[CommentSchema]`
-   **`POST /api/{user_id}/projects`**:
    -   **Request Body**: `ProjectCreateSchema` (`name: str`)
    -   **Response**: `ProjectSchema`
-   **`GET /api/{user_id}/projects`**:
    -   **Response**: `List[ProjectSchema]`
-   **`POST /api/{user_id}/projects/{project_id}/sections`**:
    -   **Request Body**: `SectionCreateSchema` (`name: str`, `order: int`)
    -   **Response**: `SectionSchema`
-   **`GET /api/{user_id}/tasks/{task_id}/activity`**:
    -   **Response**: `List[ActivityLogSchema]`
-   **`POST /api/{user_id}/tasks/{task_id}/dependencies`**:
    -   **Request Body**: `DependencyCreateSchema` (`depends_on_task_id: UUID`)
    -   **Response**: `DependencySchema`
-   **`DELETE /api/{user_id}/tasks/{task_id}/dependencies/{dependency_id}`**:
    -   **Response**: `{"message": "Dependency removed"}`

## 6. Frontend Components

**(This section will inform `frontend/components/` and `frontend/app/dashboard/` changes)**

-   **`frontend/components/PriorityBadge.tsx`**: React component to render task priority visually (e.g., colored badge).
-   **`frontend/components/StatusDropdown.tsx`**: React component for selecting and displaying task status, likely integrated with color-coding.
-   **`frontend/components/TagCloud.tsx`**: React component for displaying and managing tags associated with a task, allowing add/remove.
-   **`frontend/components/SubtaskManager.tsx`**: Complex React component for rendering a task's subtasks, allowing nested display, creation of new subtasks, and interaction with existing ones. Will likely be used in a Task Detail View.
-   **`frontend/components/DueDateInput.tsx`**: Input field for selecting a due date, potentially integrated with a reminder toggle.
-   **`frontend/components/ActivityLogView.tsx`**: Component to display the chronological activity log for a task.
-   **`frontend/app/dashboard/task/[id]/page.tsx`**: New page for detailed task view, integrating `SubtaskManager`, `PriorityBadge`, `StatusDropdown`, `TagCloud`, `DueDateInput`, `ActivityLogView`, and `CommentSection` components.

## 7. Quickstart

**(This section will inform `specs/001-pro-task-engine/quickstart.md`)**

1.  **Environment Setup**: Ensure `DATABASE_URL`, `JWT_SECRET`, and `ALLOWED_ORIGINS` are configured in `.env`.
2.  **Database Migration**: Run `alembic upgrade head` in the backend directory to apply schema changes.
3.  **Start Backend**: `uvicorn backend.src.main:app --reload`
4.  **Start Frontend**: `npm run dev` in the frontend directory.
5.  **Access UI**: Navigate to `http://localhost:3000` to interact with the new features.
6.  **Create Tasks**: Use the UI to create tasks, subtasks, assign priorities, statuses, tags, and set dependencies.
7.  **Test API Directly**: Use a tool like `curl` or Postman to test new API endpoints for filtering, comments, and activity logs.

## 8. Complexity Tracking

### Needs Clarification

-   **Recurrence Rule Format**: The exact string/JSONB format for `recurrence_rule` (e.g., iCal-like, simple "DAILY", "WEEKLY:MON,WED,FRI"). This impacts parsing logic.
    -   **Impact**: Data model flexibility, service layer parsing complexity, UI input forms.
    -   **Decision Point**: Define a clear and consistent schema for recurrence rules.
    -   **Implications**: Choosing a simple format limits future extensibility but simplifies implementation. A robust format (e.g., RRule) adds complexity but is highly flexible.

-   **Reminder Mechanism**: How reminders should be handled (e.g., server-side cron jobs, frontend polling, push notifications).
    -   **Impact**: Backend architecture, frontend real-time updates, potential external service integrations.
    -   **Decision Point**: Select a reminder delivery strategy.
    -   **Implications**: Server-side offers reliability but adds infrastructure. Frontend polling is simpler but less precise. Push notifications require additional setup.

## 9. Risks and Mitigations

-   **Risk**: Data loss during Alembic migrations due to complex schema changes.
    -   **Mitigation**: Thorough testing of migration scripts on development data; enforce review of all migration files; ensure all migrations are reversible.
-   **Risk**: Performance degradation with deeply nested subtask hierarchies or complex filters.
    -   **Mitigation**: Implement efficient database queries (e.g., CTEs, proper indexing); optimize API response serialization; implement pagination and lazy loading for large lists.
-   **Risk**: Inconsistent user isolation due to new data models.
    -   **Mitigation**: Rigorous implementation of `user_id` filtering at the database and API levels; extensive unit and integration tests specifically for user isolation.
-   **Risk**: Complexity of managing recurrence logic.
    -   **Mitigation**: Start with simpler recurrence patterns; use a well-defined external library if internal implementation becomes too complex.

## 10. Follow-ups

-   Finalize the `recurrence_rule` format and `reminder mechanism` details.
-   Design UI/UX for managing task dependencies (e.g., a visual graph or selection modal).
-   Consider project-level permissions beyond basic user isolation (e.g., shared projects).
-   Explore file storage solutions for `FileAttachment` (e.g., S3, Google Cloud Storage).

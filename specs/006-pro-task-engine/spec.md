# Feature Specification: Pro Task Engine Implementation

**Feature Branch**: `006-pro-task-engine`
**Created**: 2026-02-05
**Status**: Draft
**Input**: User description: "Pro Task Engine Implementation (Spec 5)

Target: Build the core business logic for advanced task management, including subtasks, recurrence, and rich metadata.

Focus:
- **Data Model Expansion (Backend):**
    - **Subtasks:** Self-referencing relationship (Parent-Child tasks).
    - **Metadata:** Add Priority (Low, Medium, High, Urgent), Status (To Do, In Progress, Review, Blocked, Done), and Labels/Tags.
    - **Scheduling:** Due Dates, Reminders, and Recurring logic (Daily, Weekly, Monthly).
    - **Organization:** Sections inside projects and File attachment metadata.
- **Task Dependencies:** Logic to prevent Task B from starting if Task A is incomplete.
- **Collaboration:** Comments system and Activity logs for each task.
- **API Enhancement:** Update REST endpoints to handle nested subtasks and complex filtering (by priority, tag, or status).

Success criteria:
- Database schema updated via Alembic without data loss.
- Subtasks are correctly nested (infinite nesting support).
- Task status changes trigger color-coded UI updates.
- API supports filtering: `/api/{user_id}/tasks?status=In Progress&priority=High`.

Constraints:
- Maintain strict User Isolation (User A cannot see User B's subtasks or comments).
- Use SQLModel for all relationships and Enum types for Status/Priority."

## User Scenarios & Testing

### User Story 1 - Manage Subtasks (Priority: P1)

As a user, I want to break down a main task into multiple subtasks, allowing for infinite nesting, so that I can organize complex work more granularly. I also want to see all subtasks associated with a parent task and easily navigate through the task hierarchy.

**Why this priority**: Subtasks are a core feature for advanced task management, enabling users to structure their work efficiently.

**Independent Test**: Can be fully tested by creating a parent task, adding multiple levels of subtasks, and verifying correct nesting and display of the task hierarchy.

**Acceptance Scenarios**:

1.  **Given** I have a main task, **When** I add a new subtask to it, **Then** the subtask is created and linked to the parent task.
2.  **Given** I have a task with subtasks, **When** I view the parent task, **Then** I see a list of its direct subtasks.
3.  **Given** I have a deeply nested subtask, **When** I mark it as complete, **Then** its status is updated without affecting its parent's status.
4.  **Given** I have a parent task, **When** I delete the parent task, **Then** all its associated subtasks are also deleted.

---

### User Story 2 - Prioritize and Categorize Tasks (Priority: P1)

As a user, I want to assign a priority (Low, Medium, High, Urgent), a status (To Do, In Progress, Review, Blocked, Done), and multiple labels/tags to my tasks and subtasks, so that I can easily organize, filter, and understand the urgency and progress of my work.

**Why this priority**: Metadata and categorization are fundamental for effective task management and filtering, directly impacting user workflow efficiency.

**Independent Test**: Can be fully tested by creating tasks with various priorities, statuses, and tags, then applying filters to verify correct display.

**Acceptance Scenarios**:

1.  **Given** I am creating or editing a task, **When** I assign a priority, status, and tags, **Then** these attributes are saved and displayed with the task.
2.  **Given** I have tasks with different priorities, **When** I filter tasks by "Urgent" priority, **Then** only urgent tasks are shown.
3.  **Given** I have tasks with different statuses, **When** I filter tasks by "In Progress" status, **Then** only tasks with "In Progress" status are shown.
4.  **Given** I have tasks with various tags, **When** I filter tasks by a specific tag, **Then** only tasks containing that tag are shown.
5.  **Given** a task's status changes, **When** the UI updates, **Then** the task's display reflects the new status with a corresponding color change.

---

### User Story 3 - Track Task Progress and Collaboration (Priority: P2)

As a user, I want to see an activity log for each task, including status changes, comments, and other important events, so that I can track its history. I also want to prevent a task from starting if its dependent tasks are not complete, and add comments to tasks for collaboration.

**Why this priority**: Collaboration and dependency tracking improve project coordination and ensure sequential work completion.

**Independent Test**: Can be fully tested by creating tasks with dependencies, adding comments, and observing the activity log, along with attempting to complete dependent tasks out of order.

**Acceptance Scenarios**:

1.  **Given** a task has a dependency on another task, **When** I try to mark the dependent task as "In Progress" before its predecessor is "Done", **Then** the system prevents the status change and notifies me of the dependency.
2.  **Given** I view a task, **When** I add a comment to it, **Then** my comment is saved and visible to collaborators for that specific task.
3.  **Given** various actions occur on a task (e.g., status change, comment added, priority updated), **When** I view the task's activity log, **Then** a chronological record of these events is displayed.
4.  **Given** I am User A, **When** User B adds a comment to a task I own, **Then** I can see User B's comment and User A cannot see comments on tasks they do not own.

---

### Edge Cases

-   What happens when a user attempts to create a circular dependency between tasks? (e.g., Task A depends on Task B, and Task B depends on Task A).
-   How does the system handle deleting a parent task with many nested subtasks and dependencies?
-   What is the behavior if a recurring task is updated (e.g., due date changed for all future occurrences)?
-   How does filtering behave when multiple criteria are applied (e.g., status AND priority AND tag)?
-   What is the maximum practical nesting depth for subtasks? (System supports infinite, but UI/UX may have limits).

## Requirements

### Functional Requirements

-   **FR-001**: The system MUST support a self-referencing relationship for tasks, allowing a task to have multiple subtasks and a single parent task, enabling infinite nesting.
-   **FR-002**: The system MUST allow tasks and subtasks to be assigned one of four Priority levels: Low, Medium, High, Urgent, using an Enum type.
-   **FR-003**: The system MUST allow tasks and subtasks to be assigned one of five Status levels: To Do, In Progress, Review, Blocked, Done, using an Enum type.
-   **FR-004**: The system MUST allow tasks and subtasks to have multiple associated Labels/Tags.
-   **FR-005**: The system MUST allow tasks to have a Due Date and Reminders.
-   **FR-006**: The system MUST support Recurring tasks with configurable frequencies (Daily, Weekly, Monthly).
-   **FR-007**: The system MUST support organizing tasks into Sections within Projects.
-   **FR-008**: The system MUST allow File attachment metadata to be associated with tasks.
-   **FR-009**: The system MUST enforce task dependencies, preventing a dependent task from progressing if its prerequisite tasks are not in a "Done" status.
-   **FR-010**: The system MUST provide a comments system for tasks, allowing users to add and view textual comments.
-   **FR-011**: The system MUST maintain an activity log for each task, recording significant events such as status changes, priority updates, and comments.
-   **FR-012**: The API MUST provide endpoints for creating, retrieving, updating, and deleting tasks, supporting nested subtasks.
-   **FR-013**: The API MUST support complex filtering of tasks by Priority, Status, and Labels/Tags (e.g., `/api/{user_id}/tasks?status=In Progress&priority=High`).
-   **FR-014**: The system MUST ensure strict user isolation, meaning User A can only access their own tasks, subtasks, comments, and activity logs.
-   **FR-015**: The backend MUST use SQLModel for defining all data models and relationships.

### Key Entities

-   **Task**: Represents a unit of work. Includes fields for `title`, `description`, `due_date`, `is_completed`. Expanded to include `parent_task_id` (self-referencing), `priority` (Enum), `status` (Enum), `labels` (relationship to Tag), `recurrence_pattern`, `section_id`, `project_id`.
-   **Subtask**: A Task that has a `parent_task_id` pointing to another Task. Behaves similarly to a Task but inherits user ownership from its top-level parent.
-   **Comment**: Textual feedback or discussion related to a Task. Includes `task_id`, `user_id`, `content`, `timestamp`.
-   **Tag**: A categorical label that can be applied to tasks. Includes `name`. Many-to-many relationship with Task.
-   **ActivityLog**: Records significant events on a Task. Includes `task_id`, `user_id`, `event_type` (e.g., 'status_changed', 'comment_added'), `details` (JSONB for event-specific data), `timestamp`.
-   **Dependency**: Represents a prerequisite relationship between two tasks. Includes `task_id` and `depends_on_task_id`.
-   **Section**: An organizational unit within a Project to group tasks. Includes `project_id`, `name`.
-   **Project**: A container for tasks and sections. Includes `user_id`, `name`.
-   **FileAttachment**: Metadata for files attached to tasks. Includes `task_id`, `filename`, `file_type`, `url`, `uploaded_by`.

## Success Criteria

### Measurable Outcomes

-   **SC-001**: Database schema updates via Alembic complete successfully without data loss on existing task data.
-   **SC-002**: Subtasks can be nested to an arbitrary depth (limited by practical database/ORM constraints, but not artificially by the system), and the API correctly reflects these hierarchies.
-   **SC-003**: UI visually reflects task status changes with corresponding color-coding within 500ms of an update (when UI is implemented).
-   **SC-004**: The API successfully processes task filtering requests by status and priority, returning relevant tasks within 200ms for a typical user load.
-   **SC-005**: User isolation is maintained, with no instances of User A accessing User B's task data, comments, or activity logs.
-   **SC-006**: The expanded data model for tasks, subtasks, and associated entities is correctly implemented using SQLModel.

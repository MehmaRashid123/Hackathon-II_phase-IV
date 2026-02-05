# Data Model: Pro Task Engine Implementation

This document describes the expanded data model for the "Pro Task Engine" feature, outlining existing and new entities, their attributes, and relationships. It is designed to be implemented using SQLModel for the FastAPI backend and Neon Serverless PostgreSQL.

## 1. Enums

### `PriorityEnum`
-   **Purpose**: Defines the possible priority levels for a task.
-   **Values**:
    -   `LOW`
    -   `MEDIUM`
    -   `HIGH`
    -   `URGENT`

### `StatusEnum`
-   **Purpose**: Defines the possible status levels for a task.
-   **Values**:
    -   `TO_DO`
    -   `IN_PROGRESS`
    -   `REVIEW`
    -   `BLOCKED`
    -   `DONE`

## 2. Existing Model Updates

### `Task` Model (`backend/src/models/task.py`)

-   **Description**: Represents a unit of work. Now supports subtasks, metadata, and scheduling.
-   **Attributes**:
    -   `id: UUID` (Primary Key, auto-generated)
    -   `user_id: UUID` (Foreign Key to `User.id`, `index=True`)
    -   `title: str`
    -   `description: Optional[str]`
    -   `is_completed: bool` (Default: `False`)
    -   `created_at: datetime` (Default: `utcnow()`)
    -   `updated_at: datetime` (Default: `utcnow()`, on update: `utcnow()`)
    -   `parent_id: Optional[UUID]` (Foreign Key to `Task.id` (self-referencing), `nullable=True`, `index=True`)
    -   `priority: PriorityEnum` (Default: `PriorityEnum.MEDIUM`)
    -   `status: StatusEnum` (Default: `StatusEnum.TO_DO`)
    -   `due_date: Optional[datetime]`
    -   `recurrence_rule: Optional[str]` (String for simplified recurrence patterns, e.g., "DAILY", "WEEKLY:MON,TUE")
    -   `section_id: Optional[UUID]` (Foreign Key to `Section.id`, `nullable=True`)
    -   `project_id: Optional[UUID]` (Foreign Key to `Project.id`, `nullable=True`)
-   **Relationships**:
    -   `user: User` (Many-to-one)
    -   `parent_task: Optional[Task]` (Many-to-one, self-referencing via `parent_id`)
    -   `subtasks: List[Task]` (One-to-many, self-referencing via `parent_id`, `cascade="all, delete-orphan"`)
    -   `comments: List[Comment]` (One-to-many, `cascade="all, delete-orphan"`)
    -   `activity_logs: List[ActivityLog]` (One-to-many, `cascade="all, delete-orphan"`)
    -   `dependencies: List[Dependency]` (One-to-many, where `task` is the dependent, `cascade="all, delete-orphan"`)
    -   `dependents: List[Dependency]` (One-to-many, where `task` is the prerequisite)
    -   `tags: List[Tag]` (Many-to-many via `TaskTagLink`)
    -   `section: Optional[Section]` (Many-to-one)
    -   `project: Optional[Project]` (Many-to-one)

## 3. New Models

### `Project` Model (`backend/src/models/project.py`)
-   **Description**: A container for tasks and sections, owned by a user.
-   **Attributes**:
    -   `id: UUID` (Primary Key, auto-generated)
    -   `user_id: UUID` (Foreign Key to `User.id`, `index=True`)
    -   `name: str`
    -   `created_at: datetime`
    -   `updated_at: datetime`
-   **Relationships**:
    -   `user: User` (Many-to-one)
    -   `sections: List[Section]` (One-to-many, `cascade="all, delete-orphan"`)
    -   `tasks: List[Task]` (One-to-many, `cascade="all, delete-orphan"`)

### `Section` Model (`backend/src/models/section.py`)
-   **Description**: An organizational unit within a Project to group tasks.
-   **Attributes**:
    -   `id: UUID` (Primary Key, auto-generated)
    -   `project_id: UUID` (Foreign Key to `Project.id`, `index=True`)
    -   `name: str`
    -   `order: int` (For display order within a project)
    -   `created_at: datetime`
    -   `updated_at: datetime`
-   **Relationships**:
    -   `project: Project` (Many-to-one)
    -   `tasks: List[Task]` (One-to-many, `cascade="all, delete-orphan"`)

### `Comment` Model (`backend/src/models/comment.py`)
-   **Description**: Textual feedback or discussion related to a `Task`.
-   **Attributes**:
    -   `id: UUID` (Primary Key, auto-generated)
    -   `task_id: UUID` (Foreign Key to `Task.id`, `index=True`)
    -   `user_id: UUID` (Foreign Key to `User.id`, `index=True`)
    -   `content: str`
    -   `created_at: datetime`
-   **Relationships**:
    -   `task: Task` (Many-to-one)
    -   `user: User` (Many-to-one)

### `Tag` Model (`backend/src/models/tag.py`)
-   **Description**: A categorical label that can be applied to `Task`s. Unique per user.
-   **Attributes**:
    -   `id: UUID` (Primary Key, auto-generated)
    -   `user_id: UUID` (Foreign Key to `User.id`, `index=True`)
    -   `name: str`
    -   `created_at: datetime`
-   **Constraints**: Unique (`user_id`, `name`)
-   **Relationships**:
    -   `user: User` (Many-to-one)
    -   `tasks: List[Task]` (Many-to-many via `TaskTagLink`)

### `TaskTagLink` Model (`backend/src/models/task_tag_link.py`)
-   **Description**: Association model for the Many-to-Many relationship between `Task` and `Tag`.
-   **Attributes**:
    -   `task_id: UUID` (Primary Key, Foreign Key to `Task.id`)
    -   `tag_id: UUID` (Primary Key, Foreign Key to `Tag.id`)
-   **Relationships**:
    -   `task: Task` (Many-to-one)
    -   `tag: Tag` (Many-to-one)

### `ActivityLog` Model (`backend/src/models/activity_log.py`)
-   **Description**: Records significant events on a `Task`.
-   **Attributes**:
    -   `id: UUID` (Primary Key, auto-generated)
    -   `task_id: UUID` (Foreign Key to `Task.id`, `index=True`)
    -   `user_id: Optional[UUID]` (Foreign Key to `User.id`, `nullable=True`, `index=True` for system events)
    -   `event_type: str` (e.g., "status_changed", "comment_added", "priority_updated", "task_created")
    -   `details: dict` (JSONB field to store event-specific data, e.g., `{"old_status": "To Do", "new_status": "In Progress"}`)
    -   `created_at: datetime`
-   **Relationships**:
    -   `task: Task` (Many-to-one)
    -   `user: Optional[User]` (Many-to-one)

### `Dependency` Model (`backend/src/models/dependency.py`)
-   **Description**: Represents a prerequisite relationship between two tasks. `task` depends on `depends_on_task`.
-   **Attributes**:
    -   `id: UUID` (Primary Key, auto-generated)
    -   `task_id: UUID` (Foreign Key to `Task.id`, the dependent task, `index=True`)
    -   `depends_on_task_id: UUID` (Foreign Key to `Task.id`, the prerequisite task, `index=True`)
    -   `user_id: UUID` (Foreign Key to `User.id`, for isolation)
    -   `created_at: datetime`
-   **Constraints**: Unique (`task_id`, `depends_on_task_id`)
-   **Relationships**:
    -   `dependent_task: Task` (Many-to-one, for `task_id`)
    -   `prerequisite_task: Task` (Many-to-one, for `depends_on_task_id`)
    -   `user: User` (Many-to-one)

### `FileAttachment` Model (`backend/src/models/file_attachment.py`)
-   **Description**: Metadata for files attached to `Task`s.
-   **Attributes**:
    -   `id: UUID` (Primary Key, auto-generated)
    -   `task_id: UUID` (Foreign Key to `Task.id`, `index=True`)
    -   `user_id: UUID` (Foreign Key to `User.id`, `index=True`)
    -   `filename: str`
    -   `file_type: str` (MIME type, e.g., "image/png", "application/pdf")
    -   `url: str` (URL to the actual file storage, e.g., S3 bucket)
    -   `uploaded_at: datetime`
-   **Relationships**:
    -   `task: Task` (Many-to-one)
    -   `user: User` (Many-to-one)
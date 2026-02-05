# Research Findings: Pro Task Engine Implementation

## Decisions & Rationale for Needs Clarification

### 1. Recurrence Rule Format

-   **Decision**: Implement a simplified string-based format for `recurrence_rule` in `Task` model.
    -   Examples:
        -   `DAILY`
        -   `WEEKLY:MON,TUE,WED,THU,FRI` (for weekdays)
        -   `MONTHLY:15` (for the 15th of every month)
        -   `YEARLY:JAN-01` (for January 1st)
-   **Rationale**: This format provides sufficient flexibility for common recurrence patterns without introducing the immediate complexity of a full iCal-like parsing library. It is straightforward to store and can be expanded upon in the future if more complex rules are required. Initial parsing logic in the service layer will be custom.
-   **Alternatives Considered**:
    -   Full iCal RRule standard: Rejected for initial implementation due to significant parsing complexity and overhead for the current scope.
    -   JSON object: Rejected to keep the data model simpler for direct string storage, deferring complex structure to application logic if needed.

### 2. Reminder Mechanism

-   **Decision**: Implement server-side reminders via a periodic background job.
    -   The job will query for tasks with upcoming `due_date` and enabled reminders.
    -   Notification will initially be an in-app notification or simple log entry, with potential for email integration later.
-   **Rationale**: A server-side background job is a reliable and scalable approach for triggering reminders. It centralizes the logic and does not rely on the client being active. This keeps the initial implementation focused on core logic, with clear pathways for future integration with more advanced notification systems (e.g., push notifications, dedicated email service).
-   **Alternatives Considered**:
    -   Frontend-only polling: Rejected due to unreliability (browser closed, network issues) and increased client load.
    -   Real-time push notifications: Deferred to a later phase due to added complexity of integrating a real-time messaging service (e.g., WebSockets, external push notification providers) and potential infrastructure costs.

## Best Practices (General)

-   **SQLModel Relationships**: Ensure all relationships are correctly defined with back_populates for bidirectional access, and use `sa_relationship_kwargs` for advanced configurations (e.g., `cascade`).
-   **Alembic Migrations**: Always generate migrations automatically, review the generated script, and test them locally before deployment. Ensure migrations are reversible.
-   **FastAPI Dependencies**: Utilize FastAPI's dependency injection system for database sessions and authentication/authorization.
-   **Pydantic Models**: Strictly use Pydantic models for request and response validation, ensuring clear API contracts.
-   **User Isolation**: Double-check `user_id` filtering in all service methods and API endpoints that retrieve or modify user-specific data.
-   **Error Handling**: Implement custom exception handlers for common scenarios (e.g., `404 NotFound`, `403 Forbidden`, `400 BadRequest`) for clear API responses.
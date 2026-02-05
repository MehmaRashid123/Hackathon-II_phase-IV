# Quickstart Guide: Pro Task Engine Implementation

This guide provides a quick overview of how to set up, run, and interact with the "Pro Task Engine" feature, including database migrations, starting the backend and frontend, and testing the new functionalities.

## 1. Environment Setup

Before starting, ensure your environment variables are correctly configured. These are crucial for database connectivity, authentication, and cross-origin resource sharing (CORS).

-   Create or update your `.env` file in the project root (`phase-II/.env`) with the following variables:
    ```dotenv
    # Database connection string for Neon Serverless PostgreSQL
    DATABASE_URL=postgresql://<YOUR_NEON_USER>:<YOUR_NEON_PASSWORD>@<YOUR_NEON_HOST>/<YOUR_NEON_DATABASE>

    # Secret key for JWT token generation and verification
    JWT_SECRET=your_super_secret_jwt_key_here

    # Better Auth internal secret
    BETTER_AUTH_SECRET=your_better_auth_secret_key_here

    # Frontend URL for CORS configuration (e.g., your Next.js development server)
    ALLOWED_ORIGINS=http://localhost:3000
    ```
-   Replace placeholders (`<YOUR_NEON_USER>`, etc.) with your actual Neon PostgreSQL credentials.
-   Generate strong, unique values for `JWT_SECRET` and `BETTER_AUTH_SECRET`.

## 2. Database Migration

Apply the new database schema changes using Alembic. This will update your Neon PostgreSQL database to include the new `Task` fields and the new models (`Project`, `Section`, `Comment`, `Tag`, `ActivityLog`, `Dependency`, `FileAttachment`).

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2.  Run the Alembic upgrade command:
    ```bash
    alembic upgrade head
    ```
    This command will apply all pending migrations, updating your database schema.

## 3. Start the Backend API

Launch the FastAPI application, which provides the RESTful API endpoints for managing tasks and their new features.

1.  Ensure you are in the `backend` directory.
2.  Start the FastAPI server:
    ```bash
    uvicorn src.main:app --reload
    ```
    The `--reload` flag enables auto-reloading of the server on code changes, which is useful during development.
3.  The API will typically be accessible at `http://localhost:8000`.

## 4. Start the Frontend Application

Start the Next.js frontend application, which provides the user interface to interact with the advanced task management features.

1.  Navigate to the `frontend` directory (from the project root `phase-II/`):
    ```bash
    cd frontend
    ```
2.  Install frontend dependencies if you haven't already:
    ```bash
    npm install
    ```
3.  Start the Next.js development server:
    ```bash
    npm run dev
    ```
    The frontend will typically be accessible at `http://localhost:3000`.

## 5. Access the UI and Interact with Features

1.  Open your web browser and navigate to `http://localhost:3000`.
2.  **User Authentication**: Sign up or sign in to the application.
3.  **Create Tasks**:
    -   Use the UI to create new tasks.
    -   Explore the new options for assigning priorities, statuses, due dates, and recurrence rules.
    -   Create subtasks by linking them to existing parent tasks.
4.  **Manage Metadata**:
    -   Apply tags to tasks.
    -   Change task status and priority.
5.  **Task Dependencies**:
    -   Experiment with setting up dependencies between tasks and observe the dependency check logic.
6.  **View Activity Logs**:
    -   Check the activity log for tasks after making changes (e.g., status updates, comments).

## 6. Test API Directly (Optional)

You can use tools like `curl`, Postman, or Insomnia to directly interact with the new API endpoints and verify their functionality.

-   **Base URL**: `http://localhost:8000/api/{user_id}` (replace `{user_id}` with an actual authenticated user's UUID).
-   **Authentication**: Include a valid JWT token in the `Authorization: Bearer <token>` header for all protected endpoints.

**Example API Interactions:**

-   **Get tasks with filters**:
    ```bash
    curl -X GET "http://localhost:8000/api/<USER_UUID>/tasks?status=IN_PROGRESS&priority=HIGH&include_subtasks=true" \
         -H "Authorization: Bearer <YOUR_JWT_TOKEN>"
    ```
-   **Add a comment to a task**:
    ```bash
    curl -X POST "http://localhost:8000/api/<USER_UUID>/tasks/<TASK_UUID>/comments" \
         -H "Content-Type: application/json" \
         -H "Authorization: Bearer <YOUR_JWT_TOKEN>" \
         -d '{"content": "This is a new comment."}'
    ```
-   **Create a new project**:
    ```bash
    curl -X POST "http://localhost:8000/api/<USER_UUID>/projects" \
         -H "Content-Type: application/json" \
         -H "Authorization: Bearer <YOUR_JWT_TOKEN>" \
         -d '{"name": "My New Project"}'
    ```

Refer to the OpenAPI documentation (`http://localhost:8000/docs` in the backend) for a complete list of endpoints and their specifications.
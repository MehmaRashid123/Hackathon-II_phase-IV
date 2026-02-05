# Feature Specification: Authentication and Database Foundation

**Feature Branch**: `001-auth-db-foundation`
**Created**: 2026-02-05
**Status**: Draft
**Input**: User description: "Target: Establish the monorepo, database connectivity, and the JWT-based authentication bridge.

Focus:
- Monorepo structure with /frontend (Next.js) and /backend (FastAPI) directories.
- Neon Serverless PostgreSQL connection setup.
- Better Auth configuration on the frontend to issue JWTs.
- FastAPI Middleware to intercept, verify JWTs using the shared secret, and extract user identity.

Success criteria:
- Frontend can successfully initiate login/signup via Better Auth.
- Backend has a 'health check' endpoint that returns 401 if no JWT is present and 200 with User ID if a valid JWT is present.
- Neon DB connection is verified and migrations (SQLModel) can run.
- BETTER_AUTH_SECRET is successfully shared between services via environment variables.

Constraints:
- No Task CRUD implementation yet (Focus only on Auth/DB).
- Use SQLModel for the User schema.
- Frontend must use Next.js 16+ App Router.
- Backend must use Python FastAPI.

Not building:
- Task management UI components.
- Task API endpoints (GET/POST/PUT/DELETE).
- Sophisticated error pages or styling (keep UI minimal/functional for now)."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Registration (Priority: P1)

A new user wants to create an account in the todo application so they can start managing their tasks.

**Why this priority**: Without user registration, no users can access the application. This is the foundational capability that enables all other features.

**Independent Test**: Can be fully tested by visiting the signup page, entering email and password, submitting the form, and verifying the user record is created in the database with a hashed password. Success means the user can subsequently sign in with those credentials.

**Acceptance Scenarios**:

1. **Given** the user is on the signup page, **When** they enter a valid email and password (minimum 8 characters), **Then** their account is created, password is hashed, user record is stored in the database, and they are redirected to a success confirmation.
2. **Given** the user is on the signup page, **When** they enter an email that already exists, **Then** they see an error message "Email already registered" and the form is not submitted.
3. **Given** the user is on the signup page, **When** they enter a password shorter than 8 characters, **Then** they see an error message "Password must be at least 8 characters" and the form is not submitted.
4. **Given** the user successfully completes registration, **When** the user record is created, **Then** the password is hashed using bcrypt or argon2 (never stored in plain text).

---

### User Story 2 - User Sign-In with JWT Issuance (Priority: P1)

A registered user wants to sign in to access their account and receive a JWT token for authenticated requests.

**Why this priority**: Sign-in is equally critical as registration. Without it, users cannot access their accounts or make authenticated API requests.

**Independent Test**: Can be fully tested by entering valid credentials on the signin page, verifying that Better Auth issues a JWT token, and confirming the token is stored securely (httpOnly cookie or secure storage). Success means the user receives a valid JWT that can be used for subsequent API calls.

**Acceptance Scenarios**:

1. **Given** a registered user is on the signin page, **When** they enter correct email and password, **Then** Better Auth authenticates them, issues a JWT token containing user ID and email, and redirects them to the application.
2. **Given** a registered user is on the signin page, **When** they enter incorrect credentials, **Then** they see an error message "Invalid email or password" and no token is issued.
3. **Given** a user successfully signs in, **When** the JWT is issued, **Then** the token includes user ID, email, expiration timestamp, and is signed with BETTER_AUTH_SECRET.
4. **Given** a user signs in successfully, **When** the JWT is stored, **Then** it is stored in an httpOnly cookie or secure session storage (not accessible via JavaScript to prevent XSS attacks).

---

### User Story 3 - Backend JWT Verification (Priority: P1)

The backend API verifies JWT tokens on protected endpoints to ensure only authenticated users can access resources.

**Why this priority**: JWT verification is the security foundation that prevents unauthorized access. Without it, the authentication system is incomplete and insecure.

**Independent Test**: Can be fully tested by making API requests to the health check endpoint with and without valid JWT tokens. Success means requests without tokens return 401 Unauthorized, requests with invalid tokens return 401, and requests with valid tokens return 200 with user ID.

**Acceptance Scenarios**:

1. **Given** a client makes a request to `/api/health` without an Authorization header, **When** the backend middleware processes the request, **Then** it returns HTTP 401 Unauthorized with message "Missing authentication token".
2. **Given** a client makes a request to `/api/health` with an invalid or expired JWT, **When** the backend middleware verifies the token, **Then** it returns HTTP 401 Unauthorized with message "Invalid or expired token".
3. **Given** a client makes a request to `/api/health` with a valid JWT, **When** the backend middleware verifies the token signature using BETTER_AUTH_SECRET, **Then** it extracts the user ID and email, returns HTTP 200 OK with response body containing `{"status": "healthy", "user_id": "<user_id>", "email": "<email>"}`.
4. **Given** a valid JWT is verified, **When** the user ID is extracted, **Then** it is made available to the endpoint handler for user-specific data filtering.

---

### User Story 4 - Database Connection and Migrations (Priority: P1)

The application establishes a connection to Neon Serverless PostgreSQL and runs migrations to create the User table schema.

**Why this priority**: Without database connectivity and schema setup, user data cannot be persisted. This is a foundational prerequisite for all data operations.

**Independent Test**: Can be fully tested by running the migration script and verifying the User table is created in Neon with correct columns (id, email, hashed_password, created_at, updated_at). Success means the application can connect to Neon and perform CRUD operations on the User table.

**Acceptance Scenarios**:

1. **Given** the database connection string is configured in DATABASE_URL environment variable, **When** the application starts, **Then** it successfully connects to Neon Serverless PostgreSQL.
2. **Given** the application is connected to Neon, **When** the migration script is executed, **Then** it creates a User table with columns: id (UUID primary key), email (unique, not null), hashed_password (not null), created_at (timestamp), updated_at (timestamp).
3. **Given** the User table is created, **When** a new user registers, **Then** their data is successfully inserted into the User table.
4. **Given** the database connection is lost, **When** the application attempts an operation, **Then** it handles the error gracefully and returns an appropriate error message to the user.

---

### Edge Cases

- What happens when the BETTER_AUTH_SECRET environment variable is missing or empty?
  - Application startup should fail with a clear error message indicating the missing secret.

- What happens when the DATABASE_URL is incorrect or Neon is unreachable?
  - Application should fail to start (or health check should report unhealthy) with a clear error message about database connectivity.

- What happens when a JWT token is tampered with?
  - Backend middleware should reject it with 401 Unauthorized and log the verification failure.

- What happens when two users try to register with the same email simultaneously?
  - Database unique constraint should prevent duplicate emails; one request succeeds, the other receives an error.

- What happens when Better Auth token issuance fails?
  - User should see a generic error message "Authentication failed, please try again" without exposing internal errors.

- What happens when the JWT expires while the user is using the application?
  - Subsequent API requests should return 401, prompting the frontend to redirect to the signin page (or implement token refresh if specified in future stories).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a monorepo structure with separate `/frontend` and `/backend` directories.
- **FR-002**: System MUST allow users to register with a valid email address and password (minimum 8 characters).
- **FR-003**: System MUST hash user passwords using bcrypt or argon2 before storing them in the database.
- **FR-004**: System MUST validate email format during registration (standard email regex validation).
- **FR-005**: System MUST prevent duplicate email registrations by enforcing a unique constraint on the email column.
- **FR-006**: System MUST allow registered users to sign in with their email and password.
- **FR-007**: System MUST issue a JWT token upon successful sign-in containing user ID, email, and expiration timestamp.
- **FR-008**: System MUST sign JWT tokens with a shared secret (BETTER_AUTH_SECRET) stored in environment variables.
- **FR-009**: System MUST store JWT tokens securely in httpOnly cookies to prevent XSS attacks.
- **FR-010**: System MUST provide a backend middleware that intercepts all `/api/*` requests and verifies the JWT token.
- **FR-011**: System MUST reject requests without a valid JWT token with HTTP 401 Unauthorized.
- **FR-012**: System MUST extract user ID and email from verified JWT tokens and make them available to endpoint handlers.
- **FR-013**: System MUST provide a health check endpoint `/api/health` that returns 401 if no JWT is present and 200 with user ID if a valid JWT is present.
- **FR-014**: System MUST connect to Neon Serverless PostgreSQL using a connection string from the DATABASE_URL environment variable.
- **FR-015**: System MUST use SQLModel to define the User schema with fields: id (UUID), email (string, unique), hashed_password (string), created_at (timestamp), updated_at (timestamp).
- **FR-016**: System MUST provide a migration mechanism to create and update the User table schema.
- **FR-017**: System MUST verify database connectivity on application startup and report connection status.
- **FR-018**: System MUST share the BETTER_AUTH_SECRET between frontend (Better Auth) and backend (FastAPI) via environment variables.
- **FR-019**: Frontend MUST be built using Next.js 16+ with App Router conventions.
- **FR-020**: Backend MUST be built using Python FastAPI with type hints and Pydantic models.

### Key Entities

- **User**: Represents a registered user account with authentication credentials.
  - Attributes: unique identifier, email address (unique), hashed password, account creation timestamp, last update timestamp
  - Relationships: None in this feature (will relate to Tasks in future features)
  - Constraints: Email must be unique, password must be hashed, all timestamps are auto-managed

### Assumptions

- JWT token expiration time defaults to 24 hours (can be configured via environment variable).
- Password hashing algorithm defaults to bcrypt with cost factor of 10 (industry standard).
- Email validation uses standard RFC 5322 regex pattern.
- Database connection uses connection pooling with default settings (5 min/10 max connections).
- Better Auth is configured to issue JWTs (not session-based authentication).
- Frontend and backend communicate over HTTP/HTTPS (CORS configured to allow frontend origin).
- Environment variables are managed via `.env` files (not checked into version control).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete account registration in under 30 seconds with valid credentials.
- **SC-002**: Users can sign in and receive a valid authentication token in under 5 seconds.
- **SC-003**: Backend verifies and processes authenticated requests in under 100 milliseconds.
- **SC-004**: Database connection is established successfully within 3 seconds of application startup.
- **SC-005**: Health check endpoint responds within 50 milliseconds for authenticated requests.
- **SC-006**: System rejects 100% of requests with missing, invalid, or expired tokens with appropriate HTTP 401 responses.
- **SC-007**: All user passwords are stored hashed (zero plain-text passwords in database).
- **SC-008**: Application startup fails with clear error messages if required environment variables (DATABASE_URL, BETTER_AUTH_SECRET) are missing.
- **SC-009**: User registration form validates input and displays error messages within 100 milliseconds of submission.
- **SC-010**: Database schema migrations can be run successfully on a fresh Neon database without manual intervention.

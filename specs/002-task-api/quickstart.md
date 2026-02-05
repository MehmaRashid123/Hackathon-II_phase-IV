# Quickstart Guide: Backend Task Management API

**Feature**: 002-task-api
**Date**: 2026-02-05
**Audience**: Developers implementing or testing the Task API

## Prerequisites

Before starting, ensure you have:

1. **Environment Variables** (`.env` file in project root):
   ```env
   DATABASE_URL=postgresql://user:password@host/database  # Neon connection string
   BETTER_AUTH_SECRET=your-secret-key-here                # Shared JWT secret
   ```

2. **Dependencies Installed**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

   Required packages:
   - FastAPI
   - SQLModel
   - python-jose[cryptography]
   - python-multipart
   - psycopg2-binary
   - uvicorn
   - alembic

3. **Database Ready**:
   - Neon PostgreSQL database provisioned
   - Users table exists (from 001-auth-db-foundation feature)

---

## Setup Steps

### 1. Run Database Migrations

Apply the tasks table migration:

```bash
cd backend
alembic upgrade head
```

**Expected Output**:
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 001 -> 002, Add tasks table
```

**Verification**:
```bash
# Connect to database and verify table exists
psql $DATABASE_URL -c "\d tasks"
```

### 2. Start the Development Server

```bash
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output**:
```
INFO:     Will watch for changes in these directories: ['/path/to/backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 3. Access API Documentation

Open your browser and navigate to:

**Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)

**ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Getting a JWT Token

Before testing task endpoints, you need a valid JWT token from the auth system.

### Option 1: Via Auth Endpoints (if implemented)

```bash
# Register a new user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePassword123!"
  }'

# Login to get JWT token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePassword123!"
  }'
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 123
}
```

### Option 2: Generate Test Token (Development Only)

```python
# backend/scripts/generate_test_token.py
from jose import jwt
from datetime import datetime, timedelta
import os

SECRET = os.getenv("BETTER_AUTH_SECRET")
ALGORITHM = "HS256"

# Create token for user_id = 123
payload = {
    "sub": "123",  # User ID
    "exp": datetime.utcnow() + timedelta(hours=24)
}

token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
print(f"Test Token: {token}")
```

Run:
```bash
python scripts/generate_test_token.py
```

---

## Testing Endpoints

### Using Swagger UI

1. Navigate to [http://localhost:8000/docs](http://localhost:8000/docs)
2. Click the **"Authorize"** button (top right)
3. Enter your JWT token: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
4. Click **"Authorize"** and close the dialog
5. All requests will now include the authorization header

### Using cURL

Export your token as an environment variable:

```bash
export TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
export USER_ID=123
```

#### 1. Create a Task

```bash
curl -X POST "http://localhost:8000/api/${USER_ID}/tasks" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete API documentation",
    "description": "Write comprehensive docs for all task endpoints"
  }'
```

**Expected Response (201 Created)**:
```json
{
  "id": 1,
  "title": "Complete API documentation",
  "description": "Write comprehensive docs for all task endpoints",
  "is_completed": false,
  "created_at": "2026-02-05T10:30:00Z",
  "updated_at": "2026-02-05T10:30:00Z",
  "user_id": 123
}
```

#### 2. List All Tasks

```bash
curl -X GET "http://localhost:8000/api/${USER_ID}/tasks?limit=50&offset=0" \
  -H "Authorization: Bearer ${TOKEN}"
```

**Expected Response (200 OK)**:
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Complete API documentation",
      "description": "Write comprehensive docs for all task endpoints",
      "is_completed": false,
      "created_at": "2026-02-05T10:30:00Z",
      "updated_at": "2026-02-05T10:30:00Z",
      "user_id": 123
    }
  ],
  "total": 1,
  "limit": 50,
  "offset": 0,
  "has_more": false
}
```

#### 3. Get Single Task

```bash
curl -X GET "http://localhost:8000/api/${USER_ID}/tasks/1" \
  -H "Authorization: Bearer ${TOKEN}"
```

**Expected Response (200 OK)**:
```json
{
  "id": 1,
  "title": "Complete API documentation",
  "description": "Write comprehensive docs for all task endpoints",
  "is_completed": false,
  "created_at": "2026-02-05T10:30:00Z",
  "updated_at": "2026-02-05T10:30:00Z",
  "user_id": 123
}
```

#### 4. Update a Task

```bash
curl -X PUT "http://localhost:8000/api/${USER_ID}/tasks/1" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete API documentation and testing",
    "description": "Write comprehensive docs and add integration tests"
  }'
```

**Expected Response (200 OK)**:
```json
{
  "id": 1,
  "title": "Complete API documentation and testing",
  "description": "Write comprehensive docs and add integration tests",
  "is_completed": false,
  "created_at": "2026-02-05T10:30:00Z",
  "updated_at": "2026-02-05T10:45:00Z",
  "user_id": 123
}
```

#### 5. Toggle Task Completion

```bash
curl -X PATCH "http://localhost:8000/api/${USER_ID}/tasks/1/complete" \
  -H "Authorization: Bearer ${TOKEN}"
```

**Expected Response (200 OK)**:
```json
{
  "id": 1,
  "title": "Complete API documentation and testing",
  "description": "Write comprehensive docs and add integration tests",
  "is_completed": true,
  "created_at": "2026-02-05T10:30:00Z",
  "updated_at": "2026-02-05T10:50:00Z",
  "user_id": 123
}
```

**Toggle Again** (mark incomplete):
```bash
curl -X PATCH "http://localhost:8000/api/${USER_ID}/tasks/1/complete" \
  -H "Authorization: Bearer ${TOKEN}"
```

#### 6. Delete a Task

```bash
curl -X DELETE "http://localhost:8000/api/${USER_ID}/tasks/1" \
  -H "Authorization: Bearer ${TOKEN}"
```

**Expected Response (204 No Content)**: Empty body

---

## Testing User Isolation

### Test 1: Access Another User's Tasks (Should Fail)

```bash
# Try to access user_id = 999 tasks with user_id = 123 token
curl -X GET "http://localhost:8000/api/999/tasks" \
  -H "Authorization: Bearer ${TOKEN}"
```

**Expected Response (403 Forbidden)**:
```json
{
  "detail": "Access denied: cannot access resources of other users"
}
```

### Test 2: Invalid JWT Token (Should Fail)

```bash
curl -X GET "http://localhost:8000/api/${USER_ID}/tasks" \
  -H "Authorization: Bearer invalid-token-here"
```

**Expected Response (401 Unauthorized)**:
```json
{
  "detail": "Invalid authentication credentials: Signature verification failed"
}
```

### Test 3: Missing Authorization Header (Should Fail)

```bash
curl -X GET "http://localhost:8000/api/${USER_ID}/tasks"
```

**Expected Response (403 Forbidden)**: FastAPI security scheme requires Bearer token

---

## Validation Testing

### Test 1: Empty Title (Should Fail)

```bash
curl -X POST "http://localhost:8000/api/${USER_ID}/tasks" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "",
    "description": "This should fail"
  }'
```

**Expected Response (422 Unprocessable Entity)**:
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "ensure this value has at least 1 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

### Test 2: Title Too Long (Should Fail)

```bash
curl -X POST "http://localhost:8000/api/${USER_ID}/tasks" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"$(python3 -c 'print(\"a\" * 501)')\"
  }"
```

**Expected Response (422 Unprocessable Entity)**:
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "ensure this value has at most 500 characters",
      "type": "value_error.any_str.max_length"
    }
  ]
}
```

---

## Performance Testing

### Load Test with Apache Bench

Test 100 concurrent GET requests:

```bash
ab -n 1000 -c 100 \
  -H "Authorization: Bearer ${TOKEN}" \
  http://localhost:8000/api/${USER_ID}/tasks
```

**Expected Results**:
- **Average Response Time**: < 500ms
- **Success Rate**: 100%
- **Concurrent Requests Handled**: 100

### Pagination Performance

Create 1000 test tasks and measure list endpoint performance:

```bash
# Script to create 1000 tasks
for i in {1..1000}; do
  curl -X POST "http://localhost:8000/api/${USER_ID}/tasks" \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{\"title\": \"Task $i\"}" \
    -w "\n" -o /dev/null -s
done

# Test pagination
time curl -X GET "http://localhost:8000/api/${USER_ID}/tasks?limit=50&offset=0" \
  -H "Authorization: Bearer ${TOKEN}" \
  -o /dev/null -s
```

**Expected**: < 500ms for first page of 1000 tasks

---

## Troubleshooting

### Error: "Connection to database failed"

**Cause**: Invalid `DATABASE_URL` or Neon database not accessible

**Solution**:
1. Verify `DATABASE_URL` in `.env` file
2. Test connection: `psql $DATABASE_URL -c "SELECT 1"`
3. Check Neon dashboard for database status

### Error: "Invalid authentication credentials"

**Cause**: JWT secret mismatch or expired token

**Solution**:
1. Verify `BETTER_AUTH_SECRET` matches between auth service and backend
2. Generate a fresh token (tokens expire after 24 hours by default)
3. Check token payload: `jwt decode <token>` (requires `pyjwt` CLI)

### Error: "Task not found"

**Cause**: Task ID doesn't exist or belongs to another user

**Solution**:
1. Verify task ID is correct: `SELECT * FROM tasks WHERE id = X`
2. Check task ownership: `SELECT user_id FROM tasks WHERE id = X`
3. Ensure user_id in URL matches JWT user_id

---

## Next Steps

After verifying the API works:

1. **Run Integration Tests**: `pytest backend/tests/integration/`
2. **Check OpenAPI Schema**: Compare `/docs` with `contracts/task-api.openapi.yaml`
3. **Test Frontend Integration**: Connect Next.js frontend to API
4. **Monitor Performance**: Check database query times in logs
5. **Security Audit**: Verify user isolation with multiple test users

---

## Useful Commands Reference

```bash
# Start server
uvicorn src.main:app --reload

# Run migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Generate new migration
alembic revision --autogenerate -m "description"

# Check database schema
psql $DATABASE_URL -c "\d tasks"

# View server logs
tail -f uvicorn.log

# Run tests
pytest backend/tests/ -v

# Check API health
curl http://localhost:8000/health
```

---

**Questions or Issues?**
- Review the [Implementation Plan](./plan.md) for architectural decisions
- Check [Data Model](./data-model.md) for database schema details
- Consult [API Contract](./contracts/task-api.openapi.yaml) for endpoint specifications

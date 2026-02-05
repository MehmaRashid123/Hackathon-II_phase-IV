# Data Model: Authentication and Database Foundation

**Feature**: 001-auth-db-foundation
**Created**: 2026-02-05
**Last Updated**: 2026-02-05

## Overview

This document defines the data entities for the authentication and database foundation feature. The primary entity is **User**, which stores authentication credentials and account metadata.

## Entities

### User

Represents a registered user account with authentication credentials.

**Purpose**: Store user identity and authentication information to enable secure access to the todo application.

**Attributes**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | Primary Key, NOT NULL, Auto-generated | Unique identifier for the user |
| `email` | String (255) | UNIQUE, NOT NULL | User's email address (used for login) |
| `hashed_password` | String (255) | NOT NULL | Bcrypt-hashed password (never plain-text) |
| `created_at` | Timestamp | NOT NULL, Default: CURRENT_TIMESTAMP | Account creation timestamp |
| `updated_at` | Timestamp | NOT NULL, Default: CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP | Last modification timestamp |

**Indexes**:
- Primary key index on `id` (automatic)
- Unique index on `email` (for fast lookup and duplicate prevention)

**Relationships**:
- None in this feature (future features will add Task entity with foreign key `user_id` → `users.id`)

**Validation Rules**:
1. **Email**:
   - Must be valid email format (RFC 5322 regex)
   - Must be unique across all users
   - Maximum 255 characters
   - Required (NOT NULL)

2. **Password** (before hashing):
   - Minimum 8 characters
   - No maximum length (hashed to fixed-length bcrypt string)
   - Required (NOT NULL after hashing)

3. **Hashed Password**:
   - Must be bcrypt hash (60 characters for bcrypt, up to 255 for flexibility)
   - Never store plain-text passwords
   - Cost factor: 10 (industry standard)

4. **Timestamps**:
   - `created_at`: Auto-generated on INSERT, never modified
   - `updated_at`: Auto-generated on INSERT, auto-updated on UPDATE

**State Transitions**:
- **Created**: User registers → record inserted with hashed password
- **Updated**: User changes email or password → `updated_at` timestamp updated
- **Active**: No explicit status field in this feature (future feature may add `is_active` or `is_verified`)

**Example**:

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "hashed_password": "$2b$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy",
  "created_at": "2026-02-05T10:30:00Z",
  "updated_at": "2026-02-05T10:30:00Z"
}
```

## Database Schema (PostgreSQL)

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Index on email for fast lookup (unique constraint creates index automatically)
-- CREATE UNIQUE INDEX idx_users_email ON users(email);

-- Trigger to auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
```

## SQLModel Definition (Python)

```python
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    """User entity for authentication and account management."""

    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    email: str = Field(max_length=255, unique=True, index=True, nullable=False)
    hashed_password: str = Field(max_length=255, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    class Config:
        """SQLModel configuration."""
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "hashed_password": "$2b$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy",
                "created_at": "2026-02-05T10:30:00Z",
                "updated_at": "2026-02-05T10:30:00Z"
            }
        }
```

## Pydantic Schemas (Request/Response)

```python
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime

class UserRegister(BaseModel):
    """Request schema for user registration."""
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=8, description="Password (min 8 characters)")

class UserLogin(BaseModel):
    """Request schema for user login."""
    email: EmailStr = Field(..., description="Registered email address")
    password: str = Field(..., description="User password")

class UserResponse(BaseModel):
    """Response schema for user data (never include hashed_password)."""
    id: UUID
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # Enable SQLModel integration
```

## Migration Strategy

**Tool**: Alembic (SQLAlchemy migration tool, compatible with SQLModel)

**Migration File**: `backend/migrations/versions/001_create_users_table.py`

**Operations**:
1. Create `users` table with all columns and constraints
2. Create unique index on `email`
3. Create trigger for auto-updating `updated_at`

**Rollback**:
1. Drop trigger `set_updated_at`
2. Drop function `update_updated_at_column`
3. Drop table `users` (CASCADE to remove indexes)

## Future Extensions

In subsequent features, the User entity will be extended with:
- Relationship to Task entity (one-to-many: User → Tasks)
- Optional fields: `is_active` (account status), `is_verified` (email verification), `last_login` (activity tracking)
- Additional authentication methods (OAuth, SSO) may add fields like `oauth_provider`, `oauth_id`

## Data Integrity

**Constraints Enforced**:
- Primary key uniqueness (no duplicate UUIDs)
- Email uniqueness (no duplicate accounts)
- NOT NULL constraints (all required fields must be present)
- Email format validation (application-level, not database-level)
- Password hashing (application-level, before database insert)

**Transaction Safety**:
- User registration is atomic (single INSERT operation)
- Concurrent duplicate email registrations handled by unique constraint (one succeeds, others fail with database error)
- No multi-step transactions in this feature (future features may require transactions for User + Task creation)

## Performance Considerations

**Indexes**:
- Primary key on `id`: O(log n) lookup by UUID
- Unique index on `email`: O(log n) lookup by email (used for login)

**Query Patterns**:
- **Registration**: INSERT (no lookup required, unique constraint handles duplicates)
- **Login**: SELECT by email (indexed, fast)
- **User lookup by ID**: SELECT by id (primary key, very fast)

**Expected Load**:
- <1000 concurrent users initially
- ~10 registrations/hour
- ~100 logins/hour
- Database connection pooling (5 min, 10 max) handles concurrency

## Security Considerations

**Password Storage**:
- NEVER store plain-text passwords
- Use bcrypt with salt (automatically generated by bcrypt library)
- Cost factor 10 balances security and performance (~100ms hashing time)
- Hashed passwords not exposed in API responses (UserResponse excludes `hashed_password`)

**Email Privacy**:
- Email addresses stored in plain-text (required for login)
- Consider GDPR compliance: users should be able to delete their accounts (future feature)
- Email uniqueness enforced to prevent account hijacking

**Database Access**:
- Use parameterized queries (SQLModel handles this automatically)
- No raw SQL injection vulnerabilities
- Connection string stored in environment variable (not hardcoded)

## Testing Strategy

**Unit Tests**:
- Test User model validation (email format, password min length)
- Test password hashing (bcrypt library usage)
- Test timestamp auto-generation

**Integration Tests**:
- Test user registration (INSERT into database)
- Test duplicate email prevention (unique constraint)
- Test user lookup by email (SELECT query)
- Test updated_at auto-update (UPDATE query)

**Contract Tests**:
- Verify UserRegister schema validation
- Verify UserResponse schema excludes hashed_password
- Verify email format validation

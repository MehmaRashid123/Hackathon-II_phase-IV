# Research: Authentication and Database Foundation

**Feature**: 001-auth-db-foundation
**Created**: 2026-02-05
**Purpose**: Document technology selection rationale and best practices for authentication and database infrastructure.

## Research Questions Resolved

### Q1: Which authentication library should we use for Next.js?

**Decision**: Better Auth with JWT plugin

**Rationale**:
- Modern, lightweight authentication library designed for Next.js App Router
- Built-in JWT support (critical for stateless backend authentication)
- Automatic httpOnly cookie handling (XSS prevention)
- TypeScript-first design (type safety)
- Flexible configuration (expiration, secret management)
- Active maintenance and good documentation

**Alternatives Considered**:
1. **NextAuth.js (Auth.js)**:
   - Pros: Most popular, extensive provider support
   - Cons: Session-based by default, heavier bundle size, more complex JWT configuration
   - Why Rejected: Designed primarily for session-based auth; JWT support is secondary

2. **Custom JWT Implementation**:
   - Pros: Full control, minimal dependencies
   - Cons: High security risk (easy to get wrong), no tested patterns, maintenance burden
   - Why Rejected: Reinventing the wheel with security implications

3. **Clerk**:
   - Pros: Full-featured, beautiful UI components
   - Cons: Third-party service (vendor lock-in), cost at scale, not self-hosted
   - Why Rejected: Project requires self-hosted solution

**Best Practices**:
- Store `BETTER_AUTH_SECRET` in environment variable (never commit to Git)
- Set JWT expiration to 24 hours (balance security and UX)
- Use httpOnly cookies (prevents JavaScript access → XSS protection)
- Include user ID and email in JWT payload (minimize database lookups)
- Implement token refresh if needed (future enhancement)

### Q2: How should the FastAPI backend verify JWT tokens?

**Decision**: Custom middleware using PyJWT library

**Rationale**:
- PyJWT is the standard Python library for JWT operations
- Lightweight and well-tested
- Integrates cleanly with FastAPI dependency injection
- Shared secret verification (HMAC-SHA256)
- Simple implementation for our use case

**Alternatives Considered**:
1. **FastAPI-Users**:
   - Pros: Complete authentication solution, built-in JWT support
   - Cons: Opinionated, includes features we don't need (user management, password reset)
   - Why Rejected: Too heavyweight for simple JWT verification

2. **Authlib**:
   - Pros: Comprehensive OAuth/JWT library, enterprise-grade
   - Cons: Complex API, overkill for our needs
   - Why Rejected: Adds unnecessary complexity

3. **python-jose**:
   - Pros: Good JWT support, used in FastAPI tutorials
   - Cons: Less actively maintained than PyJWT
   - Why Rejected: PyJWT is more widely adopted and better maintained

**Implementation Pattern**:
```python
from fastapi import Security, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

async def verify_jwt(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=["HS256"])
        return {"user_id": payload["user_id"], "email": payload["email"]}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
```

**Best Practices**:
- Extract token from `Authorization: Bearer <token>` header
- Verify signature using shared `BETTER_AUTH_SECRET`
- Handle exceptions gracefully (return 401, don't expose internal errors)
- Log verification failures for security monitoring
- Inject authenticated user into request context (FastAPI dependency)

### Q3: Which ORM should we use with Neon PostgreSQL?

**Decision**: SQLModel

**Rationale**:
- Combines Pydantic validation with SQLAlchemy ORM
- Type-safe database operations (Python type hints)
- FastAPI integration (Pydantic models for request/response)
- Simpler syntax than raw SQLAlchemy
- Full PostgreSQL support via SQLAlchemy
- Created by FastAPI author (Sebastián Ramírez)

**Alternatives Considered**:
1. **SQLAlchemy (alone)**:
   - Pros: Most mature Python ORM, comprehensive features
   - Cons: Verbose syntax, separate Pydantic models needed, steeper learning curve
   - Why Rejected: SQLModel provides same power with cleaner syntax

2. **Raw SQL with psycopg2**:
   - Pros: Maximum control, no abstraction overhead
   - Cons: No type safety, manual query building, SQL injection risk, verbose
   - Why Rejected: Too low-level, loses benefits of type hints and validation

3. **Prisma (Python)**:
   - Pros: Modern ORM, great TypeScript support
   - Cons: Primarily TypeScript-focused, Python support experimental
   - Why Rejected: Not production-ready for Python

4. **Django ORM**:
   - Pros: Battle-tested, full-featured
   - Cons: Tied to Django framework, heavyweight for FastAPI
   - Why Rejected: Doesn't integrate with FastAPI

**SQLModel Example**:
```python
from sqlmodel import SQLModel, Field, create_engine, Session
from uuid import UUID, uuid4

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str

# Create engine
engine = create_engine("postgresql://...")

# Query
with Session(engine) as session:
    user = session.get(User, user_id)  # Type-safe!
```

**Best Practices**:
- Use async engine with `asyncpg` driver (better concurrency)
- Define models with type hints (enables IDE autocomplete)
- Use Alembic for migrations (integrates with SQLModel/SQLAlchemy)
- Create indexes on frequently queried columns (email, user_id)
- Use UUIDs for primary keys (better distribution than sequential IDs)

### Q4: How should we hash passwords?

**Decision**: bcrypt with cost factor 10

**Rationale**:
- Industry standard for password hashing since 1999
- Built-in salt generation (no need to manage salts separately)
- Configurable cost factor (balances security and performance)
- Well-vetted against attacks (rainbow tables, brute force)
- Python library well-maintained (`bcrypt` package)

**Alternatives Considered**:
1. **Argon2**:
   - Pros: Winner of Password Hashing Competition 2015, more resistant to GPU attacks
   - Cons: Slightly slower, less widely adopted
   - Why Not Chosen: bcrypt is sufficient for our use case and more familiar

2. **PBKDF2**:
   - Pros: NIST standard, built into Python hashlib
   - Cons: Vulnerable to GPU/ASIC attacks (compared to bcrypt/argon2)
   - Why Rejected: Weaker than bcrypt for same computational cost

3. **SHA-256 (with salt)**:
   - Pros: Fast, simple
   - Cons: Too fast (enables brute force), not designed for passwords
   - Why Rejected: Completely inappropriate for password hashing

**Cost Factor Analysis**:
- Cost 10: ~100ms hashing time (acceptable UX, secure against brute force)
- Cost 12: ~400ms hashing time (more secure but slower UX)
- Cost 8: ~25ms hashing time (too fast, vulnerable to brute force)

**Recommendation**: Cost 10 (default) balances security and user experience.

**Implementation**:
```python
import bcrypt

# Hash password on registration
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=10))

# Verify password on login
is_valid = bcrypt.checkpw(password.encode('utf-8'), hashed)
```

**Best Practices**:
- NEVER store plain-text passwords
- Hash before database insert (application-level, not database-level)
- Use `bcrypt.gensalt()` for automatic salt generation
- Compare hashes using `bcrypt.checkpw()` (timing-safe comparison)
- Consider migrating to Argon2 in the future if security requirements increase

### Q5: How do we connect to Neon Serverless PostgreSQL?

**Decision**: SQLModel with asyncpg driver

**Rationale**:
- Neon provides standard PostgreSQL connection string
- asyncpg is fastest Python PostgreSQL driver (async I/O)
- SQLModel uses SQLAlchemy under the hood (supports asyncpg)
- Connection pooling built-in (handles concurrent requests efficiently)

**Connection String Format**:
```
postgresql://user:password@host/database?sslmode=require
```

**Neon-Specific Considerations**:
- SSL required (Neon enforces `sslmode=require`)
- Serverless architecture (connections automatically scaled)
- Connection pooling recommended (Neon handles many short-lived connections efficiently)

**Implementation**:
```python
from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

# Sync engine (simpler, sufficient for our use case)
engine = create_engine(DATABASE_URL, pool_size=5, max_overflow=10)

# Async engine (better for high concurrency)
async_engine = create_async_engine(
    DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    pool_size=5,
    max_overflow=10
)
```

**Best Practices**:
- Use connection pooling (5 min, 10 max connections)
- Enable SSL (`sslmode=require` in connection string)
- Store connection string in environment variable (never hardcode)
- Test connection on application startup (fail fast if database unreachable)
- Use async operations for better concurrency (optional for MVP)

### Q6: How should we handle CORS between frontend and backend?

**Decision**: FastAPI CORS middleware with specific origin allowlist

**Rationale**:
- Frontend (localhost:3000) and backend (localhost:8000) are different origins
- Browsers enforce CORS policy (blocks requests without proper headers)
- FastAPI provides built-in CORS middleware
- Need to allow credentials (httpOnly cookies)

**CORS Configuration**:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,  # Allow cookies
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Authorization", "Content-Type"],
)
```

**Best Practices**:
- **Development**: Allow `http://localhost:3000` (frontend dev server)
- **Production**: Allow specific domain (e.g., `https://app.example.com`)
- **Never use** `allow_origins=["*"]` with `allow_credentials=True` (security risk)
- Allow only necessary HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Allow only necessary headers (Authorization, Content-Type)

**Security Considerations**:
- Specific origin whitelist prevents unauthorized domains from accessing API
- `allow_credentials=True` required for httpOnly cookies
- Pre-flight requests (OPTIONS) handled automatically by middleware

## Technology Stack Summary

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Frontend Framework | Next.js (App Router) | 16+ | Server-side rendering, routing |
| Frontend Language | TypeScript | 5+ | Type safety |
| Authentication Library | Better Auth | Latest | JWT issuance, session management |
| Styling | Tailwind CSS | Latest | Utility-first CSS |
| Backend Framework | FastAPI | Latest | REST API, async support |
| Backend Language | Python | 3.11+ | Type hints, performance |
| ORM | SQLModel | Latest | Type-safe database operations |
| Database | Neon Serverless PostgreSQL | 16 | Persistent storage |
| Migrations | Alembic | Latest | Schema version control |
| Password Hashing | bcrypt | Latest | Secure password storage |
| JWT Library | PyJWT | Latest | Token verification |
| PostgreSQL Driver | psycopg2-binary / asyncpg | Latest | Database connection |

## Performance Benchmarks (Expected)

| Operation | Target | Rationale |
|-----------|--------|-----------|
| User Registration | < 5 seconds | Includes password hashing (~100ms), database insert (~50ms), network latency |
| User Sign-In | < 5 seconds | Password verification (~100ms), JWT generation (~10ms), cookie storage |
| JWT Verification | < 100ms | Signature verification only (no database lookup) |
| Database Connection | < 3 seconds | Neon cold start can be slow, but connections are pooled |
| Health Check Endpoint | < 50ms | JWT verification + JSON response |

## Security Best Practices Checklist

- [x] Store secrets in environment variables (never hardcode)
- [x] Use httpOnly cookies for JWT storage (XSS prevention)
- [x] Hash passwords with bcrypt (never store plain-text)
- [x] Verify JWT signatures with shared secret
- [x] Return 401 for invalid/missing tokens (don't expose details)
- [x] Use HTTPS in production (SSL/TLS encryption)
- [x] Configure CORS with specific origins (not wildcard)
- [x] Use parameterized queries (SQL injection prevention via ORM)
- [x] Validate email format (Pydantic EmailStr)
- [x] Enforce password minimum length (8 characters)
- [x] Log authentication failures (security monitoring)

## Future Enhancements (Out of Scope for Foundation)

- Token refresh mechanism (extend session without re-login)
- Email verification (confirm email ownership before activation)
- Password reset flow (forgot password functionality)
- OAuth providers (Google, GitHub, etc.)
- Multi-factor authentication (TOTP, SMS)
- Rate limiting (prevent brute force attacks)
- Session management (view/revoke active sessions)
- Account deletion (GDPR compliance)

## References

- Better Auth Documentation: https://www.better-auth.com/docs
- FastAPI Documentation: https://fastapi.tiangolo.com
- SQLModel Documentation: https://sqlmodel.tiangolo.com
- Neon Documentation: https://neon.tech/docs
- PyJWT Documentation: https://pyjwt.readthedocs.io
- bcrypt Documentation: https://pypi.org/project/bcrypt/
- OWASP Password Storage Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- JWT.io (JWT debugger): https://jwt.io

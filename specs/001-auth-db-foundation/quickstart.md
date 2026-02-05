# Quickstart Guide: Authentication and Database Foundation

**Feature**: 001-auth-db-foundation
**Branch**: `001-auth-db-foundation`
**Last Updated**: 2026-02-05

## Prerequisites

Before starting, ensure you have:

- **Node.js 18+** (for Next.js frontend)
- **Python 3.11+** (for FastAPI backend)
- **Git** (for version control)
- **Neon Account** (free tier: https://neon.tech)
- **Code Editor** (VS Code recommended)
- **Terminal** (bash, zsh, or PowerShell)

## Quick Start (TL;DR)

```bash
# 1. Clone and checkout branch
git clone <repository-url>
cd phase-II
git checkout 001-auth-db-foundation

# 2. Set up environment variables
cp .env.example .env
# Edit .env with your Neon DATABASE_URL and generate BETTER_AUTH_SECRET

# 3. Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn src.main:app --reload

# 4. Frontend setup (new terminal)
cd frontend
npm install
npm run dev

# 5. Test
# Visit http://localhost:3000/signup
# Create account, sign in, then test health check
```

## Detailed Setup Instructions

### Step 1: Clone Repository and Checkout Branch

```bash
git clone <repository-url>
cd phase-II
git checkout 001-auth-db-foundation
```

**Expected Output**:
```
Switched to branch '001-auth-db-foundation'
```

### Step 2: Create Neon Database

1. **Sign up for Neon** (if you haven't already):
   - Go to https://neon.tech
   - Create free account

2. **Create a new project**:
   - Click "New Project"
   - Name: "hackathon-todo-app"
   - Region: Choose closest to your location
   - PostgreSQL version: 16 (latest)

3. **Get connection string**:
   - Go to project dashboard
   - Click "Connection Details"
   - Copy the connection string (format: `postgresql://user:password@host/database`)

**Example connection string**:
```
postgresql://neondb_owner:npg_abcdefgh123@ep-cool-bird-a1b2c3d4.us-east-2.aws.neon.tech/neondb?sslmode=require
```

### Step 3: Set Up Environment Variables

1. **Create `.env` file** from example:
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file** with your values:
   ```env
   # Database
   DATABASE_URL=postgresql://neondb_owner:YOUR_PASSWORD@YOUR_HOST/neondb?sslmode=require

   # Authentication (generate a random secret)
   BETTER_AUTH_SECRET=your-super-secret-key-min-32-chars-long

   # Frontend URL (for CORS)
   FRONTEND_URL=http://localhost:3000

   # Backend URL
   BACKEND_URL=http://localhost:8000
   ```

3. **Generate `BETTER_AUTH_SECRET`**:
   ```bash
   # Option 1: Using openssl
   openssl rand -base64 32

   # Option 2: Using Python
   python -c "import secrets; print(secrets.token_urlsafe(32))"

   # Option 3: Using Node.js
   node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
   ```

**Important**: Never commit `.env` to version control! It should be in `.gitignore`.

### Step 4: Backend Setup (FastAPI)

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create Python virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**:
   ```bash
   # Linux/macOS
   source venv/bin/activate

   # Windows (PowerShell)
   venv\Scripts\Activate.ps1

   # Windows (CMD)
   venv\Scripts\activate.bat
   ```

   **Expected Output**: Your terminal prompt should now show `(venv)`.

4. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   **Expected Packages**:
   - fastapi
   - uvicorn[standard]
   - sqlmodel
   - psycopg2-binary (PostgreSQL driver)
   - alembic (migrations)
   - pyjwt (JWT verification)
   - bcrypt (password hashing)
   - python-dotenv (environment variables)
   - pydantic[email] (email validation)

5. **Run database migrations**:
   ```bash
   alembic upgrade head
   ```

   **Expected Output**:
   ```
   INFO  [alembic.runtime.migration] Running upgrade  -> 001, create users table
   ```

6. **Start FastAPI server**:
   ```bash
   uvicorn src.main:app --reload
   ```

   **Expected Output**:
   ```
   INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
   INFO:     Started reloader process [12345] using WatchFiles
   INFO:     Started server process [12346]
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   ```

7. **Verify backend is running**:
   - Open browser: http://localhost:8000/docs
   - You should see FastAPI Swagger UI with API documentation

### Step 5: Frontend Setup (Next.js)

**Open a NEW terminal** (keep backend running in the first terminal).

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

   **Expected Packages**:
   - next (v16+)
   - react
   - react-dom
   - typescript
   - @types/react
   - @types/node
   - better-auth
   - tailwindcss
   - autoprefixer
   - postcss

3. **Start Next.js development server**:
   ```bash
   npm run dev
   ```

   **Expected Output**:
   ```
   ▲ Next.js 16.0.0
   - Local:        http://localhost:3000
   - Network:      http://192.168.1.x:3000

   ✓ Ready in 2.3s
   ```

4. **Verify frontend is running**:
   - Open browser: http://localhost:3000
   - You should see the landing page

### Step 6: Test Authentication Flow

#### 6.1 User Registration

1. **Navigate to signup page**:
   - URL: http://localhost:3000/signup

2. **Fill in the form**:
   - Email: `test@example.com`
   - Password: `password123` (minimum 8 characters)

3. **Submit the form**:
   - Click "Sign Up"
   - Expected: Success message and redirect

4. **Verify in database** (optional):
   ```bash
   # In backend directory, with venv activated
   python -c "
   from src.core.database import engine
   from src.models.user import User
   from sqlmodel import Session, select

   with Session(engine) as session:
       user = session.exec(select(User).where(User.email == 'test@example.com')).first()
       if user:
           print(f'User created: {user.email} (ID: {user.id})')
           print(f'Password is hashed: {user.hashed_password[:20]}...')
       else:
           print('User not found!')
   "
   ```

#### 6.2 User Sign-In

1. **Navigate to signin page**:
   - URL: http://localhost:3000/signin

2. **Fill in the form**:
   - Email: `test@example.com`
   - Password: `password123`

3. **Submit the form**:
   - Click "Sign In"
   - Expected: JWT token issued and stored in httpOnly cookie

4. **Verify JWT token** (optional):
   - Open browser DevTools → Application → Cookies → http://localhost:3000
   - You should see a cookie (name varies by Better Auth config)
   - Value should be a long base64-encoded string (the JWT)

#### 6.3 Test Health Check Endpoint (JWT Verification)

1. **Get JWT token from cookie**:
   - Open browser DevTools → Application → Cookies
   - Copy the JWT token value

2. **Test with curl** (replace `<JWT_TOKEN>` with actual token):
   ```bash
   curl -H "Authorization: Bearer <JWT_TOKEN>" http://localhost:8000/api/health
   ```

   **Expected Response (200 OK)**:
   ```json
   {
     "status": "healthy",
     "user_id": "550e8400-e29b-41d4-a716-446655440000",
     "email": "test@example.com"
   }
   ```

3. **Test without token**:
   ```bash
   curl http://localhost:8000/api/health
   ```

   **Expected Response (401 Unauthorized)**:
   ```json
   {
     "detail": "Missing authentication token"
   }
   ```

4. **Test with invalid token**:
   ```bash
   curl -H "Authorization: Bearer invalid.token.here" http://localhost:8000/api/health
   ```

   **Expected Response (401 Unauthorized)**:
   ```json
   {
     "detail": "Invalid or expired token"
   }
   ```

## Troubleshooting

### Backend Issues

#### Issue: `ModuleNotFoundError: No module named 'fastapi'`
**Solution**: Ensure virtual environment is activated and dependencies installed:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

#### Issue: `sqlalchemy.exc.OperationalError: could not connect to server`
**Solution**: Verify `DATABASE_URL` in `.env` is correct and Neon database is running:
```bash
# Test connection
python -c "from src.core.database import engine; print(engine.url)"
```

#### Issue: `alembic.util.exc.CommandError: Can't locate revision identified by 'head'`
**Solution**: Initialize Alembic if migrations directory is empty:
```bash
alembic revision --autogenerate -m "create users table"
alembic upgrade head
```

### Frontend Issues

#### Issue: `Module not found: Can't resolve 'better-auth'`
**Solution**: Install dependencies:
```bash
npm install
```

#### Issue: `Error: Invalid `BETTER_AUTH_SECRET`
**Solution**: Ensure `.env` file exists and `BETTER_AUTH_SECRET` is at least 32 characters:
```bash
# Generate new secret
openssl rand -base64 32
# Add to .env
```

#### Issue: CORS error when calling backend API
**Solution**: Verify backend CORS configuration allows `http://localhost:3000`:
- Check `backend/src/main.py` CORS middleware
- Ensure `FRONTEND_URL` in `.env` matches frontend URL

### JWT Issues

#### Issue: Token verification fails with "Invalid signature"
**Solution**: Ensure `BETTER_AUTH_SECRET` is **exactly the same** in both:
- Frontend (Better Auth config)
- Backend (JWT verification middleware)

#### Issue: Token expires immediately
**Solution**: Check Better Auth JWT expiration config (should be 24 hours by default).

## Next Steps

After successful setup and testing:

1. **Run `/sp.tasks`** to generate actionable implementation tasks
2. **Review task breakdown** in `specs/001-auth-db-foundation/tasks.md`
3. **Execute tasks via specialized agents** (`/sp.implement`)
4. **Write tests** for all acceptance scenarios
5. **Commit and create PR** (`/sp.git.commit_pr`)

## Development Workflow

```bash
# Terminal 1: Backend (FastAPI)
cd backend
source venv/bin/activate
uvicorn src.main:app --reload

# Terminal 2: Frontend (Next.js)
cd frontend
npm run dev

# Terminal 3: Testing/Database operations
cd backend
source venv/bin/activate
python  # Interactive Python shell
```

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | Neon PostgreSQL connection string | `postgresql://user:pass@host/db` |
| `BETTER_AUTH_SECRET` | Shared secret for JWT signing/verification (min 32 chars) | `abcdefgh123456789012345678901234` |
| `FRONTEND_URL` | Next.js frontend URL (for CORS) | `http://localhost:3000` |
| `BACKEND_URL` | FastAPI backend URL | `http://localhost:8000` |

## Useful Commands

```bash
# Backend
python -m pytest                    # Run all tests
python -m pytest -v                 # Verbose test output
python -m pytest tests/unit         # Run only unit tests
alembic downgrade -1                # Rollback last migration
alembic history                     # View migration history
uvicorn src.main:app --host 0.0.0.0 --port 8000  # Expose backend publicly

# Frontend
npm run build                       # Build for production
npm run start                       # Start production server
npm run lint                        # Run ESLint
npm run type-check                  # Run TypeScript type checker

# Database
psql $DATABASE_URL                  # Connect to Neon PostgreSQL (requires psql)
```

## Health Check Endpoints

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/api/health` | GET | Yes (JWT) | Returns 200 with user ID if authenticated, 401 otherwise |
| `/docs` | GET | No | FastAPI Swagger UI (API documentation) |
| `/` | GET | No | Next.js landing page |

## Support

For issues, refer to:
- **Spec**: [spec.md](./spec.md)
- **Plan**: [plan.md](./plan.md)
- **Data Model**: [data-model.md](./data-model.md)
- **API Contracts**: [contracts/](./contracts/)

For Neon-specific issues: https://neon.tech/docs
For Better Auth issues: https://www.better-auth.com/docs

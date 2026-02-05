# Implementation Plan: Frontend Dashboard & Task Management UI

**Branch**: `003-frontend-dashboard` | **Date**: 2026-02-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-frontend-dashboard/spec.md`

## Summary

Build a responsive Next.js 16+ dashboard that enables authenticated users to perform full CRUD operations on their tasks. The dashboard consumes the FastAPI Task API using Better Auth JWT tokens for authentication. Core features include task list display, creation, editing, deletion, and completion toggling with optimistic UI updates and comprehensive error handling. The application must be fully responsive (320px-2560px) and enforce strict user isolation through JWT-based authentication.

**Technical Approach**: Implement a centralized API client utility that automatically attaches JWT tokens from Better Auth session to all API requests. Build React client components for interactive UI elements (forms, modals, buttons) and leverage Next.js App Router for authentication-protected routes. Use Tailwind CSS for mobile-first responsive design with optimistic updates for perceived performance.

## Technical Context

**Language/Version**: TypeScript 5+ (Frontend), Node.js 20+ runtime
**Primary Dependencies**:
- Next.js 16+ (App Router, React Server Components)
- Better Auth (JWT token management)
- Tailwind CSS 3+ (responsive styling)
- React 19+ (UI components, hooks)
- Fetch API / Axios (HTTP client)

**Storage**: N/A (frontend only - consumes FastAPI backend)
**Testing**: Manual browser testing (Chrome, Firefox, Safari), responsive testing at breakpoints
**Target Platform**: Modern web browsers (Chrome 90+, Firefox 88+, Safari 14+), iOS Safari, Android Chrome
**Project Type**: Web application (frontend only)
**Performance Goals**:
- Task list renders within 3 seconds of page load
- CRUD operations complete within 1 second (optimistic UI)
- Support 1000 tasks without performance degradation
- First Contentful Paint < 1.5 seconds

**Constraints**:
- Must use Next.js 16+ App Router (no Pages Router)
- Tailwind CSS only (no custom CSS files)
- JWT from Better Auth session (stateless authentication)
- API endpoints follow pattern: `/api/{user_id}/tasks/...`
- Client-side validation before API calls
- Optimistic UI updates with rollback on error

**Scale/Scope**:
- 6 user stories (3 P1, 3 P2)
- ~15 React components
- 5 API integration points (list, create, update, delete, toggle)
- 4 responsive breakpoints (mobile, tablet, desktop, wide)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Spec-Driven Development
✅ **PASS** - Feature has complete specification in `specs/003-frontend-dashboard/spec.md` with user stories, functional requirements, and success criteria. Implementation plan being created before coding begins.

### Principle II: Agentic Workflow
✅ **PASS** - Implementation will delegate to `nextjs-ui-builder` agent for all frontend components and pages. No manual coding planned.

### Principle III: Security First
✅ **PASS** - JWT tokens from Better Auth will be included in all API requests via `Authorization: Bearer <token>` header. API client will handle 401 (redirect to login) and 403 (show error) responses. User ID validation against JWT token user ID will be enforced by backend.

### Principle IV: Modern Stack with Strong Typing
✅ **PASS** - TypeScript will be used for all frontend code. Next.js 16+ App Router with React Server Components where applicable. Pydantic validation on backend (Spec 002).

### Principle V: User Isolation
✅ **PASS** - User ID from JWT token used in API URLs (`/api/{user_id}/tasks`). Backend enforces user_id matching (Spec 002). Frontend displays only authenticated user's tasks.

### Principle VI: Responsive Design
✅ **PASS** - Mobile-first design using Tailwind CSS. Responsive breakpoints: mobile (<640px), tablet (640-1024px), desktop (>1024px). Touch targets minimum 44px. No horizontal scrolling.

### Principle VII: Data Persistence
✅ **PASS** - All data persisted via FastAPI backend to Neon PostgreSQL (Spec 002). Frontend consumes REST API for CRUD operations.

**Overall Gate Status**: ✅ **PASS** - All constitutional principles satisfied. No violations to justify.

## Project Structure

### Documentation (this feature)

```text
specs/003-frontend-dashboard/
├── spec.md              # Feature specification
├── plan.md              # This file (/sp.plan output)
├── research.md          # Phase 0 output - API client patterns, Better Auth integration
├── data-model.md        # Phase 1 output - Frontend data models (Task, User types)
├── quickstart.md        # Phase 1 output - Developer setup guide
├── contracts/           # Phase 1 output - TypeScript interfaces for API contracts
│   └── api.types.ts     # Task API TypeScript types
└── checklists/
    └── requirements.md  # Specification quality checklist
```

### Source Code (repository root)

```text
frontend/                           # Next.js 16+ application
├── app/                            # App Router directory
│   ├── (auth)/                     # Authentication route group
│   │   ├── login/                  # Login page
│   │   │   └── page.tsx
│   │   └── signup/                 # Signup page
│   │       └── page.tsx
│   │
│   ├── (dashboard)/                # Protected dashboard route group
│   │   ├── layout.tsx              # Dashboard layout with navbar
│   │   └── page.tsx                # Main dashboard page (task list)
│   │
│   ├── layout.tsx                  # Root layout
│   ├── globals.css                 # Tailwind CSS imports
│   └── error.tsx                   # Global error boundary
│
├── components/                     # Reusable React components
│   ├── ui/                         # Base UI components
│   │   ├── Button.tsx              # Reusable button component
│   │   ├── Input.tsx               # Form input component
│   │   ├── Modal.tsx               # Modal dialog component
│   │   ├── Toast.tsx               # Toast notification component
│   │   └── Spinner.tsx             # Loading spinner
│   │
│   ├── tasks/                      # Task-specific components
│   │   ├── TaskList.tsx            # Task list container
│   │   ├── TaskItem.tsx            # Individual task card
│   │   ├── TaskForm.tsx            # Add/Edit task form
│   │   ├── TaskDeleteConfirm.tsx   # Delete confirmation modal
│   │   └── EmptyState.tsx          # Empty task list state
│   │
│   └── layout/                     # Layout components
│       ├── Navbar.tsx              # Dashboard navigation bar
│       └── Container.tsx           # Responsive container wrapper
│
├── lib/                            # Utility functions and configs
│   ├── api/                        # API client utilities
│   │   ├── client.ts               # Centralized API client with JWT
│   │   ├── tasks.ts                # Task API methods (CRUD)
│   │   └── auth.ts                 # Better Auth integration helpers
│   │
│   ├── hooks/                      # Custom React hooks
│   │   ├── useTasks.ts             # Task data fetching and mutations
│   │   ├── useAuth.ts              # Authentication state hook
│   │   └── useToast.ts             # Toast notification hook
│   │
│   ├── types/                      # TypeScript type definitions
│   │   ├── task.ts                 # Task entity types
│   │   └── api.ts                  # API request/response types
│   │
│   └── utils/                      # Helper functions
│       ├── validation.ts           # Client-side form validation
│       └── errors.ts               # Error message formatting
│
├── public/                         # Static assets
│   └── images/                     # Image assets
│
├── tailwind.config.ts              # Tailwind CSS configuration
├── tsconfig.json                   # TypeScript configuration
├── next.config.js                  # Next.js configuration
├── package.json                    # Dependencies
└── .env.local                      # Environment variables (API URL)
```

**Structure Decision**: Frontend-only web application using Next.js 16+ App Router structure. Components organized by domain (tasks) and type (ui, layout). API client centralized in `lib/api/` for consistent JWT token handling. Custom hooks in `lib/hooks/` for data fetching with optimistic updates. Tailwind CSS for all styling (no custom CSS modules).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No constitutional violations. This section is intentionally left empty.

## Phase 0: Research & Analysis

### Research Tasks

1. **Better Auth JWT Integration**
   - How to extract JWT token from Better Auth session in Next.js 16+
   - Best practices for storing and refreshing JWT tokens
   - Handling token expiration and automatic redirect to login

2. **Next.js 16+ App Router Patterns**
   - Server Components vs Client Components for task list
   - Route groups for authentication (`(auth)`, `(dashboard)`)
   - Middleware for authentication guards
   - Error boundaries and loading states

3. **API Client Architecture**
   - Centralized fetch wrapper with automatic JWT injection
   - Optimistic UI update patterns with React state
   - Error handling and retry logic
   - Type-safe API client with TypeScript generics

4. **State Management Strategy**
   - React useState vs external library (TanStack Query, SWR)
   - Optimistic updates with rollback on error
   - Cache invalidation after mutations
   - Loading and error state management

5. **Responsive Design Patterns**
   - Tailwind CSS mobile-first breakpoints
   - Touch-friendly UI components (44px minimum)
   - Modal dialogs on mobile vs desktop
   - Grid/List view toggle for different screen sizes

### Research Outputs

Will be documented in `research.md`:
- Decision: [Selected approach]
- Rationale: [Why chosen over alternatives]
- Alternatives considered: [Other options evaluated]
- Trade-offs: [Benefits vs costs]

## Phase 1: Design & Contracts

### Data Model

Frontend TypeScript interfaces (documented in `data-model.md`):

```typescript
// Task entity (matches backend API response)
interface Task {
  id: string;
  user_id: string;
  title: string;
  description: string;
  completed: boolean;
  created_at: string; // ISO 8601 timestamp
  updated_at: string; // ISO 8601 timestamp
}

// User entity (from Better Auth session)
interface User {
  id: string;
  email: string;
  name?: string;
}

// API request payloads
interface CreateTaskRequest {
  title: string;
  description?: string;
}

interface UpdateTaskRequest {
  title?: string;
  description?: string;
}

// API response wrappers
interface TaskListResponse {
  tasks: Task[];
  total: number;
}

interface TaskResponse {
  task: Task;
}

interface ErrorResponse {
  detail: string;
  status: number;
}
```

### API Contracts

Contract files in `contracts/` directory:

**File**: `contracts/api.types.ts`
```typescript
// Base API client configuration
export interface ApiConfig {
  baseURL: string;
  timeout: number;
  headers: Record<string, string>;
}

// Task API endpoints (TypeScript types for type safety)
export type TaskApiEndpoints = {
  listTasks: (userId: string) => Promise<Task[]>;
  getTask: (userId: string, taskId: string) => Promise<Task>;
  createTask: (userId: string, data: CreateTaskRequest) => Promise<Task>;
  updateTask: (userId: string, taskId: string, data: UpdateTaskRequest) => Promise<Task>;
  deleteTask: (userId: string, taskId: string) => Promise<void>;
  toggleComplete: (userId: string, taskId: string) => Promise<Task>;
};

// HTTP status codes
export enum HttpStatus {
  OK = 200,
  CREATED = 201,
  BAD_REQUEST = 400,
  UNAUTHORIZED = 401,
  FORBIDDEN = 403,
  NOT_FOUND = 404,
  SERVER_ERROR = 500,
}
```

### Component Architecture

**Page Components** (Server Components where possible):
- `app/(auth)/login/page.tsx` - Login form (Client Component)
- `app/(auth)/signup/page.tsx` - Signup form (Client Component)
- `app/(dashboard)/page.tsx` - Task list page (Server Component wrapper)
- `app/(dashboard)/layout.tsx` - Dashboard layout with navbar

**Client Components** (Interactive):
- `TaskList.tsx` - Fetches and displays tasks
- `TaskForm.tsx` - Add/Edit task form with validation
- `TaskItem.tsx` - Individual task card with actions
- `TaskDeleteConfirm.tsx` - Confirmation modal
- `Navbar.tsx` - User info and logout button

**UI Components** (Reusable):
- `Button.tsx` - Styled button with variants (primary, secondary, danger)
- `Input.tsx` - Form input with label and error message
- `Modal.tsx` - Generic modal dialog
- `Toast.tsx` - Notification toast
- `Spinner.tsx` - Loading indicator

### API Client Implementation Strategy

**Core API Client** (`lib/api/client.ts`):
```typescript
class ApiClient {
  private baseURL: string;
  private getAuthToken: () => Promise<string | null>;

  async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const token = await this.getAuthToken();
    const headers = {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options?.headers,
    };

    const response = await fetch(`${this.baseURL}${endpoint}`, {
      ...options,
      headers,
    });

    if (response.status === 401) {
      // Redirect to login
      window.location.href = '/login';
      throw new Error('Session expired');
    }

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'API request failed');
    }

    return response.json();
  }
}
```

**Task API Methods** (`lib/api/tasks.ts`):
```typescript
export const taskApi = {
  listTasks: (userId: string) =>
    client.request<Task[]>(`/api/${userId}/tasks`),

  createTask: (userId: string, data: CreateTaskRequest) =>
    client.request<Task>(`/api/${userId}/tasks`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  toggleComplete: (userId: string, taskId: string) =>
    client.request<Task>(`/api/${userId}/tasks/${taskId}/complete`, {
      method: 'PATCH',
    }),

  // ... other methods
};
```

### Quickstart Guide

Will be documented in `quickstart.md`:
1. Prerequisites: Node.js 20+, npm/yarn
2. Environment setup: `.env.local` with `NEXT_PUBLIC_API_URL`
3. Install dependencies: `npm install`
4. Run development server: `npm run dev`
5. Access dashboard: `http://localhost:3000`
6. Test authentication flow: Sign up → Login → See dashboard
7. Test CRUD operations: Create, toggle, edit, delete tasks

### Agent Context Update

After completing Phase 1 design:
```bash
.specify/scripts/bash/update-agent-context.sh claude
```

This will update `.claude/context` with:
- Next.js 16+ App Router patterns
- Better Auth integration approach
- API client structure with JWT handling
- Component architecture and file organization
- Tailwind CSS responsive breakpoints

## Phase 2: Implementation Workflow

**Note**: Actual task breakdown will be created by `/sp.tasks` command (not part of this plan).

### High-Level Implementation Sequence

1. **API Client Foundation** (P1 - Critical)
   - Implement centralized API client with JWT token injection
   - Add error handling for 401/403 responses
   - Create TypeScript types for API contracts

2. **Authentication Integration** (P1 - Critical)
   - Extract user ID from Better Auth session
   - Implement auth guard middleware
   - Create useAuth hook for session management

3. **Task List Display** (P1 - Core Feature)
   - Build TaskList component with data fetching
   - Implement EmptyState for no tasks
   - Add loading and error states

4. **Task Creation** (P1 - Core Feature)
   - Build TaskForm component with validation
   - Implement optimistic UI update
   - Handle error states with toast notifications

5. **Task Completion Toggle** (P1 - Core Feature)
   - Add checkbox to TaskItem component
   - Implement PATCH request with optimistic update
   - Rollback on API error

6. **Task Editing** (P2 - Enhancement)
   - Create edit mode in TaskForm
   - Build edit button in TaskItem
   - Handle cancel and save actions

7. **Task Deletion** (P2 - Enhancement)
   - Build TaskDeleteConfirm modal
   - Implement DELETE request
   - Update UI after successful deletion

8. **Responsive Design** (P2 - UX Enhancement)
   - Apply Tailwind CSS mobile-first breakpoints
   - Test on mobile, tablet, desktop viewports
   - Ensure touch targets are 44px minimum

9. **Dashboard Layout** (P1 - Core Structure)
   - Build Navbar with user info and logout
   - Create responsive Container wrapper
   - Implement dashboard layout.tsx

10. **End-to-End Testing** (P2 - Validation)
    - Manual testing across browsers
    - Test user isolation (multiple users)
    - Verify responsive behavior at all breakpoints

### Agent Delegation Strategy

All implementation tasks will be delegated to:
- **`nextjs-ui-builder` agent**: All React components, pages, layouts, and styling
- **Verification**: Manual testing and user acceptance validation

### Dependencies

**Internal** (Must be complete before implementation):
- ✅ Spec 001: Better Auth implementation (JWT token issuance)
- ✅ Spec 002: FastAPI Task API endpoints

**External** (Required packages):
- Next.js 16+
- React 19+
- Tailwind CSS 3+
- Better Auth
- TypeScript 5+

**Environment Variables**:
```bash
# .env.local (frontend)
NEXT_PUBLIC_API_URL=http://localhost:8000  # FastAPI backend URL
BETTER_AUTH_SECRET=<shared-secret>         # JWT verification secret
```

## Risk Analysis

### Technical Risks

1. **JWT Token Management**
   - Risk: Token expiration during active session
   - Mitigation: Implement automatic redirect to login on 401 response
   - Contingency: Add token refresh mechanism if needed

2. **Optimistic UI Updates**
   - Risk: UI state out of sync if API call fails
   - Mitigation: Implement rollback mechanism on error
   - Contingency: Add manual refresh button

3. **Performance with Large Task Lists**
   - Risk: Slow rendering with 1000+ tasks
   - Mitigation: Use React.memo for TaskItem components
   - Contingency: Implement pagination or virtual scrolling

4. **Cross-Browser Compatibility**
   - Risk: Styling inconsistencies across browsers
   - Mitigation: Use Tailwind CSS (cross-browser tested)
   - Contingency: Add browser-specific CSS fixes if needed

### Implementation Risks

1. **Scope Creep**
   - Risk: Adding features not in spec (dark mode, search, filters)
   - Mitigation: Strict adherence to spec-driven workflow
   - Contingency: Document feature requests in backlog

2. **Testing Coverage**
   - Risk: Missing edge cases (network failures, concurrent edits)
   - Mitigation: Comprehensive manual testing checklist
   - Contingency: Add automated tests in future iteration

## Success Criteria

Implementation will be considered complete when:

1. ✅ All functional requirements (FR-001 through FR-016) are implemented
2. ✅ All user stories (P1 and P2) pass acceptance scenarios
3. ✅ Dashboard loads within 3 seconds on 4G connection
4. ✅ CRUD operations complete within 1 second (optimistic UI)
5. ✅ Responsive design works on mobile (320px), tablet (768px), desktop (1920px)
6. ✅ Error states display user-friendly messages
7. ✅ User isolation verified (multiple users see only their tasks)
8. ✅ JWT authentication works (token expiration redirects to login)
9. ✅ No TypeScript compilation errors
10. ✅ All constitutional principles remain satisfied

## Next Steps

1. ✅ Complete this plan document
2. Execute Phase 0: Research documented patterns → `research.md`
3. Execute Phase 1: Design data models and contracts → `data-model.md`, `contracts/`, `quickstart.md`
4. Update agent context: Run `.specify/scripts/bash/update-agent-context.sh claude`
5. Re-validate Constitution Check after design phase
6. Run `/sp.tasks` to generate actionable task breakdown → `tasks.md`
7. Run `/sp.implement` to execute tasks via `nextjs-ui-builder` agent
8. Run `/sp.git.commit_pr` to commit changes and create pull request
9. Consider ADR for architectural decisions (if significant)

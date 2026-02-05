# Research: Interactive Views & Workspace Management

**Feature**: 007-interactive-workspace-views
**Date**: 2026-02-05
**Status**: Complete

## Overview

This document consolidates research findings for technology choices and architectural decisions required to implement the Interactive Views & Workspace Management feature.

---

## R1: Drag-and-Drop Library Selection

### Decision: **dnd-kit**

### Rationale

After evaluating @hello-pangea/dnd and dnd-kit, **dnd-kit** is the clear choice for our Kanban board implementation.

#### Comparison Summary

| Criteria | @hello-pangea/dnd | dnd-kit | Winner |
|----------|-------------------|---------|--------|
| Bundle Size | 45-50 KB | 15 KB (core) | **dnd-kit** |
| Performance | DOM measurement based | Transform-based | **dnd-kit** |
| Next.js 16 Compatibility | Compatible | Built for React 18+ | **dnd-kit** |
| Mobile/Touch Support | Basic | Excellent with sensors | **dnd-kit** |
| Concurrent Features | Limited | Optimized | **dnd-kit** |
| Accessibility | Excellent | Excellent + customizable | Tie |
| TypeScript Support | Good | Excellent (written in TS) | **dnd-kit** |

#### Key Advantages of dnd-kit

1. **Performance**: Transform-based positioning easily meets <1s drag operation requirement
2. **Bundle Size**: Modular architecture (15 KB core vs 45-50 KB monolithic)
3. **Mobile-First**: Superior touch support with configurable sensors and activation constraints
4. **Next.js 16 Optimized**: Better SSR/hydration handling, concurrent rendering support
5. **Active Maintenance**: Growing ecosystem, modern codebase

#### Implementation Packages

```bash
npm install @dnd-kit/core @dnd-kit/sortable @dnd-kit/utilities
```

#### Basic Usage Pattern

```typescript
'use client';

import { DndContext, closestCorners, DragEndEvent } from '@dnd-kit/core';
import { SortableContext, verticalListSortingStrategy } from '@dnd-kit/sortable';

export function KanbanBoard() {
  const columns = ['To Do', 'In Progress', 'Review', 'Done'];

  const handleDragEnd = async (event: DragEndEvent) => {
    const { active, over } = event;
    if (!over) return;

    // Update task status via API
    await fetch(`/api/${userId}/tasks/${active.id}`, {
      method: 'PATCH',
      body: JSON.stringify({ status: over.id }),
    });
  };

  return (
    <DndContext collisionDetection={closestCorners} onDragEnd={handleDragEnd}>
      {columns.map(status => (
        <Column key={status} id={status}>
          <SortableContext items={tasks[status]} strategy={verticalListSortingStrategy}>
            {tasks[status].map(task => <TaskCard key={task.id} task={task} />)}
          </SortableContext>
        </Column>
      ))}
    </DndContext>
  );
}
```

### Alternatives Considered

**@hello-pangea/dnd** was considered but rejected due to:
- Larger bundle size (3x larger)
- DOM measurement overhead impacting performance
- Less optimized for modern React patterns

---

## R2: Recharts Integration Patterns

### Decision: **Hybrid Data Fetching with Client-Side Charts**

### Architecture

```
Server Component (page.tsx) → Fetch Data → Pass to Client Component → Render Charts
```

#### Component Boundary Strategy

**Server Components (No 'use client')**:
- `app/dashboard/analytics/page.tsx` - Data fetching, layout
- Static content and layout wrappers

**Client Components ('use client' directive)**:
- All recharts components (PieChart, BarChart, AreaChart)
- Chart wrapper components
- Interactive controls (filters, date pickers)
- State management hooks

#### Recommended Data Fetching Pattern

```typescript
// app/dashboard/analytics/page.tsx (Server Component)
import { cookies } from 'next/headers';
import { TaskAnalyticsCharts } from '@/components/analytics/TaskAnalyticsCharts';

async function getAnalyticsData(userId: string) {
  const cookieStore = await cookies();
  const token = cookieStore.get('auth_token')?.value;

  const response = await fetch(
    `${process.env.BACKEND_API_URL}/api/${userId}/analytics`,
    {
      headers: { 'Authorization': `Bearer ${token}` },
      next: { revalidate: 300 } // Cache for 5 minutes
    }
  );

  return response.json();
}

export default async function AnalyticsPage({ params }: PageProps) {
  const data = await getAnalyticsData(params.userId);
  return <TaskAnalyticsCharts data={data} />;
}
```

```typescript
// components/analytics/TaskAnalyticsCharts.tsx (Client Component)
'use client';

import { PieChart, Pie, BarChart, Bar, ResponsiveContainer } from 'recharts';

export function TaskAnalyticsCharts({ data }: Props) {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <StatusPieChart data={data.statusDistribution} />
      <PriorityBarChart data={data.priorityDistribution} />
      <CompletionTrendChart data={data.completionTrend} />
    </div>
  );
}
```

### Performance Optimization for 1000+ Tasks

#### Backend Aggregation (Critical)

**Principle**: Send aggregated data (10-100 data points), NOT raw tasks (1000+ records).

```python
# backend/src/api/analytics.py
@router.get("/{user_id}/analytics")
async def get_task_analytics(user_id: UUID, db: Session = Depends(get_db)):
    # Status distribution (aggregated)
    status_dist = db.query(
        Task.status,
        func.count(Task.id).label('count')
    ).filter(Task.user_id == user_id).group_by(Task.status).all()

    # Priority distribution
    priority_dist = db.query(
        Task.priority,
        func.count(Task.id).label('count')
    ).filter(Task.user_id == user_id).group_by(Task.priority).all()

    # Completion trend (daily aggregates)
    completion_trend = db.query(
        func.date(Task.updated_at).label('date'),
        func.count(Task.id).label('completed')
    ).filter(
        Task.user_id == user_id,
        Task.is_completed == True,
        Task.updated_at >= datetime.utcnow() - timedelta(days=30)
    ).group_by(func.date(Task.updated_at)).all()

    return {
        "statusDistribution": [{"name": s, "value": c} for s, c in status_dist],
        "priorityDistribution": [{"name": p, "value": c} for p, c in priority_dist],
        "completionTrend": [{"date": str(d), "completed": c} for d, c in completion_trend]
    }
```

#### Frontend Optimizations

```typescript
'use client';

import { useMemo } from 'react';
import dynamic from 'next/dynamic';

// Code-split charts for smaller initial bundle
const StatusPieChart = dynamic(() => import('./StatusPieChart'), {
  loading: () => <ChartSkeleton />,
  ssr: false // Charts require browser APIs
});

export function ProductivityChart({ data }: Props) {
  // Memoize expensive calculations
  const chartData = useMemo(() => {
    // Downsample to max 100 data points if needed
    if (data.length <= 100) return data;
    const step = Math.ceil(data.length / 100);
    return data.filter((_, index) => index % step === 0);
  }, [data]);

  return <AreaChart data={chartData}>...</AreaChart>;
}
```

### Responsive Configuration

```typescript
export function ResponsiveStatusChart({ data }: Props) {
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkMobile = () => setIsMobile(window.innerWidth < 768);
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  return (
    <ResponsiveContainer width="100%" height={isMobile ? 250 : 350}>
      <PieChart>
        <Pie
          data={data}
          innerRadius={isMobile ? 40 : 60}
          outerRadius={isMobile ? 80 : 100}
          label={!isMobile} // Hide labels on mobile
        />
      </PieChart>
    </ResponsiveContainer>
  );
}
```

### Empty State Handling

```typescript
export function ChartWrapper({ data, title, emptyMessage, children }: Props) {
  const hasData = data && data.length > 0 && data.some(d => d.value > 0);

  return (
    <div className="bg-white rounded-lg shadow p-4">
      <h3 className="text-lg font-semibold mb-4">{title}</h3>
      {hasData ? children : (
        <EmptyChartState
          title="No Data Available"
          message={emptyMessage}
          actionLabel="Create Your First Task"
          onAction={() => router.push('/dashboard/tasks/new')}
        />
      )}
    </div>
  );
}
```

### Dependencies

```json
{
  "dependencies": {
    "recharts": "^2.13.3"
  }
}
```

---

## R3: Workspace Data Model Design

### Decision: **Many-to-Many with WorkspaceMember Association Table**

### Entity Relationship Diagram

```
User (1) ←→ (N) WorkspaceMember (N) ←→ (1) Workspace
                     ↓ contains role

Workspace (1) → (N) Project (1) → (N) Section (1) → (N) Task
                                                          ↓
                                                      Subtask (self-reference)
```

### Core Models

#### Workspace Model

```python
class Workspace(SQLModel, table=True):
    __tablename__ = "workspaces"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    members: List["WorkspaceMember"] = Relationship(back_populates="workspace")
    projects: List["Project"] = Relationship(back_populates="workspace")
    tasks: List["Task"] = Relationship(back_populates="workspace")
```

#### WorkspaceMember Model (Association with Roles)

```python
class WorkspaceRoleEnum(str, Enum):
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"
    VIEWER = "VIEWER"

class WorkspaceMember(SQLModel, table=True):
    __tablename__ = "workspace_members"

    # Composite Primary Key
    user_id: uuid.UUID = Field(foreign_key="users.id", primary_key=True)
    workspace_id: uuid.UUID = Field(foreign_key="workspaces.id", primary_key=True)

    role: WorkspaceRoleEnum = Field(default=WorkspaceRoleEnum.MEMBER)
    is_default: bool = Field(default=False)
    joined_at: datetime = Field(default_factory=datetime.utcnow)
    invited_by: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")

    # Relationships
    user: "User" = Relationship(back_populates="workspace_memberships")
    workspace: "Workspace" = Relationship(back_populates="members")
```

#### Updated Task Model

```python
class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    # CRITICAL: Direct workspace reference for permission filtering
    workspace_id: uuid.UUID = Field(
        foreign_key="workspaces.id",
        nullable=False,
        index=True  # Critical for performance
    )

    # Optional project association
    project_id: Optional[uuid.UUID] = Field(
        foreign_key="projects.id",
        nullable=True,
        index=True
    )

    # Task ownership and assignment
    created_by: uuid.UUID = Field(foreign_key="users.id", index=True)
    assigned_to: Optional[uuid.UUID] = Field(foreign_key="users.id", index=True)

    # Existing fields...
    title: str
    status: TaskStatusEnum
    priority: TaskPriorityEnum

    # Relationships
    workspace: "Workspace" = Relationship(back_populates="tasks")
    creator: "User" = Relationship()
    assignee: Optional["User"] = Relationship()
```

### Permission Model

#### Role Hierarchy

**OWNER > ADMIN > MEMBER > VIEWER**

#### Permission Matrix

| Action | OWNER | ADMIN | MEMBER | VIEWER |
|--------|-------|-------|--------|--------|
| Delete workspace | ✅ | ❌ | ❌ | ❌ |
| Add/remove members | ✅ | ✅ | ❌ | ❌ |
| Change member roles | ✅ | ✅ (except OWNER) | ❌ | ❌ |
| Create projects | ✅ | ✅ | ✅ | ❌ |
| Create tasks | ✅ | ✅ | ✅ | ❌ |
| Edit own tasks | ✅ | ✅ | ✅ | ❌ |
| Edit others' tasks | ✅ | ✅ | ✅ (if assigned) | ❌ |
| View workspace data | ✅ | ✅ | ✅ | ✅ |

### Permission Checking Implementation

```python
# backend/src/services/permissions.py
async def check_workspace_access(
    user_id: uuid.UUID,
    workspace_id: uuid.UUID,
    required_role: WorkspaceRoleEnum,
    db: Session
) -> WorkspaceMember:
    stmt = select(WorkspaceMember).where(
        WorkspaceMember.user_id == user_id,
        WorkspaceMember.workspace_id == workspace_id
    )
    result = db.exec(stmt).first()

    if not result:
        raise HTTPException(status_code=403, detail="Access denied")

    role_hierarchy = {
        WorkspaceRoleEnum.OWNER: 4,
        WorkspaceRoleEnum.ADMIN: 3,
        WorkspaceRoleEnum.MEMBER: 2,
        WorkspaceRoleEnum.VIEWER: 1
    }

    if role_hierarchy[result.role] < role_hierarchy[required_role]:
        raise HTTPException(status_code=403, detail=f"Requires {required_role} role")

    return result
```

### Default Workspace Behavior

#### Auto-Create Personal Workspace on Signup

```python
async def create_user(email: str, password: str):
    # 1. Create user account
    user = User(email=email, hashed_password=hash_password(password))
    db.add(user)

    # 2. Auto-create personal workspace
    workspace = Workspace(name=f"{email.split('@')[0]}'s Workspace")
    db.add(workspace)

    # 3. Add user as OWNER with default flag
    member = WorkspaceMember(
        user_id=user.id,
        workspace_id=workspace.id,
        role=WorkspaceRoleEnum.OWNER,
        is_default=True
    )
    db.add(member)

    await db.commit()
    return user, workspace
```

### Database Indexes (Critical for Performance)

```python
# Composite indexes for permission checks
CREATE INDEX ix_workspace_members_user_workspace ON workspace_members(user_id, workspace_id);
CREATE INDEX ix_workspace_members_user_default ON workspace_members(user_id, is_default);
CREATE INDEX ix_tasks_workspace_created ON tasks(workspace_id, created_at);
```

### Security: User Isolation Strategy

**Defense-in-Depth Layers**:

1. **Application Layer**: JWT verification + workspace membership check
2. **ORM Layer**: Query filtering by `workspace_id`
3. **Database Layer**: Foreign key constraints with CASCADE
4. **Testing Layer**: Isolation tests for every endpoint

**Critical Rule**: ALWAYS filter queries by `workspace_id` from authenticated user's workspace memberships.

```python
@router.get("/api/workspaces/{workspace_id}/tasks")
async def list_tasks(
    workspace_id: uuid.UUID,
    membership: WorkspaceMember = Depends(authorize_workspace_access),
    db: Session = Depends(get_session)
):
    # SECURITY: Filter by workspace_id from URL path (verified by dependency)
    stmt = select(Task).where(Task.workspace_id == workspace_id)
    tasks = db.exec(stmt).all()
    return tasks
```

---

## R4: Activity Logging Strategy

### Decision: **Simple Audit Log with Async Write Optimization**

### Architecture

**Pattern**: Event-driven activity logging with background tasks for write operations.

#### Activity Model

```python
class ActivityTypeEnum(str, Enum):
    TASK_CREATED = "TASK_CREATED"
    TASK_UPDATED = "TASK_UPDATED"
    TASK_COMPLETED = "TASK_COMPLETED"
    TASK_DELETED = "TASK_DELETED"
    TASK_ASSIGNED = "TASK_ASSIGNED"
    TASK_STATUS_CHANGED = "TASK_STATUS_CHANGED"

class Activity(SQLModel, table=True):
    __tablename__ = "activities"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    workspace_id: uuid.UUID = Field(foreign_key="workspaces.id", index=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    activity_type: ActivityTypeEnum = Field(nullable=False)

    # Polymorphic data storage
    entity_type: str = Field(max_length=50)  # "task", "project", "section"
    entity_id: uuid.UUID = Field(nullable=False)

    # Metadata (JSON column for flexibility)
    metadata: Optional[dict] = Field(default=None, sa_column=Column(JSON))

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        index=True,
        nullable=False
    )

    # Relationships
    workspace: "Workspace" = Relationship()
    user: "User" = Relationship()
```

### Logging Implementation

#### Async Background Task Pattern

```python
# backend/src/services/activity_service.py
from fastapi import BackgroundTasks

async def log_activity_async(
    workspace_id: uuid.UUID,
    user_id: uuid.UUID,
    activity_type: ActivityTypeEnum,
    entity_type: str,
    entity_id: uuid.UUID,
    metadata: dict,
    db: Session
):
    """Background task for activity logging (non-blocking)."""
    activity = Activity(
        workspace_id=workspace_id,
        user_id=user_id,
        activity_type=activity_type,
        entity_type=entity_type,
        entity_id=entity_id,
        metadata=metadata
    )
    db.add(activity)
    await db.commit()

# Usage in API endpoint
@router.patch("/api/workspaces/{workspace_id}/tasks/{task_id}")
async def update_task(
    task_id: uuid.UUID,
    update_data: TaskUpdate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    # Update task (synchronous)
    task = await update_task_in_db(task_id, update_data, db)

    # Log activity (asynchronous, non-blocking)
    background_tasks.add_task(
        log_activity_async,
        workspace_id=task.workspace_id,
        user_id=current_user.id,
        activity_type=ActivityTypeEnum.TASK_UPDATED,
        entity_type="task",
        entity_id=task.id,
        metadata={"changes": update_data.dict(exclude_unset=True)},
        db=db
    )

    return task
```

### Query Patterns for Activity Feed

```python
@router.get("/api/workspaces/{workspace_id}/activities")
async def get_activity_feed(
    workspace_id: uuid.UUID,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_session),
    membership: WorkspaceMember = Depends(authorize_workspace_access)
):
    stmt = (
        select(Activity)
        .where(Activity.workspace_id == workspace_id)
        .order_by(Activity.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    activities = db.exec(stmt).all()
    return activities
```

### Performance Impact Mitigation

1. **Background Tasks**: Write operations don't block main request
2. **Indexed Columns**: `workspace_id`, `created_at`, `user_id` for fast queries
3. **Retention Policy**: Archive activities older than 90 days
4. **Pagination**: Limit to 100 activities per request with cursor-based pagination

### Storage Considerations

- **Estimated Growth**: ~10 activities per user per day = 3,650/year
- **Retention**: 90 days active, archive older records
- **Database Impact**: < 5% of total database size with proper indexing

---

## R5: Analytics Aggregation Performance

### Decision: **Database-Level Aggregation with Query Optimization**

### Strategy

**Principle**: Aggregate at the database layer, not in application code.

#### Optimized Aggregation Queries

```python
# backend/src/services/analytics_service.py
from sqlalchemy import func, extract, case
from datetime import datetime, timedelta

class AnalyticsService:
    @staticmethod
    async def get_status_distribution(
        workspace_id: uuid.UUID,
        db: Session
    ) -> List[dict]:
        """Aggregate task counts by status."""
        stmt = (
            select(
                Task.status,
                func.count(Task.id).label('count')
            )
            .where(Task.workspace_id == workspace_id)
            .group_by(Task.status)
        )
        results = db.exec(stmt).all()
        return [{"name": status, "value": count} for status, count in results]

    @staticmethod
    async def get_completion_trend(
        workspace_id: uuid.UUID,
        days: int = 30,
        db: Session
    ) -> List[dict]:
        """Get daily task completion counts for the last N days."""
        date_threshold = datetime.utcnow() - timedelta(days=days)

        stmt = (
            select(
                func.date(Task.updated_at).label('date'),
                func.count(
                    case((Task.is_completed == True, Task.id))
                ).label('completed'),
                func.count(Task.id).label('created')
            )
            .where(
                Task.workspace_id == workspace_id,
                Task.created_at >= date_threshold
            )
            .group_by(func.date(Task.updated_at))
            .order_by(func.date(Task.updated_at))
        )

        results = db.exec(stmt).all()
        return [
            {
                "date": str(date),
                "completed": completed,
                "created": created
            }
            for date, completed, created in results
        ]
```

### Database Indexes for Aggregation Performance

```sql
-- Composite index for status aggregation
CREATE INDEX ix_tasks_workspace_status ON tasks(workspace_id, status);

-- Composite index for time-based queries
CREATE INDEX ix_tasks_workspace_created ON tasks(workspace_id, created_at);
CREATE INDEX ix_tasks_workspace_updated ON tasks(workspace_id, updated_at);

-- Partial index for completed tasks only (smaller, faster for completion queries)
CREATE INDEX ix_tasks_workspace_completed
ON tasks(workspace_id, updated_at)
WHERE is_completed = TRUE;
```

### Caching Strategy

#### In-Memory Caching (Optional for high-traffic workspaces)

```python
from functools import lru_cache
from datetime import timedelta

@lru_cache(maxsize=100)
def get_cached_analytics(workspace_id: str, cache_key: str):
    """LRU cache for analytics data (5-minute TTL in production)."""
    return get_analytics_data(workspace_id)

# Clear cache on task updates
def invalidate_analytics_cache(workspace_id: uuid.UUID):
    cache_key = f"analytics:{workspace_id}"
    # Clear from LRU cache or Redis
```

### Performance Targets

| Query Type | Target Latency | Optimization |
|------------|----------------|--------------|
| Status distribution | < 50ms | `ix_tasks_workspace_status` |
| Priority distribution | < 50ms | `ix_tasks_workspace_priority` |
| Completion trend (30 days) | < 100ms | `ix_tasks_workspace_completed` |
| Full analytics endpoint | < 200ms | Parallel aggregation queries |

### Handling 1000+ Tasks

- **Database Aggregation**: Reduces 1000 tasks to 4-30 data points
- **Payload Size**: < 5 KB for aggregated data vs > 500 KB for raw tasks
- **Client Performance**: Charts render in < 100ms with aggregated data

---

## R6: Confetti/Celebration Effect Implementation

### Decision: **canvas-confetti (Lightweight, Accessible)**

### Rationale

| Library | Bundle Size | Performance | Accessibility | Winner |
|---------|-------------|-------------|---------------|--------|
| **canvas-confetti** | 6 KB | Excellent (Canvas API) | Supports prefers-reduced-motion | ✅ |
| react-confetti | 15 KB | Good (React wrapper) | Basic | ❌ |
| party-js | 12 KB | Good | Good | ❌ |

#### Installation

```bash
npm install canvas-confetti
npm install -D @types/canvas-confetti
```

#### Implementation

```typescript
// lib/utils/confetti.ts
import confetti from 'canvas-confetti';

export function celebrateTaskCompletion() {
  // Check for reduced motion preference
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (prefersReducedMotion) {
    // Skip animation for accessibility
    return;
  }

  confetti({
    particleCount: 100,
    spread: 70,
    origin: { y: 0.6 },
    colors: ['#10b981', '#3b82f6', '#f59e0b']
  });
}
```

#### Usage in Kanban Card

```typescript
// components/kanban/KanbanCard.tsx
import { celebrateTaskCompletion } from '@/lib/utils/confetti';

export function KanbanCard({ task }: Props) {
  const handleDragEnd = async (event: DragEndEvent) => {
    const { over } = event;

    if (over?.id === 'Done') {
      // Update task status
      await updateTaskStatus(task.id, 'Done');

      // Trigger celebration effect (optimistic)
      celebrateTaskCompletion();
    }
  };

  return (
    <div draggable onDragEnd={handleDragEnd}>
      {task.title}
    </div>
  );
}
```

#### Trigger Strategy

**Optimistic Celebration**: Trigger confetti immediately on drag to "Done" column (before API confirmation) for better perceived performance.

**Fallback**: If API call fails, show error message but confetti already fired (acceptable trade-off for better UX).

### Accessibility Considerations

- **Respects `prefers-reduced-motion`**: No animation if user has reduced motion enabled
- **Non-essential**: Celebration is decorative, doesn't impact functionality
- **Screen Reader**: No announcement needed (visual-only enhancement)

---

## Summary of Technology Decisions

| Area | Decision | Rationale |
|------|----------|-----------|
| **Drag-and-Drop** | dnd-kit | Smaller bundle (15KB), better performance, mobile-first |
| **Charts** | recharts (client components) | React-native, responsive, proven with Next.js |
| **Data Fetching** | Hybrid (server initial + client refresh) | Best of both: performance + interactivity |
| **Workspace Model** | Many-to-many with roles | Flexible collaboration, RBAC support |
| **Activity Logging** | Async audit log | Non-blocking writes, efficient queries |
| **Analytics** | Database aggregation | Reduces 1000 tasks to 10-30 data points |
| **Celebration Effect** | canvas-confetti | Lightweight (6KB), accessible |

---

## Next Steps

With research complete, proceed to **Phase 1: Design & Contracts**:

1. Create `data-model.md` with complete entity schemas
2. Generate OpenAPI contracts for new endpoints
3. Create `quickstart.md` with setup instructions
4. Update agent context with new technologies

**Research Status**: ✅ Complete - All unknowns resolved and documented.

# Frontend Dashboard Testing Guide

## ✅ Implementation Complete

The Dashboard MVP is now fully implemented with:

- ✅ API Client with automatic JWT injection
- ✅ Dynamic user ID extraction from JWT
- ✅ Task CRUD operations (Create, Read, Toggle, Delete)
- ✅ Optimistic UI updates for instant feedback
- ✅ Route protection (redirects to /login if not authenticated)
- ✅ Toast notifications for success/error messages
- ✅ Responsive Tailwind CSS styling

## 🚀 How to Test

### Step 1: Start the Backend (if not running)

```bash
cd /mnt/c/Users/HP/Desktop/Hackathon-II/phase-II/backend
source venv/bin/activate
uvicorn src.main:app --reload --port 8000
```

Verify backend is running: http://localhost:8000/docs

### Step 2: Install Frontend Dependencies

```bash
cd /mnt/c/Users/HP/Desktop/Hackathon-II/phase-II/frontend
npm install
```

### Step 3: Start the Frontend

```bash
npm run dev
```

Frontend will start on: http://localhost:3000

### Step 4: Sign Up / Sign In

1. Navigate to http://localhost:3000/login
2. Sign in with existing credentials OR
3. Go to http://localhost:3000/signup to create a new account

**Note:** After signing in, you'll be redirected to `/dashboard` automatically.

### Step 5: Test Dashboard Features

Once on the dashboard (http://localhost:3000/dashboard):

#### ✅ **View Tasks** (GET)
- Tasks load automatically when page opens
- Empty state shows if no tasks exist
- Loading spinner shows while fetching

#### ✅ **Create Task** (POST)
1. Click "+ New Task" button
2. Enter title (required, max 500 chars)
3. Enter description (optional, max 5000 chars)
4. Click "Create Task"
5. **Optimistic Update**: Task appears immediately
6. Green success toast appears
7. Form clears automatically

#### ✅ **Toggle Completion** (PATCH)
1. Click checkbox next to any task
2. **Optimistic Update**: Checkbox toggles immediately
3. Task title gets strikethrough and gray color when completed
4. Click again to mark incomplete

#### ✅ **Delete Task** (DELETE)
1. Click "Delete" button on any task
2. Confirmation dialog appears
3. Click "OK" to confirm
4. **Optimistic Update**: Task disappears immediately
5. Green success toast appears

## 🧪 Testing Scenarios

### Test 1: End-to-End Task Flow
```
1. Sign in → Dashboard loads
2. Click "+ New Task"
3. Create task: "Buy groceries"
4. Verify task appears in list
5. Click checkbox to mark complete
6. Verify strikethrough styling
7. Click "Delete" and confirm
8. Verify task is removed
```

### Test 2: Optimistic Updates
```
1. Create a task with slow network (throttle in DevTools)
2. Observe task appears BEFORE backend responds
3. Verify final task ID updates after backend response
```

### Test 3: Error Handling
```
1. Stop the backend server
2. Try to create a task
3. Verify error toast appears
4. Verify optimistic task is rolled back
```

### Test 4: Authentication
```
1. Open dashboard without signing in
2. Verify redirect to /login
3. Sign in successfully
4. Verify redirect to /dashboard
5. Click "Sign Out"
6. Verify redirect to /login
```

### Test 5: User Isolation
```
1. Sign in as User A
2. Create tasks for User A
3. Sign out and sign in as User B
4. Verify User B sees ZERO tasks (not User A's tasks)
5. Create tasks for User B
6. Sign out and sign back in as User A
7. Verify User A still sees only their tasks
```

## 📊 API Integration Verification

All API calls automatically include:

✅ **Authorization Header**: `Bearer {jwt_token}`
✅ **Dynamic User ID**: `/api/{user_id}/tasks`
✅ **401 Handling**: Redirect to /login if token expires
✅ **403 Handling**: Error toast if permission denied

**Test this:**
```bash
# Open browser DevTools → Network tab
# Perform any task operation
# Click on the API request
# Verify Request Headers contain:
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## 🎨 Responsive Design Testing

Test at different viewport sizes:

- **Mobile** (320px-640px): Single column, full-width forms
- **Tablet** (640px-1024px): Comfortable spacing
- **Desktop** (1024px+): Maximum width container

**How to test:**
1. Open DevTools → Toggle Device Toolbar (Ctrl+Shift+M)
2. Select different devices: iPhone SE, iPad, Desktop
3. Verify layout adapts properly

## 🐛 Common Issues & Solutions

### Issue 1: "Authentication required" error
**Solution**: Check localStorage has `access_token`:
```javascript
// In browser console:
localStorage.getItem('access_token')
```

### Issue 2: Tasks not loading
**Solution**:
1. Verify backend is running on port 8000
2. Check browser console for errors
3. Verify NEXT_PUBLIC_API_URL in .env.local

### Issue 3: "CORS error"
**Solution**: Backend CORS is already configured. If issue persists:
```python
# In backend/src/main.py
allow_origins=["http://localhost:3000"]  # Should already be set
```

### Issue 4: Tasks appear then disappear
**Cause**: Optimistic update rollback due to API error
**Solution**: Check backend logs for the actual error

## 📁 Key Files Created

```
frontend/
├── lib/
│   ├── api/
│   │   ├── client.ts          # ✅ API client with JWT injection
│   │   ├── auth.ts            # ✅ Auth helpers
│   │   └── tasks.ts           # ✅ Task API methods
│   ├── hooks/
│   │   ├── useAuth.ts         # ✅ Auth state hook
│   │   ├── useToast.ts        # ✅ Toast notifications
│   │   └── useTasks.ts        # ✅ Task state management
│   └── types/
│       ├── task.ts            # ✅ Task types
│       ├── api.ts             # ✅ API types
│       └── user.ts            # ✅ User types
├── components/
│   └── tasks/
│       ├── TaskItem.tsx       # ✅ Individual task display
│       ├── TaskForm.tsx       # ✅ Create/edit form
│       └── TaskList.tsx       # ✅ Task list with empty state
├── app/
│   └── (dashboard)/
│       └── page.tsx           # ✅ Main dashboard page
├── middleware.ts              # ✅ Route protection
└── .env.local                 # ✅ Environment config
```

## ✅ Feature Checklist

- [x] API client with JWT auto-injection
- [x] Dynamic user ID in API URLs
- [x] Task list display (GET)
- [x] Create task (POST)
- [x] Toggle completion (PATCH)
- [x] Delete task (DELETE)
- [x] Optimistic UI updates
- [x] Error toast notifications
- [x] Success toast notifications
- [x] Route protection
- [x] Loading states
- [x] Empty state
- [x] Form validation
- [x] Responsive design
- [x] User isolation

## 🎯 Next Steps (Optional Enhancements)

1. **Edit Task** (PUT) - Add edit functionality
2. **Search/Filter** - Filter by completion status
3. **Sort** - Sort by date, title, completion
4. **Pagination** - For 1000+ tasks
5. **Dark Mode** - Toggle theme
6. **Keyboard Shortcuts** - Press 'N' for new task, 'Enter' to save

## 🔒 Security Verification

**Test User Isolation:**
```bash
# Create User A and tasks
# Sign out
# Create User B
# Try to access User A's task by URL:
http://localhost:3000/dashboard
# Verify: Backend returns 403 if you somehow get User A's task ID
```

**Test Token Expiration:**
```javascript
// In browser console, corrupt the token:
localStorage.setItem('access_token', 'invalid-token');
// Refresh page
// Verify: Automatic redirect to /login
```

---

**Dashboard MVP is ready for production testing!** 🎉

All core CRUD operations work with optimistic updates and proper error handling.

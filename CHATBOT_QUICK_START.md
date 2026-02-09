# 🚀 Chatbot Quick Start (No Login Required!)

Signup issue hai but chatbot ke liye login ki zaroorat nahi! Direct test karo:

## Option 1: Test Chatbot Directly

### Step 1: Open Browser
```
http://localhost:3000
```

### Step 2: Skip Signup Page
URL bar mein directly type karo:
```
http://localhost:3000/dashboard
```

Ya phir browser console mein (F12):
```javascript
localStorage.setItem('access_token', 'test-token');
localStorage.setItem('user_id', '123e4567-e89b-12d3-a456-426614174000');
window.location.href = '/dashboard';
```

### Step 3: Chatbot Dikhega!
Bottom-right corner mein purple floating button dikhega 💬

### Step 4: Test Commands
- "create task name learning"
- "show tasks"
- "add task: Buy groceries"

---

## Option 2: Direct MCP Test (No Frontend)

`test-chatbot-api.html` file browser mein kholo:

1. File Explorer → `test-chatbot-api.html`
2. Double click
3. Browser mein open hoga
4. "Test MCP Endpoint" button click karo

---

## Option 3: Fix Signup Issue

Agar signup fix karna hai:

### Check 1: Backend Running?
```bash
curl http://localhost:8000/
```
Should return: `{"status":"healthy"}`

### Check 2: CORS Headers?
Backend logs mein dekho - OPTIONS request aa rahi hai?

### Check 3: Frontend .env.local
```bash
cat frontend/.env.local | findstr API
```
Should show: `NEXT_PUBLIC_API_URL="http://localhost:8000"`

### Check 4: Try Simple Password
Signup form mein **short password** try karo (6-8 characters):
- Email: test@test.com
- Password: Test123

Long password bcrypt issue create kar raha hai.

---

## Quick Fix: Bypass Auth

Frontend mein temporary bypass:

1. Open: `frontend/app/dashboard/layout.tsx`
2. Comment out auth check (if any)
3. Restart frontend

---

## Summary

**Chatbot test karne ke liye signup ki zaroorat nahi!**

Easiest way:
1. Browser console (F12)
2. Paste:
```javascript
localStorage.setItem('access_token', 'test-token');
localStorage.setItem('user_id', '123e4567-e89b-12d3-a456-426614174000');
window.location.href = '/dashboard';
```
3. Chatbot floating button dikhega!

Try karo! 🚀

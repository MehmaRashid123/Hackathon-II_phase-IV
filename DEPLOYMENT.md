# Deployment Guide - Task Manager App

## Architecture
- **Frontend:** Next.js 16 (Vercel)
- **Backend:** FastAPI (Render/Railway)
- **Database:** Neon PostgreSQL (Serverless)

---

## 🚀 Step-by-Step Deployment

### 1. Frontend Deployment (Vercel)

#### A. Sign Up & Connect GitHub
1. Go to https://vercel.com
2. Click "Sign Up" → "Continue with GitHub"
3. Authorize Vercel to access your repositories

#### B. Import Project
1. Click "Add New..." → "Project"
2. Select your repository: `Hackathon-II`
3. Click "Import"

#### C. Configure Build Settings
```
Framework Preset: Next.js
Root Directory: frontend
Build Command: npm run build (auto-detected)
Output Directory: .next (auto-detected)
Install Command: npm install (auto-detected)
Node Version: 18.x (auto-detected)
```

#### D. Environment Variables
Click "Environment Variables" and add:
```
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
```
(You'll update this after deploying backend)

#### E. Deploy
1. Click "Deploy"
2. Wait 2-3 minutes
3. You'll get a URL like: `https://your-app.vercel.app`

---

### 2. Backend Deployment (Render)

#### A. Sign Up
1. Go to https://render.com
2. Click "Get Started" → "Sign in with GitHub"
3. Authorize Render

#### B. Create Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select your repository

#### C. Configure Service
```
Name: task-manager-backend
Region: Oregon (US West) or Frankfurt (Europe)
Branch: main (or your default branch)
Root Directory: backend
Runtime: Python 3.11
Build Command: pip install -r requirements.txt
Start Command: uvicorn src.main:app --host 0.0.0.0 --port $PORT
Instance Type: Free
```

#### D. Environment Variables
Add the following in the "Environment" section:

```bash
# Database
DATABASE_URL=postgresql://user:password@host/database
# Get this from Neon dashboard

# Security
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
# Generate: openssl rand -hex 32

# CORS
ALLOWED_ORIGINS=https://your-app.vercel.app
# Update with your Vercel URL

# Port (Render provides this)
PORT=10000
```

#### E. Deploy
1. Click "Create Web Service"
2. Wait 5-10 minutes for initial deployment
3. You'll get a URL like: `https://task-manager-backend.onrender.com`

---

### 3. Update Frontend with Backend URL

#### A. Update Vercel Environment Variable
1. Go to your Vercel project
2. Settings → Environment Variables
3. Update `NEXT_PUBLIC_API_URL` with your Render backend URL:
   ```
   NEXT_PUBLIC_API_URL=https://task-manager-backend.onrender.com
   ```
4. Click "Save"

#### B. Redeploy Frontend
1. Go to "Deployments" tab
2. Click "..." on latest deployment
3. Click "Redeploy"

---

### 4. Update Backend CORS

#### A. Update Render Environment Variable
1. Go to your Render service
2. Environment → Edit
3. Update `ALLOWED_ORIGINS`:
   ```
   ALLOWED_ORIGINS=https://your-app.vercel.app,https://your-app-git-main.vercel.app
   ```
4. Click "Save Changes"
5. Service will auto-redeploy

---

## 🔐 Security Checklist

### Before Production:
- [ ] Change JWT_SECRET to a strong random value
- [ ] Add your actual Vercel URL to ALLOWED_ORIGINS
- [ ] Enable HTTPS only (both platforms do this by default)
- [ ] Review Neon database connection settings
- [ ] Set up proper error logging (Sentry, LogRocket)
- [ ] Enable rate limiting on backend

---

## 🧪 Testing Deployment

### 1. Test Backend API
```bash
curl https://your-backend.onrender.com/health
# Should return: {"status":"healthy"}
```

### 2. Test Frontend
1. Open: `https://your-app.vercel.app`
2. Sign up with test account
3. Create a task
4. Check Kanban board
5. Verify drag & drop works

### 3. Test Full Flow
1. Sign up → Should create account
2. Login → Should get JWT token
3. Create task → Should save to database
4. View Kanban → Should show tasks
5. Drag task → Should update status
6. Refresh page → Tasks should persist

---

## 📊 Monitoring

### Vercel Analytics
- Go to your project → Analytics
- View page views, performance metrics

### Render Logs
- Go to your service → Logs
- View real-time application logs
- Check for errors

### Neon Database
- Go to Neon dashboard
- Monitor connections, queries
- Check storage usage

---

## 🐛 Common Issues & Fixes

### Issue 1: CORS Error
**Symptom:** "Access to fetch blocked by CORS policy"
**Fix:**
1. Check ALLOWED_ORIGINS in backend env vars
2. Ensure it matches your Vercel URL exactly
3. Include both `your-app.vercel.app` and `your-app-git-*.vercel.app`

### Issue 2: Database Connection Error
**Symptom:** "Could not connect to database"
**Fix:**
1. Verify DATABASE_URL in Render env vars
2. Check Neon database is active (not paused)
3. Ensure IP allowlist in Neon includes Render IPs

### Issue 3: Build Failed
**Symptom:** Deployment fails during build
**Fix:**
- **Frontend:** Check package.json dependencies, clear build cache
- **Backend:** Verify requirements.txt has correct versions

### Issue 4: API 404 Errors
**Symptom:** API calls return 404
**Fix:**
1. Check NEXT_PUBLIC_API_URL has correct backend URL
2. Verify backend routes are deployed correctly
3. Check backend logs for errors

---

## 🔄 Continuous Deployment

Both Vercel and Render support auto-deployment:

### Vercel (Frontend)
- Push to `main` branch → Auto-deploys
- Pull requests → Preview deployments

### Render (Backend)
- Push to `main` branch → Auto-deploys
- Check "Auto-Deploy" is enabled in settings

---

## 💰 Cost Breakdown

### Free Tier Limits:
- **Vercel:** 100GB bandwidth/month, unlimited deployments
- **Render:** 750 hours/month free (sleeps after 15min inactivity)
- **Neon:** 3GB storage, 1 database free

### When to Upgrade:
- Vercel: If >100GB bandwidth or need advanced features
- Render: If need 24/7 uptime (Starter: $7/mo)
- Neon: If >3GB data or need more databases

---

## 📚 Resources

- **Vercel Docs:** https://vercel.com/docs
- **Render Docs:** https://render.com/docs
- **Neon Docs:** https://neon.tech/docs
- **FastAPI Deployment:** https://fastapi.tiangolo.com/deployment/
- **Next.js Deployment:** https://nextjs.org/docs/deployment

---

## 🆘 Support

If you encounter issues:
1. Check deployment logs on Vercel/Render
2. Verify environment variables
3. Test API endpoints individually
4. Check browser console for frontend errors
5. Review Neon database connection

---

**Last Updated:** 2026-02-06
**Version:** 1.0.0

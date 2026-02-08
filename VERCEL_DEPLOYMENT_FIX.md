# Vercel Deployment Fix - HTTPS Mixed Content Issue

## Problem
Tasks were being created but disappearing after refresh on Vercel production because:
1. Backend URL was using HTTP instead of HTTPS (Mixed Content blocked by browser)
2. Backend CORS didn't include Vercel URLs

## Solution Applied

### 1. Backend CORS Configuration (Hugging Face Space)
Update environment variable:
```
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,https://hackathon-ii-phase-9a0zcw3d1-mehma-rashids-projects-1f756fc3.vercel.app,https://hackathon-ii-phase-ii.vercel.app
```

**Steps:**
1. Go to Hugging Face Space: https://huggingface.co/spaces/mehma-app
2. Settings → Variables and secrets
3. Update `CORS_ORIGINS` variable
4. Space will restart automatically

### 2. Frontend Environment Variable (Vercel)
Update to use HTTPS:
```
NEXT_PUBLIC_API_URL=https://mehma-app.hf.space
```

**Steps:**
1. Go to Vercel Dashboard: https://vercel.com/dashboard
2. Select your project
3. Settings → Environment Variables
4. Edit `NEXT_PUBLIC_API_URL` and change from `http://` to `https://`
5. Save
6. Go to Deployments tab
7. Click "..." on latest deployment → Redeploy

### 3. Code Fixes (Already Applied)
Fixed localStorage sync issues in `frontend/lib/hooks/useTasks.ts`:
- `createTask`: Now saves task status to localStorage
- `updateTask`: Updates localStorage when status changes
- `deleteTask`: Removes task from localStorage

## Testing After Deployment

1. Open your Vercel app: https://hackathon-ii-phase-9a0zcw3d1-mehma-rashids-projects-1f756fc3.vercel.app
2. Login/Signup
3. Create a task
4. Refresh the page
5. Task should still be there ✅

## Common Issues

### Issue: CORS Error
**Symptom:** "Access to fetch blocked by CORS policy"
**Fix:** Make sure Vercel URL is in backend CORS_ORIGINS

### Issue: Mixed Content Error
**Symptom:** "Mixed Content: The page was loaded over HTTPS, but requested an insecure resource"
**Fix:** Make sure NEXT_PUBLIC_API_URL uses `https://` not `http://`

### Issue: Tasks still disappearing
**Symptom:** Tasks create but disappear on refresh
**Fix:** 
1. Check browser console for errors
2. Verify backend is accessible: https://mehma-app.hf.space/health
3. Check Network tab to see if API calls are succeeding

## Vercel URLs to Add to CORS
```
https://hackathon-ii-phase-9a0zcw3d1-mehma-rashids-projects-1f756fc3.vercel.app
https://hackathon-ii-phase-ii.vercel.app
https://*.vercel.app (for preview deployments)
```

## Backend URL
```
Production: https://mehma-app.hf.space
Local: http://localhost:8000
```

---
**Last Updated:** 2026-02-08

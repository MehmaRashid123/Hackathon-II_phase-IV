# Critical Vercel Fixes for Persistent Tasks and Mixed Content Errors

## 🚨 IMMEDIATE ACTIONS REQUIRED

Your application is currently failing because:
1.  **Frontend is using HTTP instead of HTTPS**: Browser blocks this ("Mixed Content").
2.  **Database might be temporary**: If tasks vanish on refresh, the backend might be using SQLite instead of Neon.

Please follow these steps EXACTLY in this order.

### Step 1: Fix Vercel Environment Variables (Crucial)

1.  Go to your [Vercel Dashboard](https://vercel.com/dashboard).
2.  Select your project (`hackathon-ii-phase-ii` or similar).
3.  Click **Settings** > **Environment Variables**.
4.  Find `NEXT_PUBLIC_API_URL`.
5.  **Edit** it and ensure the value is:
    ```
    https://mehma-app.hf.space
    ```
    *(Note: It MUST be `https://`. If it is `http://`, change it immediately.)*

### Step 2: Redeploy Frontend (Mandatory)

Changing the variable above does NOT update the live site. You must redeploy.

1.  Go to the **Deployments** tab in Vercel.
2.  Click the three dots (`...`) on the top/latest deployment.
3.  Select **Redeploy**.
4.  **Wait** for the deployment to finish (Status: `Ready`).
5.  **Test**: Open the new URL. Create a task. Refresh.

### Step 3: Verify Hugging Face Database (For Persistence)

If tasks still disappear after refresh, your backend is likely using a temporary database.

1.  Go to your [Hugging Face Space](https://huggingface.co/spaces/mehma-app).
2.  Click **Settings** > **Variables and secrets**.
3.  Look for a **Secret** (not Variable) named `DATABASE_URL`.
    *   **If it's missing**: You are using SQLite (temporary). All data is lost on restart.
    *   **Fix**: Add a new Secret `DATABASE_URL` with your **Neon Connection String**:
        `postgresql://neondb_owner:.......@ep-.....neon.tech/neondb?sslmode=require`

### Step 4: Verify Fix

1.  Open your Vercel App (HTTPS).
2.  Open Browser Console (`F12` > Network).
3.  Perform an action (create task).
4.  Look at the network request.
    *   **URL**: Should start with `https://mehma-app.hf.space/...` (NOT `http://` and NOT `localhost`).
    *   **Status**: Should be `200` or `201`.
5.  Refresh the page.
    *   Task should remain.

---

### Troubleshooting the "500 Internal Server Error"

If you still see a 500 error after fixing the above:
1.  It implies the backend is crashing.
2.  This is likely because of a database connection issue or a schema mismatch.
3.  **Action**: Check your Hugging Face Space **Logs** tab. It will show the exact Python error causing the crash.

# BoardingEdu Deployment Guide

This document covers deploying the BoardingEdu prototype:

- **Frontend** → [Vercel](https://vercel.com)
- **Backend** → [Render](https://render.com)
- **Database** → Hosted PostgreSQL (Render Postgres or any provider)

Never commit real secrets. Use each platform's environment variable UI.

---

## ⚠️ Non-Negotiable Pre-Launch Checklist

**Do these first — if the live demo fails it's almost always one of these:**

| # | Where | Setting | Value |
|---|-------|---------|-------|
| 1 | **Vercel → Project → Settings → Environment Variables** | `VITE_API_BASE_URL` | `https://boardingedu-platform-1.onrender.com/api`  *(no trailing slash, no trailing period)* |
| 2 | **Render → Backend → Environment** | `CORS_ORIGINS` | `https://boardingedu-platform.vercel.app` *(exact Vercel URL, no trailing slash)* |
| 3 | **Render → Backend → Environment** | `DATABASE_URL` | Provided automatically by Render's internal PG, or your hosted PostgreSQL URL |
| 4 | **Render → Backend → Environment** | `SECRET_KEY` + `JWT_SECRET_KEY` | Two different long random strings |

**After each env var change you must Redeploy** the affected service (both if you changed both).

---

## 0. Verify the Backend First

Before deploying the frontend anywhere, confirm your Render backend returns healthy:

```
https://boardingedu-platform-1.onrender.com/api/health
```

Expected output:
```json
{"status":"ok","database":"connected","success":true}
```

If this doesn't work, fix the backend + DB first. The frontend can't load data without it.

---

## 1. Database (PostgreSQL)

1. Create a PostgreSQL instance (Render Dashboard → New → PostgreSQL is fine).
2. Copy the **External Database URL**.
3. You will paste it into the backend as `DATABASE_URL`.

Optional first-time schema + demo data (from your machine, pointed at the remote DB):

```bash
cd backend
# set DATABASE_URL in .env to the hosted URL
python seed.py
```

---

## 2. Backend on Render

### Option A — Blueprint (`backend/render.yaml`)

From the Render dashboard, use **Blueprint** and point at the repo’s `backend/render.yaml`, or create a Web Service manually.

### Option B — Manual Web Service

| Setting | Value |
|---------|--------|
| Root directory | `backend` |
| Runtime | Python 3 |
| Build command | `pip install -r requirements.txt` |
| Start command | `gunicorn app:app` |

### Environment variables

| Key | Notes |
|-----|--------|
| `DATABASE_URL` | Hosted Postgres URL (Render can inject this) |
| `SECRET_KEY` | Long random string |
| `JWT_SECRET_KEY` | Different long random string |
| `CORS_ORIGINS` | Your Vercel URL, e.g. `https://your-app.vercel.app` |
| `DEMO_ADMIN_EMAIL` / `DEMO_ADMIN_PASSWORD` | Only if you re-run seed on the host |
| `DEMO_PARENT_EMAIL` / `DEMO_PARENT_PASSWORD` | Same |

After the first deploy, open `https://your-api.onrender.com/api/health` and confirm `"database": "connected"`.

---

## 3. Frontend on Vercel

1. Import the GitHub repo in Vercel.
2. Set **Root Directory** to `frontend`.
3. Framework preset: Vite (build `npm run build`, output `dist`).
4. Environment variable:

| Key | Value |
|-----|--------|
| `VITE_API_BASE_URL` | `https://your-api.onrender.com/api` |

`frontend/vercel.json` already rewrites all routes to `index.html` for React Router.

---

## 4. CORS checklist

Backend `CORS_ORIGINS` must include the exact frontend origin (no trailing slash), for example:

```text
https://boardingedu-platform.vercel.app
```

Redeploy the API after changing CORS.

---

## 5. Local verification before deploy

```bash
# Backend tests
cd backend
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q

# Frontend production build
cd frontend
npm install
npm run build
```

Import `postman/BoardingEdu_API.postman_collection.json` into Postman for manual API checks.

---

## 6. Demo accounts after seed

Use the emails/passwords from your hosted env vars (`DEMO_*`). Do not publish them in the README or public issues.

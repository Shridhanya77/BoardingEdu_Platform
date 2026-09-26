# BoardingEdu – School Discovery & Admission Platform

A full-stack web application that helps parents and students discover schools, compare options, shortlist favourites, and submit admission enquiries. Administrators can manage schools and enquiries.

> **Status:** Phases 1–15 complete — including automated tests and deployment docs.

## Project Overview

**Discover school → Understand school → Compare → Shortlist → Enquire for admission**

Portfolio / job-evaluation app demonstrating REST APIs, PostgreSQL design, JWT auth, CRUD, search/filtering, and a responsive React UI.

## Features

- Public school discovery, search, filter, sort, pagination
- School detail (fees, facilities, infrastructure, contact)
- Compare 2–3 schools (API-backed values)
- Parent/student register, login, shortlist, enquiries
- Admin dashboard, school CRUD, users, enquiry status updates
- JWT auth + role-based access

## Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | React.js, Vite, JavaScript, Bootstrap 5, Bootstrap Icons, React Router, Axios |
| Backend | Python 3, Flask, Flask-CORS, Flask-SQLAlchemy, Flask-JWT-Extended, Werkzeug |
| Database | PostgreSQL |
| Deploy | Frontend → Vercel · Backend → Render · Hosted PostgreSQL |

## Quick start

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# Edit DATABASE_URL and DEMO_* passwords
python seed.py
python app.py
```

API: http://localhost:5000

### Frontend

```bash
cd frontend
npm install
copy .env.example .env
npm run dev
```

App: http://localhost:5173

## Demo credentials

Set in `backend/.env` (see `.env.example`). Created by `python seed.py`:

- Admin: `DEMO_ADMIN_EMAIL` / `DEMO_ADMIN_PASSWORD`
- Parent: `DEMO_PARENT_EMAIL` / `DEMO_PARENT_PASSWORD`

Never commit a real `.env`.

## Main API surface

| Area | Endpoints |
|------|-----------|
| Auth | `POST /api/auth/register`, `POST /api/auth/login`, `GET /api/auth/me` |
| Schools | `GET/POST /api/schools`, `GET/PUT/DELETE /api/schools/:id`, related fees/facilities/images/infrastructure, `GET /api/schools/filters` |
| Shortlists | `GET/POST /api/shortlists`, `DELETE /api/shortlists/:school_id` |
| Enquiries | `POST/GET /api/enquiries`, `GET /api/enquiries/:id` |
| Admin | `GET /api/admin/dashboard`, `GET /api/admin/users`, `GET /api/admin/enquiries`, `PUT /api/admin/enquiries/:id/status` |

## Frontend routes

`/`, `/schools`, `/schools/:id`, `/compare`, `/login`, `/register`, `/dashboard`, `/shortlisted`, `/enquiries`, `/profile`, `/admin`, `/admin/schools`, `/admin/schools/new`, `/admin/schools/:id/edit`, `/admin/enquiries`, `/admin/users`

## Deployment notes

- **Frontend (Vercel):** root `frontend/`, build `npm run build`, output `dist`, set `VITE_API_BASE_URL` to your Render API URL + `/api`
- **Backend (Render):** root `backend/`, start `gunicorn app:app`, set `DATABASE_URL`, `SECRET_KEY`, `JWT_SECRET_KEY`, `CORS_ORIGINS`
- Run `python seed.py` once against the hosted database

## Architecture

```
React (Vite)  --HTTP/JSON-->  Flask REST API  --ORM-->  PostgreSQL
 AuthContext / CompareContext     JWT + RBAC
 Axios service layer              models / routes / services
```

## Local verification / tests

```bash
cd backend
pytest -q
```

Postman: import `postman/BoardingEdu_API.postman_collection.json`

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for Vercel + Render + PostgreSQL steps.

## License

MIT – see [LICENSE](LICENSE).

## Future improvements

- Image uploads to object storage
- Email notifications on enquiry status change
- Saved searches and email alerts
- Soft-delete + audit log for admin actions
- Automated API tests (pytest) and frontend e2e tests

# BoardingEdu – School Discovery & Admission Platform

A full-stack web application that helps parents and students **discover schools**, explore fees and facilities, **compare and shortlist** options, and **submit admission enquiries**. Administrators can manage schools, users, and enquiry status.

Built as a production-minded portfolio / job-evaluation project for **BoardingEdu**, inspired by the general concept of school discovery platforms — **without copying** any third-party branding, UI, text, images, or proprietary content.

---

## 1. Project overview

**Core journey**

```text
Discover school → Understand school → Compare → Shortlist → Enquire for admission
```

BoardingEdu demonstrates end-to-end full-stack skills:

- REST APIs with clean architecture
- Relational database design (PostgreSQL)
- JWT authentication and role-based authorization
- CRUD, search, filtering, sorting, pagination
- React frontend integrated with a Flask backend
- Validation, error handling, and responsive UI

School profiles and fees in the demo are **fictional sample data** for evaluation purposes.

---

## 2. Screenshots

These screenshots are included in the repository and are ready to render on GitHub.

![Home page](docs/screenshots/01-home.png)

![Schools listing](docs/screenshots/02-schools.png)

![School detail](docs/screenshots/03-school-detail.png)

![Compare view](docs/screenshots/04-compare.png)

![Login page](docs/screenshots/05-login.png)

![Parent dashboard](docs/screenshots/06-parent-dashboard.png)

![Admin dashboard](docs/screenshots/07-admin-dashboard.png)

## 3. Features

### Public (Guest)

- Browse and search schools
- Filter by board, school type, boarding, gender, fee range, facilities
- Sort by name, fee, or rating
- View school details (fees, facilities, infrastructure, admission process)
- Compare 2–3 schools (values loaded from the API)

### Parent / Student

- Register and login
- Shortlist / remove schools
- Submit admission enquiries
- Track enquiry status
- View profile and parent dashboard

### Admin

- Dashboard statistics (schools, users, shortlists, enquiries)
- Create, update, and delete schools
- View registered users
- View and update enquiry status (`Pending` → `Contacted` → `In Review` → `Closed`)

---

## 3. Technology stack

| Layer | Technology | Why |
|-------|------------|-----|
| Frontend | React.js, Vite, JavaScript | Component UI, fast local tooling |
| UI | Bootstrap 5, Bootstrap Icons | Responsive, consistent, interview-friendly |
| Routing | React Router | SPA navigation and protected routes |
| HTTP | Axios | Central API client with JWT interceptors |
| Backend | Python 3, Flask | Lightweight REST API |
| Auth | Flask-JWT-Extended, Werkzeug | JWT sessions + password hashing |
| ORM | Flask-SQLAlchemy | Safe parameterized queries / relationships |
| Database | PostgreSQL | Relational integrity for schools, fees, enquiries |
| Deploy | Vercel (frontend), Render (API + Postgres) | Simple cloud deployment |

---

## 4. Architecture

```text
┌────────────────────┐         JSON / JWT          ┌────────────────────┐
│  React (Vite) SPA  │  ─────────────────────────► │   Flask REST API   │
│  AuthContext       │                             │   Blueprints       │
│  CompareContext    │  ◄───────────────────────── │   Services         │
│  Axios services    │                             │   SQLAlchemy models│
└────────────────────┘                             └─────────┬──────────┘
                                                             │
                                                             ▼
                                                    ┌────────────────────┐
                                                    │    PostgreSQL      │
                                                    └────────────────────┘
```

**Project layout**

```text
BoardingEdu_Platform/
├── frontend/                 # React + Vite SPA
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── layouts/
│   │   ├── services/
│   │   ├── context/
│   │   └── utils/
│   ├── vercel.json
│   └── package.json
├── backend/                  # Flask REST API
│   ├── routes/
│   ├── models/
│   ├── services/
│   ├── utils/
│   ├── tests/
│   ├── app.py
│   ├── config.py
│   ├── seed.py
│   ├── setup_postgres.py
│   └── requirements.txt
├── database/
│   └── schema.sql            # Reference SQL schema
├── postman/
│   └── BoardingEdu_API.postman_collection.json
├── DEPLOYMENT.md
├── README.md
├── .gitignore
└── LICENSE
```

---

## 5. Database design

PostgreSQL with normalized tables and foreign keys.

| Table | Purpose |
|-------|---------|
| `users` | Parents, students, admins (hashed passwords) |
| `schools` | School profiles, fees range, boarding, rating |
| `school_fees` | Per-class fee breakdown |
| `facilities` | Facility catalogue |
| `school_facilities` | Many-to-many school ↔ facility (unique pair) |
| `infrastructure` | Category + description per school |
| `school_images` | Gallery image URLs |
| `shortlists` | User shortlist (unique user + school) |
| `admission_enquiries` | Enquiry workflow + status |

Reference DDL: [`database/schema.sql`](database/schema.sql)

Tables are created automatically by `python seed.py` (`db.create_all()`).

---

## 6. API endpoints

Base URL (local): `http://localhost:5000/api`

### Auth

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| POST | `/auth/register` | Public | Register parent/student only |
| POST | `/auth/login` | Public | Login → JWT |
| GET | `/auth/me` | JWT | Current user profile |

### Schools

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| GET | `/schools` | Public | List + search/filter/sort/paginate |
| GET | `/schools/filters` | Public | Filter dropdown options |
| GET | `/schools/:id` | Public | Full school detail |
| POST | `/schools` | Admin | Create school |
| PUT | `/schools/:id` | Admin | Update school |
| DELETE | `/schools/:id` | Admin | Delete school |
| GET | `/schools/:id/fees` | Public | Fee rows |
| GET | `/schools/:id/facilities` | Public | Facilities |
| GET | `/schools/:id/infrastructure` | Public | Infrastructure |
| GET | `/schools/:id/images` | Public | Images |

**Useful query params for `GET /schools`:**  
`q` / `name`, `city`, `board`, `school_type`, `gender`, `hostel_available`, `min_fee`, `max_fee`, `facility_ids`, `sort` (`name` \| `fee_asc` \| `fee_desc` \| `rating`), `page`, `per_page`

### Shortlists

| Method | Endpoint | Access |
|--------|----------|--------|
| GET | `/shortlists` | Parent/Student |
| POST | `/shortlists` | Parent/Student (`{ "school_id": 1 }`) |
| DELETE | `/shortlists/:school_id` | Parent/Student |

### Enquiries

| Method | Endpoint | Access |
|--------|----------|--------|
| POST | `/enquiries` | Parent/Student |
| GET | `/enquiries` | Parent/Student (own) or Admin (all) |
| GET | `/enquiries/:id` | Owner or Admin |

### Admin

| Method | Endpoint | Access |
|--------|----------|--------|
| GET | `/admin/dashboard` | Admin |
| GET | `/admin/users` | Admin |
| GET | `/admin/enquiries` | Admin |
| PUT | `/admin/enquiries/:id/status` | Admin |

### Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | API + database connectivity |
| GET | `/` | Friendly API index |

Authenticated requests:

```http
Authorization: Bearer <access_token>
```

---

## 7. Installation instructions

### Prerequisites

- Node.js 18+ and npm
- Python 3.10+
- PostgreSQL 14+ (local or hosted)
- Git

### Clone

```bash
git clone <your-repo-url>
cd BoardingEdu_Platform
```

---

## 8. Environment variables

### Backend — copy `backend/.env.example` → `backend/.env`

| Variable | Purpose |
|----------|---------|
| `SECRET_KEY` | Flask secret |
| `JWT_SECRET_KEY` | JWT signing key |
| `DATABASE_URL` | PostgreSQL connection URL |
| `CORS_ORIGINS` | Allowed frontend origins |
| `DEMO_ADMIN_EMAIL` / `DEMO_ADMIN_PASSWORD` | Seeded admin (seed only) |
| `DEMO_PARENT_EMAIL` / `DEMO_PARENT_PASSWORD` | Seeded parent (seed only) |

Example:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/boardingedu
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### Frontend — copy `frontend/.env.example` → `frontend/.env`

| Variable | Purpose |
|----------|---------|
| `VITE_API_BASE_URL` | Flask API base, e.g. `http://localhost:5000/api` |

**Never commit `.env` files or real passwords.**

---

## 9. Database setup

1. Install PostgreSQL and start the service.
2. Set `DATABASE_URL` in `backend/.env` with your real password.
3. Create the database and verify connectivity:

```bash
cd backend
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
# source .venv/bin/activate

pip install -r requirements.txt
python setup_postgres.py
```

`setup_postgres.py` creates the `boardingedu` database if it does not exist and checks the connection.

You can also create the DB manually:

```sql
CREATE DATABASE boardingedu;
```

---

## 10. Seed instructions

With the venv active and `DATABASE_URL` set:

```bash
cd backend
python seed.py
```

This will:

- Create tables
- Insert ~12 facilities and **13 fictional schools**
- Create demo admin + parent accounts
- Add sample shortlists and one pending enquiry

Re-running `seed.py` clears and reloads demo data by default.

---

## 11. Running the backend

```bash
cd backend
.venv\Scripts\Activate.ps1   # or: source .venv/bin/activate
python app.py
```

- API root: http://localhost:5000  
- Health: http://localhost:5000/api/health  

Expect `"database": "connected"` when PostgreSQL is configured correctly.

Production-style start:

```bash
gunicorn app:app
```

---

## 12. Running the frontend

```bash
cd frontend
npm install
npm run dev
```

App: http://localhost:5173

Production build:

```bash
npm run build
npm run preview
```

---

## 13. Demo credentials

Demo users are created by `seed.py` using values from `backend/.env`.

Defaults from `.env.example` (change these in your private `.env`):

| Role | Email | Password env var |
|------|-------|------------------|
| Admin | `admin@boardingedu.demo` | `DEMO_ADMIN_PASSWORD` |
| Parent | `parent@boardingedu.demo` | `DEMO_PARENT_PASSWORD` |

Suggested demo walkthrough:

1. Open **Schools** → search / filter → open a school  
2. Add 2–3 schools to **Compare**  
3. Login as **parent** → shortlist → submit enquiry  
4. Login as **admin** → update enquiry status → manage schools  

---

## 14. Deployment instructions

Detailed steps: **[DEPLOYMENT.md](DEPLOYMENT.md)**

### Summary

| Part | Platform | Notes |
|------|----------|--------|
| Frontend | Vercel | Root = `frontend`, set `VITE_API_BASE_URL` |
| Backend | Render | Root = `backend`, start `gunicorn app:app` |
| Database | Render Postgres (or any hosted Postgres) | Set `DATABASE_URL`, then run `seed.py` once |

Also set on Render:

- `SECRET_KEY`
- `JWT_SECRET_KEY`
- `CORS_ORIGINS` = your Vercel URL (no trailing slash)

---

## 15. Testing

### Automated API tests

```bash
cd backend
.venv\Scripts\Activate.ps1
pytest -q
```

### Manual API testing

Import Postman collection:

[`postman/BoardingEdu_API.postman_collection.json`](postman/BoardingEdu_API.postman_collection.json)

---

## Frontend routes

| Route | Description |
|-------|-------------|
| `/` | Home / landing |
| `/schools` | Listing, search, filters |
| `/schools/:id` | School details |
| `/compare` | Side-by-side comparison |
| `/login` / `/register` | Auth |
| `/dashboard` | Parent dashboard |
| `/shortlisted` | Shortlisted schools |
| `/enquiries` | Parent enquiries |
| `/profile` | User profile |
| `/admin` | Admin dashboard |
| `/admin/schools` | Manage schools |
| `/admin/schools/new` | Add school |
| `/admin/schools/:id/edit` | Edit school |
| `/admin/enquiries` | Manage enquiries |
| `/admin/users` | Registered users |

---

## Security notes

- Passwords hashed with Werkzeug (never stored in plain text)
- JWT authentication for protected routes
- Role-based authorization (parent/student vs admin)
- Input validation on auth, schools, and enquiries
- CORS limited to configured origins
- Secrets via environment variables
- SQLAlchemy ORM (parameterized queries)
- Duplicate shortlists blocked by unique constraint

---

## Future improvements

- Image uploads to cloud object storage
- Email / SMS notifications when enquiry status changes
- Soft delete and admin audit logs
- Saved searches and alerts for parents
- Frontend e2e tests (Playwright/Cypress)
- Caching for popular school listings
- Pagination UX improvements and richer admin analytics

---

## License

MIT — see [LICENSE](LICENSE).

---

## Acknowledgements

Built as an independent BoardingEdu product prototype for full-stack developer evaluation. Demo school names, fees, and images are fictional / placeholder content.

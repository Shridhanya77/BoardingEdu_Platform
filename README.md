# 🏫 BoardingEdu – School Discovery & Admission Platform

<div align="center">

**A full-stack web application that helps parents and students discover schools, explore fees and facilities, compare and shortlist options, and submit admission enquiries.**

[![React](https://img.shields.io/badge/React-18.3-61dafb?style=flat&logo=react&logoColor=white)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-336791?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![SQLite](https://img.shields.io/badge/SQLite-Fallback-003b57?style=flat&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Demo:** http://localhost:5173  
**API Base:** http://localhost:5000/api

</div>

---

## 📸 Screenshots

These screenshots showcase the key pages of the BoardingEdu platform.

### 🏠 Home Page
Landing page with hero search, featured schools, city-based browsing, and feature highlights.

![Home page](""C:\Users\HP\OneDrive\Documents\BoardingEdu_Platform\docs\screenshots\01-home.png"")

### 🔍 Schools Listing
Search, filter (board, fees, boarding, facilities), sort, and paginate through all schools.

![Schools listing](docs/screenshots/02-schools.png)

### 🎓 School Detail Page
Full school profile with fees breakdown, facilities, infrastructure, gallery, and admission process.

![School detail](docs/screenshots/03-school-detail.png)

### ⚖️ Compare Schools
Side-by-side comparison of 2–3 shortlisted schools.

![Compare view](docs/screenshots/04-compare.png)

### 🔐 Login / Register
Secure JWT authentication for parents, students, and administrators.

![Login page](docs/screenshots/05-login.png)

### 👨‍👩‍👧 Parent Dashboard
Parent overview with shortlisted schools, enquiry tracking, and account management.

![Parent dashboard](docs/screenshots/06-parent-dashboard.png)

### 🛡️ Admin Dashboard
Admin statistics, school management, user listing, and enquiry status updates.

![Admin dashboard](docs/screenshots/07-admin-dashboard.jpg)

---

## ✨ Features

### 🌐 Public (Guest)
- Browse and search schools by name, city, board, and more
- Advanced filters: board, school type, boarding, gender, fee range, facilities
- Sort results by name, fee (asc/desc), or rating
- Paginated school listings
- Detailed school profiles (fees, facilities, infrastructure, admission process)
- Side-by-side comparison of 2–3 schools

### 👨‍👩‍👧 Parent / Student
- Register and login (JWT authentication)
- Shortlist / remove schools from favourites
- Submit admission enquiries with student details
- Track enquiry status from dashboard
- View profile and parent dashboard summary

### 🛡️ Administrator
- Dashboard with key statistics (schools, users, shortlists, enquiries)
- Full CRUD operations for school records
- View registered users directory
- Manage enquiry workflow: `Pending` → `Contacted` → `In Review` → `Closed`

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | React 18, Vite, JavaScript | Component-based SPA UI, fast dev tooling |
| **UI Framework** | Bootstrap 5, Bootstrap Icons | Responsive, consistent design system |
| **Routing** | React Router v6 | SPA navigation + protected role-based routes |
| **HTTP Client** | Axios | Centralized API client with JWT interceptors |
| **Backend** | Python 3, Flask | Lightweight, modular REST API |
| **Authentication** | Flask-JWT-Extended, Werkzeug | JWT sessions + secure password hashing |
| **ORM** | Flask-SQLAlchemy 3.x | Safe parameterized queries, model relationships |
| **Database** | PostgreSQL (primary) / SQLite (fallback) | Relational integrity for all domain entities |
| **Deployment** | Vercel (FE), Render (BE+DB) | Simple cloud deployment paths |

---

## 🏗️ Architecture

```
┌────────────────────────────┐      JSON / JWT       ┌────────────────────────────┐
│   React (Vite) SPA         │ ────────────────────► │   Flask REST API           │
│   • AuthContext            │                       │   • Blueprint routes       │
│   • CompareContext         │ ◄──────────────────── │   • Service layer          │
│   • Axios service layer    │                       │   • SQLAlchemy models      │
└────────────────────────────┘                       └──────────────┬─────────────┘
                                                                    │
                                                                    ▼
                                                   ┌────────────────────────────┐
                                                   │   PostgreSQL / SQLite DB   │
                                                   └────────────────────────────┘
```

### Project Layout

```text
BoardingEdu_Platform/
├── frontend/                 # React + Vite SPA
│   ├── src/
│   │   ├── components/       # Reusable UI components (Navbar, SchoolCard, etc.)
│   │   ├── pages/            # Route-level pages (public, parent, admin)
│   │   │   └── admin/        # Admin-only management pages
│   │   ├── layouts/          # Shared layout wrappers
│   │   ├── services/         # Axios-based API service modules
│   │   ├── context/          # React Context (Auth, Compare)
│   │   └── utils/            # Helper functions (formatters)
│   ├── index.html
│   ├── vite.config.js        # Dev server + /api proxy configuration
│   └── package.json
├── backend/                  # Flask REST API
│   ├── routes/               # API blueprints (auth, schools, admin, etc.)
│   ├── models/               # SQLAlchemy ORM models
│   ├── services/             # Business logic layer
│   ├── utils/                # Decorators, response helpers, validators
│   ├── tests/                # pytest API test suite
│   ├── app.py                # Flask app factory
│   ├── config.py             # Environment-driven config
│   ├── seed.py               # Demo data seeder (13 schools + accounts)
│   └── requirements.txt
├── database/
│   └── schema.sql            # Reference SQL DDL schema
├── postman/
│   └── BoardingEdu_API.postman_collection.json
├── docs/screenshots/         # README screenshots (7 pages)
├── DEPLOYMENT.md             # Cloud deployment steps
└── README.md
```

---

## 🗄️ Database Design

PostgreSQL / SQLite with normalized tables and foreign-key relationships.

| Table | Description |
|-------|-------------|
| `users` | Parents, students, admins — passwords stored as Werkzeug hashes |
| `schools` | Core school profiles: fees range, board, rating, boarding flag |
| `school_fees` | Per-class fee breakdown rows (admission, tuition, hostel, transport) |
| `facilities` | Facility master catalog (library, lab, pool, etc.) |
| `school_facilities` | Many-to-many school ↔ facility join (unique constraint) |
| `infrastructure` | Per-school category/description infrastructure rows |
| `school_images` | Gallery image URLs + captions |
| `shortlists` | User shortlist entries (unique user+school constraint) |
| `admission_enquiries` | Enquiry records with workflow status tracking |

Reference DDL: [`database/schema.sql`](database/schema.sql)

Tables are auto-created by `python seed.py` via `db.create_all()`.

---

## 📡 API Endpoints

**Base URL (local):** `http://localhost:5000/api`

### 🔐 Authentication

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| POST | `/auth/register` | Public | Register a parent/student account |
| POST | `/auth/login` | Public | Exchange credentials for JWT |
| GET | `/auth/me` | JWT | Fetch current user profile |

### 🏫 Schools

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| GET | `/schools` | Public | List/search/filter/sort/paginate schools |
| GET | `/schools/filters` | Public | Available filter dropdown options |
| GET | `/schools/:id` | Public | Full school detail (fees, facilities, images) |
| POST | `/schools` | Admin | Create a new school |
| PUT | `/schools/:id` | Admin | Update existing school |
| DELETE | `/schools/:id` | Admin | Soft-delete / remove school |
| GET | `/schools/:id/fees` | Public | Per-class fee rows |
| GET | `/schools/:id/facilities` | Public | School facility list |
| GET | `/schools/:id/infrastructure` | Public | Infrastructure entries |
| GET | `/schools/:id/images` | Public | Gallery image list |

**Query params for `GET /schools`:**
`q`, `name`, `city`, `board`, `school_type`, `gender`, `hostel_available`, `min_fee`, `max_fee`, `facility_ids`, `sort` (`name` \| `fee_asc` \| `fee_desc` \| `rating`), `page`, `per_page`

### ❤️ Shortlists

| Method | Endpoint | Access |
|--------|----------|--------|
| GET | `/shortlists` | Parent / Student |
| POST | `/shortlists` | Parent / Student — body: `{ "school_id": 1 }` |
| DELETE | `/shortlists/:school_id` | Parent / Student |

### 📨 Enquiries

| Method | Endpoint | Access |
|--------|----------|--------|
| POST | `/enquiries` | Parent / Student |
| GET | `/enquiries` | Parent (own) / Admin (all) |
| GET | `/enquiries/:id` | Owner or Admin |
| PUT | `/admin/enquiries/:id/status` | Admin only |

### 🛡️ Admin

| Method | Endpoint | Access |
|--------|----------|--------|
| GET | `/admin/dashboard` | Admin |
| GET | `/admin/users` | Admin |
| GET | `/admin/enquiries` | Admin |
| PUT | `/admin/enquiries/:id/status` | Admin |

### 💚 Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Friendly API index + endpoint listing |
| GET | `/api/health` | API live + database connectivity probe |

**Authenticated requests:**
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

---

## 🚀 Local Development Setup

### Prerequisites
- **Node.js** 18+ and npm
- **Python** 3.10+
- **PostgreSQL** 14+ **or** use the built-in **SQLite fallback** (zero-config)
- **Git**

### Step 1: Clone the repository
```bash
git clone <your-repo-url>
cd BoardingEdu_Platform
```

### Step 2: Environment variables

**Backend** — copy (or create) `backend/.env`:
```env
# Flask / JWT
SECRET_KEY=change-me-to-a-long-random-string
JWT_SECRET_KEY=change-me-another-long-random-string
JWT_ACCESS_TOKEN_EXPIRES_HOURS=24

# Database — use SQLite for zero-config local dev:
DATABASE_URL=sqlite:///boardingedu.db

# ... or use PostgreSQL if you have it:
# DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/boardingedu

CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# Seed demo credentials (only used by seed.py)
DEMO_ADMIN_EMAIL=admin@boardingedu.demo
DEMO_ADMIN_PASSWORD=AdminDemo@123
DEMO_PARENT_EMAIL=parent@boardingedu.demo
DEMO_PARENT_PASSWORD=ParentDemo@123
```

**Frontend** — copy (or create) `frontend/.env`:
```env
VITE_API_BASE_URL=http://localhost:5000/api
```

> ⚠️ **Never commit `.env` files or real passwords.** They are already listed in `.gitignore`.

### Step 3: Database + seed data

```bash
cd backend

# (Optional) Create a Python virtual environment
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS / Linux:
# source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# (PostgreSQL only) Create the "boardingedu" database:
python setup_postgres.py

# Seed the database with demo schools + users:
python seed.py
```

`seed.py` will output:
```
Facilities : 12
Schools    : 13
Users      : 2
Shortlists : 2
Enquiries  : 1
```

### Step 4: Run the backend API

```bash
cd backend
python app.py
```

- API root: http://localhost:5000
- Health check: http://localhost:5000/api/health
- Expected: `{ "database": "connected", "status": "ok" }`

### Step 5: Run the frontend SPA

```bash
cd frontend
npm install
npm run dev
```

- App: http://localhost:5173

---

## 🔑 Demo Credentials

Seeded automatically by `python seed.py` using the `DEMO_*` values in your `backend/.env`:

| Role | Email | Default Password |
|------|-------|------------------|
| 🛡️ **Admin** | `admin@boardingedu.demo` | `AdminDemo@123` |
| 👨‍👩‍👧 **Parent** | `parent@boardingedu.demo` | `ParentDemo@123` |

### Suggested Demo Walkthrough
1. Open **Schools** → search / filter → open a school profile
2. Add 2–3 schools to **Compare** → review side-by-side
3. Login as **parent** → shortlist favourites → submit an admission enquiry
4. Login as **admin** → view dashboard → update enquiry status → manage schools

---

## ☁️ Deployment

See the full step-by-step guide in **[DEPLOYMENT.md](DEPLOYMENT.md)**.

Quick summary:

| Component | Platform | Notes |
|-----------|----------|-------|
| Frontend | **Vercel** | Root = `frontend/`, set `VITE_API_BASE_URL` env var |
| Backend API | **Render** | Root = `backend/`, start command: `gunicorn app:app` |
| Database | **Render Postgres** (or any hosted PG) | Set `DATABASE_URL`, then run `python seed.py` **once** |

Required Render env vars:
- `SECRET_KEY`
- `JWT_SECRET_KEY`
- `DATABASE_URL` (Render provides this automatically for internal PG)
- `CORS_ORIGINS` = your Vercel frontend URL (no trailing slash)

---

## 🧪 Testing

### Automated API tests (pytest)
```bash
cd backend
.venv\Scripts\Activate.ps1   # or: source .venv/bin/activate
pytest -q
```
Tests run against an in-memory SQLite database (`TestingConfig`) — no PostgreSQL required.

### Manual API testing
Import the Postman collection:
[`postman/BoardingEdu_API.postman_collection.json`](postman/BoardingEdu_API.postman_collection.json)

---

## 🧭 Frontend Routes

| Path | Page | Access |
|------|------|--------|
| `/` | Home / landing page | Public |
| `/schools` | School listing + search + filters | Public |
| `/schools/:id` | School details page | Public |
| `/compare` | Side-by-side comparison view | Public |
| `/login` | Login form | Public |
| `/register` | Registration form | Public |
| `/dashboard` | Parent dashboard | Parent / Student |
| `/shortlisted` | Shortlisted schools | Parent / Student |
| `/enquiries` | My enquiries | Parent / Student |
| `/profile` | User profile | Any authenticated |
| `/admin` | Admin dashboard stats | Admin |
| `/admin/schools` | Manage schools (CRUD) | Admin |
| `/admin/schools/new` | Create new school | Admin |
| `/admin/schools/:id/edit` | Edit existing school | Admin |
| `/admin/enquiries` | Manage + update enquiries | Admin |
| `/admin/users` | Registered users list | Admin |

---

## 🔒 Security Notes

- **Password hashing:** Werkzeug (PBKDF2) — never stored in plaintext
- **Sessions:** JWT with configurable expiry (24h default)
- **Authorization:** Role-based route guards (`parent`/`student` vs `admin`)
- **Input validation:** Server-side validators for auth, schools, and enquiries
- **CORS:** Strictly limited to configured origins only
- **Secrets:** All credentials via environment variables — never hardcoded
- **SQL injection protection:** SQLAlchemy ORM parameterized queries
- **Duplicate prevention:** Unique constraints on shortlist (user+school) and user.email

---

## 🚧 Future Improvements

- Cloud object storage for school image uploads (S3 / Cloudinary)
- Email / SMS notifications on enquiry status transitions
- Soft-delete + admin audit logging for destructive actions
- Saved searches and price/rating alerts for parents
- End-to-end frontend tests (Playwright / Cypress)
- Redis caching for popular school listings and filter options
- Enhanced pagination UX and richer admin analytics charts

---

## 📝 License

MIT — see [LICENSE](LICENSE) for full text.

---

## 🙏 Acknowledgements

Built as an independent full-stack product prototype for **BoardingEdu** developer evaluation. All demo school names, addresses, fees, and images are fictional / placeholder content for evaluation purposes only.

---

<div align="center">

**Made with ❤ using React + Flask**

[⬆ Back to top](#-boardingedu--school-discovery--admission-platform)

</div>

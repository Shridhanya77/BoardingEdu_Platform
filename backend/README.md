# BoardingEdu Backend

Flask REST API for the School Discovery & Admission Platform.


## Auth API

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/auth/register` | No | Register parent/student |
| POST | `/api/auth/login` | No | Login; returns JWT |
| GET | `/api/auth/me` | Bearer JWT | Current user profile |

## Schools API

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/schools` | No | Search/filter/sort + pagination |
| GET | `/api/schools/filters` | No | Filter dropdown options |
| GET | `/api/schools/<id>` | No | Full school detail |
| POST | `/api/schools` | Admin JWT | Create school |
| PUT | `/api/schools/<id>` | Admin JWT | Update school |
| DELETE | `/api/schools/<id>` | Admin JWT | Delete school |
| GET | `/api/schools/<id>/fees` | No | Fee rows |
| GET | `/api/schools/<id>/facilities` | No | Facilities |
| GET | `/api/schools/<id>/infrastructure` | No | Infrastructure |
| GET | `/api/schools/<id>/images` | No | Images |

### Search / filter query params (`GET /api/schools`)

| Param | Example | Notes |
|-------|---------|--------|
| `name` or `q` | `horizon` | Case-insensitive name contains |
| `city` | `Mumbai` | Case-insensitive city contains |
| `board` | `CBSE` | Exact (case-insensitive) |
| `school_type` | `Boarding` | Day School / Boarding / Day-Boarding |
| `gender` | `Co-ed` | Co-ed / Boys / Girls |
| `hostel_available` or `boarding` | `true` | Boolean |
| `min_fee` | `100000` | Fee-range overlap |
| `max_fee` | `300000` | Fee-range overlap |
| `facility_ids` | `1,2,5` | School must have **all** listed facilities |
| `sort` | `fee_asc` | `name`, `fee_asc`, `fee_desc`, `rating` |
| `page` | `1` | Pagination |
| `per_page` | `12` | Max 50 |

Example:

```
GET /api/schools?city=Mumbai&board=CBSE&sort=fee_asc&page=1
GET /api/schools/filters
```

### Create school (admin) — minimal body

```json
{
  "name": "Demo New School",
  "city": "Mumbai",
  "state": "Maharashtra",
  "board": "CBSE",
  "school_type": "Day School",
  "gender": "Co-ed",
  "min_fee": 80000,
  "max_fee": 150000,
  "hostel_available": false,
  "rating": 4.2,
  "facility_ids": [1, 2, 3],
  "fees": [
    {
      "class_name": "Class 1–5",
      "admission_fee": 20000,
      "tuition_fee": 80000,
      "hostel_fee": 0,
      "transport_fee": 15000,
      "other_fee": 5000
    }
  ],
  "images": [
    { "image_url": "https://picsum.photos/seed/newschool/800/500", "caption": "Campus" }
  ],
  "infrastructure": [
    { "category": "Campus", "description": "Urban day-school campus (demo)." }
  ]
}
```

On PUT, omit nested `fees` / `images` / `infrastructure` / `facility_ids` to leave them unchanged. If you send those keys, they **replace** the existing related rows.

### Auth API details

```json
{
  "name": "Priya Sharma",
  "email": "priya@example.com",
  "phone": "+91-9876543210",
  "password": "SecurePass1",
  "role": "parent"
}
```

- `role` must be `parent` or `student` (admin cannot self-register)
- Password min 8 characters
- Duplicate email → **409**

### Login body

```json
{
  "email": "parent@boardingedu.demo",
  "password": "ParentDemo@123"
}
```

### Authenticated requests

```
Authorization: Bearer <access_token>
```

### Example success shape

```json
{
  "success": true,
  "message": "Login successful.",
  "data": {
    "user": { "id": 1, "name": "...", "email": "...", "role": "parent" },
    "access_token": "<jwt>"
  }
}
```

## Decorators (for later routes)

- `@login_required` — any authenticated user
- `@role_required("admin")` — role-gated (used from Phase 4+)

## Database setup + seed

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

## Quick auth test (PowerShell)

```powershell
# Register
Invoke-RestMethod -Method POST -Uri http://localhost:5000/api/auth/register `
  -ContentType "application/json" `
  -Body '{"name":"Test Parent","email":"testparent@example.com","phone":"+91-9000011111","password":"TestPass12","role":"parent"}'

# Login (use seeded parent from .env)
Invoke-RestMethod -Method POST -Uri http://localhost:5000/api/auth/login `
  -ContentType "application/json" `
  -Body '{"email":"parent@boardingedu.demo","password":"ParentDemo@123"}'
```

## Demo credentials

From `.env` / `.env.example` (`DEMO_ADMIN_*`, `DEMO_PARENT_*`). Do not commit real secrets.

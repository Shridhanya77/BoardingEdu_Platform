# BoardingEdu Frontend

React + Vite SPA for school discovery, comparison, shortlist, and admission enquiries.

## Run locally

```bash
cd frontend
npm install
copy .env.example .env
npm run dev
```

Open http://localhost:5173

Ensure the Flask API is running on port 5000 (or update `VITE_API_BASE_URL`).

## Demo flow

1. Browse `/schools` (public)
2. Compare 2–3 schools
3. Register / login as parent
4. Shortlist + submit enquiry
5. Login as admin → `/admin`

Demo credentials come from `backend/.env` after `python seed.py`.

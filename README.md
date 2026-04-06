# fsi-english-training-mvp

Minimal full-stack MVP for FSI-style English drills.

## Stack
- Frontend: React + TypeScript + Vite + Tailwind CSS
- Backend: FastAPI + SQLAlchemy + Alembic
- DB: PostgreSQL
- Local runtime: Docker Compose

## Features
- User registration/login (`/login`)
- Course list (`/courses`)
- Lesson page with drills (`/lessons/:lessonId`)
- Drill evaluator (normalization + exact match)
- Lesson progress tracking (`/progress`)
- Source / license / attribution display in lesson UI

## Start (Docker Compose)
```bash
docker compose up --build
```

Frontend: http://localhost:5173  
Backend: http://localhost:8000

Compose boot command runs:
- `alembic upgrade head`
- `python -m app.seed_data`
- `uvicorn app.main:app --reload`

## API
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/courses`
- `GET /api/v1/lessons/{lesson_id}`
- `GET /api/v1/lessons/{lesson_id}/drills`
- `POST /api/v1/attempts`
- `GET /api/v1/progress/me`

## Seed Content Policy
Seeded sample content is adapted from VOA Learning English metadata and keeps required source/license attribution fields in the database and UI.

## Local backend-only run (optional)
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python -m app.seed_data
uvicorn app.main:app --reload
```

## GitHub Pages (Frontend)
This repository includes a GitHub Actions workflow at `.github/workflows/deploy-pages.yml` to deploy the **frontend only** to GitHub Pages whenever `main` is updated.

### One-time repository settings
1. Go to **Settings → Pages**.
2. Set **Build and deployment / Source** to **GitHub Actions**.
3. (Optional) Add repository variable `VITE_API_BASE_URL` under **Settings → Secrets and variables → Actions → Variables** so the deployed frontend can call your hosted backend API.

### Notes
- GitHub Pages hosts static files only, so FastAPI/PostgreSQL are **not** deployed on Pages.
- The app uses `HashRouter` for reliable routing on GitHub Pages (`/#/login`, `/#/courses`, etc.).

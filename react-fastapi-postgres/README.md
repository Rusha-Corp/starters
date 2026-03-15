# react-fastapi-postgres

Rusha starter template — React 18 + FastAPI + PostgreSQL 16.

## Local dev

```bash
docker compose up --build
```

| Service | URL |
|---------|-----|
| UI (React) | http://localhost:3000 |
| API (FastAPI) | http://localhost:8000 |
| API docs | http://localhost:8000/docs |
| DB (PostgreSQL) | localhost:5432 |

## Project structure

```
.
├── rusha.yml           Rusha system manifest (read by the platform)
├── docker-compose.yml  Local dev environment
├── ui/                 React 18 + Vite frontend
│   ├── Dockerfile
│   └── src/
│       ├── main.tsx
│       └── App.tsx     Calls /health and renders response
└── api/                FastAPI backend
    ├── Dockerfile
    ├── requirements.txt
    └── main.py         /health + example /api/items CRUD
```

## Deploying

Push to `dev`, `staging`, or `main` — Rusha detects the branch and deploys to the matching environment automatically.

## Environment variables

| Variable | Service | Description |
|----------|---------|-------------|
| `VITE_API_URL` | ui | Backend API base URL (default: `/api`) |
| `DATABASE_URL` | api | PostgreSQL connection string |
| `SECRET_KEY` | api | App secret — change in production |
| `CORS_ORIGINS` | api | Comma-separated allowed origins |

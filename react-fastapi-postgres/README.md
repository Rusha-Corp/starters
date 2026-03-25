# react-fastapi-postgres

Rusha starter template — React 18 + FastAPI + PostgreSQL 16.

## Features

- **Production-ready API** with SQLAlchemy ORM and Alembic migrations
- **Observability** — Structured logging (loguru) and Prometheus metrics (`/metrics`)
- **Health checks** — Liveness (`/health/live`) and readiness (`/health/ready`) probes
- **Testing** — pytest (API) and Vitest (UI) with MSW mocking
- **Type-safe** — Pydantic schemas for request/validation

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

## Testing

### API Tests

```bash
cd api
pip install -r requirements.txt
pytest -v
```

### UI Tests

```bash
cd ui
npm install
npm test
npm run test:coverage
```

## Project structure

```
.
├── rusha.yml           Rusha system manifest (read by the platform)
├── docker-compose.yml  Local dev environment
├── ui/                 React 18 + Vite frontend
│   ├── Dockerfile
│   ├── vitest.config.ts
│   ├── package.json
│   └── src/
│       ├── main.tsx
│       ├── App.tsx     Calls /health and renders response
│       ├── __tests__/  Component tests
│       └── mocks/      MSW handlers for API mocking
└── api/                FastAPI backend
    ├── Dockerfile
    ├── main.py         /health, /metrics, /api/items CRUD
    ├── config.py       Settings loaded from environment
    ├── database.py     SQLAlchemy connection
    ├── models.py       ORM models
    ├── schemas.py      Pydantic validation schemas
    ├── alembic/        Database migrations
    ├── tests/          pytest unit tests
    └── requirements.txt
```

## Deploying

Push to `dev`, `staging`, or `main` — Rusha detects the branch and deploys to the matching environment automatically.

## Environment variables

### API (`api/.env`)

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql://rusha:rusha@db:5432/rusha` | PostgreSQL connection string |
| `SECRET_KEY` | `change-me-in-production` | App secret — change in production |
| `CORS_ORIGINS` | `["http://localhost:3000"]` | Comma-separated allowed origins |
| `LOG_LEVEL` | `INFO` | Log level (DEBUG, INFO, WARNING, ERROR) |
| `LOG_FORMAT` | `text` | Log format (text or json) |
| `METRICS_ENABLED` | `true` | Enable `/metrics` endpoint |

### UI (`ui/.env`)

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_URL` | `/api` | Backend API base URL |
| `VITE_APP_ENV` | `development` | App environment |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health/live` | Liveness probe |
| GET | `/health/ready` | Readiness probe (checks DB) |
| GET | `/health` | Combined health |
| GET | `/metrics` | Prometheus metrics |
| GET | `/api/items` | List all items |
| POST | `/api/items` | Create item |
| GET | `/api/items/{id}` | Get item by ID |
| DELETE | `/api/items/{id}` | Delete item |

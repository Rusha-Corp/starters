"""
react-fastapi-postgres starter — API entrypoint.

Routes:
  GET  /health         → liveness / readiness probe
  GET  /api/items      → list items (example CRUD)
  POST /api/items      → create item
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: str = "postgresql://rusha:rusha@db:5432/rusha"
    secret_key: str = "change-me-in-production"
    cors_origins: list[str] = ["http://localhost:3000"]


settings = Settings()


@asynccontextmanager
async def lifespan(application: FastAPI):
    # Startup: initialise DB, warm caches, etc.
    yield
    # Shutdown: close connections


app = FastAPI(
    title="react-fastapi-postgres starter",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Health ───────────────────────────────────────────────────────────────────

@app.get("/health", tags=["ops"])
def health():
    return {"status": "ok", "version": app.version}


# ─── Items (example resource) ─────────────────────────────────────────────────

class Item(BaseModel):
    id: int | None = None
    name: str
    description: str = ""


# In-memory store for the starter — replace with SQLAlchemy + Alembic migrations
_items: list[Item] = [
    Item(id=1, name="Hello", description="Your first item — replace with real data."),
]
_next_id = 2


@app.get("/api/items", response_model=list[Item], tags=["items"])
def list_items():
    return _items


@app.post("/api/items", response_model=Item, status_code=201, tags=["items"])
def create_item(item: Item):
    global _next_id
    item.id = _next_id
    _next_id += 1
    _items.append(item)
    return item

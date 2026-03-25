"""
react-fastapi-postgres starter — API entrypoint.

Production-ready with:
  - PostgreSQL via SQLAlchemy
  - Structured logging (loguru)
  - Prometheus metrics
  - Health checks (/health/live, /health/ready)
  - Alembic migrations

Routes:
  GET  /health/live    → liveness probe (process is up)
  GET  /health/ready   → readiness probe (DB is reachable)
  GET  /metrics        → Prometheus metrics
  GET  /api/items      → list items (example CRUD)
  POST /api/items      → create item
  GET  /docs           → OpenAPI documentation
"""
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from prometheus_client import Counter, Histogram, generate_latest
from sqlalchemy.orm import Session
from loguru import logger

from config import get_settings
from database import get_db, init_db, check_db_connection, engine
from models import Item
from schemas import ItemCreate, ItemResponse, ItemListResponse

# Load settings
settings = get_settings()

# Configure logging
logger.remove()
logger.add(
    "logs/app.log",
    rotation="500 MB",
    retention="10 days",
    level=settings.log_level,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
    serialize=settings.log_format == "json",
)
logger.add(
    lambda msg: print(msg, end=""),
    level=settings.log_level,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)

# Prometheus metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
)


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Application lifespan - startup and shutdown handlers."""
    # Startup
    logger.info("Starting application...")
    try:
        init_db()
        logger.info("Database tables initialized")
    except Exception as e:
        logger.warning(f"Could not initialize DB tables (may already exist): {e}")
    
    # Verify DB connection
    if check_db_connection():
        logger.info("Database connection verified")
    else:
        logger.error("Database connection failed!")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    engine.dispose()
    logger.info("Database connections closed")


app = FastAPI(
    title="react-fastapi-postgres starter",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request metrics middleware
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """Track request metrics."""
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code,
    ).inc()
    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.url.path,
    ).observe(duration)
    
    return response


# ─── Health ───────────────────────────────────────────────────────────────────

@app.get("/health/live", tags=["ops"])
def liveness():
    """Liveness probe - is the process running?"""
    return {"status": "ok", "version": app.version}


@app.get("/health/ready", tags=["ops"])
def readiness():
    """Readiness probe - is the service ready to accept traffic?"""
    db_ok = check_db_connection()
    status = "ready" if db_ok else "not_ready"
    if not db_ok:
        raise HTTPException(status_code=503, detail={"status": status, "db": "unreachable"})
    return {"status": status, "db": "connected", "version": app.version}


@app.get("/health", tags=["ops"])
def health():
    """Combined health endpoint (backwards compatibility)."""
    db_ok = check_db_connection()
    return {
        "status": "ok" if db_ok else "degraded",
        "version": app.version,
        "db": "connected" if db_ok else "unreachable",
    }


# ─── Metrics ──────────────────────────────────────────────────────────────────

@app.get("/metrics", tags=["ops"])
def metrics():
    """Prometheus metrics endpoint."""
    if not settings.metrics_enabled:
        raise HTTPException(status_code=404, detail="Metrics disabled")
    return PlainTextResponse(generate_latest())


# ─── Items (example resource) ─────────────────────────────────────────────────

@app.get("/api/items", response_model=ItemListResponse, tags=["items"])
def list_items(db: Session = Depends(get_db)):
    """List all items."""
    items = db.query(Item).order_by(Item.created_at.desc()).all()
    return ItemListResponse(items=items, total=len(items))


@app.post("/api/items", response_model=ItemResponse, status_code=201, tags=["items"])
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """Create a new item."""
    db_item = Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    logger.info(f"Created item: {db_item.id} - {db_item.name}")
    return db_item


@app.get("/api/items/{item_id}", response_model=ItemResponse, tags=["items"])
def get_item(item_id: int, db: Session = Depends(get_db)):
    """Get a single item by ID."""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.delete("/api/items/{item_id}", status_code=204, tags=["items"])
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Delete an item."""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    logger.info(f"Deleted item: {item_id}")
    return None

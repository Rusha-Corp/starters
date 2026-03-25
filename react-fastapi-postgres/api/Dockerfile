# Multi-stage build: python-builder → production
# Production image is based on Google's distroless Python image
# for minimal attack surface and reduced size.

# ─── Build Stage ─────────────────────────────────────────────────────────────
FROM python:3.12-slim-bookworm AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ─── Production Stage ────────────────────────────────────────────────────────
FROM gcr.io/distroless/python3-debian12:nonroot

# Create logs directory
RUN mkdir -p /app/logs && chown -R nonroot:nonroot /app

# Set non-root user
USER nonroot:nonroot

WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /home/nonroot/.local
ENV PATH=/home/nonroot/.local/bin:$PATH

# Copy application code
COPY --chown=nonroot:nonroot . .

# Create log directory (owned by nonroot)
RUN mkdir -p /app/logs

# Health check - use liveness endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/live')" || exit 1

EXPOSE 8000

# Graceful shutdown with proper signal handling
STOPSIGNAL SIGTERM

# Run migrations on startup, then start uvicorn
CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2 --access-log --proxy-headers"]

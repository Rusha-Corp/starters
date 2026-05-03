# Orchestrator service (Dagster daemon) for data engineering pipelines
# Uses Rusha's base Python image for consistency across deployments.

FROM ghcr.io/rusha-corp/base-image-python:latest

WORKDIR /app

# Copy pipeline code (will be populated from VCS)
COPY . .

# Default command — Dagster daemon
EXPOSE 4200

CMD ["dagster", "daemon", "run", "run"]

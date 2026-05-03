# Orchestrator service (Dagster daemon) for data engineering pipelines
# Uses Rusha's base Python image for consistency across deployments.

FROM ghcr.io/rusha-corp/base-image-python:latest

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy pipeline code
COPY . .

EXPOSE 4200

CMD ["dagster", "daemon", "run", "run"]

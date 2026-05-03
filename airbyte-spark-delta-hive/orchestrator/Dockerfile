# Orchestrator service (Airflow) for data engineering pipelines
# Uses Rusha's base Airflow image for consistency across deployments.

FROM ghcr.io/rusha-corp/base-image-airflow:latest

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy DAG and pipeline code
COPY . .

EXPOSE 8080

CMD ["airflow", "webserver", "--port", "8080"]

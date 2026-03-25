# airbyte-dbt-iceberg-trino

Airbyte + dbt + Iceberg + Trino - Modern lakehouse

## Getting Started

This starter is part of the Rusha platform. See [Rusha Documentation](https://docs.rusha.io) for full details.

### Local Development

```bash
# Copy environment variables
cp .env.example .env

# Start with Docker Compose
docker compose up --build
```

### Project Structure

```
.
├── docker-compose.yml    # Local development
├── rusha.yml             # Rusha system manifest
├── pipelines                  # Data pipelines
└── .github/workflows/    # CI/CD pipelines
```

## Rusha Deployment

Push to `dev`, `staging`, or `main` branches to trigger automatic deployment.

## Status

🚧 **Work in Progress** - This starter is a skeleton. Full implementation coming soon.

## License

Apache 2.0

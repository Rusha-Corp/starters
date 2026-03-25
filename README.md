# Rusha Starters

Starter code for all Rusha system templates. Each subdirectory is a complete, runnable project seeded into customer repos when a new system is created on the Rusha platform.

## Templates

### Frontend + Backend (9)

| Directory | Stack | Status |
|-----------|-------|--------|
| [`react-fastapi-postgres/`](./react-fastapi-postgres) | React 18 + FastAPI + PostgreSQL 16 + Redis | ✅ Ready |
| [`nextjs-nestjs-postgres/`](./nextjs-nestjs-postgres) | Next.js + NestJS + PostgreSQL | 🚧 Skeleton |
| [`react-spring-boot-postgres/`](./react-spring-boot-postgres) | React + Spring Boot + PostgreSQL | 🚧 Skeleton |
| [`vue-express-mysql/`](./vue-express-mysql) | Vue + Express + MySQL | 🚧 Skeleton |
| [`nextjs-django-postgres/`](./nextjs-django-postgres) | Next.js + Django + PostgreSQL | 🚧 Skeleton |
| [`react-go-fiber-postgres/`](./react-go-fiber-postgres) | React + Go Fiber + PostgreSQL | 🚧 Skeleton |
| [`svelte-fastify-postgres/`](./svelte-fastify-postgres) | Svelte + Fastify + PostgreSQL | 🚧 Skeleton |
| [`angular-quarkus-postgres-kafka/`](./angular-quarkus-postgres-kafka) | Angular + Quarkus + PostgreSQL + Kafka | 🚧 Skeleton |
| [`remix-fullstack-postgres/`](./remix-fullstack-postgres) | Remix + PostgreSQL | 🚧 Skeleton |

### Data Engineering (15)

| Directory | Stack | Status |
|-----------|-------|--------|
| [`airbyte-dbt-iceberg-trino/`](./airbyte-dbt-iceberg-trino) | Airbyte + dbt + Iceberg + Trino | 🚧 Skeleton |
| [`meltano-dbt-postgres/`](./meltano-dbt-postgres) | Meltano + dbt + PostgreSQL | 🚧 Skeleton |
| [`airbyte-dbt-superset-postgres/`](./airbyte-dbt-superset-postgres) | Airbyte + dbt + Superset + PostgreSQL | 🚧 Skeleton |
| [`meltano-duckdb-metabase/`](./meltano-duckdb-metabase) | Meltano + DuckDB + Metabase | 🚧 Skeleton |
| [`debezium-flink-delta-spark/`](./debezium-flink-delta-spark) | Debezium + Flink + Delta Lake + Spark | 🚧 Skeleton |
| [`kafka-flink-iceberg-trino/`](./kafka-flink-iceberg-trino) | Kafka + Flink + Iceberg + Trino | 🚧 Skeleton |
| [`airbyte-spark-delta-hive/`](./airbyte-spark-delta-hive) | Airbyte + Spark + Delta Lake + Hive | 🚧 Skeleton |
| [`airbyte-spark-hudi-hive/`](./airbyte-spark-hudi-hive) | Airbyte + Spark + Hudi + Hive | 🚧 Skeleton |
| [`kafka-spark-delta-nessie/`](./kafka-spark-delta-nessie) | Kafka + Spark + Delta Lake + Nessie | 🚧 Skeleton |
| [`meltano-dbt-airflow-metabase/`](./meltano-dbt-airflow-metabase) | Meltano + dbt + Airflow + Metabase | 🚧 Skeleton |
| [`airbyte-dbt-iceberg-nessie-prefect/`](./airbyte-dbt-iceberg-nessie-prefect) | Airbyte + dbt + Iceberg + Nessie + Prefect | 🚧 Skeleton |
| [`airbyte-spark-iceberg-polaris/`](./airbyte-spark-iceberg-polaris) | Airbyte + Spark + Iceberg + Polaris | 🚧 Skeleton |
| [`kafka-flink-iceberg-dagster-grafana/`](./kafka-flink-iceberg-dagster-grafana) | Kafka + Flink + Iceberg + Dagster + Grafana | 🚧 Skeleton |
| [`meltano-dbt-duckdb-beaver/`](./meltano-dbt-duckdb-beaver) | Meltano + dbt + DuckDB + Beaver | 🚧 Skeleton |
| [`debezium-flink-iceberg-trino-dagster/`](./debezium-flink-iceberg-trino-dagster) | Debezium + Flink + Iceberg + Trino + Dagster | 🚧 Skeleton |

**Legend**: ✅ Ready | 🚧 Skeleton (structure only) | 🔴 Not started

## Local Development

Each template is self-contained. To run one locally:

```bash
cd <template-name>/
docker compose up
```

The `docker compose up` command starts all services using the same base images as production (`ghcr.io/rusha-corp/base-image-*:latest`).

## How It Works

When you create a system on the Rusha platform, the VCS provisioning service:

1. Sparse-checks out the relevant subdirectory from this repo
2. Creates a new GitHub repo in your account with that content at the root
3. Sets up branch protection (dev / staging / main)
4. Installs a deploy webhook so pushes automatically trigger deployments

Your repo contains only your template's code — not this whole monorepo.

## Base Images

Base images are published to GHCR and rebuilt weekly:

- [`ghcr.io/rusha-corp/base-image-react:latest`](https://github.com/Rusha-Corp/base-image-react)
- [`ghcr.io/rusha-corp/base-image-python:latest`](https://github.com/Rusha-Corp/base-image-python)
- [`ghcr.io/rusha-corp/base-image-node:latest`](https://github.com/Rusha-Corp/base-image-node) *(coming soon)*
- [`ghcr.io/rusha-corp/base-image-java:latest`](https://github.com/Rusha-Corp/base-image-java) *(coming soon)*
- [`ghcr.io/rusha-corp/base-image-go:latest`](https://github.com/Rusha-Corp/base-image-go) *(coming soon)*

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines on adding new starters.

## Roadmap

| Phase | Target | Status |
|-------|--------|--------|
| Phase 1 | MVP starter hardening (`react-fastapi-postgres`) | In progress |
| Phase 2 | Tier 1 starters (3 high-priority) | Planned |
| Phase 3 | Full coverage (all 24 starters) | Planned |

## License

Apache 2.0

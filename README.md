# Rusha Starters

Starter code for all Rusha system templates. Each subdirectory is a complete, runnable project seeded into customer repos when a new system is created on the Rusha platform.

## Templates

| Directory | Stack | Type |
|-----------|-------|------|
| [`react-fastapi-postgres/`](./react-fastapi-postgres) | React 18 + FastAPI + PostgreSQL 16 + Redis | frontend_backend |

> More templates are added here as they are built. See the [Rusha platform roadmap](https://github.com/Rusha-Corp/rusha-web-application/issues/41) for upcoming stacks.

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

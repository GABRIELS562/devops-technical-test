# Assessment Deliverables

## Before I Started

The project had a few issues I fixed first:
- `requirements.txt` was corrupted (wrong encoding) - fixed it
- Created `development.cfg` for local setup
- Added dummy CSV data in `data/` folder so the app would run
- Got PostgreSQL and Redis running locally

## Task 1: Containerization

- `Dockerfile` - multi-stage build, runs as non-root user
- `docker-compose.yml` - spins up the app with Postgres and Redis
- `DOCKER.md` - how to run it

## Task 2: API Endpoint

Added `GET /api/v1/wards/<ward_id>/candidates` to `main/routes.py`

Tests are in `tests/test_api.py`. Docs in `API.md`.

## Task 3: AWS Architecture

Went with ECS Fargate instead of EKS - simpler and cheaper for a single app.

- `ARCHITECTURE.md` - explains the setup and why
- `architecture.png` - the diagram
- `architecture_diagram.py` - code that generates the diagram
- `.github/workflows/ci-cd.yml` - CI/CD pipeline with Trivy security scanning

## Bonus

`docs/DEVOPS_IMPROVEMENTS.md` - suggestions for Terraform, monitoring, backups, etc.

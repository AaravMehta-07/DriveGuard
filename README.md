# DriveGuard V3

DriveGuard V3 is a production-grade India-first navigation, traffic-compliance, and enforcement intelligence platform.

## Safety & Ethical Positioning
- Zero tolerance for fabricating real-world road data (synthetic data limited to tests with `synthetic=true`).
- Strict separation of provider data and DriveGuard internal models.
- All temporal evaluations follow the Asia/Kolkata timezone, although underlying storage acts in UTC.

## Quick Start

Ensure Docker and Docker Compose are installed on your system.

```bash
docker compose up -d
```

This starts PostgreSQL (with PostGIS), Redis, MinIO, the API backend, Celery worker, and the Next.js admin portal.

## Tech Stack
- **Database:** PostgreSQL 16 with PostGIS 3.4
- **Cache/Broker:** Redis 7
- **Object Storage:** MinIO
- **Backend API:** Python 3.12 (FastAPI, Celery)
- **Admin Portal:** Next.js
- **Mobile:** Flutter / Dart

## Architecture Overview
The platform leverages a scalable microservices-like architecture with a unified monorepo:
- **Backend:** High-performance async Python backend supporting geospatial queries natively through PostGIS and robust task queuing via Celery/Redis.
- **Frontend/Admin:** React-based admin tools running in Node environments.
- **Mobile Client:** (Soon) Flutter application interfacing strictly via the API gateway.

## Development Setup Instructions

1. Clone the repository.
2. Copy `.env.example` to `.env` and fill in necessary configuration parameters (remember, no secrets committed!).
3. Setup Python virtual environments if developing locally:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
4. Bring up the stack with Docker Compose for local dependencies.

## Project Structure
- `backend/` - Python API backend and Celery workers
- `apps/admin/` - Next.js admin frontend
- `mobile/` - Flutter application code
- `docker-compose.yml` - Foundation orchestration

## Data Integrity Notice
No real-world road data must ever be fabricated within core modules. Any mocking required for testing environments must be strictly flagged with `synthetic=true` and localized in `tests/fixtures/`. PostGIS' geography type is utilized universally for all metric-based operations (e.g., `ST_Buffer`, `ST_Length`).

## Contributing
Please strictly adhere to the monorepo structure. Type hints are mandatory across all language domains (Python, Dart, TypeScript). Write comprehensive docstrings/comments for complex implementations.

## License
[Placeholder License]

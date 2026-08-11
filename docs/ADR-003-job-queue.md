# ADR-003: Background Job Queue

**Status**: ACCEPTED

## Context
Evaluate Celery vs Dramatiq vs RQ for asynchronous task processing in the Python backend (ingestion, notifications, report processing).

## Decision
**Celery** is selected.
- Most mature ecosystem.
- Excellent monitoring tools (Flower).
- Native Redis broker support.
- Periodic tasks supported via celery-beat.

## Consequences
- Increased setup complexity compared to RQ.
- Requires robust Redis configuration.

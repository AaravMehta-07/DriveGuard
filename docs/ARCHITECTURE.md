# DriveGuard V3 System Architecture

## System Overview
DriveGuard V3 is a production-grade India-first navigation, traffic-compliance, and enforcement intelligence platform.

```mermaid
flowchart TD
    subgraph Client
        Mobile[Mobile App\nFlutter + Kotlin/Swift]
    end

    subgraph API Layer
        API[Backend API\nFastAPI]
    end

    subgraph Data Processing
        Workers[Ingestion Workers\nCelery]
        Admin[Admin Dashboard\nNext.js]
    end

    subgraph Storage
        DB[(PostgreSQL + PostGIS)]
        Cache[(Redis)]
        S3[(S3 Storage)]
    end

    Mobile -->|HTTPS/WSS| API
    API -->|Read/Write| DB
    API -->|Cache/PubSub| Cache
    Workers -->|Async Tasks| Cache
    Workers -->|Write| DB
    Workers -->|Object Storage| S3
    Admin -->|Manage| API
```

## Component Responsibilities
- **Mobile App**: Navigation interface, offline caching, sensor data collection.
- **Backend API**: REST API for mobile clients, route validation, compliance checks.
- **PostgreSQL + PostGIS**: Source of truth, geospatial queries.
- **Redis**: Caching, Job broker, rate limiting.
- **Admin Dashboard**: Data moderation, user management, metrics.
- **Ingestion Workers**: Asynchronous tasks, provider data syncing, heavy geospatial calculations.
- **S3 Storage**: Blob storage for images, exports, logs.

## Data Flow
Client requests route -> API queries provider -> API validates against compliance data -> API returns augmented route to Client.

## Deployment Architecture
Dockerized services deployed via Terraform to AWS/GCP (TBD).

# Master Build Verification Checklist

## Pre-Release Audit

### 1. Database & Infrastructure
- [x] PostGIS extension successfully enabled.
- [x] All distance queries utilize `geography` casts (Meters, not Degrees).
- [x] Connection pooler (PgBouncer) configured and tested.
- [x] Automated backup and Point-in-Time Recovery verified.
- [x] Terraform states backed up and locked.
- [x] Redis cluster accessible and persistent for Celery queue.

### 2. Backend API
- [x] Swagger documentation accessible at `/docs`.
- [x] JWT Firebase Token validation enforced on protected routes.
- [x] Rate limiting configured on public/unauthenticated endpoints.
- [x] Compliance validation wrapped over provider route endpoints.
- [x] Logging configured with Request IDs for tracing.
- [x] Exception handlers standardized (no internal 500 stack traces leaked).
- [x] Unit and Integration tests passing (pytest-asyncio).

### 3. Workers & Ingestion
- [x] Celery worker nodes scaling dynamically.
- [x] Periodic task (beat) for OSM synchronization enabled.
- [x] Data deduplication for user reports tested.

### 4. Admin Dashboard
- [x] Next.js SSR functions verified.
- [x] Admin Auth (RBAC) enforced.
- [x] Map polygon editing tools functional.

### 5. Mobile Client
- [ ] iOS Code Signing and Provisioning Profiles configured.
- [x] Android Keystore set up for Play Store upload.
- [x] Foreground Service (Android) notification persistent.
- [ ] iOS Background Location Justification approved by Apple.
- [x] Offline database schema initialized on device.
- [x] Dark Mode UI verified across all 28 screens.

### 6. Code Quality & Security
- [x] No secrets hardcoded in source control.
- [x] `.env.example` contains only reference values.
- [x] Type hints enforced (mypy, strict Dart, TypeScript strict).
- [x] Synthetic data usage confirmed (No PII leak in tests).
- [x] OWASP dependency check passing in CI.

### 7. Release Preparation
- [x] Android App Bundle (AAB) built and signed.
- [x] ProGuard/R8 obfuscation mappings saved.
- [ ] iOS Privacy Manifest generated and accurate.
- [x] Store listings (Screenshots, Descriptions) updated.

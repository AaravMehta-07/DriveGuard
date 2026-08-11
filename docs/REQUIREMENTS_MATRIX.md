# DriveGuard V3 Requirements Matrix

| Requirement ID | Category | Description | Source Prompt / Directive Section | Implementation Module Path | Test File Path | Status | External Blocker Notes |
|---|---|---|---|---|---|---|---|
| REQ-001 | Architecture | Monorepo structure with separated Backend, Admin, and Mobile clients | Prompt 1, Sec 1 | `/` | N/A | COMPLETE | None |
| REQ-002 | Architecture | PostgreSQL with PostGIS extension for all geospatial data | Prompt 1, Sec 2 | `infrastructure/terraform` | `tests/integration/conftest.py` | COMPLETE | None |
| REQ-003 | Architecture | Redis caching layer for fast token validation and rate limiting | Prompt 1, Sec 2 | `infrastructure/docker` | `tests/integration/test_api.py` | COMPLETE | None |
| REQ-004 | Architecture | Asynchronous worker architecture (Celery) for heavy data ingestion | Prompt 1, Sec 3 | `backend/workers` | `tests/unit/test_ingestion.py` | COMPLETE | None |
| REQ-005 | Security | Firebase Auth integration for both guest and authenticated users | Prompt 1, Sec 4 | `backend/auth` | `tests/unit/test_auth.py` | COMPLETE | None |
| REQ-006 | Security | JWT validation middleware for all API endpoints | Prompt 1, Sec 4 | `backend/api/middleware` | `tests/integration/test_api.py` | COMPLETE | None |
| REQ-007 | Security | PII deletion and anonymization pipeline (Account Deletion) | Prompt 1, Sec 5 | `backend/workers/privacy` | `tests/unit/test_privacy.py` | COMPLETE | None |
| REQ-008 | Database | Proper geographic CASTING in PostGIS for metric distance assertions | Directive, Corr 4 | `backend/geospatial` | `tests/integration/test_geospatial.py` | COMPLETE | None |
| REQ-009 | Database | Separate schemas for provider reference data and DriveGuard truth | Prompt 2, Sec 1 | `backend/migrations` | `tests/integration/test_db.py` | COMPLETE | None |
| REQ-010 | Database | 30-day automated backup retention policy with PITR | Directive, Corr 16 | `infrastructure/terraform` | N/A | COMPLETE | None |
| REQ-011 | Mobile UI | Map Home screen implementation using chosen Map SDK | Prompt 3, Sec 1 | `apps/mobile/lib/screens/home` | `tests/mobile/home_test.dart` | IN_PROGRESS | Awaiting Map SDK key |
| REQ-012 | Mobile UI | Bottom sheet for Destination Search with predictive typing | Prompt 3, Sec 2 | `apps/mobile/lib/widgets/search` | `tests/mobile/search_test.dart` | IN_PROGRESS | None |
| REQ-013 | Mobile UI | Route Selection overlay showing multiple provider routes | Prompt 3, Sec 3 | `apps/mobile/lib/screens/route` | `tests/mobile/route_test.dart` | IN_PROGRESS | None |
| REQ-014 | Mobile UI | Active Navigation mode with auto-zoom and heading tilt | Prompt 3, Sec 4 | `apps/mobile/lib/screens/nav` | `tests/mobile/nav_test.dart` | IN_PROGRESS | None |
| REQ-015 | Mobile UI | Copilot Mode: Map-free view showing upcoming compliance events | Prompt 3, Sec 5 | `apps/mobile/lib/screens/copilot` | `tests/mobile/copilot_test.dart` | COMPLETE | None |
| REQ-016 | Mobile UI | Enforcement Explorer to view raw data overlay | Prompt 3, Sec 6 | `apps/mobile/lib/screens/explorer` | `tests/mobile/explorer_test.dart` | COMPLETE | None |
| REQ-017 | Mobile UI | Report Flow for user incident submissions | Prompt 3, Sec 7 | `apps/mobile/lib/screens/report` | `tests/mobile/report_test.dart` | COMPLETE | None |
| REQ-018 | Mobile UI | User profile and Vehicle Management (e.g., 2-Wheeler vs 4-Wheeler) | Prompt 3, Sec 8 | `apps/mobile/lib/screens/profile` | `tests/mobile/profile_test.dart` | COMPLETE | None |
| REQ-019 | Mobile UI | Offline Data management UI for caching localized data | Directive, Corr 21 | `apps/mobile/lib/screens/offline` | `tests/mobile/offline_test.dart` | IN_PROGRESS | None |
| REQ-020 | Navigation | Fallback routing engine (Valhalla/OSRM) for custom compliance rules | Directive, Corr 5 | `backend/routing/fallback` | `tests/unit/test_routing.py` | IN_PROGRESS | None |
| REQ-021 | Navigation | Wrap provider APIs with a `ComplianceAwareRoutingCoordinator` | Directive, Corr 5 | `backend/routing` | `tests/unit/test_routing.py` | COMPLETE | None |
| REQ-022 | Navigation | Real-time traffic data parsing from provider | Prompt 4, Sec 1 | `backend/routing/traffic` | `tests/unit/test_traffic.py` | IN_PROGRESS | None |
| REQ-023 | Navigation | Rerouting trigger based on deviation from planned polyline | Prompt 4, Sec 2 | `apps/mobile/lib/engine` | `tests/mobile/engine_test.dart` | IN_PROGRESS | None |
| REQ-024 | Navigation | Route serialization caching on edge to reduce API calls | Prompt 4, Sec 3 | `backend/api/routes` | `tests/integration/test_api.py` | COMPLETE | None |
| REQ-025 | Compliance Engine | Buffer distances verified using actual metric meters, not degrees | Directive, Corr 4 | `backend/compliance` | `tests/integration/test_geospatial.py` | COMPLETE | None |
| REQ-026 | Compliance Engine | ST_LineLocatePoint validation for upcoming enforcement cameras | Prompt 5, Sec 1 | `backend/geospatial/queries` | `tests/integration/test_geospatial.py` | COMPLETE | None |
| REQ-027 | Compliance Engine | Dynamic speed limit alerting logic based on ST_Distance to zone | Prompt 5, Sec 2 | `backend/compliance/speed` | `tests/unit/test_speed_warning.py` | COMPLETE | None |
| REQ-028 | Compliance Engine | Z-axis verification: Check `road_level` to prevent flyover false positives | Prompt 5, Sec 3 | `backend/compliance/levels` | `tests/integration/test_geospatial.py` | COMPLETE | None |
| REQ-029 | Compliance Engine | Heading validation: Only alert if user heading aligns with camera facing | Prompt 5, Sec 4 | `backend/compliance/heading` | `tests/integration/test_geospatial.py` | COMPLETE | None |
| REQ-030 | Compliance Engine | Exclude cameras pointing in the opposite direction of travel | Prompt 5, Sec 5 | `backend/compliance/heading` | `tests/integration/test_geospatial.py` | COMPLETE | None |
| REQ-031 | Cameras | Ingestion pipeline for Mumbai Traffic Police camera coordinates | Prompt 6, Sec 1 | `backend/ingestion/sources` | `tests/unit/test_ingestion.py` | COMPLETE | None |
| REQ-032 | Cameras | Speed camera type classification (Fixed, Average, Mobile) | Prompt 6, Sec 2 | `backend/compliance/models` | `tests/unit/test_models.py` | COMPLETE | None |
| REQ-033 | Cameras | Red light camera intersection mapping with PostGIS polygons | Prompt 6, Sec 3 | `backend/compliance/models` | `tests/integration/test_geospatial.py` | COMPLETE | None |
| REQ-034 | Signals | Traffic signal timer prediction integration (if provider allows) | Prompt 7, Sec 1 | `backend/ingestion/signals` | `tests/unit/test_signals.py` | IN_PROGRESS | Data provider access |
| REQ-035 | Restrictions | Heavy vehicle temporary restriction (time-based) routing exclusion | Prompt 7, Sec 2 | `backend/routing/rules` | `tests/unit/test_temporal.py` | COMPLETE | None |
| REQ-036 | Restrictions | Two-wheeler restricted flyover logic (e.g. JJ Flyover) | Prompt 7, Sec 3 | `backend/routing/rules` | `tests/unit/test_compliance.py` | COMPLETE | None |
| REQ-037 | Copilot | Minimal UI rendering logic for low battery consumption | Prompt 8, Sec 1 | `apps/mobile/lib/copilot` | `tests/mobile/copilot_test.dart` | COMPLETE | None |
| REQ-038 | Copilot | Background service configuration (Foreground Service on Android) | Directive, Corr 17 | `apps/mobile/android` | N/A | IN_PROGRESS | None |
| REQ-039 | Copilot | Background location updates via `Location Always` on iOS | Directive, Corr 17 | `apps/mobile/ios` | N/A | IN_PROGRESS | Apple Approval |
| REQ-040 | Admin | Next.js Admin dashboard for data moderation and approval | Prompt 9, Sec 1 | `apps/web/admin` | `tests/e2e/admin.spec.ts` | IN_PROGRESS | None |
| REQ-041 | Admin | Map view with manual polygon editing for restricted zones | Prompt 9, Sec 2 | `apps/web/admin/map` | `tests/e2e/map.spec.ts` | IN_PROGRESS | None |
| REQ-042 | Admin | User management and ban/suspend capabilities | Prompt 9, Sec 3 | `apps/web/admin/users` | `tests/e2e/users.spec.ts` | COMPLETE | None |
| REQ-043 | Ingestion | OpenStreetMap data parser mapping OSM tags to DriveGuard schema | Prompt 10, Sec 1 | `backend/ingestion/osm` | `tests/unit/test_osm.py` | COMPLETE | None |
| REQ-044 | Ingestion | Source reliability scoring mechanism based on provider vs community | Prompt 10, Sec 2 | `backend/ai/scoring` | `tests/unit/test_scoring.py` | COMPLETE | None |
| REQ-045 | Testing | Pytest-asyncio usage for backend tests | Directive, Corr 4 | `tests/integration` | `tests/integration/conftest.py` | COMPLETE | None |
| REQ-046 | Testing | Mock provider responses for deterministic test executions | Prompt 11, Sec 1 | `tests/unit/mocks` | `tests/unit/test_routing.py` | COMPLETE | None |
| REQ-047 | DevOps | GitHub Actions CI workflow for Backend (Lint, Test, Docker Build) | Prompt 12, Sec 1 | `.github/workflows` | N/A | COMPLETE | None |
| REQ-048 | DevOps | GitHub Actions CI workflow for Flutter (Analyze, Test, Build) | Prompt 12, Sec 2 | `.github/workflows` | N/A | COMPLETE | None |
| REQ-049 | Release | Android Play Store deployment checklist automation | Directive, Corr 17 | `scripts/release` | N/A | IN_PROGRESS | None |
| REQ-050 | Release | Apple App Store Privacy Manifest generation | Directive, Corr 17 | `scripts/release` | N/A | COMPLETE | None |
| REQ-051 | Compliance Engine | Complex intersection modeling (multi-polygon union for detection) | Prompt 13, Sec 1 | `backend/compliance/intersections` | `tests/unit/test_intersections.py` | COMPLETE | None |
| REQ-052 | Architecture | Ensure No Secrets in Source Control (.env.example verification) | Core Guideline | `/` | N/A | COMPLETE | None |
| REQ-053 | Architecture | Use Type Hints everywhere in Python, Dart, TypeScript | Core Guideline | `backend/`, `apps/` | N/A | COMPLETE | None |
| REQ-054 | UI State | Handle Degraded/Error States gracefully (Offline, No GPS, API down) | Prompt 14, Sec 1 | `apps/mobile/lib/states` | `tests/mobile/state_test.dart` | IN_PROGRESS | None |
| REQ-055 | Security | Rate limit open API endpoints using Redis token bucket | Prompt 14, Sec 2 | `backend/api/middleware` | `tests/integration/test_rate_limit.py` | COMPLETE | None |
| REQ-056 | Routing | Provide up to 3 alternate routes from provider | Prompt 15, Sec 1 | `backend/routing/alternates` | `tests/unit/test_alternates.py` | COMPLETE | None |
| REQ-057 | Offline | Download regional SQLite DB of static cameras for offline copilot | Directive, Corr 21 | `apps/mobile/lib/offline` | `tests/mobile/offline_db_test.dart` | IN_PROGRESS | None |
| REQ-058 | Architecture | Ensure local time zone conversion (Asia/Kolkata) for temporal evaluation | Core Guideline | `backend/utils/timezone.py` | `tests/unit/test_timezone.py` | COMPLETE | None |
| REQ-059 | Compliance Engine | Correct calculation of multi-linestring length | Directive, Corr 4 | `backend/geospatial` | `tests/integration/test_geospatial.py` | COMPLETE | None |
| REQ-060 | AI | Traffic pattern prediction modeling (ETA adjustment) | Prompt 16, Sec 1 | `backend/ai/eta` | `tests/unit/test_eta.py` | IN_PROGRESS | None |
| REQ-061 | Ingestion | API polling for public transport API integration | Prompt 16, Sec 2 | `backend/ingestion/transit` | `tests/unit/test_transit.py` | IN_PROGRESS | None |
| REQ-062 | UI | Route Share / Deep-Link handling capability | Prompt 17, Sec 1 | `apps/mobile/lib/deeplink` | `tests/mobile/deeplink_test.dart` | IN_PROGRESS | Domain mapping |
| REQ-063 | Simulation | GPS spoofing simulator for test harness | Prompt 17, Sec 2 | `tests/simulation/gps_spoofer.py`| N/A | COMPLETE | None |
| REQ-064 | Admin | Data quality reporting metric dashboard | Prompt 18, Sec 1 | `apps/web/admin/quality` | `tests/e2e/quality.spec.ts` | IN_PROGRESS | None |
| REQ-065 | Routing | Penalize routes going through historical congestion zones | Prompt 18, Sec 2 | `backend/routing/penalties` | `tests/unit/test_penalties.py` | COMPLETE | None |
| REQ-066 | Architecture | Provider data architecturally separated from DriveGuard data | Core Guideline | `backend/models` | `tests/unit/test_models.py` | COMPLETE | None |
| REQ-067 | Mobile UI | Voice Engine integration for spoken alerts in Copilot mode | Prompt 19, Sec 1 | `apps/mobile/lib/voice` | `tests/mobile/voice_test.dart` | IN_PROGRESS | None |
| REQ-068 | Mobile UI | Dark Mode theme compliance across all 28 screens | Prompt 19, Sec 2 | `apps/mobile/lib/theme` | `tests/mobile/theme_test.dart` | COMPLETE | None |
| REQ-069 | Testing | Golden image testing for Flutter widgets | Prompt 20, Sec 1 | `tests/mobile/golden` | `tests/mobile/golden/widgets_test.dart` | IN_PROGRESS | None |
| REQ-070 | Backend | Fast API exception handler standardisation | Prompt 20, Sec 2 | `backend/api/exceptions.py`| `tests/unit/test_api_exceptions.py` | COMPLETE | None |
| REQ-071 | Backend | Logging middleware mapping Request ID | Prompt 21, Sec 1 | `backend/api/middleware` | `tests/unit/test_middleware.py`| COMPLETE | None |
| REQ-072 | DevOps | Docker multi-stage builds for backend minimizing image size | Prompt 21, Sec 2 | `infrastructure/docker` | N/A | COMPLETE | None |
| REQ-073 | Security | Token refresh logic via Firebase Auth client SDK | Prompt 22, Sec 1 | `apps/mobile/lib/auth` | `tests/mobile/auth_test.dart` | COMPLETE | None |
| REQ-074 | Security | Restrict API keys to specific origins/bundle IDs | Prompt 22, Sec 2 | `infrastructure/terraform` | N/A | COMPLETE | None |
| REQ-075 | Database | Indexing geometry columns with GIST | Prompt 23, Sec 1 | `backend/migrations/` | N/A | COMPLETE | None |
| REQ-076 | Web | Admin Role-Based Access Control (RBAC) | Prompt 23, Sec 2 | `apps/web/auth` | `tests/e2e/auth.spec.ts` | COMPLETE | None |
| REQ-077 | Ingestion | Webhook receivers for third-party traffic alerts | Prompt 24, Sec 1 | `backend/api/webhooks` | `tests/integration/test_webhooks.py`| IN_PROGRESS | None |
| REQ-078 | Database | Connection pooling sizing configuration | Prompt 24, Sec 2 | `infrastructure/terraform` | N/A | COMPLETE | None |
| REQ-079 | Mobile | Battery usage optimization (throttling GPS updates when idle) | Prompt 25, Sec 1 | `apps/mobile/lib/location` | `tests/mobile/location_test.dart` | IN_PROGRESS | None |
| REQ-080 | CI/CD | automated semantic versioning tagging based on conventional commits | Prompt 25, Sec 2 | `.github/workflows` | N/A | COMPLETE | None |
| REQ-081 | Mobile | Vehicle type toggle (2W vs 4W) affecting routing profile | Prompt 26, Sec 1 | `apps/mobile/lib/screens/home`| `tests/mobile/vehicle_toggle_test.dart`| IN_PROGRESS | None |
| REQ-082 | Testing | E2E integration testing suite with Playwright for Web | Prompt 26, Sec 2 | `tests/e2e` | `tests/e2e/admin.spec.ts` | IN_PROGRESS | None |
| REQ-083 | Mobile | Haptic feedback for major route events | Prompt 27, Sec 1 | `apps/mobile/lib/haptics` | N/A | COMPLETE | None |
| REQ-084 | Ingestion | Bulk CSV import capability for camera data | Prompt 27, Sec 2 | `backend/workers/import` | `tests/unit/test_csv_import.py` | COMPLETE | None |
| REQ-085 | API | Swagger UI documentation exposing v1 endpoints | Prompt 28, Sec 1 | `backend/api/main.py` | `tests/integration/test_api.py` | COMPLETE | None |
| REQ-086 | Ingestion | Deduplication logic for overlapping user reports | Prompt 28, Sec 2 | `backend/workers/dedup` | `tests/unit/test_dedup.py` | COMPLETE | None |
| REQ-087 | Mobile | Network retry interceptor for robust API connectivity | Prompt 29, Sec 1 | `apps/mobile/lib/network` | `tests/mobile/network_test.dart` | COMPLETE | None |
| REQ-088 | Analytics | Anonymized telemetry beaconing for route quality tracking | Prompt 29, Sec 2 | `backend/api/telemetry` | `tests/integration/test_telemetry.py` | IN_PROGRESS | None |
| REQ-089 | Security | OWASP dependency check integration in CI | Prompt 30, Sec 1 | `.github/workflows` | N/A | COMPLETE | None |
| REQ-090 | DevOps | Terraform state locking in S3/DynamoDB | Prompt 30, Sec 2 | `infrastructure/terraform` | N/A | COMPLETE | None |
| REQ-091 | Mobile | Splash screen implementation native per OS | Directive, Corr 17 | `apps/mobile/` | N/A | COMPLETE | None |
| REQ-092 | Web | Admin SSR implementation for faster load times | Prompt 31, Sec 1 | `apps/web/pages` | N/A | IN_PROGRESS | None |
| REQ-093 | Routing | Custom cost function evaluation engine for Valhalla | Directive, Corr 5 | `backend/routing/valhalla` | `tests/unit/test_valhalla.py` | IN_PROGRESS | None |
| REQ-094 | Admin | Audit logging for all moderator actions | Prompt 32, Sec 1 | `backend/api/audit` | `tests/unit/test_audit.py` | COMPLETE | None |
| REQ-095 | App Store | Provide justification for background location in review notes | Directive, Corr 17 | `docs/` | N/A | COMPLETE | None |
| REQ-096 | App Store | Handle CarPlay `BLOCKED_EXTERNAL` entitlement issue | Directive, Corr 17 | `docs/KNOWN_BLOCKERS.md` | N/A | BLOCKED_EXTERNAL| Apple approval pending |
| REQ-097 | Database | Synthetic data creation for test harnesses | Core Guideline | `data/synthetic` | N/A | COMPLETE | None |
| REQ-098 | Backend | Integration test suite using test-specific Docker containers | Prompt 33, Sec 1 | `tests/integration` | `tests/integration/conftest.py` | COMPLETE | None |
| REQ-099 | UI | Data coverage visualization maps in app | Prompt 33, Sec 2 | `apps/mobile/lib/coverage` | `tests/mobile/coverage_test.dart`| IN_PROGRESS | None |
| REQ-100 | Database | Explicitly use metric meters, not degrees, in geospatial ST_Distance | Directive, Corr 4 | `backend/geospatial` | `tests/integration/test_geospatial.py`| COMPLETE | None |
| REQ-101 | CI | End-to-end integration proving DB, API, and Mock Provider flow | Prompt 34, Sec 1 | `.github/workflows` | `tests/e2e/e2e_flow.py` | IN_PROGRESS | None |

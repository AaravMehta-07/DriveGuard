# ADR-004: Compliance-Aware Routing

**Status**: ACCEPTED

## Context
Need to validate and potentially reject provider-generated routes that contain prohibited maneuvers or violate local compliance rules (e.g., wrong-way driving on temporarily restricted roads, avoiding certain vehicle types).

## Decision
Implement a `ComplianceAwareRoutingCoordinator` that wraps the chosen provider's routing API.
The system will evaluate Valhalla / OSRM / GraphHopper as a DriveGuard-controlled fallback routing engine if the provider consistently fails compliance checks or if we need to generate fully custom compliant routes.

## Consequences
- Routing latency will increase due to validation step.
- We must maintain an up-to-date geospatial index of restrictions.

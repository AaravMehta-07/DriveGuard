# ADR-001: Navigation Provider Selection

**Status**: APPROVED

## Context
DriveGuard requires a navigation, geocoding, and routing provider optimized for Indian road networks, specifically Mumbai metro region. We evaluated Mappls (MapmyIndia), Google Maps Platform, and OpenStreetMap.

## Decision Criteria
1. Accuracy of Mumbai road network & flyover vs surface road topology
2. House/building level geocoding for Indian addresses
3. Compliance with Indian National Geospatial Policy (2022)
4. Commercial terms & overlay mixing permissions (DriveGuard camera layer over provider maps)
5. Offline navigation & tile caching support
6. Flutter SDK integration quality & platform capabilities (Android Auto / CarPlay)

## Decision
**Mappls (MapmyIndia)** is selected as the primary navigation and geocoding provider for DriveGuard in India.

### Key Factors for Mappls:
- **Geospatial Policy Compliance**: Full compliance with Ministry of Science and Technology guidelines for high-resolution mapping data in India.
- **Data Rights & Overlay**: Mappls licensing permits overlaying custom vector layers (DriveGuard verified speed camera markers, signal enforcement junctions, temporary turn restrictions).
- **India Address Geocoding**: Superior doorstep-level and pin-code-level geocoding accuracy in dense Mumbai corridors (BKC, Bandra West, South Mumbai).
- **Offline Capabilities**: Supports localized offline region packs (Mumbai Compliance Pack) for speed limits and restrictions.

### Hybrid Fallback:
OpenStreetMap (OSM) vector tiles serve as an open fallback for offline map rendering and basic route visualization when Mappls API credentials are unconfigured or offline.

## Consequences
- Production deployments must supply valid `MAPPLS_API_KEY`, `MAPPLS_CLIENT_ID`, and `MAPPLS_CLIENT_SECRET`.
- In the absence of credentials, the system returns `BLOCKED_EXTERNAL_CREDENTIAL` rather than serving fake or fabricated routes.

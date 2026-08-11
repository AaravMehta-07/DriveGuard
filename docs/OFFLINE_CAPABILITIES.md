# Offline Capabilities

## Truthful Capability Matrix
| Feature | Type | Status/Implementation |
|---|---|---|
| **Offline Compliance Data** | DriveGuard-owned | Cacheable SQLite database synced periodically. |
| **Offline Map Tiles** | Provider-dependent | Depends on Mappls/Google SDK caching limits. |
| **Offline Search** | Provider-dependent | Usually unavailable or highly restricted. |
| **Offline Routing** | Provider-dependent | Varies; Google supports pre-downloaded areas. |
| **Offline Navigation** | Provider-dependent | GPS-only matching, often lacks rerouting. |

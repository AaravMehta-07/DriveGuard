from typing import Any, Dict

class ComplianceEngine:
    async def analyze_route(self, route_wkt: str, vehicle_type: str) -> Dict[str, Any]:
        # Implement logic to analyze compliance for route
        return {}

class GeospatialQueryService:
    async def query_route_features(self, route_wkt: str) -> Dict[str, Any]:
        # Query features overlapping route
        return {}

class RouteComplianceScan:
    def __init__(
        self,
        speed_cameras: int,
        signal_enforcement: int,
        restricted_movements: int,
        speed_changes: int,
        closures: int,
        coverage_percentage: float
    ):
        self.speed_cameras = speed_cameras
        self.signal_enforcement = signal_enforcement
        self.restricted_movements = restricted_movements
        self.speed_changes = speed_changes
        self.closures = closures
        self.coverage_percentage = coverage_percentage

class RouteScanner:
    def __init__(self, compliance_engine: ComplianceEngine, geo_query_service: GeospatialQueryService):
        self.compliance_engine = compliance_engine
        self.geo_query_service = geo_query_service

    async def scan_route(self, route_wkt: str, vehicle_type: str) -> RouteComplianceScan:
        """
        Scan a route and return compliance metrics based on actual database values.
        Wraps ComplianceEngine + GeospatialQueryService.
        """
        features = await self.geo_query_service.query_route_features(route_wkt)
        compliance = await self.compliance_engine.analyze_route(route_wkt, vehicle_type)

        speed_cameras = features.get("speed_cameras", 0)
        signal_enforcement = features.get("signal_enforcement", 0)
        restricted_movements = compliance.get("restricted_movements", 0)
        speed_changes = features.get("speed_changes", 0)
        closures = compliance.get("closures", 0)
        coverage_percentage = features.get("coverage_percentage", 0.0)

        return RouteComplianceScan(
            speed_cameras=speed_cameras,
            signal_enforcement=signal_enforcement,
            restricted_movements=restricted_movements,
            speed_changes=speed_changes,
            closures=closures,
            coverage_percentage=coverage_percentage,
        )

from datetime import datetime
from typing import Any, Dict, List

from .engine import ComplianceEngine


class RouteCandidate:
    def __init__(self, id: str, geometry_wkt: str, maneuvers: List[Dict[str, Any]]):
        self.id = id
        self.geometry_wkt = geometry_wkt
        self.maneuvers = maneuvers
        self.status = "UNCERTAIN"
        self.score = 0.0
        self.explanation = ""

class ComplianceAwareRoutingCoordinator:
    def __init__(self, compliance_engine: ComplianceEngine):
        self.engine = compliance_engine

    async def evaluate_routes(
        self, candidates: List[RouteCandidate], vehicle_type: str, current_datetime: datetime
    ) -> List[RouteCandidate]:
        for route in candidates:
            route_valid = True

            # Scan route
            scan = await self.engine.scan_route(route.geometry_wkt, vehicle_type, current_datetime)

            # Validate every maneuver
            for maneuver in route.maneuvers:
                result = await self.engine.validate_maneuver(
                    maneuver.get("junction_id", ""),
                    maneuver.get("from_segment_id", ""),
                    maneuver.get("to_segment_id", ""),
                    vehicle_type,
                    current_datetime
                )

                if result.status == "PROHIBITED":
                    route_valid = False
                    route.status = "PROHIBITED"
                    route.explanation = f"Prohibited maneuver: {result.reason}"
                    break

            if route_valid:
                route.status = "COMPLIANT"
                route.score = scan.confidence

        return candidates

    async def get_best_route(
        self, candidates: List[RouteCandidate], vehicle_type: str, current_datetime: datetime
    ) -> RouteCandidate:
        evaluated = await self.evaluate_routes(candidates, vehicle_type, current_datetime)

        compliant = [r for r in evaluated if r.status == "COMPLIANT"]
        if compliant:
            return sorted(compliant, key=lambda x: x.score, reverse=True)[0]

        uncertain = [r for r in evaluated if r.status == "UNCERTAIN"]
        if uncertain:
            return sorted(uncertain, key=lambda x: x.score, reverse=True)[0]

        # All PROHIBITED
        return evaluated[0] if evaluated else None

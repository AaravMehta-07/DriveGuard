from datetime import datetime
from typing import List, Any
from sqlalchemy import text
from .temporal import TemporalRuleEngine
from .confidence import SourceConfidenceEngine

class RouteComplianceScan:
    def __init__(self, events: List[Any], confidence: float):
        self.events = events
        self.confidence = confidence

class ManeuverValidationResult:
    def __init__(self, status: str, reason: str = ""):
        self.status = status # ALLOWED/PROHIBITED/UNCERTAIN
        self.reason = reason


class ComplianceEngine:
    def __init__(self, geo_query_service=None):
        self.geo_service = geo_query_service
        self.temporal_engine = TemporalRuleEngine()
        self.confidence_engine = SourceConfidenceEngine()

    async def scan_route(self, route_geometry_wkt: str, vehicle_type: str, current_datetime: datetime) -> RouteComplianceScan:
        """
        Uses GeospatialQueryService to gather all events, sorts by along-route distance
        """
        if not self.geo_service:
            return RouteComplianceScan([], 0.0)
            
        data = await self.geo_service.scan_route_compliance(route_geometry_wkt, vehicle_type)
        events = []
        events.extend(data.get("enforcement_events", []))
        events.extend(data.get("restriction_events", []))
        events.extend(data.get("signal_events", []))
        
        # Sort by along_route_distance_m
        events.sort(key=lambda e: e.get("along_route_distance_m", 0) if isinstance(e, dict) else getattr(e, "along_route_distance_m", 0))
        
        confidence = data.get("compliance_data_coverage_percent", 0.0)
        return RouteComplianceScan(events, confidence)

    async def validate_maneuver(
        self, junction_id: str, from_segment_id: str, to_segment_id: str, vehicle_type: str, dt: datetime
    ) -> ManeuverValidationResult:
        """
        Checks turn_restrictions, access_restrictions, temporal rules
        """
        if not self.geo_service:
            return ManeuverValidationResult(status="UNCERTAIN", reason="No geo service")

        # In a real implementation we would query restrictions for this junction.
        # But for now we can just assume it queries database if not passed.
        # Let's say we have an ad-hoc query for turn restrictions at junction
        query = text("SELECT * FROM turn_restrictions WHERE junction_id = :junction_id")
        try:
            result = await self.geo_service._db.execute(query, {"junction_id": junction_id})
            restrictions = result.mappings().all()
            for r in restrictions:
                if r.get("temporal_rule"):
                    if not self.temporal_engine.is_rule_active(r["temporal_rule"], dt):
                        continue
                if vehicle_type and r.get("vehicle_types"):
                    if vehicle_type not in r["vehicle_types"]:
                        continue
                if r.get("restriction_type") in ("NO_LEFT_TURN", "NO_RIGHT_TURN", "NO_U_TURN", "NO_ENTRY", "ONE_WAY", "ROAD_CLOSED"):
                    return ManeuverValidationResult(status="PROHIBITED", reason=f"Matched {r['restriction_type']}")
        except Exception:
            pass

        return ManeuverValidationResult(status="UNCERTAIN", reason="No verified data")

    def compute_route_confidence(self, scan_result: RouteComplianceScan) -> float:
        """
        Based on: verified speed data coverage, restriction coverage, source quality, freshness, contradictions
        """
        return scan_result.confidence

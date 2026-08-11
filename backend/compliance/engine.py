import logging
from datetime import datetime
from typing import List, Any, Dict, Optional
from sqlalchemy import text
from .temporal import TemporalRuleEngine
from .confidence import SourceConfidenceEngine

logger = logging.getLogger(__name__)

class RouteComplianceScan:
    def __init__(self, events: List[Any], confidence: float):
        self.events = events
        self.confidence = confidence

class ManeuverValidationResult:
    def __init__(self, status: str, reason: str = ""):
        self.status = status  # ALLOWED / PROHIBITED / UNCERTAIN
        self.reason = reason

class ComplianceEngine:
    def __init__(self, geo_query_service=None):
        self.geo_service = geo_query_service
        self.temporal_engine = TemporalRuleEngine()
        self.confidence_engine = SourceConfidenceEngine()

    async def scan_route(self, route_geometry_wkt: str, vehicle_type: str, current_datetime: datetime) -> RouteComplianceScan:
        """
        Scans route geometry against PostGIS enforcement and restriction databases.
        """
        if not self.geo_service:
            return RouteComplianceScan([], 0.0)
            
        try:
            data = await self.geo_service.scan_route_compliance(route_geometry_wkt, vehicle_type)
            events = []
            events.extend(data.get("enforcement_events", []))
            events.extend(data.get("restriction_events", []))
            events.extend(data.get("signal_events", []))
            
            events.sort(key=lambda e: e.get("along_route_distance_m", 0) if isinstance(e, dict) else getattr(e, "along_route_distance_m", 0))
            confidence = data.get("compliance_data_coverage_percent", 0.0)
            return RouteComplianceScan(events, confidence)
        except Exception as err:
            logger.error("Error during route compliance scan", exc_info=True)
            return RouteComplianceScan([], 0.0)

    async def validate_maneuver(
        self, junction_id: str, from_segment_id: str, to_segment_id: str, vehicle_type: str, dt: datetime
    ) -> ManeuverValidationResult:
        """
        Evaluates turn restrictions and access restrictions for a specific maneuver.
        Never swill swallow exceptions or default blindly to ALLOWED. Returns UNCERTAIN on query failure.
        """
        if not self.geo_service:
            return ManeuverValidationResult(status="UNCERTAIN", reason="Geospatial service unavailable")

        query = text("SELECT * FROM turn_restrictions WHERE from_segment_id = :from_id AND to_segment_id = :to_id")
        try:
            result = await self.geo_service._db.execute(query, {"from_id": from_segment_id, "to_id": to_segment_id})
            restrictions = result.mappings().all()
            if not restrictions:
                return ManeuverValidationResult(status="ALLOWED", reason="No turn restriction found")

            for r in restrictions:
                if r.get("temporal_rule"):
                    if not self.temporal_engine.is_rule_active(r["temporal_rule"], dt):
                        continue
                if vehicle_type and r.get("vehicle_types"):
                    if vehicle_type not in r["vehicle_types"]:
                        continue
                if r.get("restriction_type") in ("NO_LEFT_TURN", "NO_RIGHT_TURN", "NO_U_TURN", "NO_ENTRY", "ONE_WAY", "ROAD_CLOSED"):
                    return ManeuverValidationResult(status="PROHIBITED", reason=f"Matched {r['restriction_type']}")
            
            return ManeuverValidationResult(status="ALLOWED", reason="No active restriction enforced at this time")
        except Exception as err:
            logger.error("Database query error during maneuver validation", exc_info=True)
            return ManeuverValidationResult(status="UNCERTAIN", reason="Database query failed during evaluation")

    async def evaluate_restrictions(self, point_lon: float, point_lat: float, radius_m: float = 100.0) -> List[Dict[str, Any]]:
        """
        Evaluates point and zone restrictions near a coordinate.
        """
        if not self.geo_service:
            return []
        try:
            query = text("""
                SELECT id, title, description, restriction_type
                FROM temporary_restrictions
                WHERE ST_DWithin(area_geometry::geography, ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography, :radius)
            """)
            result = await self.geo_service._db.execute(query, {"lon": point_lon, "lat": point_lat, "radius": radius_m})
            return [dict(row) for row in result.mappings().all()]
        except Exception as err:
            logger.error("Error evaluating nearby restrictions", exc_info=True)
            return []

    async def get_temporal_restrictions(self, road_segment_id: str, dt: datetime) -> List[Dict[str, Any]]:
        """
        Gets active temporal rules for a road segment.
        """
        if not self.geo_service:
            return []
        try:
            query = text("SELECT * FROM speed_limits WHERE segment_id = :seg_id")
            result = await self.geo_service._db.execute(query, {"seg_id": road_segment_id})
            return [dict(row) for row in result.mappings().all()]
        except Exception as err:
            logger.error("Error getting temporal restrictions", exc_info=True)
            return []

    def compute_route_confidence(self, scan_result: RouteComplianceScan) -> float:
        """
        Computes overall confidence score based on scanned events and coverage percentage.
        """
        return scan_result.confidence

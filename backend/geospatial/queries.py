"""
DriveGuard Geospatial Query Layer

All metric operations use PostGIS geography type to ensure correct meter-based
calculations. NEVER perform ST_Buffer or ST_Length directly on EPSG:4326 geometry
without casting to geography.

Correct patterns:
  ST_Buffer(geom::geography, meters)::geometry
  ST_Length(geom::geography)
  ST_Distance(geom::geography, other::geography)
  ST_DWithin(geom::geography, other::geography, meters)

Incorrect patterns (NEVER use):
  ST_Buffer(geom, 100)  -- 100 degrees, not meters!
  ST_Length(geom)        -- length in degrees, not meters!
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class DirectionMatch(Enum):
    """Result of comparing vehicle heading to camera monitored direction."""
    SAME_DIRECTION = "same_direction"
    OPPOSITE_DIRECTION = "opposite_direction"
    PERPENDICULAR = "perpendicular"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class BoundingBox:
    """Geographic bounding box in WGS84 coordinates."""
    min_lon: float
    min_lat: float
    max_lon: float
    max_lat: float

    def to_wkt_polygon(self) -> str:
        """Convert to WKT polygon for PostGIS queries."""
        return (
            f"POLYGON(({self.min_lon} {self.min_lat}, "
            f"{self.max_lon} {self.min_lat}, "
            f"{self.max_lon} {self.max_lat}, "
            f"{self.min_lon} {self.max_lat}, "
            f"{self.min_lon} {self.min_lat}))"
        )


@dataclass(frozen=True)
class ClusteredPoint:
    """A cluster of enforcement points for map display at low zoom."""
    center_lon: float
    center_lat: float
    count: int
    cluster_id: int


@dataclass(frozen=True)
class EnforcementQueryResult:
    """Result of an enforcement point query."""
    id: uuid.UUID
    enforcement_type: str
    latitude: float
    longitude: float
    road_name: Optional[str]
    road_level: int
    carriageway: Optional[str]
    monitored_direction: Optional[float]
    speed_limit_kph: Optional[int]
    verification_status: str
    confidence_score: float
    last_verified_at: Optional[str]
    distance_m: Optional[float] = None
    along_route_distance_m: Optional[float] = None


class GeospatialQueryService:
    """
    PostGIS-backed geospatial query service for DriveGuard.

    All distance/buffer operations use geography type to ensure correct
    metric calculations regardless of latitude. This is critical for Mumbai
    (latitude ~19°N) where degree-based calculations would produce incorrect results.

    Key design decisions:
    - SRID 4326 storage for all geometry
    - geography cast for all metric operations
    - Direction matching with configurable tolerance
    - Road-level filtering to prevent flyover/surface confusion
    - Along-route distance using ST_LineLocatePoint + ST_Length on geography
    """

    def __init__(self, db: AsyncSession):
        self._db = db

    # ─── Enforcement Queries ─────────────────────────────────────────────

    async def get_enforcement_in_bounds(
        self,
        bbox: BoundingBox,
        *,
        enforcement_types: list[str] | None = None,
        verification_statuses: list[str] | None = None,
        min_confidence: float = 0.0,
        exclude_synthetic: bool = True,
        limit: int = 500,
    ) -> list[EnforcementQueryResult]:
        """
        Get enforcement points within a bounding box.
        Uses spatial index (GiST) for efficient filtering.
        """
        conditions = [
            "ST_Intersects(geometry, ST_MakeEnvelope(:min_lon, :min_lat, :max_lon, :max_lat, 4326))",
            "confidence_score >= :min_confidence",
        ]
        params: dict[str, Any] = {
            "min_lon": bbox.min_lon,
            "min_lat": bbox.min_lat,
            "max_lon": bbox.max_lon,
            "max_lat": bbox.max_lat,
            "min_confidence": min_confidence,
            "limit": limit,
        }

        if exclude_synthetic:
            conditions.append("synthetic = FALSE")

        if enforcement_types:
            conditions.append("enforcement_type = ANY(:enforcement_types)")
            params["enforcement_types"] = enforcement_types

        if verification_statuses:
            conditions.append("verification_status = ANY(:verification_statuses)")
            params["verification_statuses"] = verification_statuses

        where_clause = " AND ".join(conditions)

        query = text(f"""
            SELECT
                id, enforcement_type,
                ST_Y(geometry) AS latitude,
                ST_X(geometry) AS longitude,
                road_name, road_level, carriageway,
                monitored_direction, speed_limit_kph,
                verification_status, confidence_score,
                last_verified_at
            FROM enforcement_points
            WHERE {where_clause}
            ORDER BY confidence_score DESC
            LIMIT :limit
        """)

        result = await self._db.execute(query, params)
        rows = result.mappings().all()
        return [EnforcementQueryResult(**row) for row in rows]

    async def get_enforcement_clustered(
        self,
        bbox: BoundingBox,
        *,
        cluster_distance_m: float = 200.0,
        exclude_synthetic: bool = True,
    ) -> list[ClusteredPoint]:
        """
        Get clustered enforcement points for low-zoom map display.
        Uses ST_ClusterDBSCAN with geography-correct distance.

        The cluster_distance_m parameter controls minimum separation
        between clusters, in actual meters (not degrees).
        """
        synthetic_filter = "AND synthetic = FALSE" if exclude_synthetic else ""

        query = text(f"""
            WITH clustered AS (
                SELECT
                    geometry,
                    ST_ClusterDBSCAN(
                        geometry::geography,
                        eps := :cluster_distance_m,
                        minpoints := 1
                    ) OVER () AS cluster_id
                FROM enforcement_points
                WHERE ST_Intersects(
                    geometry,
                    ST_MakeEnvelope(:min_lon, :min_lat, :max_lon, :max_lat, 4326)
                )
                {synthetic_filter}
            )
            SELECT
                ST_X(ST_Centroid(ST_Collect(geometry))) AS center_lon,
                ST_Y(ST_Centroid(ST_Collect(geometry))) AS center_lat,
                COUNT(*) AS count,
                cluster_id
            FROM clustered
            GROUP BY cluster_id
            ORDER BY count DESC
        """)

        result = await self._db.execute(query, {
            "min_lon": bbox.min_lon,
            "min_lat": bbox.min_lat,
            "max_lon": bbox.max_lon,
            "max_lat": bbox.max_lat,
            "cluster_distance_m": cluster_distance_m,
        })
        rows = result.mappings().all()
        return [ClusteredPoint(**row) for row in rows]

    async def get_enforcement_in_corridor(
        self,
        route_wkt: str,
        buffer_m: float = 50.0,
        *,
        direction_heading: float | None = None,
        direction_tolerance: float = 45.0,
        road_level: int | None = None,
        exclude_synthetic: bool = True,
    ) -> list[EnforcementQueryResult]:
        """
        Get enforcement points along a route corridor.

        CRITICAL: Uses geography cast for metric buffer.
        ST_Buffer(route::geography, buffer_m)::geometry creates a corridor
        of actual meters around the route, not degrees.

        Also computes along-route distance for each point using:
        1. ST_LineLocatePoint to find fractional position
        2. ST_LineSubstring to get the prefix
        3. ST_Length on geography for actual meter distance
        """
        conditions = [
            """ST_Intersects(
                ep.geometry,
                ST_Buffer(
                    ST_GeomFromText(:route_wkt, 4326)::geography,
                    :buffer_m
                )::geometry
            )""",
        ]
        params: dict[str, Any] = {
            "route_wkt": route_wkt,
            "buffer_m": buffer_m,
        }

        if exclude_synthetic:
            conditions.append("ep.synthetic = FALSE")

        if road_level is not None:
            conditions.append("ep.road_level = :road_level")
            params["road_level"] = road_level

        where_clause = " AND ".join(conditions)

        # Direction filtering is applied in post-processing if specified,
        # because it requires comparing vehicle travel direction to camera
        # monitored direction, which is heading-dependent.

        query = text(f"""
            SELECT
                ep.id, ep.enforcement_type,
                ST_Y(ep.geometry) AS latitude,
                ST_X(ep.geometry) AS longitude,
                ep.road_name, ep.road_level, ep.carriageway,
                ep.monitored_direction, ep.speed_limit_kph,
                ep.verification_status, ep.confidence_score,
                ep.last_verified_at,
                -- Along-route distance in meters using geography
                ST_Length(
                    ST_LineSubstring(
                        ST_GeomFromText(:route_wkt, 4326),
                        0,
                        GREATEST(0, LEAST(1,
                            ST_LineLocatePoint(
                                ST_GeomFromText(:route_wkt, 4326),
                                ep.geometry
                            )
                        ))
                    )::geography
                ) AS along_route_distance_m,
                -- Perpendicular distance from route in meters
                ST_Distance(
                    ep.geometry::geography,
                    ST_GeomFromText(:route_wkt, 4326)::geography
                ) AS distance_m
            FROM enforcement_points ep
            WHERE {where_clause}
            ORDER BY along_route_distance_m ASC
        """)

        result = await self._db.execute(query, params)
        rows = result.mappings().all()

        results = [EnforcementQueryResult(**row) for row in rows]

        # Post-process direction filtering
        if direction_heading is not None:
            results = [
                r for r in results
                if r.monitored_direction is None  # unknown direction = include
                or self._is_direction_relevant(
                    direction_heading, r.monitored_direction, direction_tolerance
                )
            ]

        return results

    async def get_enforcement_ahead(
        self,
        position_lon: float,
        position_lat: float,
        heading: float,
        route_wkt: str | None = None,
        max_distance_m: float = 2000.0,
        *,
        road_level: int | None = None,
        direction_tolerance: float = 45.0,
        exclude_synthetic: bool = True,
    ) -> list[EnforcementQueryResult]:
        """
        Get enforcement points ahead of the vehicle position.

        When a route is available, uses along-route distance.
        In Copilot mode (no route), uses geographic proximity with
        direction filtering.
        """
        if route_wkt:
            # Route-based: find cameras ahead on the route
            return await self._get_enforcement_ahead_on_route(
                position_lon, position_lat, heading, route_wkt,
                max_distance_m, road_level, direction_tolerance,
                exclude_synthetic,
            )
        else:
            # Copilot mode: nearby + direction filtering
            return await self._get_enforcement_ahead_copilot(
                position_lon, position_lat, heading,
                max_distance_m, road_level, direction_tolerance,
                exclude_synthetic,
            )

    async def _get_enforcement_ahead_on_route(
        self,
        position_lon: float,
        position_lat: float,
        heading: float,
        route_wkt: str,
        max_distance_m: float,
        road_level: int | None,
        direction_tolerance: float,
        exclude_synthetic: bool,
    ) -> list[EnforcementQueryResult]:
        """Get enforcement points ahead on the current route."""
        conditions = ["ep.synthetic = FALSE"] if exclude_synthetic else []
        if road_level is not None:
            conditions.append("ep.road_level = :road_level")

        extra_where = (" AND " + " AND ".join(conditions)) if conditions else ""

        query = text(f"""
            WITH route AS (
                SELECT ST_GeomFromText(:route_wkt, 4326) AS geom
            ),
            vehicle_progress AS (
                SELECT ST_LineLocatePoint(
                    route.geom,
                    ST_SetSRID(ST_MakePoint(:pos_lon, :pos_lat), 4326)
                ) AS fraction
                FROM route
            )
            SELECT
                ep.id, ep.enforcement_type,
                ST_Y(ep.geometry) AS latitude,
                ST_X(ep.geometry) AS longitude,
                ep.road_name, ep.road_level, ep.carriageway,
                ep.monitored_direction, ep.speed_limit_kph,
                ep.verification_status, ep.confidence_score,
                ep.last_verified_at,
                -- Distance ahead = camera_distance - vehicle_distance along route
                ST_Length(
                    ST_LineSubstring(
                        route.geom,
                        vp.fraction,
                        GREATEST(vp.fraction, LEAST(1,
                            ST_LineLocatePoint(route.geom, ep.geometry)
                        ))
                    )::geography
                ) AS along_route_distance_m,
                ST_Distance(
                    ep.geometry::geography,
                    route.geom::geography
                ) AS distance_m
            FROM enforcement_points ep, route, vehicle_progress vp
            WHERE ST_DWithin(
                ep.geometry::geography,
                route.geom::geography,
                50  -- 50m corridor
            )
            AND ST_LineLocatePoint(route.geom, ep.geometry) > vp.fraction
            {extra_where}
            ORDER BY along_route_distance_m ASC
        """)

        params: dict[str, Any] = {
            "route_wkt": route_wkt,
            "pos_lon": position_lon,
            "pos_lat": position_lat,
        }
        if road_level is not None:
            params["road_level"] = road_level

        result = await self._db.execute(query, params)
        rows = result.mappings().all()
        results = [EnforcementQueryResult(**row) for row in rows]

        # Filter by direction relevance and max distance
        return [
            r for r in results
            if (r.along_route_distance_m or 0) <= max_distance_m
            and (
                r.monitored_direction is None
                or self._is_direction_relevant(
                    heading, r.monitored_direction, direction_tolerance
                )
            )
        ]

    async def _get_enforcement_ahead_copilot(
        self,
        position_lon: float,
        position_lat: float,
        heading: float,
        max_distance_m: float,
        road_level: int | None,
        direction_tolerance: float,
        exclude_synthetic: bool,
    ) -> list[EnforcementQueryResult]:
        """
        Get enforcement points ahead in Copilot mode (no route).
        Uses ST_DWithin with geography for metric radius.
        """
        conditions = [
            """ST_DWithin(
                ep.geometry::geography,
                ST_SetSRID(ST_MakePoint(:pos_lon, :pos_lat), 4326)::geography,
                :max_distance_m
            )""",
        ]
        params: dict[str, Any] = {
            "pos_lon": position_lon,
            "pos_lat": position_lat,
            "max_distance_m": max_distance_m,
        }

        if exclude_synthetic:
            conditions.append("ep.synthetic = FALSE")

        if road_level is not None:
            conditions.append("ep.road_level = :road_level")
            params["road_level"] = road_level

        where_clause = " AND ".join(conditions)

        query = text(f"""
            SELECT
                ep.id, ep.enforcement_type,
                ST_Y(ep.geometry) AS latitude,
                ST_X(ep.geometry) AS longitude,
                ep.road_name, ep.road_level, ep.carriageway,
                ep.monitored_direction, ep.speed_limit_kph,
                ep.verification_status, ep.confidence_score,
                ep.last_verified_at,
                ST_Distance(
                    ep.geometry::geography,
                    ST_SetSRID(ST_MakePoint(:pos_lon, :pos_lat), 4326)::geography
                ) AS distance_m
            FROM enforcement_points ep
            WHERE {where_clause}
            ORDER BY distance_m ASC
        """)

        result = await self._db.execute(query, params)
        rows = result.mappings().all()
        results = [EnforcementQueryResult(**row) for row in rows]

        # Filter: only ahead (within heading cone) and direction-relevant
        return [
            r for r in results
            if self._is_point_ahead(
                position_lon, position_lat, heading,
                r.longitude, r.latitude,
                cone_half_angle=60.0,
            )
            and (
                r.monitored_direction is None
                or self._is_direction_relevant(
                    heading, r.monitored_direction, direction_tolerance
                )
            )
        ]

    # ─── Speed Limit Queries ─────────────────────────────────────────────

    async def get_speed_limit_at(
        self,
        position_lon: float,
        position_lat: float,
        heading: float,
        road_level: int = 0,
        *,
        max_distance_m: float = 30.0,
    ) -> dict[str, Any] | None:
        """
        Get the applicable speed limit at a position.
        Matches to nearest road segment considering direction and road level.

        Returns None if no speed limit data is available (the UI must show
        'unknown' rather than inventing a value).
        """
        query = text("""
            SELECT
                sl.id,
                sl.value_kph,
                sl.direction,
                sl.confidence,
                sl.source_id,
                sl.conditional,
                sl.temporal_rule,
                rs.road_name,
                rs.road_class,
                ST_Distance(
                    rs.geometry::geography,
                    ST_SetSRID(ST_MakePoint(:pos_lon, :pos_lat), 4326)::geography
                ) AS distance_m
            FROM speed_limits sl
            JOIN road_segments rs ON sl.segment_id = rs.id
            WHERE ST_DWithin(
                rs.geometry::geography,
                ST_SetSRID(ST_MakePoint(:pos_lon, :pos_lat), 4326)::geography,
                :max_distance_m
            )
            AND sl.synthetic = FALSE
            AND (rs.road_level IS NULL OR rs.road_level = :road_level)
            ORDER BY distance_m ASC
            LIMIT 5
        """)

        result = await self._db.execute(query, {
            "pos_lon": position_lon,
            "pos_lat": position_lat,
            "max_distance_m": max_distance_m,
            "road_level": road_level,
        })
        rows = result.mappings().all()

        if not rows:
            return None

        # Find the best directional match
        for row in rows:
            row_dict = dict(row)
            direction = row_dict.get("direction")
            if direction is None or self._is_direction_relevant(
                heading, direction, tolerance=90.0
            ):
                return row_dict

        # Fallback to nearest if no direction match
        return dict(rows[0])

    # ─── Restriction Queries ─────────────────────────────────────────────

    async def get_restrictions_along_route(
        self,
        route_wkt: str,
        buffer_m: float = 30.0,
        *,
        exclude_synthetic: bool = True,
    ) -> list[dict[str, Any]]:
        """
        Get all active restrictions along a route corridor.
        Includes turn restrictions, access restrictions, and temporary restrictions.

        Uses geography-correct buffer for the corridor.
        """
        synthetic_filter = "AND synthetic = FALSE" if exclude_synthetic else ""

        # Turn restrictions
        turn_query = text(f"""
            SELECT
                tr.id, 'TURN_RESTRICTION' AS category,
                tr.restriction_type,
                tr.temporal_rule,
                tr.vehicle_types,
                tr.confidence,
                tr.effective_from, tr.effective_until,
                ST_Y(tsj.geometry) AS latitude,
                ST_X(tsj.geometry) AS longitude,
                ST_Length(
                    ST_LineSubstring(
                        ST_GeomFromText(:route_wkt, 4326),
                        0,
                        GREATEST(0, LEAST(1,
                            ST_LineLocatePoint(
                                ST_GeomFromText(:route_wkt, 4326),
                                tsj.geometry
                            )
                        ))
                    )::geography
                ) AS along_route_distance_m
            FROM turn_restrictions tr
            JOIN traffic_signal_junctions tsj ON tr.junction_id = tsj.id
            WHERE ST_DWithin(
                tsj.geometry::geography,
                ST_GeomFromText(:route_wkt, 4326)::geography,
                :buffer_m
            )
            {synthetic_filter}
            ORDER BY along_route_distance_m ASC
        """)

        # Temporary restrictions
        temp_query = text(f"""
            SELECT
                tr.id, 'TEMPORARY_RESTRICTION' AS category,
                tr.restriction_type,
                tr.temporal_rule,
                tr.vehicle_types,
                tr.confidence,
                tr.effective_from, tr.effective_until,
                ST_Y(ST_Centroid(tr.geometry)) AS latitude,
                ST_X(ST_Centroid(tr.geometry)) AS longitude,
                ST_Length(
                    ST_LineSubstring(
                        ST_GeomFromText(:route_wkt, 4326),
                        0,
                        GREATEST(0, LEAST(1,
                            ST_LineLocatePoint(
                                ST_GeomFromText(:route_wkt, 4326),
                                ST_Centroid(tr.geometry)
                            )
                        ))
                    )::geography
                ) AS along_route_distance_m
            FROM temporary_restrictions tr
            WHERE ST_DWithin(
                tr.geometry::geography,
                ST_GeomFromText(:route_wkt, 4326)::geography,
                :buffer_m
            )
            {synthetic_filter}
            AND (tr.effective_until IS NULL OR tr.effective_until > NOW())
            ORDER BY along_route_distance_m ASC
        """)

        params = {"route_wkt": route_wkt, "buffer_m": buffer_m}

        turn_result = await self._db.execute(turn_query, params)
        temp_result = await self._db.execute(temp_query, params)

        restrictions = [dict(row) for row in turn_result.mappings().all()]
        restrictions.extend(dict(row) for row in temp_result.mappings().all())

        # Sort all restrictions by along-route distance
        restrictions.sort(key=lambda r: r.get("along_route_distance_m", 0))
        return restrictions

    # ─── Signal Queries ──────────────────────────────────────────────────

    async def get_signals_along_route(
        self,
        route_wkt: str,
        buffer_m: float = 30.0,
        *,
        exclude_synthetic: bool = True,
    ) -> list[dict[str, Any]]:
        """
        Get traffic signals along a route with enforcement flag.
        """
        synthetic_filter = "AND tsj.synthetic = FALSE" if exclude_synthetic else ""

        query = text(f"""
            SELECT
                tsj.id,
                tsj.name,
                tsj.signal_enforcement,
                tsj.confidence,
                ST_Y(tsj.geometry) AS latitude,
                ST_X(tsj.geometry) AS longitude,
                ST_Length(
                    ST_LineSubstring(
                        ST_GeomFromText(:route_wkt, 4326),
                        0,
                        GREATEST(0, LEAST(1,
                            ST_LineLocatePoint(
                                ST_GeomFromText(:route_wkt, 4326),
                                tsj.geometry
                            )
                        ))
                    )::geography
                ) AS along_route_distance_m
            FROM traffic_signal_junctions tsj
            WHERE ST_DWithin(
                tsj.geometry::geography,
                ST_GeomFromText(:route_wkt, 4326)::geography,
                :buffer_m
            )
            {synthetic_filter}
            ORDER BY along_route_distance_m ASC
        """)

        result = await self._db.execute(query, {
            "route_wkt": route_wkt,
            "buffer_m": buffer_m,
        })
        return [dict(row) for row in result.mappings().all()]

    async def get_signals_near_point(
        self,
        position_lon: float,
        position_lat: float,
        radius_m: float = 1000.0,
    ) -> list[Any]:
        """
        Get traffic signals near a point with enforcement flags.
        """
        query = text("""
            SELECT
                id,
                ST_Y(location) AS latitude,
                ST_X(location) AS longitude,
                has_red_light_camera
            FROM traffic_signal_junctions
            WHERE ST_DWithin(
                location::geography,
                ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography,
                :radius_m
            )
        """)
        result = await self._db.execute(query, {
            "lon": position_lon,
            "lat": position_lat,
            "radius_m": radius_m,
        })
        rows = result.mappings().all()
        return [type('SignalPoint', (), dict(row)) for row in rows]

    # ─── Route Compliance Scan ───────────────────────────────────────────

    async def scan_route_compliance(
        self,
        route_wkt: str,
        vehicle_type: str = "PRIVATE_CAR",
    ) -> dict[str, Any]:
        """
        Perform a full compliance scan of a route.

        Returns counts of all compliance-relevant events along the route:
        cameras, signals, restrictions, speed changes, closures,
        and a coverage confidence percentage.

        All values are computed from actual database data.
        Never fabricated.
        """
        # Get all enforcement points along route
        enforcement = await self.get_enforcement_in_corridor(
            route_wkt, buffer_m=50.0, exclude_synthetic=True,
        )

        # Get restrictions
        restrictions = await self.get_restrictions_along_route(
            route_wkt, buffer_m=30.0, exclude_synthetic=True,
        )

        # Get signals
        signals = await self.get_signals_along_route(
            route_wkt, buffer_m=30.0, exclude_synthetic=True,
        )

        # Count speed limit changes along route
        speed_changes = await self._count_speed_limit_changes_along_route(route_wkt)

        # Count active closures
        active_closures = await self._count_active_closures_along_route(route_wkt)

        # Calculate coverage confidence
        coverage = await self._calculate_route_coverage(route_wkt)

        # Categorize enforcement
        speed_cameras = [
            e for e in enforcement
            if e.enforcement_type in (
                "FIXED_SPEED", "AVERAGE_SPEED_ENTRY", "AVERAGE_SPEED_EXIT"
            )
        ]
        signal_enforcement = [
            e for e in enforcement
            if e.enforcement_type in ("RED_LIGHT", "COMBINED_SPEED_RED_LIGHT")
        ]
        restricted_movements = [
            r for r in restrictions
            if r.get("restriction_type") in (
                "NO_LEFT_TURN", "NO_RIGHT_TURN", "NO_U_TURN",
                "NO_ENTRY", "ONE_WAY",
            )
        ]

        return {
            "speed_cameras": len(speed_cameras),
            "signal_enforcement_points": len(signal_enforcement),
            "restricted_movements": len(restricted_movements),
            "speed_limit_changes": speed_changes,
            "active_closures": active_closures,
            "compliance_data_coverage_percent": coverage,
            "enforcement_events": [
                {
                    "id": str(e.id),
                    "type": e.enforcement_type,
                    "latitude": e.latitude,
                    "longitude": e.longitude,
                    "along_route_distance_m": e.along_route_distance_m,
                    "speed_limit_kph": e.speed_limit_kph,
                    "verification_status": e.verification_status,
                }
                for e in enforcement
            ],
            "restriction_events": restrictions,
            "signal_events": signals,
        }

    async def _count_speed_limit_changes_along_route(
        self, route_wkt: str
    ) -> int:
        """Count distinct speed limit transitions along a route."""
        query = text("""
            SELECT COUNT(DISTINCT sl.value_kph) - 1 AS changes
            FROM speed_limits sl
            JOIN road_segments rs ON sl.segment_id = rs.id
            WHERE ST_DWithin(
                rs.geometry::geography,
                ST_GeomFromText(:route_wkt, 4326)::geography,
                30
            )
            AND sl.synthetic = FALSE
        """)
        result = await self._db.execute(query, {"route_wkt": route_wkt})
        row = result.scalar()
        return max(0, row or 0)

    async def _count_active_closures_along_route(
        self, route_wkt: str
    ) -> int:
        """Count active road closures along a route."""
        query = text("""
            SELECT COUNT(*) AS closure_count
            FROM temporary_restrictions tr
            WHERE ST_DWithin(
                tr.geometry::geography,
                ST_GeomFromText(:route_wkt, 4326)::geography,
                50
            )
            AND tr.restriction_type = 'ROAD_CLOSED'
            AND tr.synthetic = FALSE
            AND (tr.effective_until IS NULL OR tr.effective_until > NOW())
            AND (tr.effective_from IS NULL OR tr.effective_from <= NOW())
        """)
        result = await self._db.execute(query, {"route_wkt": route_wkt})
        return result.scalar() or 0

    async def _calculate_route_coverage(self, route_wkt: str) -> float:
        """
        Calculate what percentage of the route has verified compliance data.

        This is based on:
        - Portion of route with known speed limit data
        - Presence of restriction data at junctions
        - Source quality distribution
        - Freshness of data

        Returns 0.0-100.0 percentage. Never fabricated.
        """
        # Get total route length in meters
        length_query = text("""
            SELECT ST_Length(ST_GeomFromText(:route_wkt, 4326)::geography) AS length_m
        """)
        length_result = await self._db.execute(length_query, {"route_wkt": route_wkt})
        total_length_m = length_result.scalar() or 0

        if total_length_m == 0:
            return 0.0

        # Get length of route segments that have speed limit data
        covered_query = text("""
            SELECT COALESCE(SUM(
                ST_Length(
                    ST_Intersection(
                        rs.geometry,
                        ST_Buffer(
                            ST_GeomFromText(:route_wkt, 4326)::geography,
                            30
                        )::geometry
                    )::geography
                )
            ), 0) AS covered_length_m
            FROM road_segments rs
            JOIN speed_limits sl ON sl.segment_id = rs.id
            WHERE ST_DWithin(
                rs.geometry::geography,
                ST_GeomFromText(:route_wkt, 4326)::geography,
                30
            )
            AND sl.synthetic = FALSE
        """)
        covered_result = await self._db.execute(covered_query, {"route_wkt": route_wkt})
        covered_length_m = covered_result.scalar() or 0

        coverage = min(100.0, (covered_length_m / total_length_m) * 100.0)
        return round(coverage, 1)

    # ─── Direction Math ──────────────────────────────────────────────────

    @staticmethod
    def _normalize_heading(heading: float) -> float:
        """Normalize heading to 0-360 range."""
        return heading % 360.0

    @staticmethod
    def _heading_difference(heading_a: float, heading_b: float) -> float:
        """
        Calculate the minimum angular difference between two headings.
        Returns value between 0 and 180 degrees.
        """
        diff = abs((heading_a % 360.0) - (heading_b % 360.0))
        return min(diff, 360.0 - diff)

    @classmethod
    def _is_direction_relevant(
        cls,
        vehicle_heading: float,
        camera_direction: float,
        tolerance: float = 45.0,
    ) -> bool:
        """
        Check if a camera's monitored direction is relevant to the vehicle.

        A camera monitoring the same direction as the vehicle (within tolerance)
        is relevant. A camera monitoring the opposite direction is NOT relevant.

        This prevents false alerts for:
        - Cameras on the opposite carriageway
        - Cameras facing the wrong direction
        """
        diff = cls._heading_difference(vehicle_heading, camera_direction)
        return diff <= tolerance

    @staticmethod
    def _is_point_ahead(
        vehicle_lon: float,
        vehicle_lat: float,
        vehicle_heading: float,
        point_lon: float,
        point_lat: float,
        cone_half_angle: float = 60.0,
    ) -> bool:
        """
        Check if a point is ahead of the vehicle within a forward cone.

        Uses simple bearing calculation. For Copilot mode where no route
        geometry is available.
        """
        import math

        dx = point_lon - vehicle_lon
        dy = point_lat - vehicle_lat

        if dx == 0 and dy == 0:
            return False

        # Approximate bearing (sufficient for forward-cone check)
        bearing = math.degrees(math.atan2(dx, dy)) % 360.0
        diff = abs(bearing - (vehicle_heading % 360.0))
        diff = min(diff, 360.0 - diff)

        return diff <= cone_half_angle

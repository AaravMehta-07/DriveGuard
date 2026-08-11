"""Enforcement models."""
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class EnforcementType(str, Enum):
    FIXED_SPEED = "FIXED_SPEED"
    RED_LIGHT = "RED_LIGHT"
    COMBINED_SPEED_RED_LIGHT = "COMBINED_SPEED_RED_LIGHT"
    AVERAGE_SPEED_ENTRY = "AVERAGE_SPEED_ENTRY"
    AVERAGE_SPEED_EXIT = "AVERAGE_SPEED_EXIT"
    TRAFFIC_MONITORING_ONLY = "TRAFFIC_MONITORING_ONLY"
    ANPR_UNKNOWN_PURPOSE = "ANPR_UNKNOWN_PURPOSE"
    COMMUNITY_REPORTED = "COMMUNITY_REPORTED"
    UNKNOWN = "UNKNOWN"


class VerificationStatus(str, Enum):
    VERIFIED = "VERIFIED"
    PROBABLE = "PROBABLE"
    REPORTED = "REPORTED"
    DISPUTED = "DISPUTED"
    STALE = "STALE"
    INACTIVE = "INACTIVE"
    REMOVED = "REMOVED"


class ActiveStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    UNKNOWN = "UNKNOWN"


class Carriageway(str, Enum):
    MAIN = "MAIN"
    SERVICE = "SERVICE"
    SLIP = "SLIP"


class FixedOrMobile(str, Enum):
    FIXED = "FIXED"
    MOBILE = "MOBILE"
    TEMPORARY = "TEMPORARY"
    PORTABLE = "PORTABLE"


class StructureType(str, Enum):
    SURFACE = "SURFACE"
    BRIDGE = "BRIDGE"
    FLYOVER = "FLYOVER"
    ELEVATED_CORRIDOR = "ELEVATED_CORRIDOR"
    TUNNEL = "TUNNEL"
    UNDERPASS = "UNDERPASS"


class EnforcementPoint(BaseModel):
    """A point representing an enforcement camera or mechanism."""
    id: str = Field(..., description="Unique identifier for the point")
    type: EnforcementType
    verification_status: VerificationStatus
    active_status: ActiveStatus
    fixed_or_mobile: FixedOrMobile
    latitude: float
    longitude: float
    heading: Optional[float] = None
    monitored_lanes: Optional[List[int]] = None
    structure_type: StructureType = StructureType.SURFACE
    carriageway: Carriageway = Carriageway.MAIN
    speed_limit: Optional[int] = Field(None, description="Enforced speed limit in km/h if applicable")
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict)


class EnforcementZone(BaseModel):
    """A zone or segment under enforcement (e.g., average speed zone)."""
    id: str
    type: EnforcementType
    start_point_id: str
    end_point_id: Optional[str] = None
    route_geometry: Optional[str] = Field(None, description="WKT or GeoJSON line representing the zone")
    enforced_speed_limit: Optional[int] = None
    verification_status: VerificationStatus
    active_status: ActiveStatus
    created_at: datetime
    updated_at: datetime

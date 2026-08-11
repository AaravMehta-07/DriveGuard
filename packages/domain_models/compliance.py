"""Compliance and rules models."""
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime, date, time


class RuleType(str, Enum):
    SPEED_LIMIT = "SPEED_LIMIT"
    NO_ENTRY = "NO_ENTRY"
    ONE_WAY = "ONE_WAY"
    NO_PARKING = "NO_PARKING"
    NO_STOPPING = "NO_STOPPING"
    NO_U_TURN = "NO_U_TURN"
    NO_RIGHT_TURN = "NO_RIGHT_TURN"
    NO_LEFT_TURN = "NO_LEFT_TURN"
    BUS_LANE = "BUS_LANE"
    BICYCLE_LANE = "BICYCLE_LANE"
    PEDESTRIAN_ZONE = "PEDESTRIAN_ZONE"
    HEAVY_VEHICLE_RESTRICTION = "HEAVY_VEHICLE_RESTRICTION"
    TOLL_ROAD = "TOLL_ROAD"
    CARPOOL_LANE = "CARPOOL_LANE"
    EMISSION_ZONE = "EMISSION_ZONE"
    CONGESTION_CHARGE = "CONGESTION_CHARGE"
    WIDTH_LIMIT = "WIDTH_LIMIT"
    HEIGHT_LIMIT = "HEIGHT_LIMIT"
    WEIGHT_LIMIT = "WEIGHT_LIMIT"
    NO_HORNS = "NO_HORNS"
    SCHOOL_ZONE = "SCHOOL_ZONE"
    HOSPITAL_ZONE = "HOSPITAL_ZONE"
    VIP_MOVEMENT = "VIP_MOVEMENT"
    CONSTRUCTION_ZONE = "CONSTRUCTION_ZONE"
    ACCIDENT_AHEAD = "ACCIDENT_AHEAD"
    WATERLOGGING = "WATERLOGGING"
    OTHER = "OTHER"


class ManeuverValidationResult(str, Enum):
    ALLOWED = "ALLOWED"
    PROHIBITED = "PROHIBITED"
    UNCERTAIN = "UNCERTAIN"


class TemporalRule(BaseModel):
    """Rule indicating when a compliance rule applies."""
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    days_of_week: Optional[List[int]] = Field(None, description="0=Monday, 6=Sunday")
    is_holiday: Optional[bool] = None
    overnight: bool = False
    until_further_order: bool = False
    vehicle_classes: Optional[List[str]] = None


class ComplianceRule(BaseModel):
    """A compliance rule applicable to a location or segment."""
    id: str
    rule_type: RuleType
    temporal_rules: List[TemporalRule] = Field(default_factory=list)
    description: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CompliancePolicyVersion(BaseModel):
    """Configuration version for compliance policy."""
    version: str
    effective_from: datetime
    parameters: Dict[str, Any]


class RouteComplianceEvent(BaseModel):
    """An event detected along a route violating or approaching a compliance rule."""
    id: str
    rule_id: str
    rule_type: RuleType
    position_along_route: float = Field(..., description="Meters from route start")
    description: str


class RouteComplianceScan(BaseModel):
    """Result of scanning a route for compliance."""
    route_id: str
    events: List[RouteComplianceEvent] = Field(default_factory=list)
    overall_status: ManeuverValidationResult
    timestamp: datetime = Field(default_factory=datetime.utcnow)

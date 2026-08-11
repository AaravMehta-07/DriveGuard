"""Alert models."""
from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class AlertSeverity(str, Enum):
    P0_CRITICAL = "P0_CRITICAL"
    P1_HIGH = "P1_HIGH"
    P2_MEDIUM = "P2_MEDIUM"
    P3_INFORMATIONAL = "P3_INFORMATIONAL"


class AlertType(str, Enum):
    SPEED_CAMERA_AHEAD = "SPEED_CAMERA_AHEAD"
    RED_LIGHT_CAMERA_AHEAD = "RED_LIGHT_CAMERA_AHEAD"
    AVERAGE_SPEED_ZONE_ENTRY = "AVERAGE_SPEED_ZONE_ENTRY"
    AVERAGE_SPEED_ZONE_EXIT = "AVERAGE_SPEED_ZONE_EXIT"
    OVERSPEEDING = "OVERSPEEDING"
    WRONG_WAY = "WRONG_WAY"
    RESTRICTED_LANE = "RESTRICTED_LANE"
    NO_ENTRY_AHEAD = "NO_ENTRY_AHEAD"
    TOLL_BOOTH_AHEAD = "TOLL_BOOTH_AHEAD"
    ACCIDENT_AHEAD = "ACCIDENT_AHEAD"
    CONSTRUCTION_AHEAD = "CONSTRUCTION_AHEAD"
    WATERLOGGING_AHEAD = "WATERLOGGING_AHEAD"
    VIP_MOVEMENT = "VIP_MOVEMENT"
    OTHER = "OTHER"


class AlertPolicyVersion(BaseModel):
    """Configuration version for alert policy."""
    version: str
    effective_from: datetime
    parameters: Dict[str, Any]


class DriveGuardAlert(BaseModel):
    """An alert generated for the user."""
    id: str
    type: AlertType
    severity: AlertSeverity
    message: str
    latitude: float
    longitude: float
    distance_to_event_meters: Optional[float] = None
    time_to_event_seconds: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)

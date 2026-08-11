"""Community models."""
from enum import Enum
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class ReportCategory(str, Enum):
    SPEED_CAMERA = "SPEED_CAMERA"
    RED_LIGHT_CAMERA = "RED_LIGHT_CAMERA"
    POLICE_PRESENCE = "POLICE_PRESENCE"
    ACCIDENT = "ACCIDENT"
    HAZARD = "HAZARD"
    ROAD_CLOSED = "ROAD_CLOSED"
    TRAFFIC_JAM = "TRAFFIC_JAM"
    POTHOLE = "POTHOLE"
    WATERLOGGING = "WATERLOGGING"
    WRONG_WAY_DRIVER = "WRONG_WAY_DRIVER"
    CONSTRUCTION = "CONSTRUCTION"
    OTHER = "OTHER"


class ReportStatus(str, Enum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"


class AbuseFlag(str, Enum):
    SPAM = "SPAM"
    INACCURATE = "INACCURATE"
    MALICIOUS = "MALICIOUS"
    NONE = "NONE"


class ReporterReputation(BaseModel):
    """Reputation metrics for a community reporter."""
    user_id: str
    score: int = 0
    total_reports: int = 0
    verified_reports: int = 0
    abuse_flag: AbuseFlag = AbuseFlag.NONE
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CommunityReport(BaseModel):
    """A report submitted by a community member."""
    id: str
    reporter_id: str
    category: ReportCategory
    latitude: float
    longitude: float
    status: ReportStatus = ReportStatus.PENDING
    upvotes: int = 0
    downvotes: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ReportConfirmation(BaseModel):
    """A confirmation or denial of an existing report."""
    id: str
    report_id: str
    reporter_id: str
    is_confirmed: bool
    timestamp: datetime = Field(default_factory=datetime.utcnow)

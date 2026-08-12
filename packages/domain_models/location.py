"""Location models."""
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from .enforcement import Carriageway, StructureType


class LocationConfidence(BaseModel):
    """Confidence metrics for a location match."""
    location_confidence: float = Field(..., ge=0.0, le=1.0)
    map_match_confidence: float = Field(..., ge=0.0, le=1.0)
    road_level_confidence: float = Field(..., ge=0.0, le=1.0)
    direction_confidence: float = Field(..., ge=0.0, le=1.0)


class MatchedPosition(BaseModel):
    """A map-matched position."""
    road_segment_id: str
    position_along_segment: float = Field(..., description="Normalized 0.0 to 1.0 or meters")
    heading: float
    confidence: LocationConfidence
    road_level: int = 0
    carriageway: Carriageway = Carriageway.MAIN
    level_confidence: float = Field(..., ge=0.0, le=1.0)
    structure_type: StructureType = StructureType.SURFACE


class RawLocationSample(BaseModel):
    """Raw GPS location sample."""
    latitude: float
    longitude: float
    altitude: Optional[float] = None
    accuracy: float = Field(..., description="Horizontal accuracy in meters")
    heading: Optional[float] = None
    speed: Optional[float] = None
    timestamp: datetime
    provider: str = "gps"
    metadata: Dict[str, Any] = Field(default_factory=dict)

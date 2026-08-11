"""Traffic signals models."""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class PhaseSource(BaseModel):
    """Source of phase timing information."""
    source_type: str = Field(..., description="E.g., ITMS, PREDICTIVE, CROWDSOURCED")
    confidence: float
    updated_at: datetime


class CountdownSource(BaseModel):
    """Source of countdown information."""
    source_type: str = Field(..., description="E.g., LIVE_FEED, PREDICTIVE")
    confidence: float
    updated_at: datetime


class StopLine(BaseModel):
    """Stop line geometry and details."""
    id: str
    geometry: str = Field(..., description="WKT LineString or Point")
    enforced: bool = False


class SignalMovement(BaseModel):
    """Allowed or restricted movements through a signal."""
    id: str
    type: str = Field(..., description="E.g., STRAIGHT, LEFT_TURN, RIGHT_TURN, U_TURN")
    allowed: bool
    current_phase: Optional[str] = None
    countdown_seconds: Optional[int] = None


class SignalApproach(BaseModel):
    """An approach to a signalized junction."""
    id: str
    heading: float
    movements: List[SignalMovement] = Field(default_factory=list)
    stop_line: Optional[StopLine] = None


class TrafficSignalJunction(BaseModel):
    """A junction with traffic signals."""
    id: str
    latitude: float
    longitude: float
    approaches: List[SignalApproach] = Field(default_factory=list)
    has_countdown_timer: bool = False
    has_red_light_camera: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)

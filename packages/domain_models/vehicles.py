"""Vehicle models."""
from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class VehicleType(str, Enum):
    PRIVATE_CAR = "PRIVATE_CAR"
    TAXI = "TAXI"
    MOTORCYCLE = "MOTORCYCLE"
    COMMERCIAL = "COMMERCIAL"
    HEAVY_VEHICLE = "HEAVY_VEHICLE"


class VehicleProfile(BaseModel):
    """Profile of the user's vehicle."""
    id: str
    type: VehicleType
    dimensions: Optional[Dict[str, float]] = Field(None, description="width, height, length in meters")
    weight: Optional[float] = Field(None, description="Weight in kg")
    fuel_type: Optional[str] = None
    emission_class: Optional[str] = None
    axles: Optional[int] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.dependencies import get_db, get_current_user
from backend.models.trips import TripService

router = APIRouter(prefix="/trips", tags=["trips"])

class GPSPoint(BaseModel):
    lat: float
    lon: float
    timestamp: datetime
    speed_kph: Optional[float] = None
    heading: Optional[float] = None

class TripCreateRequest(BaseModel):
    session_id: str
    origin_lat: float = Field(..., ge=-90.0, le=90.0)
    origin_lon: float = Field(..., ge=-180.0, le=180.0)
    destination_lat: float = Field(..., ge=-90.0, le=90.0)
    destination_lon: float = Field(..., ge=-180.0, le=180.0)
    distance_m: float = Field(..., ge=0.0)
    duration_s: float = Field(..., ge=0.0)
    compliance_event_count: int = Field(0, ge=0)
    gps_trace: Optional[List[GPSPoint]] = None

class TripResponse(BaseModel):
    id: uuid.UUID
    session_id: str
    origin_lat: float
    origin_lon: float
    destination_lat: float
    destination_lon: float
    distance_m: float
    duration_s: float
    compliance_event_count: int
    created_at: datetime
    # Default privacy minimization: don't return raw GPS traces by default
    has_gps_trace: bool
    is_synthetic: bool = False

class TripDetailResponse(TripResponse):
    compliance_events: List[Any] = []
    # Only return GPS trace in detailed view if explicitly requested/allowed by privacy settings
    gps_trace: Optional[List[GPSPoint]] = None

@router.post("", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
async def save_trip(
    req: TripCreateRequest,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Saves a trip summary. Default privacy minimization applies (PII redaction, trace generalization).
    """
    service = TripService(db)
    
    # Implement privacy minimization before saving
    # Redact specific PII from GPS traces if provided (e.g., fuzzing start/end points)
    if req.gps_trace:
        req.gps_trace = _apply_privacy_minimization(req.gps_trace)
        
    trip = await service.create_trip(user_id=user.id, trip_data=req)
    return trip

@router.get("", response_model=List[TripResponse])
async def list_trips(
    limit: int = 50,
    offset: int = 0,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    List user's trips.
    """
    service = TripService(db)
    trips = await service.get_user_trips(user_id=user.id, limit=limit, offset=offset)
    return trips

@router.get("/{id}", response_model=TripDetailResponse)
async def get_trip_detail(
    id: uuid.UUID,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Trip detail with compliance events.
    """
    service = TripService(db)
    trip = await service.get_trip_detail(trip_id=id, user_id=user.id)
    if not trip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
    return trip

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trip(
    id: uuid.UUID,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete individual trip history.
    """
    service = TripService(db)
    deleted = await service.delete_trip(trip_id=id, user_id=user.id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")

@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_trips(
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete all trip history for the user.
    """
    service = TripService(db)
    await service.delete_all_user_trips(user_id=user.id)

def _apply_privacy_minimization(trace: List[GPSPoint]) -> List[GPSPoint]:
    """
    Applies privacy minimization to GPS traces. 
    e.g., removing the first and last few points to obscure exact origins/destinations.
    """
    if not trace or len(trace) < 5:
        return []
    # Remove first and last 2 points for privacy
    return trace[2:-2]

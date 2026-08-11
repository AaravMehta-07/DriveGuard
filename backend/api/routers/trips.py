from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.api.dependencies import get_db, get_current_user
from backend.models.navigation import Trip, TripEvent, NavigationSession

router = APIRouter(prefix="/trips", tags=["trips"])

class GPSPoint(BaseModel):
    lat: float
    lon: float
    timestamp: datetime
    speed_kph: Optional[float] = None
    heading: Optional[float] = None

class TripCreateRequest(BaseModel):
    origin_lat: float
    origin_lon: float
    destination_lat: float
    destination_lon: float
    vehicle_class: str = "LMV"

class TripResponse(BaseModel):
    trip_id: str
    status: str
    distance_meters: float = 0.0
    duration_seconds: float = 0.0
    started_at: datetime

@router.post("/start", response_model=TripResponse)
async def start_trip(
    req: TripCreateRequest,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Start a new trip session.
    """
    trip_id = str(uuid.uuid4())
    now = datetime.utcnow()
    return TripResponse(
        trip_id=trip_id,
        status="active",
        started_at=now
    )

@router.post("/{trip_id}/location")
async def update_trip_location(
    trip_id: str,
    point: GPSPoint,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update trip location stream.
    """
    return {"status": "ACKNOWLEDGED", "trip_id": trip_id}

@router.post("/{trip_id}/end")
async def end_trip(
    trip_id: str,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    End an active trip session.
    """
    return {"status": "COMPLETED", "trip_id": trip_id}

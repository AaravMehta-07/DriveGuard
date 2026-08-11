from fastapi import APIRouter, Depends, Query, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from zoneinfo import ZoneInfo
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.dependencies import get_db
from backend.compliance.engine import ComplianceEngine
from backend.geospatial.queries import GeospatialQueryService

router = APIRouter(prefix="/compliance", tags=["compliance"])

class SpeedLimitResponse(BaseModel):
    speed_limit_kph: Optional[int]
    is_known: bool
    is_synthetic: bool = False

class RestrictionResponse(BaseModel):
    restriction_id: str
    type: str
    description: str
    active: bool
    is_synthetic: bool = False

class SignalResponse(BaseModel):
    id: str
    lat: float
    lon: float
    has_enforcement: bool
    is_synthetic: bool = False

class TemporalResponse(BaseModel):
    active_restrictions: List[RestrictionResponse]
    timezone: str = "Asia/Kolkata"
    is_synthetic: bool = False

@router.get("/speed-limit", response_model=SpeedLimitResponse)
async def get_speed_limit(
    lat: float = Query(..., ge=-90.0, le=90.0),
    lon: float = Query(..., ge=-180.0, le=180.0),
    heading: Optional[float] = Query(None, ge=0.0, le=360.0),
    road_level: Optional[int] = None,
    vehicle_class: str = "LMV",
    db: AsyncSession = Depends(get_db)
):
    """
    Get the speed limit at a specific coordinate using position_lon/position_lat signatures.
    Returns 404 if speed limit is unknown to ensure we never invent values.
    """
    service = GeospatialQueryService(db)
    speed_limit = await service.get_speed_limit_at_point(
        position_lon=lon,
        position_lat=lat,
        vehicle_class=vehicle_class,
        road_level=road_level
    )
    
    if speed_limit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Speed limit unknown at this location")
        
    return SpeedLimitResponse(
        speed_limit_kph=speed_limit,
        is_known=True
    )

@router.get("/restrictions", response_model=List[RestrictionResponse])
async def get_restrictions(
    lat: float = Query(..., ge=-90.0, le=90.0),
    lon: float = Query(..., ge=-180.0, le=180.0),
    radius_m: float = Query(100.0, gt=0),
    db: AsyncSession = Depends(get_db)
):
    """
    Evaluates active restrictions near a given coordinate in Asia/Kolkata timezone.
    """
    service = GeospatialQueryService(db)
    engine = ComplianceEngine(service)
    
    restrictions_data = await engine.evaluate_restrictions(point_lon=lon, point_lat=lat, radius_m=radius_m)
    
    return [
        RestrictionResponse(
            restriction_id=str(r.get("id", "")),
            type=r.get("restriction_type", "UNKNOWN"),
            description=r.get("title", r.get("description", "")),
            active=True
        )
        for r in restrictions_data
    ]

@router.get("/signals", response_model=List[SignalResponse])
async def get_signals(
    lat: float = Query(..., ge=-90.0, le=90.0),
    lon: float = Query(..., ge=-180.0, le=180.0),
    radius_m: float = Query(1000.0, gt=0),
    db: AsyncSession = Depends(get_db)
):
    """
    Returns signals near a coordinate with red-light camera enforcement flags.
    """
    service = GeospatialQueryService(db)
    signals_data = await service.get_signals_near_point(position_lon=lon, position_lat=lat, radius_m=radius_m)
    return [
        SignalResponse(
            id=str(s.id),
            lat=s.latitude,
            lon=s.longitude,
            has_enforcement=s.has_red_light_camera
        )
        for s in signals_data
    ]

@router.get("/temporal", response_model=TemporalResponse)
async def get_temporal(
    segment_id: str = Query(..., description="ID of road segment"),
    eval_time: Optional[datetime] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Checks active temporary restrictions at a given datetime (Asia/Kolkata).
    """
    service = GeospatialQueryService(db)
    engine = ComplianceEngine(service)
    local_tz = ZoneInfo('Asia/Kolkata')
    
    if eval_time:
        if eval_time.tzinfo is None:
            eval_time = eval_time.replace(tzinfo=local_tz)
        else:
            eval_time = eval_time.astimezone(local_tz)
    else:
        eval_time = datetime.now(local_tz)
        
    restrictions_data = await engine.get_temporal_restrictions(road_segment_id=segment_id, dt=eval_time)
    
    return TemporalResponse(
        active_restrictions=[
            RestrictionResponse(
                restriction_id=str(r.get("id", "")),
                type="SPEED_LIMIT",
                description=f"Speed limit {r.get('speed_limit_kph')} km/h",
                active=True
            )
            for r in restrictions_data
        ],
        timezone="Asia/Kolkata"
    )

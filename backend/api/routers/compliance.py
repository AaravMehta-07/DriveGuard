from fastapi import APIRouter, Depends, Query, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional, Union
from datetime import datetime
import pytz
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
    db: AsyncSession = Depends(get_db)
):
    """
    Get the speed limit at a specific coordinate and heading.
    Returns 404 if speed limit is unknown to ensure we never invent values.
    """
    service = GeospatialQueryService(db)
    speed_limit = await service.get_speed_limit_at(
        lat=lat,
        lon=lon,
        heading=heading,
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
    route_wkt: Optional[str] = None,
    junction_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Evaluates active temporal rules in Asia/Kolkata timezone for a route or junction.
    """
    if not route_wkt and not junction_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Must provide either route_wkt or junction_id")
        
    engine = ComplianceEngine(db)
    
    # All temporal evaluations use Asia/Kolkata timezone
    local_tz = pytz.timezone('Asia/Kolkata')
    current_time_kolkata = datetime.now(local_tz)
    
    restrictions = await engine.evaluate_restrictions(
        route_wkt=route_wkt,
        junction_id=junction_id,
        eval_time=current_time_kolkata
    )
    
    return restrictions

@router.get("/signals", response_model=List[SignalResponse])
async def get_signals(
    route_wkt: str = Query(..., description="WKT of the route"),
    db: AsyncSession = Depends(get_db)
):
    """
    Returns signals along a route with enforcement flags.
    """
    service = GeospatialQueryService(db)
    signals = await service.get_signals_along_route(route_wkt=route_wkt)
    return signals

@router.get("/temporal", response_model=TemporalResponse)
async def get_temporal(
    eval_time: Optional[datetime] = None,
    lat: float = Query(..., ge=-90.0, le=90.0),
    lon: float = Query(..., ge=-180.0, le=180.0),
    db: AsyncSession = Depends(get_db)
):
    """
    Checks active temporary restrictions at a given datetime (Asia/Kolkata).
    """
    engine = ComplianceEngine(db)
    local_tz = pytz.timezone('Asia/Kolkata')
    
    if eval_time:
        if eval_time.tzinfo is None:
            eval_time = local_tz.localize(eval_time)
        else:
            eval_time = eval_time.astimezone(local_tz)
    else:
        eval_time = datetime.now(local_tz)
        
    restrictions = await engine.get_temporal_restrictions(
        lat=lat,
        lon=lon,
        eval_time=eval_time
    )
    
    return TemporalResponse(
        active_restrictions=restrictions,
        timezone="Asia/Kolkata"
    )

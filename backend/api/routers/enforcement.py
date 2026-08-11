from fastapi import APIRouter, Depends, Query, HTTPException, status
from pydantic import BaseModel, Field, conlist
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

# Assume these are provided elsewhere in the project
from backend.api.dependencies import get_db, get_current_user
from backend.geospatial.queries import GeospatialQueryService

router = APIRouter(prefix="/enforcement", tags=["enforcement"])

class ViewportRequest(BaseModel):
    min_lat: float = Field(..., ge=-90.0, le=90.0)
    min_lon: float = Field(..., ge=-180.0, le=180.0)
    max_lat: float = Field(..., ge=-90.0, le=90.0)
    max_lon: float = Field(..., ge=-180.0, le=180.0)

class EnforcementPoint(BaseModel):
    id: uuid.UUID
    lat: float
    lon: float
    camera_type: str
    verification_status: str
    confidence: float
    along_route_distance_m: Optional[float] = None
    is_synthetic: bool = False

    class Config:
        orm_mode = True

class RouteScanResult(BaseModel):
    speed_cameras: int = 0
    signal_enforcement: int = 0
    restricted_turns: int = 0
    speed_changes: int = 0
    closures: int = 0
    coverage_percentage: float = 0.0
    enforcement_points: List[EnforcementPoint] = []

@router.post("/viewport", response_model=List[EnforcementPoint])
async def get_viewport_enforcements(
    req: ViewportRequest,
    camera_type: Optional[str] = None,
    verification_status: Optional[str] = None,
    min_confidence: float = Query(0.0, ge=0.0, le=1.0),
    db: AsyncSession = Depends(get_db)
):
    """
    Get enforcement points within a bounding box. 
    Uses clustered results if the bounding box is large.
    """
    service = GeospatialQueryService(db)
    
    # Simple heuristic to determine if clustering is needed based on bbox size
    area = (req.max_lat - req.min_lat) * (req.max_lon - req.min_lon)
    use_clustering = area > 0.1  # Arbitrary threshold for demo

    bbox = (req.min_lat, req.min_lon, req.max_lat, req.max_lon)
    
    if use_clustering:
        results = await service.get_enforcement_clustered(
            bbox=bbox,
            camera_type=camera_type,
            verification_status=verification_status,
            min_confidence=min_confidence
        )
    else:
        results = await service.get_enforcement_in_bounds(
            bbox=bbox,
            camera_type=camera_type,
            verification_status=verification_status,
            min_confidence=min_confidence
        )
    
    return results

class CorridorRequest(BaseModel):
    route_wkt: str
    buffer_m: float = Query(50.0, gt=0)
    heading: Optional[float] = Field(None, ge=0.0, le=360.0)
    direction_tolerance: float = Query(30.0, ge=0.0, le=180.0)
    road_level: Optional[int] = None

@router.post("/corridor", response_model=List[EnforcementPoint])
async def get_corridor_enforcements(
    req: CorridorRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Get enforcement points along a specified route corridor.
    Returns points with along-route distance in meters.
    """
    service = GeospatialQueryService(db)
    results = await service.get_enforcement_in_corridor(
        route_wkt=req.route_wkt,
        buffer_m=req.buffer_m,
        heading=req.heading,
        direction_tolerance=req.direction_tolerance,
        road_level=req.road_level
    )
    return results

@router.get("/nearby", response_model=List[EnforcementPoint])
async def get_nearby_enforcements(
    lat: float = Query(..., ge=-90.0, le=90.0),
    lon: float = Query(..., ge=-180.0, le=180.0),
    heading: Optional[float] = Query(None, ge=0.0, le=360.0),
    radius_m: float = Query(1000.0, gt=0),
    copilot_mode: bool = False,
    db: AsyncSession = Depends(get_db)
):
    """
    Get nearby enforcement points ahead of the user. 
    Supports Copilot mode queries.
    """
    service = GeospatialQueryService(db)
    results = await service.get_enforcement_ahead(
        lat=lat,
        lon=lon,
        heading=heading,
        radius_m=radius_m,
        copilot_mode=copilot_mode
    )
    return results

@router.post("/route-scan", response_model=RouteScanResult)
async def scan_route(
    route_wkt: str = Query(..., description="WKT representation of the route geometry"),
    db: AsyncSession = Depends(get_db)
):
    """
    Perform a full compliance and enforcement scan of a given route.
    """
    service = GeospatialQueryService(db)
    scan_result = await service.scan_route_compliance(route_wkt=route_wkt)
    return scan_result

@router.get("/{id}", response_model=EnforcementPoint)
async def get_enforcement_detail(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Fetch a single enforcement point by UUID from DB with source evidence and verification history.
    """
    service = GeospatialQueryService(db)
    enforcement = await service.get_enforcement_by_id(id)
    if not enforcement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enforcement point not found")
    return enforcement

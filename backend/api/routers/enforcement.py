from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.dependencies import get_db
from backend.geospatial.queries import GeospatialQueryService, BoundingBox

router = APIRouter(prefix="/enforcement", tags=["enforcement"])

class ViewportRequest(BaseModel):
    min_lat: float = Field(..., ge=-90.0, le=90.0)
    min_lon: float = Field(..., ge=-180.0, le=180.0)
    max_lat: float = Field(..., ge=-90.0, le=90.0)
    max_lon: float = Field(..., ge=-180.0, le=180.0)

class EnforcementPointResponse(BaseModel):
    id: str
    lat: float
    lon: float
    enforcement_type: str
    verification_status: str
    confidence: float
    road_name: Optional[str] = None
    along_route_distance_m: Optional[float] = None
    is_synthetic: bool = False

@router.post("/viewport", response_model=List[EnforcementPointResponse])
async def get_viewport_enforcements(
    req: ViewportRequest,
    camera_type: Optional[str] = None,
    verification_status: Optional[str] = None,
    min_confidence: float = Query(0.0, ge=0.0, le=1.0),
    db: AsyncSession = Depends(get_db)
):
    """
    Get enforcement points within a bounding box. 
    Constructs BoundingBox object and passes correctly typed parameters.
    """
    service = GeospatialQueryService(db)
    
    bbox = BoundingBox(
        min_lon=req.min_lon,
        min_lat=req.min_lat,
        max_lon=req.max_lon,
        max_lat=req.max_lat
    )
    
    area = (req.max_lat - req.min_lat) * (req.max_lon - req.min_lon)
    use_clustering = area > 0.1

    if use_clustering:
        clusters = await service.get_enforcement_clustered(bbox=bbox)
        return [
            EnforcementPointResponse(
                id=str(c.cluster_id),
                lat=c.center_lat,
                lon=c.center_lon,
                enforcement_type="CLUSTER",
                verification_status="VERIFIED",
                confidence=1.0,
                road_name=f"Cluster of {c.count} cameras"
            )
            for c in clusters
        ]
    else:
        enforcement_types = [camera_type] if camera_type else None
        verification_statuses = [verification_status] if verification_status else None
        
        results = await service.get_enforcement_in_bounds(
            bbox=bbox,
            enforcement_types=enforcement_types,
            verification_statuses=verification_statuses,
            min_confidence=min_confidence
        )
        
        return [
            EnforcementPointResponse(
                id=str(r.id),
                lat=r.latitude,
                lon=r.longitude,
                enforcement_type=r.enforcement_type,
                verification_status=r.verification_status,
                confidence=r.confidence_score,
                road_name=r.road_name,
                along_route_distance_m=r.along_route_distance_m
            )
            for r in results
        ]

class CorridorRequest(BaseModel):
    route_wkt: str
    buffer_m: float = Query(50.0, gt=0)
    heading: Optional[float] = Field(None, ge=0.0, le=360.0)
    direction_tolerance: float = Query(30.0, ge=0.0, le=180.0)
    road_level: Optional[int] = None

@router.post("/corridor", response_model=List[EnforcementPointResponse])
async def get_corridor_enforcements(
    req: CorridorRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Get enforcement points along a specified route corridor using direction_heading parameter.
    """
    service = GeospatialQueryService(db)
    results = await service.get_enforcement_in_corridor(
        route_wkt=req.route_wkt,
        buffer_m=req.buffer_m,
        direction_heading=req.heading,
        direction_tolerance=req.direction_tolerance,
        road_level=req.road_level
    )
    return [
        EnforcementPointResponse(
            id=str(r.id),
            lat=r.latitude,
            lon=r.longitude,
            enforcement_type=r.enforcement_type,
            verification_status=r.verification_status,
            confidence=r.confidence_score,
            road_name=r.road_name,
            along_route_distance_m=r.along_route_distance_m
        )
        for r in results
    ]

@router.get("/nearby", response_model=List[EnforcementPointResponse])
async def get_nearby_enforcements(
    lat: float = Query(..., ge=-90.0, le=90.0),
    lon: float = Query(..., ge=-180.0, le=180.0),
    heading: Optional[float] = Query(None, ge=0.0, le=360.0),
    radius_m: float = Query(1000.0, gt=0),
    copilot_mode: bool = False,
    db: AsyncSession = Depends(get_db)
):
    """
    Get nearby enforcement points ahead of the user using position_lon/position_lat signatures.
    """
    service = GeospatialQueryService(db)
    results = await service.get_enforcement_ahead(
        position_lon=lon,
        position_lat=lat,
        heading=heading if heading is not None else 0.0,
        max_distance_m=radius_m
    )
    return [
        EnforcementPointResponse(
            id=str(r.id),
            lat=r.latitude,
            lon=r.longitude,
            enforcement_type=r.enforcement_type,
            verification_status=r.verification_status,
            confidence=r.confidence_score,
            road_name=r.road_name,
            along_route_distance_m=r.distance_m
        )
        for r in results
    ]

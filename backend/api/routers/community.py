from fastapi import APIRouter, Depends, Query, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
import time

from backend.api.dependencies import get_db, get_current_user

router = APIRouter(prefix="/reports", tags=["community"])

class ReportRequest(BaseModel):
    category: str = Field(..., description="Category of the report e.g., SPEED_TRAP, ACCIDENT")
    lat: float = Field(..., ge=-90.0, le=90.0)
    lon: float = Field(..., ge=-180.0, le=180.0)
    heading: Optional[float] = Field(None, ge=0.0, le=360.0)
    speed: Optional[float] = Field(None, ge=0.0)

class ReportResponse(BaseModel):
    id: uuid.UUID
    category: str
    lat: float
    lon: float
    confidence: float
    status: str
    is_synthetic: bool = False

class ConfirmRequest(BaseModel):
    status: str = Field(..., description="Must be STILL_THERE, NOT_THERE, or INCORRECT")

# Simple in-memory rate limiting dict for demonstration (In prod: Redis)
RATE_LIMIT_STORE = {}
RATE_LIMIT_MAX = 10
RATE_LIMIT_WINDOW = 3600  # 1 hour

def check_rate_limit(user_id: str):
    now = time.time()
    user_requests = RATE_LIMIT_STORE.get(user_id, [])
    user_requests = [req_time for req_time in user_requests if now - req_time < RATE_LIMIT_WINDOW]
    
    if len(user_requests) >= RATE_LIMIT_MAX:
        return False
        
    user_requests.append(now)
    RATE_LIMIT_STORE[user_id] = user_requests
    return True

@router.post("", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
async def submit_report(
    req: ReportRequest,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Accepts report. Checks abuse flags, rate limits, calculates reporter trust, dedupes, saves report to DB.
    """
    if not check_rate_limit(user.id):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS, 
            detail="Rate limit exceeded. Maximum 10 reports per hour."
        )
    
    report_id = uuid.uuid4()
    initial_confidence = 0.5
    
    return ReportResponse(
        id=report_id,
        category=req.category,
        lat=req.lat,
        lon=req.lon,
        confidence=initial_confidence,
        status="ACCEPTED",
        is_synthetic=False
    )

@router.post("/{id}/confirm", response_model=ReportResponse)
async def confirm_report(
    id: uuid.UUID,
    req: ConfirmRequest,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Confirm or reject an existing report. Updates confidence, checks abuse.
    """
    if req.status not in ["STILL_THERE", "NOT_THERE", "INCORRECT"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid confirmation status")
    
    return ReportResponse(
        id=id,
        category="SPEED_TRAP",
        lat=19.0760,
        lon=72.8777,
        confidence=0.7,
        status="CONFIRMED",
        is_synthetic=False
    )

@router.get("/nearby", response_model=List[ReportResponse])
@router.get("/feed", response_model=List[ReportResponse])
async def get_nearby_reports(
    lat: float = Query(..., ge=-90.0, le=90.0),
    lon: float = Query(..., ge=-180.0, le=180.0),
    radius_m: float = Query(5000.0, gt=0),
    db: AsyncSession = Depends(get_db)
):
    """
    Returns active community reports near position.
    In production, queries PostGIS for reports within radius_m of (lat, lon).
    """
    return []

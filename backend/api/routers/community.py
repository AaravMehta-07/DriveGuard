from fastapi import APIRouter, Depends, Query, HTTPException, status, Request
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
import time

from backend.api.dependencies import get_db, get_current_user
from backend.community.processor import ReportProcessor
from backend.community.trust import ReporterTrustEngine

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
    # Filter valid requests within the window
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
        
    processor = ReportProcessor(db)
    trust_engine = ReporterTrustEngine(db)
    
    # 1. Check abuse flags
    is_abusive = await trust_engine.check_abuse(user.id, req)
    if is_abusive:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Report flagged for abuse")
        
    # 2. Calculate trust
    reporter_trust = await trust_engine.get_trust_score(user.id)
    
    # 3. Dedupe and save
    report = await processor.process_new_report(
        user_id=user.id,
        trust_score=reporter_trust,
        report_data=req
    )
    
    return report

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
        
    processor = ReportProcessor(db)
    trust_engine = ReporterTrustEngine(db)
    
    is_abusive = await trust_engine.check_confirmation_abuse(user.id, id)
    if is_abusive:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Action flagged for abuse")
        
    reporter_trust = await trust_engine.get_trust_score(user.id)
    updated_report = await processor.process_confirmation(
        report_id=id,
        user_id=user.id,
        trust_score=reporter_trust,
        status=req.status
    )
    
    if not updated_report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
        
    return updated_report

@router.get("/nearby", response_model=List[ReportResponse])
async def get_nearby_reports(
    lat: float = Query(..., ge=-90.0, le=90.0),
    lon: float = Query(..., ge=-180.0, le=180.0),
    radius_m: float = Query(5000.0, gt=0),
    db: AsyncSession = Depends(get_db)
):
    """
    Returns active community reports near position.
    """
    processor = ReportProcessor(db)
    reports = await processor.get_active_reports_nearby(
        lat=lat,
        lon=lon,
        radius_m=radius_m
    )
    return reports

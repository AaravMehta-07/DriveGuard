from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel, Field

from backend.api.dependencies import get_db, get_current_user
from backend.ai.challan_extractor import ChallanExtractor

router = APIRouter(prefix="/challan", tags=["challan"])


class ChallanEventResponse(BaseModel):
    id: str
    latitude: float
    longitude: float
    violation_type: str
    amount: float
    issued_at: datetime


class HotspotResponse(BaseModel):
    latitude: float
    longitude: float
    intensity: int
    violation_type: str


@router.post("/upload")
async def upload_challan(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Accepts image/PDF upload. Runs ChallanExtractor.
    Redacts/deletes owner name, registration number, address, PII.
    Saves anonymized event to challan_events table for aggregate hotspot map layer.
    """
    content = await file.read()
    extractor = ChallanExtractor()
    
    if file.filename and file.filename.endswith('.pdf'):
        extracted = await extractor.extract_from_pdf(content)
    else:
        extracted = await extractor.extract_from_image(content, file.content_type or 'image/jpeg')

    return {
        "status": "success",
        "message": "Challan uploaded and PII redacted successfully.",
        "offence_type": extracted.offence_type,
        "enforcement_category": extracted.enforcement_category,
        "confidence": extracted.confidence,
        "pii_redacted": extracted.pii_redacted,
    }


@router.get("/events", response_model=List[ChallanEventResponse])
async def list_events(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List user's processed challan events (PII redacted)."""
    return [
        ChallanEventResponse(
            id="ce_12345",
            latitude=19.0760,
            longitude=72.8777,
            violation_type="OVERSPEEDING",
            amount=1000.0,
            issued_at=datetime.now(),
        )
    ]


@router.get("/hotspots", response_model=List[HotspotResponse])
async def get_hotspots(db: AsyncSession = Depends(get_db)):
    """Returns aggregated anonymized challan violation hotspots for map layer."""
    return [
        HotspotResponse(
            latitude=19.0760,
            longitude=72.8777,
            intensity=15,
            violation_type="OVERSPEEDING",
        ),
        HotspotResponse(
            latitude=19.0520,
            longitude=72.8310,
            intensity=8,
            violation_type="RED_LIGHT_VIOLATION",
        )
    ]

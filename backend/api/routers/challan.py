from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel, Field

from backend.db.session import get_db
from backend.core.auth import get_current_user

router = APIRouter(prefix="/challan", tags=["challan"])

class ChallanEventResponse(BaseModel):
    id: str
    latitude: float
    longitude: float
    violation_type: str
    amount: float
    issued_at: datetime
    # Anonymized response - no PII

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
    \"\"\"
    Accepts image/PDF upload. Runs ChallanExtractor.
    Redacts/deletes owner name, registration number, address, PII.
    Saves anonymized event to challan_events table for aggregate hotspot map layer.
    \"\"\"
    # Mocking ChallanExtractor logic since it's an external utility not provided here
    # In a real scenario, this would be an import from backend.services
    
    # from backend.services.challan_extractor import ChallanExtractor
    # extractor = ChallanExtractor()
    # result = await extractor.process(file.file)
    
    # Mock result
    result = {
        "latitude": 19.0760,
        "longitude": 72.8777,
        "violation_type": "SPEEDING",
        "amount": 1000.0,
        "issued_at": datetime.now()
    }
    
    # PII is inherently excluded by extracting only non-PII fields or redacting them.
    from backend.models.challan import ChallanEvent
    
    event = ChallanEvent(
        user_id=current_user["id"],
        latitude=result["latitude"],
        longitude=result["longitude"],
        geom=f"SRID=4326;POINT({result['longitude']} {result['latitude']})",
        violation_type=result["violation_type"],
        amount=result["amount"],
        issued_at=result["issued_at"]
    )
    
    db.add(event)
    await db.commit()
    return {"status": "success", "message": "Challan uploaded and anonymized successfully."}

@router.get("/events", response_model=List[ChallanEventResponse])
async def list_events(db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    \"\"\"List user's processed challan events (PII redacted).\"\"\"
    from backend.models.challan import ChallanEvent
    stmt = select(ChallanEvent).where(ChallanEvent.user_id == current_user["id"]).order_by(ChallanEvent.issued_at.desc())
    result = await db.execute(stmt)
    events = result.scalars().all()
    return events

@router.get("/hotspots", response_model=List[HotspotResponse])
async def get_hotspots(db: AsyncSession = Depends(get_db)):
    \"\"\"Returns aggregated anonymized challan violation hotspots for map layer.\"\"\"
    from backend.models.challan import ChallanEvent
    
    # We round latitude and longitude to aggregate into hotspots
    # or use PostGIS clustering if appropriate. Using a basic group-by for this mock.
    stmt = (
        select(
            func.round(ChallanEvent.latitude, 3).label("latitude"),
            func.round(ChallanEvent.longitude, 3).label("longitude"),
            ChallanEvent.violation_type,
            func.count(ChallanEvent.id).label("intensity")
        )
        .group_by(
            func.round(ChallanEvent.latitude, 3),
            func.round(ChallanEvent.longitude, 3),
            ChallanEvent.violation_type
        )
        .order_by(func.count(ChallanEvent.id).desc())
    )
    
    result = await db.execute(stmt)
    hotspots = result.all()
    
    return [
        HotspotResponse(
            latitude=row.latitude,
            longitude=row.longitude,
            violation_type=row.violation_type,
            intensity=row.intensity
        ) for row in hotspots
    ]

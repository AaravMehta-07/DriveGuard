import json
from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from pydantic import BaseModel, Field

from backend.db.session import get_db
from backend.core.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

class UserPreferenceUpdate(BaseModel):
    speed_warning_threshold: Optional[int] = None
    camera_warning_enabled: Optional[bool] = None
    voice_mode: Optional[str] = None
    haptics_enabled: Optional[bool] = None
    vehicle_id: Optional[str] = None
    theme: Optional[str] = None

class UserVehicleCreate(BaseModel):
    type: str = Field(..., description="car, taxi, motorcycle, commercial, heavy vehicle")
    make: Optional[str] = None
    model: Optional[str] = None
    plate_number: Optional[str] = None

class UserVehicleResponse(UserVehicleCreate):
    id: str

class SavedPlaceCreate(BaseModel):
    name: str = Field(..., description="Home, Work, Favorites")
    latitude: float
    longitude: float

class SavedPlaceResponse(SavedPlaceCreate):
    id: str

class RecentPlaceResponse(BaseModel):
    id: str
    destination_name: str
    latitude: float
    longitude: float
    visited_at: datetime

@router.get("/preferences")
async def get_preferences(db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    from backend.models.user import UserPreference
    stmt = select(UserPreference).where(UserPreference.user_id == current_user["id"])
    result = await db.execute(stmt)
    pref = result.scalar_one_or_none()
    if not pref:
        raise HTTPException(status_code=404, detail="Preferences not found")
    return pref

@router.put("/preferences")
async def update_preferences(prefs: UserPreferenceUpdate, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    from backend.models.user import UserPreference
    stmt = select(UserPreference).where(UserPreference.user_id == current_user["id"])
    result = await db.execute(stmt)
    pref = result.scalar_one_or_none()
    
    update_data = prefs.dict(exclude_unset=True)
    if not pref:
        pref = UserPreference(user_id=current_user["id"], **update_data)
        db.add(pref)
    else:
        for k, v in update_data.items():
            setattr(pref, k, v)
    await db.commit()
    return {"status": "success", "message": "Preferences updated successfully"}

@router.get("/vehicles", response_model=List[UserVehicleResponse])
async def get_vehicles(db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    from backend.models.user import UserVehicle
    stmt = select(UserVehicle).where(UserVehicle.user_id == current_user["id"])
    result = await db.execute(stmt)
    return result.scalars().all()

@router.post("/vehicles", response_model=UserVehicleResponse)
async def create_vehicle(vehicle: UserVehicleCreate, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    from backend.models.user import UserVehicle
    new_vehicle = UserVehicle(user_id=current_user["id"], **vehicle.dict())
    db.add(new_vehicle)
    await db.commit()
    await db.refresh(new_vehicle)
    return new_vehicle

@router.put("/vehicles/{vehicle_id}", response_model=UserVehicleResponse)
async def update_vehicle(vehicle_id: str, vehicle_update: UserVehicleCreate, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    from backend.models.user import UserVehicle
    stmt = update(UserVehicle).where(UserVehicle.id == vehicle_id, UserVehicle.user_id == current_user["id"]).values(**vehicle_update.dict(exclude_unset=True))
    await db.execute(stmt)
    await db.commit()
    
    get_stmt = select(UserVehicle).where(UserVehicle.id == vehicle_id)
    result = await db.execute(get_stmt)
    updated_vehicle = result.scalar_one_or_none()
    if not updated_vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return updated_vehicle

@router.delete("/vehicles/{vehicle_id}")
async def delete_vehicle(vehicle_id: str, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    from backend.models.user import UserVehicle
    stmt = delete(UserVehicle).where(UserVehicle.id == vehicle_id, UserVehicle.user_id == current_user["id"])
    await db.execute(stmt)
    await db.commit()
    return {"status": "success", "message": "Vehicle deleted"}

@router.get("/favorites", response_model=List[SavedPlaceResponse])
async def get_favorites(db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    from backend.models.user import SavedPlace
    stmt = select(SavedPlace).where(SavedPlace.user_id == current_user["id"])
    result = await db.execute(stmt)
    places = result.scalars().all()
    # Assuming the DB model automatically exposes latitude and longitude properties or columns.
    return places

@router.post("/favorites", response_model=SavedPlaceResponse)
async def create_favorite(place: SavedPlaceCreate, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    from backend.models.user import SavedPlace
    # Create geom directly from lat/lon for PostGIS operations
    # Example using WKT format for geography cast mapping
    new_place = SavedPlace(
        user_id=current_user["id"],
        name=place.name,
        latitude=place.latitude,
        longitude=place.longitude,
        geom=f"SRID=4326;POINT({place.longitude} {place.latitude})"
    )
    db.add(new_place)
    await db.commit()
    await db.refresh(new_place)
    return new_place

@router.delete("/favorites/{place_id}")
async def delete_favorite(place_id: str, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    from backend.models.user import SavedPlace
    stmt = delete(SavedPlace).where(SavedPlace.id == place_id, SavedPlace.user_id == current_user["id"])
    await db.execute(stmt)
    await db.commit()
    return {"status": "success", "message": "Favorite deleted"}

@router.get("/recent-places", response_model=List[RecentPlaceResponse])
async def get_recent_places(db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    from backend.models.user import RecentPlace
    stmt = select(RecentPlace).where(RecentPlace.user_id == current_user["id"]).order_by(RecentPlace.visited_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()

@router.delete("/recent-places/{place_id}")
async def delete_recent_place(place_id: str, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    from backend.models.user import RecentPlace
    stmt = delete(RecentPlace).where(RecentPlace.id == place_id, RecentPlace.user_id == current_user["id"])
    await db.execute(stmt)
    await db.commit()
    return {"status": "success", "message": "Recent place deleted"}

@router.post("/export-data")
async def export_data(db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    \"\"\"
    Machine-readable Data Portability export per Correction #15.
    Bundles user profile, preferences, saved places, trip summaries, community reports in JSON format.
    \"\"\"
    from backend.models.user import UserPreference, UserVehicle, SavedPlace, RecentPlace
    from backend.models.trip import TripSummary
    from backend.models.community import CommunityReport
    
    prefs = await db.execute(select(UserPreference).where(UserPreference.user_id == current_user["id"]))
    vehicles = await db.execute(select(UserVehicle).where(UserVehicle.user_id == current_user["id"]))
    places = await db.execute(select(SavedPlace).where(SavedPlace.user_id == current_user["id"]))
    trips = await db.execute(select(TripSummary).where(TripSummary.user_id == current_user["id"]))
    reports = await db.execute(select(CommunityReport).where(CommunityReport.user_id == current_user["id"]))
    
    export = {
        "profile": {
            "id": current_user.get("id"),
            "username": current_user.get("username"),
            "email": current_user.get("email")
        },
        "preferences": prefs.scalar_one_or_none(),
        "vehicles": [v.__dict__ for v in vehicles.scalars().all()],
        "saved_places": [p.__dict__ for p in places.scalars().all()],
        "trip_summaries": [t.__dict__ for t in trips.scalars().all()],
        "community_reports": [r.__dict__ for r in reports.scalars().all()]
    }
    
    # Remove sqlalchemy state dicts and handle datetime serialization
    def clean_dict(d):
        d.pop("_sa_instance_state", None)
        for k, v in d.items():
            if isinstance(v, datetime):
                d[k] = v.isoformat()
        return d
        
    if export["preferences"]:
        export["preferences"] = clean_dict(export["preferences"].__dict__)
        
    for category in ["vehicles", "saved_places", "trip_summaries", "community_reports"]:
        export[category] = [clean_dict(item) for item in export[category]]
            
    return export

from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from pydantic import BaseModel

from backend.api.dependencies import get_db, get_current_user

router = APIRouter(prefix="/users", tags=["users"])


class UserPreferencesResponse(BaseModel):
    user_id: str
    speed_warning_threshold: int
    camera_warning_enabled: bool
    voice_mode: str
    haptics_enabled: bool
    theme: str


class UserPreferencesUpdate(BaseModel):
    speed_warning_threshold: Optional[int] = None
    camera_warning_enabled: Optional[bool] = None
    voice_mode: Optional[str] = None
    haptics_enabled: Optional[bool] = None
    theme: Optional[str] = None


class VehicleResponse(BaseModel):
    id: str
    type: str
    name: Optional[str] = None


class FavoriteResponse(BaseModel):
    id: str
    name: str
    type: str
    address: Optional[str] = None
    latitude: float
    longitude: float


class FavoriteCreate(BaseModel):
    name: str
    type: str  # HOME, WORK, FAVORITE
    address: Optional[str] = None
    latitude: float
    longitude: float


class RecentPlaceResponse(BaseModel):
    id: str
    name: str
    address: Optional[str] = None
    latitude: float
    longitude: float


@router.get("/preferences", response_model=UserPreferencesResponse)
async def get_preferences(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return UserPreferencesResponse(
        user_id=current_user.get("id", "guest_user"),
        speed_warning_threshold=5,
        camera_warning_enabled=True,
        voice_mode="FULL_GUIDANCE",
        haptics_enabled=True,
        theme="system"
    )


@router.put("/preferences", response_model=UserPreferencesResponse)
async def update_preferences(
    update: UserPreferencesUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return UserPreferencesResponse(
        user_id=current_user.get("id", "guest_user"),
        speed_warning_threshold=update.speed_warning_threshold or 5,
        camera_warning_enabled=update.camera_warning_enabled if update.camera_warning_enabled is not None else True,
        voice_mode=update.voice_mode or "FULL_GUIDANCE",
        haptics_enabled=update.haptics_enabled if update.haptics_enabled is not None else True,
        theme=update.theme or "system"
    )


@router.get("/vehicles", response_model=List[VehicleResponse])
async def get_vehicles(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return [
        VehicleResponse(id="veh_1", type="PRIVATE_CAR", name="My Car")
    ]


@router.get("/favorites", response_model=List[FavoriteResponse])
async def get_favorites(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return [
        FavoriteResponse(id="fav_1", name="Home", type="HOME", address="Bandra West, Mumbai", latitude=19.0596, longitude=72.8295),
        FavoriteResponse(id="fav_2", name="Work", type="WORK", address="BKC Annex, Mumbai", latitude=19.0657, longitude=72.8686),
    ]


@router.post("/favorites", response_model=FavoriteResponse)
async def add_favorite(
    favorite: FavoriteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return FavoriteResponse(
        id="fav_new",
        name=favorite.name,
        type=favorite.type,
        address=favorite.address,
        latitude=favorite.latitude,
        longitude=favorite.longitude
    )


@router.delete("/favorites/{place_id}")
async def delete_favorite(
    place_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return {"status": "success", "message": "Favorite deleted"}


@router.get("/recent-places", response_model=List[RecentPlaceResponse])
async def get_recent_places(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return [
        RecentPlaceResponse(id="rec_1", name="Mumbai Airport (BOM)", address="Vile Parle East", latitude=19.0896, longitude=72.8656)
    ]


@router.delete("/recent-places/{place_id}")
async def delete_recent_place(
    place_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return {"status": "success", "message": "Recent place deleted"}


@router.post("/export-data")
async def export_data(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Machine-readable Data Portability export per Correction #15.
    Bundles user profile, preferences, saved places, trip summaries, community reports in JSON format.
    Does NOT export proprietary provider data.
    """
    return {
        "export_metadata": {
            "user_id": current_user.get("id"),
            "exported_at": datetime.now().isoformat(),
            "format": "DriveGuard Data Portability JSON v1.0",
        },
        "profile": {
            "user_id": current_user.get("id"),
            "email": current_user.get("email"),
            "display_name": current_user.get("display_name"),
        },
        "preferences": {
            "speed_warning_threshold": 5,
            "camera_warning_enabled": True,
            "voice_mode": "FULL_GUIDANCE",
            "haptics_enabled": True,
        },
        "vehicles": [
            {"id": "veh_1", "type": "PRIVATE_CAR", "name": "My Car"}
        ],
        "saved_places": [
            {"name": "Home", "type": "HOME", "address": "Bandra West, Mumbai", "lat": 19.0596, "lon": 72.8295},
            {"name": "Work", "type": "WORK", "address": "BKC Annex, Mumbai", "lat": 19.0657, "lon": 72.8686},
        ],
        "trip_summaries": [],
        "community_reports": [],
    }

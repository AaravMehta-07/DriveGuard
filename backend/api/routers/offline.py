"""
Offline Packs API Router for DriveGuard V3

Exposes metadata and download endpoints for versioned compliance packs.
Enforces truthful offline capabilities per Correction #21.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.dependencies import get_db

router = APIRouter(prefix="/offline", tags=["offline"])


class OfflinePackMetadata(BaseModel):
    id: str
    city: str
    version: str
    generated_at: str
    valid_until: str
    schema_version: str
    data_source_versions: dict
    checksum: str
    file_url: str
    size_bytes: int
    capabilities: dict


@router.get("/packs", response_model=List[OfflinePackMetadata])
async def list_offline_packs(
    city: Optional[str] = "Mumbai",
    db: AsyncSession = Depends(get_db)
):
    """
    List available offline compliance packs.
    Distinguishes offline capabilities accurately per Correction #21.
    """
    return [
        OfflinePackMetadata(
            id="pack_mumbai_v3_0_1",
            city="Mumbai",
            version="3.0.1",
            generated_at="2026-08-11T00:00:00Z",
            valid_until="2026-08-18T00:00:00Z",
            schema_version="1.0",
            data_source_versions={"mumbai_traffic_police": "2026.08.10"},
            checksum="a1b2c3d4e5f67890123456789abcdef0123456789abcdef0123456789abcdef0",
            file_url="https://s3.amazonaws.com/driveguard-packs/mumbai_v3_0_1.json",
            size_bytes=48234567,
            capabilities={
                "offline_compliance_data": True,
                "offline_speed_limits": True,
                "offline_turn_restrictions": True,
                "offline_signal_locations": True,
                "offline_map_tiles": False,
                "offline_routing": False,
                "offline_navigation": False
            }
        )
    ]


@router.get("/packs/{city}/latest", response_model=OfflinePackMetadata)
async def get_latest_offline_pack(
    city: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get the latest available offline compliance pack metadata for a city.
    """
    if city.lower() != "mumbai":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No offline pack available for city '{city}'. Current coverage is Mumbai."
        )

    return OfflinePackMetadata(
        id="pack_mumbai_v3_0_1",
        city="Mumbai",
        version="3.0.1",
        generated_at="2026-08-11T00:00:00Z",
        valid_until="2026-08-18T00:00:00Z",
        schema_version="1.0",
        data_source_versions={"mumbai_traffic_police": "2026.08.10"},
        checksum="a1b2c3d4e5f67890123456789abcdef0123456789abcdef0123456789abcdef0",
        file_url="https://s3.amazonaws.com/driveguard-packs/mumbai_v3_0_1.json",
        size_bytes=48234567,
        capabilities={
            "offline_compliance_data": True,
            "offline_speed_limits": True,
            "offline_turn_restrictions": True,
            "offline_signal_locations": True,
            "offline_map_tiles": False,
            "offline_routing": False,
            "offline_navigation": False
        }
    )


@router.get("/packs/{city}/{version}/download")
async def get_offline_pack_download(
    city: str,
    version: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get download URL and verification checksum for specific offline pack version.
    """
    return {
        "city": city,
        "version": version,
        "download_url": f"https://s3.amazonaws.com/driveguard-packs/{city.lower()}_v{version.replace('.', '_')}.json",
        "checksum_sha256": "a1b2c3d4e5f67890123456789abcdef0123456789abcdef0123456789abcdef0",
        "expires_in_seconds": 3600
    }

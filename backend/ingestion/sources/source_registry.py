from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.sources import DataSource

class SourceRegistry:
    """
    Registry for populating and managing legitimate data sources in the data_sources table.
    """
    
    SOURCES = [
        {
            "name": "mumbai_traffic_police",
            "provider": "Mumbai Traffic Police",
            "license_type": "official",
            "base_confidence": 0.95,
            "render_allowed": True,
            "cache_allowed": True,
            "persistent_storage_allowed": True,
            "derived_storage_allowed": True,
            "redistribution_allowed": False,
            "overlay_allowed": True,
            "cross_provider_display_allowed": True
        },
        {
            "name": "maharashtra_authorities",
            "provider": "Maharashtra State Authorities",
            "license_type": "official",
            "base_confidence": 0.95,
            "render_allowed": True,
            "cache_allowed": True,
            "persistent_storage_allowed": True,
            "derived_storage_allowed": True,
            "redistribution_allowed": False,
            "overlay_allowed": True,
            "cross_provider_display_allowed": True
        },
        {
            "name": "bmc_mcgm",
            "provider": "BMC / MCGM",
            "license_type": "official",
            "base_confidence": 0.9,
            "render_allowed": True,
            "cache_allowed": True,
            "persistent_storage_allowed": True,
            "derived_storage_allowed": True,
            "redistribution_allowed": False,
            "overlay_allowed": True,
            "cross_provider_display_allowed": True
        },
        {
            "name": "government_open_data",
            "provider": "Government Open Data Portal",
            "license_type": "open_data",
            "base_confidence": 0.85,
            "render_allowed": True,
            "cache_allowed": True,
            "persistent_storage_allowed": True,
            "derived_storage_allowed": True,
            "redistribution_allowed": True,
            "overlay_allowed": True,
            "cross_provider_display_allowed": True
        },
        {
            "name": "osm",
            "provider": "OpenStreetMap",
            "license_type": "odbl",
            "base_confidence": 0.7,
            "render_allowed": True,
            "cache_allowed": True,
            "persistent_storage_allowed": True,
            "derived_storage_allowed": True,
            "redistribution_allowed": True,
            "overlay_allowed": True,
            "cross_provider_display_allowed": True
        },
        {
            "name": "community_reports",
            "provider": "DriveGuard Community",
            "license_type": "ugc",
            "base_confidence": 0.5,
            "render_allowed": True,
            "cache_allowed": True,
            "persistent_storage_allowed": True,
            "derived_storage_allowed": True,
            "redistribution_allowed": True,
            "overlay_allowed": True,
            "cross_provider_display_allowed": True
        }
    ]

    def __init__(self, db: AsyncSession):
        self.db = db

    async def initialize_sources(self):
        """
        Populate the data_sources table with known legitimate sources if they do not exist.
        """
        for source_data in self.SOURCES:
            stmt = select(DataSource).where(DataSource.name == source_data["name"])
            result = await self.db.execute(stmt)
            existing = result.scalar_one_or_none()
            
            if not existing:
                new_source = DataSource(
                    name=source_data["name"],
                    provider=source_data["provider"],
                    render_allowed=source_data["render_allowed"],
                    cache_allowed=source_data["cache_allowed"],
                    persistent_storage_allowed=source_data["persistent_storage_allowed"],
                    derived_storage_allowed=source_data["derived_storage_allowed"],
                    redistribution_allowed=source_data["redistribution_allowed"],
                    overlay_allowed=source_data["overlay_allowed"],
                    cross_provider_display_allowed=source_data["cross_provider_display_allowed"]
                )
                self.db.add(new_source)
                
        await self.db.commit()

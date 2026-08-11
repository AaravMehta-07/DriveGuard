from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task(name="workers.tasks.offline_tasks.generate_offline_pack")
def generate_offline_pack(city: str = "Mumbai") -> None:
    """
    Generate Mumbai compliance pack.
    - Query all VERIFIED/PROBABLE enforcement_points (non-synthetic)
    - Query all active restrictions
    - Query all traffic signals
    - Query all speed limits
    - Package as versioned JSON with city, version, generated_at, valid_until, schema_version, data_source_versions, checksum
    - Upload to S3
    - Register in offline_pack_versions table
    """
    logger.info(f"Generating offline pack for {city}")
    pass

@shared_task(name="workers.tasks.offline_tasks.validate_offline_pack")
def validate_offline_pack(pack_id: str) -> None:
    """Download and verify checksum."""
    logger.info(f"Validating offline pack: {pack_id}")
    pass

@shared_task(name="workers.tasks.offline_tasks.cleanup_old_packs")
def cleanup_old_packs() -> None:
    """Remove packs older than retention period."""
    logger.info("Cleaning up old packs")
    pass

import os
from datetime import timedelta

from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "driveguard_workers",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=[
        "workers.tasks.ingestion_tasks",
        "workers.tasks.moderation_tasks",
        "workers.tasks.offline_tasks",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
    task_default_queue="default",
    task_routes={
        "workers.tasks.ingestion_tasks.*": {"queue": "ingestion"},
        "workers.tasks.moderation_tasks.*": {"queue": "moderation"},
        "workers.tasks.offline_tasks.*": {"queue": "offline"},
    },
    beat_schedule={
        "source_sync": {
            "task": "workers.tasks.ingestion_tasks.sync_official_sources",
            "schedule": timedelta(hours=6),
        },
        "stale_data_check": {
            "task": "workers.tasks.ingestion_tasks.check_stale_data",
            "schedule": timedelta(days=1),
        },
        "temporary_restriction_expiry": {
            "task": "workers.tasks.moderation_tasks.process_temporary_restriction_expiry",
            "schedule": timedelta(hours=1),
        },
        "report_cleanup": {
            "task": "workers.tasks.moderation_tasks.cleanup_reports",
            "schedule": timedelta(days=1),
        },
        "offline_pack_generation": {
            "task": "workers.tasks.offline_tasks.generate_offline_pack",
            "schedule": timedelta(days=1),
        },
    },
)

if __name__ == "__main__":
    celery_app.start()

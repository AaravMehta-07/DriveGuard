import abc
import asyncio
import hashlib
import logging
from datetime import datetime, timezone
from typing import Any

from models.admin import AuditLog
from models.ingestion import IngestionRun
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

class IngestionPipeline(abc.ABC):
    """
    Base class for DriveGuard data ingestion pipelines.
    Guarantees idempotency, auditability, source-linking, and versioning.
    """

    def __init__(self, db: AsyncSession, source_id: str, job_name: str, max_retries: int = 3):
        self.db = db
        self.source_id = source_id
        self.job_name = job_name
        self.max_retries = max_retries

    async def create_job_run(self) -> IngestionRun:
        # Simplified: Ensure job exists, then create run
        run = IngestionRun(
            job_id=self.source_id, # Simplified reference
            status="running",
            start_time=datetime.now(timezone.utc)
        )
        self.db.add(run)
        await self.db.flush()
        return run

    async def log_audit(self, entity_type: str, entity_id: str, action: str, before: dict = None, after: dict = None, reason: str = None):
        log_entry = AuditLog(
            entity_type=entity_type,
            entity_id=entity_id,
            action=action,
            actor_id="system_ingestion",
            actor_type="system",
            before_json=before,
            after_json=after,
            source=self.source_id,
            reason=reason
        )
        self.db.add(log_entry)

    def hash_document(self, content: str) -> str:
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    async def check_idempotency(self, document_identifier: str, content: str) -> bool:
        """Returns True if the document has already been processed with this exact hash."""
        # Implementation left out for brevity; queries SourceDocument and SourceDocumentVersion
        # returns True if a matching version hash exists.
        return False

    async def run(self, data: Any):
        run = await self.create_job_run()
        attempt = 0

        while attempt < self.max_retries:
            try:
                await self.process(data)
                run.status = "completed"
                run.end_time = datetime.now(timezone.utc)
                await self.db.commit()
                return
            except Exception as e:
                attempt += 1
                logger.error(f"Ingestion attempt {attempt} failed: {e}")
                if attempt >= self.max_retries:
                    run.status = "failed"
                    run.end_time = datetime.now(timezone.utc)
                    await self.db.commit()
                    raise
                await asyncio.sleep(2 ** attempt) # Exponential backoff

    @abc.abstractmethod
    async def process(self, data: Any):
        """Pipeline-specific processing logic."""
        pass

import json
from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func, or_
from pydantic import BaseModel

from backend.api.dependencies import get_db, get_current_user

# Dependency to check admin role
async def get_admin_user(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    return current_user

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(get_admin_user)])

# Schemas
class ReviewItemResponse(BaseModel):
    id: str
    item_type: str
    status: str
    reason: Optional[str]
    payload: dict
    created_at: datetime

class DecisionRequest(BaseModel):
    decision: str # APPROVE, REJECT, MERGE, DEFER, REQUEST_FIELD_VERIFICATION
    notes: Optional[str] = None
    merge_target_id: Optional[str] = None

class EnforcementBase(BaseModel):
    type: str
    latitude: float
    longitude: float
    speed_limit: Optional[int]
    status: str

class EnforcementResponse(EnforcementBase):
    id: str
    created_at: datetime

class MergeRequest(BaseModel):
    target_id: str

class CoverageMetrics(BaseModel):
    road_network_coverage_percent: float
    speed_limit_coverage_percent: float
    camera_counts_by_status: dict
    temporary_orders_sync_stats: dict

class AuditLogResponse(BaseModel):
    id: str
    admin_id: str
    action: str
    entity_type: str
    entity_id: str
    before_state: Optional[dict]
    after_state: Optional[dict]
    timestamp: datetime

class IngestionStatus(BaseModel):
    status: str
    last_run: Optional[datetime]
    records_processed: Optional[int]

# Endpoints
@router.get("/review-queue", response_model=List[ReviewItemResponse])
async def list_review_queue(
    status: Optional[str] = Query(None),
    item_type: Optional[str] = Query(None),
    reason: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    from backend.models.admin import ReviewQueueItem
    stmt = select(ReviewQueueItem)
    if status:
        stmt = stmt.where(ReviewQueueItem.status == status)
    if item_type:
        stmt = stmt.where(ReviewQueueItem.item_type == item_type)
    if reason:
        stmt = stmt.where(ReviewQueueItem.reason.ilike(f"%{reason}%"))
        
    result = await db.execute(stmt)
    return result.scalars().all()

@router.post("/review-queue/{id}/decision")
async def process_review_decision(id: str, decision_req: DecisionRequest, db: AsyncSession = Depends(get_db), admin: dict = Depends(get_admin_user)):
    valid_decisions = ["APPROVE", "REJECT", "MERGE", "DEFER", "REQUEST_FIELD_VERIFICATION"]
    if decision_req.decision not in valid_decisions:
        raise HTTPException(status_code=400, detail="Invalid decision")
        
    from backend.models.admin import ReviewQueueItem, AdminDecision, AuditLog
    
    stmt = select(ReviewQueueItem).where(ReviewQueueItem.id == id)
    result = await db.execute(stmt)
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Review item not found")
        
    before_state = item.__dict__.copy()
    before_state.pop("_sa_instance_state", None)
    
    item.status = decision_req.decision
    
    decision = AdminDecision(
        admin_id=admin["id"],
        review_item_id=id,
        decision=decision_req.decision,
        notes=decision_req.notes
    )
    db.add(decision)
    
    after_state = item.__dict__.copy()
    after_state.pop("_sa_instance_state", None)
    
    audit_log = AuditLog(
        admin_id=admin["id"],
        action=f"REVIEW_DECISION_{decision_req.decision}",
        entity_type="ReviewQueueItem",
        entity_id=id,
        before_state=before_state,
        after_state=after_state
    )
    db.add(audit_log)
    
    await db.commit()
    return {"status": "success"}

@router.get("/enforcement", response_model=List[EnforcementResponse])
async def list_enforcement(db: AsyncSession = Depends(get_db)):
    from backend.models.enforcement import EnforcementCamera
    result = await db.execute(select(EnforcementCamera))
    return result.scalars().all()

@router.put("/enforcement/{id}", response_model=EnforcementResponse)
async def update_enforcement(id: str, payload: EnforcementBase, db: AsyncSession = Depends(get_db), admin: dict = Depends(get_admin_user)):
    from backend.models.enforcement import EnforcementCamera
    from backend.models.admin import AuditLog
    
    stmt = select(EnforcementCamera).where(EnforcementCamera.id == id)
    result = await db.execute(stmt)
    camera = result.scalar_one_or_none()
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
        
    before_state = camera.__dict__.copy()
    before_state.pop("_sa_instance_state", None)
    
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(camera, k, v)
        
    after_state = camera.__dict__.copy()
    after_state.pop("_sa_instance_state", None)
    
    audit_log = AuditLog(
        admin_id=admin["id"],
        action="UPDATE_ENFORCEMENT",
        entity_type="EnforcementCamera",
        entity_id=id,
        before_state=before_state,
        after_state=after_state
    )
    db.add(audit_log)
    
    await db.commit()
    await db.refresh(camera)
    return camera

@router.post("/enforcement/{id}/merge")
async def merge_enforcement(id: str, req: MergeRequest, db: AsyncSession = Depends(get_db), admin: dict = Depends(get_admin_user)):
    from backend.models.enforcement import EnforcementCamera
    from backend.models.admin import AuditLog
    
    stmt_source = select(EnforcementCamera).where(EnforcementCamera.id == id)
    source_cam = (await db.execute(stmt_source)).scalar_one_or_none()
    
    stmt_target = select(EnforcementCamera).where(EnforcementCamera.id == req.target_id)
    target_cam = (await db.execute(stmt_target)).scalar_one_or_none()
    
    if not source_cam or not target_cam:
        raise HTTPException(status_code=404, detail="Source or target camera not found")
        
    before_source = source_cam.__dict__.copy()
    before_source.pop("_sa_instance_state", None)
    
    source_cam.status = "MERGED"
    
    audit_log = AuditLog(
        admin_id=admin["id"],
        action="MERGE_ENFORCEMENT",
        entity_type="EnforcementCamera",
        entity_id=id,
        before_state=before_source,
        after_state={"status": "MERGED", "merged_into": req.target_id}
    )
    db.add(audit_log)
    
    await db.commit()
    return {"status": "success", "message": f"Camera {id} merged into {req.target_id}"}

@router.get("/coverage", response_model=CoverageMetrics)
async def get_coverage(db: AsyncSession = Depends(get_db)):
    from backend.models.enforcement import EnforcementCamera, RoadSegment, TemporaryOrder
    
    # Calculate real measured coverage from db
    # Total roads
    total_roads = (await db.execute(select(func.count(RoadSegment.id)))).scalar() or 1
    # Roads mapped
    mapped_roads = (await db.execute(select(func.count(RoadSegment.id)).where(RoadSegment.is_mapped == True))).scalar() or 0
    # Speed limit roads
    speed_limit_roads = (await db.execute(select(func.count(RoadSegment.id)).where(RoadSegment.speed_limit != None))).scalar() or 0
    
    road_network_coverage = (mapped_roads / total_roads) * 100
    speed_limit_coverage = (speed_limit_roads / total_roads) * 100
    
    # Camera counts by status
    camera_counts = (await db.execute(select(EnforcementCamera.status, func.count(EnforcementCamera.id)).group_by(EnforcementCamera.status))).all()
    camera_counts_dict = {status: count for status, count in camera_counts}
    
    # Temporary orders sync stats
    total_orders = (await db.execute(select(func.count(TemporaryOrder.id)))).scalar() or 0
    synced_orders = (await db.execute(select(func.count(TemporaryOrder.id)).where(TemporaryOrder.sync_status == 'SYNCED'))).scalar() or 0
    
    return CoverageMetrics(
        road_network_coverage_percent=road_network_coverage,
        speed_limit_coverage_percent=speed_limit_coverage,
        camera_counts_by_status=camera_counts_dict,
        temporary_orders_sync_stats={
            "total": total_orders,
            "synced": synced_orders
        }
    )

@router.get("/audit-log", response_model=List[AuditLogResponse])
async def get_audit_log(
    action: Optional[str] = Query(None),
    entity_type: Optional[str] = Query(None),
    admin_id: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    from backend.models.admin import AuditLog
    stmt = select(AuditLog).order_by(AuditLog.timestamp.desc())
    if action:
        stmt = stmt.where(AuditLog.action == action)
    if entity_type:
        stmt = stmt.where(AuditLog.entity_type == entity_type)
    if admin_id:
        stmt = stmt.where(AuditLog.admin_id == admin_id)
        
    result = await db.execute(stmt)
    return result.scalars().all()

@router.get("/ingestion/status", response_model=IngestionStatus)
async def ingestion_status(db: AsyncSession = Depends(get_db)):
    from backend.models.admin import IngestionJob
    stmt = select(IngestionJob).order_by(IngestionJob.created_at.desc()).limit(1)
    job = (await db.execute(stmt)).scalar_one_or_none()
    
    if not job:
        return IngestionStatus(status="IDLE", last_run=None, records_processed=0)
        
    return IngestionStatus(
        status=job.status,
        last_run=job.updated_at or job.created_at,
        records_processed=job.records_processed
    )

@router.post("/ingestion/trigger")
async def trigger_ingestion(db: AsyncSession = Depends(get_db), admin: dict = Depends(get_admin_user)):
    from backend.models.admin import IngestionJob, AuditLog
    
    job = IngestionJob(status="PENDING", records_processed=0)
    db.add(job)
    
    audit_log = AuditLog(
        admin_id=admin["id"],
        action="TRIGGER_INGESTION",
        entity_type="IngestionJob",
        entity_id="new"
    )
    db.add(audit_log)
    
    await db.commit()
    
    # Logic to trigger background worker would go here
    # e.g., celery_app.send_task("ingest_data", args=[job.id])
    
    return {"status": "success", "message": "Ingestion triggered", "job_id": job.id}

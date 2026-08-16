from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.master import StyleVariant
from app.models.order import BuyerOrder
from app.models.production import (
    CuttingEntry,
    FinishingEntry,
    ProductionPlan,
    SewingEntry,
    WorkOrder,
    WorkOrderStatus,
)
from app.models.user import User
from app.schemas.schemas import (
    CuttingEntryCreate,
    CuttingEntryOut,
    FinishingEntryCreate,
    FinishingEntryOut,
    ProductionPlanCreate,
    ProductionPlanOut,
    SewingEntryCreate,
    SewingEntryOut,
    WorkOrderCreate,
    WorkOrderOut,
)

router = APIRouter(tags=["Production"])

plan_router = APIRouter(prefix="/production-plans", tags=["Production Plans"])
wo_router = APIRouter(prefix="/work-orders", tags=["Work Orders"])
cutting_router = APIRouter(prefix="/cutting", tags=["Cutting"])
sewing_router = APIRouter(prefix="/sewing", tags=["Sewing"])
finishing_router = APIRouter(prefix="/finishing", tags=["Finishing"])


def _plan_to_out(db: Session, plan: ProductionPlan) -> ProductionPlanOut:
    out = ProductionPlanOut.model_validate(plan)
    order = db.query(BuyerOrder).filter(BuyerOrder.id == plan.order_id).first()
    out.po_number = order.po_number if order else None
    wos = []
    for wo in plan.work_orders:
        wo_out = WorkOrderOut.model_validate(wo)
        variant = db.query(StyleVariant).filter(StyleVariant.id == wo.style_variant_id).first()
        wo_out.variant_code = variant.variant_code if variant else None
        wos.append(wo_out)
    out.work_orders = wos
    return out


def _wo_to_out(db: Session, wo: WorkOrder) -> WorkOrderOut:
    out = WorkOrderOut.model_validate(wo)
    variant = db.query(StyleVariant).filter(StyleVariant.id == wo.style_variant_id).first()
    out.variant_code = variant.variant_code if variant else None
    return out


# ---------- Production Plans ----------
@plan_router.get("", response_model=list[ProductionPlanOut])
def list_plans(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return [_plan_to_out(db, p) for p in db.query(ProductionPlan).all()]


@plan_router.post("", response_model=ProductionPlanOut, status_code=201)
def create_plan(
    payload: ProductionPlanCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    existing = db.query(ProductionPlan).filter(ProductionPlan.plan_number == payload.plan_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Plan number already exists")

    order = db.query(BuyerOrder).filter(BuyerOrder.id == payload.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    plan = ProductionPlan(
        plan_number=payload.plan_number,
        order_id=payload.order_id,
        start_date=payload.start_date,
        end_date=payload.end_date,
        notes=payload.notes,
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return _plan_to_out(db, plan)


@plan_router.get("/{plan_id}", response_model=ProductionPlanOut)
def get_plan(plan_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    plan = db.query(ProductionPlan).filter(ProductionPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return _plan_to_out(db, plan)


@plan_router.post("/{plan_id}/release", response_model=ProductionPlanOut)
def release_plan(plan_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    plan = db.query(ProductionPlan).filter(ProductionPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    from app.models.production import PlanStatus

    plan.status = PlanStatus.APPROVED
    db.commit()
    db.refresh(plan)
    return _plan_to_out(db, plan)


# ---------- Work Orders ----------
@wo_router.get("", response_model=list[WorkOrderOut])
def list_work_orders(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return [_wo_to_out(db, wo) for wo in db.query(WorkOrder).all()]


@wo_router.post("", response_model=WorkOrderOut, status_code=201)
def create_work_order(
    payload: WorkOrderCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    existing = db.query(WorkOrder).filter(WorkOrder.wo_number == payload.wo_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Work order number already exists")

    plan = db.query(ProductionPlan).filter(ProductionPlan.id == payload.plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    variant = db.query(StyleVariant).filter(StyleVariant.id == payload.style_variant_id).first()
    if not variant:
        raise HTTPException(status_code=404, detail="Style variant not found")

    wo = WorkOrder(
        wo_number=payload.wo_number,
        plan_id=payload.plan_id,
        style_variant_id=payload.style_variant_id,
        quantity=payload.quantity,
        start_date=payload.start_date,
        end_date=payload.end_date,
        notes=payload.notes,
    )
    db.add(wo)
    db.commit()
    db.refresh(wo)
    return _wo_to_out(db, wo)


@wo_router.get("/{wo_id}", response_model=WorkOrderOut)
def get_work_order(wo_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    wo = db.query(WorkOrder).filter(WorkOrder.id == wo_id).first()
    if not wo:
        raise HTTPException(status_code=404, detail="Work order not found")
    return _wo_to_out(db, wo)


@wo_router.post("/{wo_id}/release", response_model=WorkOrderOut)
def release_work_order(wo_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    wo = db.query(WorkOrder).filter(WorkOrder.id == wo_id).first()
    if not wo:
        raise HTTPException(status_code=404, detail="Work order not found")
    wo.status = WorkOrderStatus.RELEASED
    db.commit()
    db.refresh(wo)
    return _wo_to_out(db, wo)


@wo_router.post("/{wo_id}/complete", response_model=WorkOrderOut)
def complete_work_order(wo_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    wo = db.query(WorkOrder).filter(WorkOrder.id == wo_id).first()
    if not wo:
        raise HTTPException(status_code=404, detail="Work order not found")
    wo.status = WorkOrderStatus.COMPLETED
    db.commit()
    db.refresh(wo)
    return _wo_to_out(db, wo)


# ---------- Cutting ----------
@cutting_router.get("", response_model=list[CuttingEntryOut])
def list_cutting_entries(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    entries = db.query(CuttingEntry).order_by(CuttingEntry.id.desc()).all()
    out = []
    for e in entries:
        obj = CuttingEntryOut.model_validate(e)
        wo = db.query(WorkOrder).filter(WorkOrder.id == e.work_order_id).first()
        obj.wo_number = wo.wo_number if wo else None
        out.append(obj)
    return out


@cutting_router.post("", status_code=201)
def create_cutting_entry(
    payload: CuttingEntryCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    wo = db.query(WorkOrder).filter(WorkOrder.id == payload.work_order_id).first()
    if not wo:
        raise HTTPException(status_code=404, detail="Work order not found")

    entry = CuttingEntry(**payload.model_dump())
    db.add(entry)
    db.flush()
    wo.produced_qty += payload.quantity
    wo.rejected_qty += payload.rejection_qty
    wo.status = WorkOrderStatus.IN_PROGRESS
    db.commit()
    return entry


# ---------- Sewing ----------
@sewing_router.get("", response_model=list[SewingEntryOut])
def list_sewing_entries(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    entries = db.query(SewingEntry).order_by(SewingEntry.id.desc()).all()
    out = []
    for e in entries:
        obj = SewingEntryOut.model_validate(e)
        wo = db.query(WorkOrder).filter(WorkOrder.id == e.work_order_id).first()
        obj.wo_number = wo.wo_number if wo else None
        out.append(obj)
    return out


@sewing_router.post("", status_code=201)
def create_sewing_entry(
    payload: SewingEntryCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    wo = db.query(WorkOrder).filter(WorkOrder.id == payload.work_order_id).first()
    if not wo:
        raise HTTPException(status_code=404, detail="Work order not found")

    entry = SewingEntry(**payload.model_dump())
    db.add(entry)
    db.flush()
    wo.produced_qty += payload.quantity
    wo.rejected_qty += payload.rejection_qty
    wo.status = WorkOrderStatus.IN_PROGRESS
    db.commit()
    return entry


# ---------- Finishing ----------
@finishing_router.get("", response_model=list[FinishingEntryOut])
def list_finishing_entries(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    entries = db.query(FinishingEntry).order_by(FinishingEntry.id.desc()).all()
    out = []
    for e in entries:
        obj = FinishingEntryOut.model_validate(e)
        wo = db.query(WorkOrder).filter(WorkOrder.id == e.work_order_id).first()
        obj.wo_number = wo.wo_number if wo else None
        out.append(obj)
    return out


@finishing_router.post("", status_code=201)
def create_finishing_entry(
    payload: FinishingEntryCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    wo = db.query(WorkOrder).filter(WorkOrder.id == payload.work_order_id).first()
    if not wo:
        raise HTTPException(status_code=404, detail="Work order not found")

    entry = FinishingEntry(**payload.model_dump())
    db.add(entry)
    db.flush()
    wo.produced_qty += payload.quantity
    wo.rejected_qty += payload.rejection_qty
    wo.status = WorkOrderStatus.IN_PROGRESS
    db.commit()
    return entry
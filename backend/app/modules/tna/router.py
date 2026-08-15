from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.order import BuyerOrder
from app.models.tna import TNAMilestone, TNAPlan, TNAStatus
from app.models.user import User
from app.schemas.schemas import TNAMilestoneOut, TNAPlanCreate, TNAPlanOut

router = APIRouter(prefix="/tna", tags=["TNA"])

DEFAULT_MILESTONES = [
    "Order Received",
    "Tech Pack",
    "Sample Submission",
    "Sample Approval",
    "Fabric Booking",
    "Fabric Received",
    "Accessories Received",
    "Cutting",
    "Sewing",
    "Finishing",
    "Final Inspection",
    "Packing",
    "Shipment",
]


def _update_milestone_status(milestone: TNAMilestone) -> None:
    if milestone.actual_date:
        milestone.status = TNAStatus.COMPLETED
    elif milestone.planned_date < date.today():
        milestone.status = TNAStatus.OVERDUE
    elif milestone.planned_date == date.today():
        milestone.status = TNAStatus.ON_TRACK
    else:
        milestone.status = TNAStatus.PENDING


def _to_out(db: Session, plan: TNAPlan) -> TNAPlanOut:
    out = TNAPlanOut.model_validate(plan)
    order = db.query(BuyerOrder).filter(BuyerOrder.id == plan.order_id).first()
    out.po_number = order.po_number if order else None
    milestones = []
    for m in plan.milestones:
        milestones.append(TNAMilestoneOut.model_validate(m))
    out.milestones = milestones
    return out


@router.get("/plans", response_model=list[TNAPlanOut])
def list_plans(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    plans = db.query(TNAPlan).all()
    for plan in plans:
        for m in plan.milestones:
            _update_milestone_status(m)
    db.commit()
    return [_to_out(db, p) for p in plans]


@router.post("/plans", response_model=TNAPlanOut, status_code=201)
def create_plan(
    payload: TNAPlanCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    order = db.query(BuyerOrder).filter(BuyerOrder.id == payload.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    plan = TNAPlan(
        order_id=payload.order_id,
        plan_name=payload.plan_name,
        notes=payload.notes,
    )
    db.add(plan)
    db.flush()

    milestones = payload.milestones if payload.milestones else []
    if not milestones:
        # Auto-create default milestones spread over days from order date to delivery date
        total_days = max((order.delivery_date - order.order_date).days, 1)
        for i, name in enumerate(DEFAULT_MILESTONES):
            planned = order.order_date + (order.delivery_date - order.order_date) * (i / len(DEFAULT_MILESTONES))
            milestones.append(
                TNAMilestone(
                    tna_plan_id=plan.id,
                    milestone_name=name,
                    planned_date=planned,
                )
            )
    else:
        for m_data in milestones:
            milestone = TNAMilestone(
                tna_plan_id=plan.id,
                milestone_name=m_data.milestone_name,
                planned_date=m_data.planned_date,
                responsible_person=m_data.responsible_person,
                remarks=m_data.remarks,
            )
            _update_milestone_status(milestone)
            db.add(milestone)

    db.commit()
    db.refresh(plan)
    return _to_out(db, plan)


@router.get("/plans/{plan_id}", response_model=TNAPlanOut)
def get_plan(plan_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    plan = db.query(TNAPlan).filter(TNAPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="TNA plan not found")
    for m in plan.milestones:
        _update_milestone_status(m)
    db.commit()
    return _to_out(db, plan)


@router.post("/milestones/{milestone_id}/complete", response_model=TNAMilestoneOut)
def complete_milestone(milestone_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    milestone = db.query(TNAMilestone).filter(TNAMilestone.id == milestone_id).first()
    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")
    milestone.actual_date = date.today()
    milestone.status = TNAStatus.COMPLETED
    db.commit()
    db.refresh(milestone)
    return TNAMilestoneOut.model_validate(milestone)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.master import Material
from app.models.material_requirement import MaterialRequirement
from app.models.order import BuyerOrder
from app.models.user import User
from app.schemas.schemas import MaterialRequirementOut
from app.services.material_requirement_service import calculate_material_requirements

router = APIRouter(prefix="/material-requirements", tags=["Material Requirements"])


def _to_out(db: Session, req: MaterialRequirement) -> MaterialRequirementOut:
    out = MaterialRequirementOut.model_validate(req)
    order = db.query(BuyerOrder).filter(BuyerOrder.id == req.order_id).first()
    material = db.query(Material).filter(Material.id == req.material_id).first()
    out.po_number = order.po_number if order else None
    out.material_code = material.code if material else None
    out.material_name = material.name if material else None
    out.category = material.category if material else None
    return out


@router.get("", response_model=list[MaterialRequirementOut])
def list_requirements(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    reqs = db.query(MaterialRequirement).all()
    return [_to_out(db, r) for r in reqs]


@router.post("/calculate/{order_id}", response_model=list[MaterialRequirementOut])
def calculate_for_order(order_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    order = db.query(BuyerOrder).filter(BuyerOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    try:
        reqs = calculate_material_requirements(db, order_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    db.commit()
    return [_to_out(db, r) for r in reqs]


@router.get("/order/{order_id}", response_model=list[MaterialRequirementOut])
def get_requirements_for_order(order_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    reqs = db.query(MaterialRequirement).filter(MaterialRequirement.order_id == order_id).all()
    return [_to_out(db, r) for r in reqs]
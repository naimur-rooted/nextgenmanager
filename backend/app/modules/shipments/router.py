from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.master import StyleVariant
from app.models.order import BuyerOrder
from app.models.shipment import Shipment, ShipmentItem, ShipmentStatus
from app.models.user import User
from app.schemas.schemas import ShipmentCreate, ShipmentItemOut, ShipmentOut

router = APIRouter(prefix="/shipments", tags=["Shipments"])


def _to_out(db: Session, shipment: Shipment) -> ShipmentOut:
    out = ShipmentOut.model_validate(shipment)
    order = db.query(BuyerOrder).filter(BuyerOrder.id == shipment.order_id).first()
    out.po_number = order.po_number if order else None
    items = []
    for item in shipment.items:
        item_out = ShipmentItemOut.model_validate(item)
        variant = db.query(StyleVariant).filter(StyleVariant.id == item.style_variant_id).first()
        item_out.variant_code = variant.variant_code if variant else None
        items.append(item_out)
    out.items = items
    return out


@router.get("", response_model=list[ShipmentOut])
def list_shipments(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return [_to_out(db, s) for s in db.query(Shipment).all()]


@router.post("", response_model=ShipmentOut, status_code=201)
def create_shipment(
    payload: ShipmentCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    existing = db.query(Shipment).filter(Shipment.shipment_number == payload.shipment_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Shipment number already exists")

    shipment = Shipment(
        shipment_number=payload.shipment_number,
        order_id=payload.order_id,
        packing_list_id=payload.packing_list_id,
        shipment_date=payload.shipment_date,
        carrier=payload.carrier,
        tracking_number=payload.tracking_number,
        port_of_loading=payload.port_of_loading,
        port_of_discharge=payload.port_of_discharge,
        remarks=payload.remarks,
    )
    db.add(shipment)
    db.flush()

    for item_data in payload.items:
        db.add(
            ShipmentItem(
                shipment_id=shipment.id,
                style_variant_id=item_data.style_variant_id,
                quantity=item_data.quantity,
                cartons=item_data.cartons,
            )
        )

    db.commit()
    db.refresh(shipment)
    return _to_out(db, shipment)


@router.get("/{shipment_id}", response_model=ShipmentOut)
def get_shipment(shipment_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return _to_out(db, shipment)


@router.post("/{shipment_id}/status", response_model=ShipmentOut)
def update_shipment_status(
    shipment_id: int,
    status: ShipmentStatus,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    shipment.status = status
    db.commit()
    db.refresh(shipment)
    return _to_out(db, shipment)
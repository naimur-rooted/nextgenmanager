from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.master import Buyer, Color, Size, Style, StyleVariant
from app.models.order import BuyerOrder, BuyerOrderItem
from app.models.user import User
from app.schemas.schemas import (
    BuyerOrderCreate,
    BuyerOrderItemOut,
    BuyerOrderOut,
    BuyerOrderUpdate,
)

router = APIRouter(prefix="/orders", tags=["Buyer Orders"])


def _to_order_out(db: Session, order: BuyerOrder) -> BuyerOrderOut:
    out = BuyerOrderOut.model_validate(order)
    buyer = db.query(Buyer).filter(Buyer.id == order.buyer_id).first()
    style = db.query(Style).filter(Style.id == order.style_id).first()
    out.buyer_name = buyer.name if buyer else None
    out.style_no = style.style_no if style else None
    out.total_quantity = sum(item.quantity for item in order.items)

    items = []
    for item in order.items:
        item_out = BuyerOrderItemOut.model_validate(item)
        variant = db.query(StyleVariant).filter(StyleVariant.id == item.style_variant_id).first()
        if variant:
            item_out.variant_code = variant.variant_code
        if item.color_id:
            color = db.query(Color).filter(Color.id == item.color_id).first()
            item_out.color_name = color.name if color else None
        if item.size_id:
            size = db.query(Size).filter(Size.id == item.size_id).first()
            item_out.size_name = size.name if size else None
        items.append(item_out)
    out.items = items
    return out


@router.get("", response_model=list[BuyerOrderOut])
def list_orders(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    orders = db.query(BuyerOrder).all()
    return [_to_order_out(db, o) for o in orders]


@router.post("", response_model=BuyerOrderOut, status_code=201)
def create_order(payload: BuyerOrderCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    existing = db.query(BuyerOrder).filter(BuyerOrder.po_number == payload.po_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="PO number already exists")

    order = BuyerOrder(
        po_number=payload.po_number,
        buyer_id=payload.buyer_id,
        style_id=payload.style_id,
        order_date=payload.order_date,
        delivery_date=payload.delivery_date,
        currency=payload.currency,
        status=payload.status,
        remarks=payload.remarks,
    )
    db.add(order)
    db.flush()

    for item_data in payload.items:
        item = BuyerOrderItem(
            order_id=order.id,
            style_variant_id=item_data.style_variant_id,
            quantity=item_data.quantity,
            unit_price=item_data.unit_price,
            color_id=item_data.color_id,
            size_id=item_data.size_id,
        )
        db.add(item)

    db.commit()
    db.refresh(order)
    return _to_order_out(db, order)


@router.get("/{order_id}", response_model=BuyerOrderOut)
def get_order(order_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    order = db.query(BuyerOrder).filter(BuyerOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return _to_order_out(db, order)


@router.put("/{order_id}", response_model=BuyerOrderOut)
def update_order(
    order_id: int,
    payload: BuyerOrderUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    order = db.query(BuyerOrder).filter(BuyerOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(order, key, value)
    db.commit()
    db.refresh(order)
    return _to_order_out(db, order)


@router.delete("/{order_id}", status_code=204)
def delete_order(order_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    order = db.query(BuyerOrder).filter(BuyerOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
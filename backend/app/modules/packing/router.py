from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.inventory import StockCategory, TransactionType
from app.models.master import Color, Size, StyleVariant
from app.models.order import BuyerOrder
from app.models.packing import PackingList, PackingListItem
from app.models.user import User
from app.schemas.schemas import PackingListCreate, PackingListItemOut, PackingListOut
from app.services.inventory_service import post_inventory_transaction

router = APIRouter(prefix="/packing", tags=["Packing"])


def _to_out(db: Session, pack: PackingList) -> PackingListOut:
    out = PackingListOut.model_validate(pack)
    order = db.query(BuyerOrder).filter(BuyerOrder.id == pack.order_id).first()
    out.po_number = order.po_number if order else None
    items = []
    for item in pack.items:
        item_out = PackingListItemOut.model_validate(item)
        if item.size_id:
            size = db.query(Size).filter(Size.id == item.size_id).first()
            item_out.size_name = size.name if size else None
        if item.color_id:
            color = db.query(Color).filter(Color.id == item.color_id).first()
            item_out.color_name = color.name if color else None
        items.append(item_out)
    out.items = items
    return out


@router.get("/lists", response_model=list[PackingListOut])
def list_packing_lists(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return [_to_out(db, p) for p in db.query(PackingList).all()]


@router.post("/lists", response_model=PackingListOut, status_code=201)
def create_packing_list(
    payload: PackingListCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    existing = db.query(PackingList).filter(PackingList.packing_number == payload.packing_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Packing number already exists")

    total_cartons = len(payload.items)
    total_quantity = sum(item.quantity for item in payload.items)

    packing = PackingList(
        packing_number=payload.packing_number,
        order_id=payload.order_id,
        style_variant_id=payload.style_variant_id,
        packing_date=payload.packing_date,
        total_cartons=total_cartons,
        total_quantity=total_quantity,
        warehouse=payload.warehouse,
        remarks=payload.remarks,
    )
    db.add(packing)
    db.flush()

    for item_data in payload.items:
        db.add(
            PackingListItem(
                packing_list_id=packing.id,
                carton_no=item_data.carton_no,
                quantity=item_data.quantity,
                size_id=item_data.size_id,
                color_id=item_data.color_id,
                gross_weight=item_data.gross_weight,
                net_weight=item_data.net_weight,
                carton_dimensions=item_data.carton_dimensions,
            )
        )

    db.commit()
    db.refresh(packing)
    return _to_out(db, packing)


@router.get("/lists/{packing_id}", response_model=PackingListOut)
def get_packing_list(packing_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    packing = db.query(PackingList).filter(PackingList.id == packing_id).first()
    if not packing:
        raise HTTPException(status_code=404, detail="Packing list not found")
    return _to_out(db, packing)
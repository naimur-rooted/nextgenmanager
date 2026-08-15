from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.inventory import InventoryTransaction, StockBalance
from app.models.master import Material
from app.models.user import User
from app.schemas.schemas import InventoryTransactionCreate, InventoryTransactionOut, StockBalanceOut
from app.services.inventory_service import post_inventory_transaction

router = APIRouter(prefix="/inventory", tags=["Inventory"])


def _balance_to_out(db: Session, balance: StockBalance) -> StockBalanceOut:
    out = StockBalanceOut.model_validate(balance)
    if balance.material_id:
        material = db.query(Material).filter(Material.id == balance.material_id).first()
        if material:
            out.material_code = material.code
            out.material_name = material.name
    return out


def _tx_to_out(db: Session, tx: InventoryTransaction) -> InventoryTransactionOut:
    out = InventoryTransactionOut.model_validate(tx)
    if tx.material_id:
        material = db.query(Material).filter(Material.id == tx.material_id).first()
        if material:
            out.material_code = material.code
            out.material_name = material.name
    return out


@router.get("/balances", response_model=list[StockBalanceOut])
def list_balances(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    balances = db.query(StockBalance).all()
    return [_balance_to_out(db, b) for b in balances]


@router.get("/transactions", response_model=list[InventoryTransactionOut])
def list_transactions(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    txs = db.query(InventoryTransaction).order_by(InventoryTransaction.transaction_date.desc()).limit(500).all()
    return [_tx_to_out(db, t) for t in txs]


@router.post("/transactions", response_model=InventoryTransactionOut, status_code=201)
def create_transaction(
    payload: InventoryTransactionCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    tx = post_inventory_transaction(
        db,
        transaction_type=payload.transaction_type,
        quantity=payload.quantity,
        category=payload.category,
        material_id=payload.material_id,
        style_variant_id=payload.style_variant_id,
        reference_type=payload.reference_type,
        reference_id=payload.reference_id,
        remarks=payload.remarks,
    )
    db.commit()
    db.refresh(tx)
    return _tx_to_out(db, tx)
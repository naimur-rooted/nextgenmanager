from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.inventory import InventoryTransaction, StockBalance, StockCategory, TransactionType


def get_or_create_stock_balance(
    db: Session,
    category: StockCategory,
    material_id: int | None = None,
    style_variant_id: int | None = None,
) -> StockBalance:
    balance = (
        db.query(StockBalance)
        .filter(
            StockBalance.category == category,
            StockBalance.material_id == material_id,
            StockBalance.style_variant_id == style_variant_id,
        )
        .first()
    )
    if balance is None:
        balance = StockBalance(
            category=category,
            material_id=material_id,
            style_variant_id=style_variant_id,
            quantity=Decimal("0.0000"),
            reserved_qty=Decimal("0.0000"),
        )
        db.add(balance)
        db.flush()
    return balance


def post_inventory_transaction(
    db: Session,
    transaction_type: TransactionType,
    quantity: Decimal,
    category: StockCategory,
    material_id: int | None = None,
    style_variant_id: int | None = None,
    reference_type: str | None = None,
    reference_id: int | None = None,
    remarks: str | None = None,
) -> InventoryTransaction:
    balance = get_or_create_stock_balance(
        db, category=category, material_id=material_id, style_variant_id=style_variant_id
    )

    balance.quantity += quantity

    transaction = InventoryTransaction(
        transaction_type=transaction_type,
        quantity=quantity,
        balance_after=balance.quantity,
        material_id=material_id,
        style_variant_id=style_variant_id,
        category=category,
        reference_type=reference_type,
        reference_id=reference_id,
        remarks=remarks,
    )
    db.add(transaction)
    db.flush()
    return transaction


def get_stock_balance(
    db: Session,
    category: StockCategory,
    material_id: int | None = None,
    style_variant_id: int | None = None,
) -> Decimal:
    balance = get_or_create_stock_balance(
        db, category=category, material_id=material_id, style_variant_id=style_variant_id
    )
    return balance.quantity
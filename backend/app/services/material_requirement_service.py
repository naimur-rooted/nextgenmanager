from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy.orm import Session

from app.models.bom import GarmentBom, GarmentBomItem, BomStatus
from app.models.inventory import StockBalance, StockCategory
from app.models.material_requirement import MaterialRequirement, RequirementStatus
from app.models.order import BuyerOrder, BuyerOrderItem
from app.models.procurement import PurchaseOrder, PurchaseOrderItem, PurchaseOrderStatus


def _round_qty(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)


def calculate_required_qty(order_qty: int, consumption_per_unit: Decimal, wastage_percent: Decimal) -> Decimal:
    base = Decimal(order_qty) * consumption_per_unit
    wastage = base * wastage_percent / Decimal("100")
    return _round_qty(base + wastage)


def get_active_bom(db: Session, style_id: int) -> GarmentBom | None:
    return (
        db.query(GarmentBom)
        .filter(GarmentBom.style_id == style_id, GarmentBom.is_active.is_(True))
        .order_by(GarmentBom.version.desc())
        .first()
    )


def get_available_qty(db: Session, material_id: int) -> Decimal:
    balance = (
        db.query(StockBalance)
        .filter(
            StockBalance.category == StockCategory.RAW_MATERIAL,
            StockBalance.material_id == material_id,
        )
        .first()
    )
    if balance is None:
        return Decimal("0.0000")
    return balance.quantity


def get_reserved_qty(db: Session, material_id: int) -> Decimal:
    balance = (
        db.query(StockBalance)
        .filter(
            StockBalance.category == StockCategory.RAW_MATERIAL,
            StockBalance.material_id == material_id,
        )
        .first()
    )
    if balance is None:
        return Decimal("0.0000")
    return balance.reserved_qty


def get_incoming_qty(db: Session, material_id: int) -> Decimal:
    total = Decimal("0.0000")
    items = (
        db.query(PurchaseOrderItem)
        .join(PurchaseOrder)
        .filter(
            PurchaseOrderItem.material_id == material_id,
            PurchaseOrder.status.in_([PurchaseOrderStatus.SENT, PurchaseOrderStatus.PARTIALLY_RECEIVED]),
        )
        .all()
    )
    for item in items:
        total += item.quantity - item.received_qty
    return _round_qty(total)


def calculate_material_requirements(db: Session, order_id: int) -> list[MaterialRequirement]:
    order = db.query(BuyerOrder).filter(BuyerOrder.id == order_id).first()
    if order is None:
        raise ValueError("Order not found")

    bom = get_active_bom(db, order.style_id)
    if bom is None:
        raise ValueError("No active BOM found for style")

    total_order_qty = sum(item.quantity for item in order.items)

    requirements = []
    for bom_item in bom.items:
        if not bom_item.is_mandatory:
            continue

        required = calculate_required_qty(
            total_order_qty, bom_item.quantity_per_garment, bom_item.wastage_percent
        )
        available = get_available_qty(db, bom_item.material_id)
        reserved = get_reserved_qty(db, bom_item.material_id)
        incoming = get_incoming_qty(db, bom_item.material_id)
        shortage = _round_qty(required - available - incoming)

        existing = (
            db.query(MaterialRequirement)
            .filter(
                MaterialRequirement.order_id == order_id,
                MaterialRequirement.material_id == bom_item.material_id,
            )
            .first()
        )

        if shortage > 0:
            status = RequirementStatus.PARTIAL if incoming > 0 else RequirementStatus.OPEN
        else:
            status = RequirementStatus.FULFILLED

        data = {
            "order_id": order_id,
            "material_id": bom_item.material_id,
            "bom_item_id": bom_item.id,
            "total_order_qty": total_order_qty,
            "consumption_per_unit": bom_item.quantity_per_garment,
            "wastage_percent": bom_item.wastage_percent,
            "required_qty": required,
            "available_qty": available,
            "reserved_qty": reserved,
            "incoming_qty": incoming,
            "shortage_qty": shortage,
            "status": status,
        }

        if existing:
            for key, value in data.items():
                setattr(existing, key, value)
            requirements.append(existing)
        else:
            req = MaterialRequirement(**data)
            db.add(req)
            db.flush()
            requirements.append(req)

    db.flush()
    return requirements
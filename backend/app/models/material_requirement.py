from decimal import Decimal
from enum import Enum
from sqlalchemy import String, Numeric, Integer, ForeignKey, Text, Enum as SAEnum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class RequirementStatus(str, Enum):
    OPEN = "Open"
    PARTIAL = "Partial"
    FULFILLED = "Fulfilled"
    CLOSED = "Closed"


class MaterialRequirement(TimestampMixin, Base):
    __tablename__ = "material_requirements"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("buyer_orders.id"), nullable=False, index=True)
    material_id: Mapped[int] = mapped_column(ForeignKey("materials.id"), nullable=False)
    bom_item_id: Mapped[int | None] = mapped_column(ForeignKey("garment_bom_items.id"))

    total_order_qty: Mapped[int] = mapped_column(Integer, nullable=False)
    consumption_per_unit: Mapped[Decimal] = mapped_column(Numeric(12, 4), nullable=False)
    wastage_percent: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False, default=Decimal("0.00"))
    required_qty: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    available_qty: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False, default=Decimal("0.0000"))
    reserved_qty: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False, default=Decimal("0.0000"))
    incoming_qty: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False, default=Decimal("0.0000"))
    shortage_qty: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False, default=Decimal("0.0000"))
    status: Mapped[RequirementStatus] = mapped_column(
        SAEnum(RequirementStatus, name="requirement_status", native_enum=False),
        nullable=False, default=RequirementStatus.OPEN,
    )
    notes: Mapped[str | None] = mapped_column(Text)

    __table_args__ = (UniqueConstraint("order_id", "material_id", name="uq_order_material"),)

    order: Mapped["BuyerOrder"] = relationship()
    material: Mapped["Material"] = relationship()
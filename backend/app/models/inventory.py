from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from sqlalchemy import String, Numeric, Integer, ForeignKey, DateTime, Date, Enum as SAEnum, Text, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class StockCategory(str, Enum):
    RAW_MATERIAL = "Raw Material"
    WIP = "WIP"
    FINISHED_GOODS = "Finished Goods"


class TransactionType(str, Enum):
    PURCHASE_RECEIPT = "Purchase Receipt"
    MATERIAL_ISSUE = "Material Issue"
    PRODUCTION_INPUT = "Production Input"
    PRODUCTION_OUTPUT = "Production Output"
    SALE_ISSUE = "Sale Issue"
    ADJUSTMENT_IN = "Adjustment In"
    ADJUSTMENT_OUT = "Adjustment Out"
    TRANSFER_IN = "Transfer In"
    TRANSFER_OUT = "Transfer Out"
    PACKING_INPUT = "Packing Input"
    SHIPMENT_ISSUE = "Shipment Issue"
    WASTE = "Waste"
    RETURN = "Return"


class StockBalance(TimestampMixin, Base):
    __tablename__ = "stock_balances"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    material_id: Mapped[int | None] = mapped_column(ForeignKey("materials.id"), index=True)
    style_variant_id: Mapped[int | None] = mapped_column(ForeignKey("style_variants.id"), index=True)
    category: Mapped[StockCategory] = mapped_column(SAEnum(StockCategory, name="stock_category", native_enum=False), nullable=False, default=StockCategory.RAW_MATERIAL)
    quantity: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False, default=Decimal("0.0000"))
    reserved_qty: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False, default=Decimal("0.0000"))

    material: Mapped["Material | None"] = relationship()
    style_variant: Mapped["StyleVariant | None"] = relationship()


class InventoryTransaction(TimestampMixin, Base):
    __tablename__ = "inventory_transactions"

    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
    transaction_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, index=True)
    transaction_type: Mapped[TransactionType] = mapped_column(SAEnum(TransactionType, name="transaction_type", native_enum=False), nullable=False)
    material_id: Mapped[int | None] = mapped_column(ForeignKey("materials.id"), index=True)
    style_variant_id: Mapped[int | None] = mapped_column(ForeignKey("style_variants.id"), index=True)
    category: Mapped[StockCategory] = mapped_column(SAEnum(StockCategory, name="stock_category", native_enum=False), nullable=False, default=StockCategory.RAW_MATERIAL)
    quantity: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)  # positive = in, negative = out
    balance_after: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    reference_type: Mapped[str | None] = mapped_column(String(100))
    reference_id: Mapped[int | None] = mapped_column(Integer)
    remarks: Mapped[str | None] = mapped_column(Text)

    material: Mapped["Material | None"] = relationship()
    style_variant: Mapped["StyleVariant | None"] = relationship()
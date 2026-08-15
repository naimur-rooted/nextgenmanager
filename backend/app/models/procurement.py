from datetime import date
from decimal import Decimal
from enum import Enum
from sqlalchemy import String, Date, Numeric, Integer, ForeignKey, Text, Enum as SAEnum, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class RequisitionStatus(str, Enum):
    DRAFT = "Draft"
    SUBMITTED = "Submitted"
    APPROVED = "Approved"
    ORDERED = "Ordered"
    CANCELLED = "Cancelled"


class PurchaseOrderStatus(str, Enum):
    DRAFT = "Draft"
    SENT = "Sent"
    PARTIALLY_RECEIVED = "Partially Received"
    RECEIVED = "Received"
    CLOSED = "Closed"
    CANCELLED = "Cancelled"


class GoodsReceiptStatus(str, Enum):
    DRAFT = "Draft"
    RECEIVED = "Received"
    POSTED = "Posted"


class PurchaseRequisition(TimestampMixin, Base):
    __tablename__ = "purchase_requisitions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pr_number: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    order_id: Mapped[int | None] = mapped_column(ForeignKey("buyer_orders.id"))
    requested_by: Mapped[str | None] = mapped_column(String(255))
    required_date: Mapped[date | None] = mapped_column(Date)
    status: Mapped[RequisitionStatus] = mapped_column(
        SAEnum(RequisitionStatus, name="requisition_status", native_enum=False),
        nullable=False, default=RequisitionStatus.DRAFT,
    )
    notes: Mapped[str | None] = mapped_column(Text)

    items: Mapped[list["PurchaseRequisitionItem"]] = relationship(back_populates="requisition", cascade="all, delete-orphan")


class PurchaseRequisitionItem(TimestampMixin, Base):
    __tablename__ = "purchase_requisition_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    requisition_id: Mapped[int] = mapped_column(ForeignKey("purchase_requisitions.id"), nullable=False)
    material_id: Mapped[int] = mapped_column(ForeignKey("materials.id"), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    uom: Mapped[str] = mapped_column(String(20), nullable=False)
    requirement_id: Mapped[int | None] = mapped_column(ForeignKey("material_requirements.id"))
    notes: Mapped[str | None] = mapped_column(Text)

    requisition: Mapped["PurchaseRequisition"] = relationship(back_populates="items")
    material: Mapped["Material"] = relationship()


class PurchaseOrder(TimestampMixin, Base):
    __tablename__ = "purchase_orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    po_number: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"), nullable=False)
    requisition_id: Mapped[int | None] = mapped_column(ForeignKey("purchase_requisitions.id"))
    order_date: Mapped[date] = mapped_column(Date, nullable=False)
    expected_date: Mapped[date | None] = mapped_column(Date)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="USD")
    status: Mapped[PurchaseOrderStatus] = mapped_column(
        SAEnum(PurchaseOrderStatus, name="purchase_order_status", native_enum=False),
        nullable=False, default=PurchaseOrderStatus.DRAFT,
    )
    notes: Mapped[str | None] = mapped_column(Text)

    supplier: Mapped["Supplier"] = relationship()
    items: Mapped[list["PurchaseOrderItem"]] = relationship(back_populates="purchase_order", cascade="all, delete-orphan")


class PurchaseOrderItem(TimestampMixin, Base):
    __tablename__ = "purchase_order_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    purchase_order_id: Mapped[int] = mapped_column(ForeignKey("purchase_orders.id"), nullable=False)
    material_id: Mapped[int] = mapped_column(ForeignKey("materials.id"), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    received_qty: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False, default=Decimal("0.0000"))
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 4), nullable=False, default=Decimal("0.0000"))
    uom: Mapped[str] = mapped_column(String(20), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text)

    purchase_order: Mapped["PurchaseOrder"] = relationship(back_populates="items")
    material: Mapped["Material"] = relationship()


class GoodsReceipt(TimestampMixin, Base):
    __tablename__ = "goods_receipts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    gr_number: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    purchase_order_id: Mapped[int] = mapped_column(ForeignKey("purchase_orders.id"), nullable=False)
    receipt_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[GoodsReceiptStatus] = mapped_column(
        SAEnum(GoodsReceiptStatus, name="goods_receipt_status", native_enum=False),
        nullable=False, default=GoodsReceiptStatus.DRAFT,
    )
    received_by: Mapped[str | None] = mapped_column(String(255))
    notes: Mapped[str | None] = mapped_column(Text)

    purchase_order: Mapped["PurchaseOrder"] = relationship()
    items: Mapped[list["GoodsReceiptItem"]] = relationship(back_populates="goods_receipt", cascade="all, delete-orphan")


class GoodsReceiptItem(TimestampMixin, Base):
    __tablename__ = "goods_receipt_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    goods_receipt_id: Mapped[int] = mapped_column(ForeignKey("goods_receipts.id"), nullable=False)
    po_item_id: Mapped[int] = mapped_column(ForeignKey("purchase_order_items.id"), nullable=False)
    material_id: Mapped[int] = mapped_column(ForeignKey("materials.id"), nullable=False)
    received_qty: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    accepted_qty: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    rejected_qty: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False, default=Decimal("0.0000"))
    uom: Mapped[str] = mapped_column(String(20), nullable=False)

    goods_receipt: Mapped["GoodsReceipt"] = relationship(back_populates="items")
    po_item: Mapped["PurchaseOrderItem"] = relationship()
    material: Mapped["Material"] = relationship()
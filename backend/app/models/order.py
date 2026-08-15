from datetime import date
from decimal import Decimal
from enum import Enum
from sqlalchemy import String, Date, Numeric, Integer, ForeignKey, Text, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class OrderStatus(str, Enum):
    DRAFT = "Draft"
    CONFIRMED = "Confirmed"
    IN_PRODUCTION = "In Production"
    SHIPPED = "Shipped"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class BuyerOrder(TimestampMixin, Base):
    __tablename__ = "buyer_orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    po_number: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    buyer_id: Mapped[int] = mapped_column(ForeignKey("buyers.id"), nullable=False)
    style_id: Mapped[int] = mapped_column(ForeignKey("styles.id"), nullable=False)
    order_date: Mapped[date] = mapped_column(Date, nullable=False)
    delivery_date: Mapped[date] = mapped_column(Date, nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="USD")
    status: Mapped[OrderStatus] = mapped_column(SAEnum(OrderStatus, name="order_status", native_enum=False), nullable=False, default=OrderStatus.DRAFT)
    remarks: Mapped[str | None] = mapped_column(Text)

    buyer: Mapped["Buyer"] = relationship(back_populates="orders")
    style: Mapped["Style"] = relationship()
    items: Mapped[list["BuyerOrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan")


class BuyerOrderItem(TimestampMixin, Base):
    __tablename__ = "buyer_order_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("buyer_orders.id"), nullable=False)
    style_variant_id: Mapped[int] = mapped_column(ForeignKey("style_variants.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 4), nullable=False, default=Decimal("0.0000"))
    color_id: Mapped[int | None] = mapped_column(ForeignKey("colors.id"))
    size_id: Mapped[int | None] = mapped_column(ForeignKey("sizes.id"))

    order: Mapped["BuyerOrder"] = relationship(back_populates="items")
    style_variant: Mapped["StyleVariant"] = relationship()
    color: Mapped["Color | None"] = relationship()
    size: Mapped["Size | None"] = relationship()
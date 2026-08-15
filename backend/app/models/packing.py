from datetime import date
from decimal import Decimal
from enum import Enum
from sqlalchemy import String, Date, Numeric, Integer, ForeignKey, Text, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class PackingStatus(str, Enum):
    DRAFT = "Draft"
    PACKED = "Packed"
    SHIPPED = "Shipped"
    CANCELLED = "Cancelled"


class PackingList(TimestampMixin, Base):
    __tablename__ = "packing_lists"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    packing_number: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    order_id: Mapped[int] = mapped_column(ForeignKey("buyer_orders.id"), nullable=False)
    style_variant_id: Mapped[int] = mapped_column(ForeignKey("style_variants.id"), nullable=False)
    packing_date: Mapped[date] = mapped_column(Date, nullable=False)
    total_cartons: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[PackingStatus] = mapped_column(SAEnum(PackingStatus, name="packing_status", native_enum=False), nullable=False, default=PackingStatus.DRAFT)
    warehouse: Mapped[str | None] = mapped_column(String(255))
    remarks: Mapped[str | None] = mapped_column(Text)

    order: Mapped["BuyerOrder"] = relationship()
    style_variant: Mapped["StyleVariant"] = relationship()
    items: Mapped[list["PackingListItem"]] = relationship(back_populates="packing_list", cascade="all, delete-orphan")


class PackingListItem(TimestampMixin, Base):
    __tablename__ = "packing_list_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    packing_list_id: Mapped[int] = mapped_column(ForeignKey("packing_lists.id"), nullable=False)
    carton_no: Mapped[str] = mapped_column(String(50), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    size_id: Mapped[int | None] = mapped_column(ForeignKey("sizes.id"))
    color_id: Mapped[int | None] = mapped_column(ForeignKey("colors.id"))
    gross_weight: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    net_weight: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    carton_dimensions: Mapped[str | None] = mapped_column(String(100))

    packing_list: Mapped["PackingList"] = relationship(back_populates="items")
    size: Mapped["Size | None"] = relationship()
    color: Mapped["Color | None"] = relationship()
from datetime import date
from enum import Enum
from sqlalchemy import String, Date, Integer, ForeignKey, Text, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class ShipmentStatus(str, Enum):
    PLANNED = "Planned"
    IN_TRANSIT = "In Transit"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"


class Shipment(TimestampMixin, Base):
    __tablename__ = "shipments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    shipment_number: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    order_id: Mapped[int] = mapped_column(ForeignKey("buyer_orders.id"), nullable=False)
    packing_list_id: Mapped[int | None] = mapped_column(ForeignKey("packing_lists.id"))
    shipment_date: Mapped[date] = mapped_column(Date, nullable=False)
    carrier: Mapped[str | None] = mapped_column(String(255))
    tracking_number: Mapped[str | None] = mapped_column(String(255))
    port_of_loading: Mapped[str | None] = mapped_column(String(255))
    port_of_discharge: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[ShipmentStatus] = mapped_column(SAEnum(ShipmentStatus, name="shipment_status", native_enum=False), nullable=False, default=ShipmentStatus.PLANNED)
    remarks: Mapped[str | None] = mapped_column(Text)

    order: Mapped["BuyerOrder"] = relationship()
    packing_list: Mapped["PackingList | None"] = relationship()
    items: Mapped[list["ShipmentItem"]] = relationship(back_populates="shipment", cascade="all, delete-orphan")


class ShipmentItem(TimestampMixin, Base):
    __tablename__ = "shipment_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    shipment_id: Mapped[int] = mapped_column(ForeignKey("shipments.id"), nullable=False)
    style_variant_id: Mapped[int] = mapped_column(ForeignKey("style_variants.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    cartons: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    shipment: Mapped["Shipment"] = relationship(back_populates="items")
    style_variant: Mapped["StyleVariant"] = relationship()
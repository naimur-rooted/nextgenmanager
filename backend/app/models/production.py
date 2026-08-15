from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from sqlalchemy import String, Date, DateTime, Numeric, Integer, ForeignKey, Text, Enum as SAEnum, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class PlanStatus(str, Enum):
    DRAFT = "Draft"
    APPROVED = "Approved"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class WorkOrderStatus(str, Enum):
    PLANNED = "Planned"
    RELEASED = "Released"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class ProductionStage(str, Enum):
    CUTTING = "Cutting"
    SEWING = "Sewing"
    FINISHING = "Finishing"
    QC = "QC"
    PACKING = "Packing"


class ProductionPlan(TimestampMixin, Base):
    __tablename__ = "production_plans"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    plan_number: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    order_id: Mapped[int] = mapped_column(ForeignKey("buyer_orders.id"), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[PlanStatus] = mapped_column(SAEnum(PlanStatus, name="plan_status", native_enum=False), nullable=False, default=PlanStatus.DRAFT)
    notes: Mapped[str | None] = mapped_column(Text)

    order: Mapped["BuyerOrder"] = relationship()
    work_orders: Mapped[list["WorkOrder"]] = relationship(back_populates="plan", cascade="all, delete-orphan")


class WorkOrder(TimestampMixin, Base):
    __tablename__ = "work_orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    wo_number: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    plan_id: Mapped[int] = mapped_column(ForeignKey("production_plans.id"), nullable=False)
    style_variant_id: Mapped[int] = mapped_column(ForeignKey("style_variants.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    produced_qty: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rejected_qty: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[WorkOrderStatus] = mapped_column(SAEnum(WorkOrderStatus, name="work_order_status", native_enum=False), nullable=False, default=WorkOrderStatus.PLANNED)
    notes: Mapped[str | None] = mapped_column(Text)

    plan: Mapped["ProductionPlan"] = relationship(back_populates="work_orders")
    style_variant: Mapped["StyleVariant"] = relationship()


class CuttingEntry(TimestampMixin, Base):
    __tablename__ = "cutting_entries"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    work_order_id: Mapped[int] = mapped_column(ForeignKey("work_orders.id"), nullable=False)
    entry_date: Mapped[date] = mapped_column(Date, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)  # garments cut
    rejection_qty: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    alteration_qty: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    waste_qty: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    shift: Mapped[str | None] = mapped_column(String(50))
    operator: Mapped[str | None] = mapped_column(String(255))
    remarks: Mapped[str | None] = mapped_column(Text)

    work_order: Mapped["WorkOrder"] = relationship()


class SewingEntry(TimestampMixin, Base):
    __tablename__ = "sewing_entries"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    work_order_id: Mapped[int] = mapped_column(ForeignKey("work_orders.id"), nullable=False)
    entry_date: Mapped[date] = mapped_column(Date, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    rejection_qty: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    alteration_qty: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    waste_qty: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    shift: Mapped[str | None] = mapped_column(String(50))
    operator: Mapped[str | None] = mapped_column(String(255))
    remarks: Mapped[str | None] = mapped_column(Text)

    work_order: Mapped["WorkOrder"] = relationship()


class FinishingEntry(TimestampMixin, Base):
    __tablename__ = "finishing_entries"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    work_order_id: Mapped[int] = mapped_column(ForeignKey("work_orders.id"), nullable=False)
    entry_date: Mapped[date] = mapped_column(Date, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    rejection_qty: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    alteration_qty: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    waste_qty: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    shift: Mapped[str | None] = mapped_column(String(50))
    operator: Mapped[str | None] = mapped_column(String(255))
    remarks: Mapped[str | None] = mapped_column(Text)

    work_order: Mapped["WorkOrder"] = relationship()
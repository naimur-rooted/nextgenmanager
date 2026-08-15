from datetime import date
from enum import Enum
from sqlalchemy import String, Date, Integer, ForeignKey, Text, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class QCType(str, Enum):
    INCOMING = "Incoming"
    INLINE = "Inline"
    FINAL = "Final"


class QCStatus(str, Enum):
    PENDING = "Pending"
    PASSED = "Passed"
    REJECTED = "Rejected"
    REWORK = "Rework"


class QualityInspection(TimestampMixin, Base):
    __tablename__ = "quality_inspections"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    inspection_number: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    qc_type: Mapped[QCType] = mapped_column(SAEnum(QCType, name="qc_type", native_enum=False), nullable=False)
    status: Mapped[QCStatus] = mapped_column(SAEnum(QCStatus, name="qc_status", native_enum=False), nullable=False, default=QCStatus.PENDING)
    work_order_id: Mapped[int | None] = mapped_column(ForeignKey("work_orders.id"))
    order_id: Mapped[int | None] = mapped_column(ForeignKey("buyer_orders.id"))
    style_variant_id: Mapped[int | None] = mapped_column(ForeignKey("style_variants.id"))
    material_id: Mapped[int | None] = mapped_column(ForeignKey("materials.id"))
    inspected_qty: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    passed_qty: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rejected_qty: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    inspector: Mapped[str | None] = mapped_column(String(255))
    inspection_date: Mapped[date] = mapped_column(Date, nullable=False)
    remarks: Mapped[str | None] = mapped_column(Text)

    defects: Mapped[list["Defect"]] = relationship(back_populates="inspection", cascade="all, delete-orphan")


class Defect(TimestampMixin, Base):
    __tablename__ = "defects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    inspection_id: Mapped[int] = mapped_column(ForeignKey("quality_inspections.id"), nullable=False)
    defect_type: Mapped[str] = mapped_column(String(100), nullable=False)  # Fabric Defect, Stitching Defect, etc.
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    remarks: Mapped[str | None] = mapped_column(Text)

    inspection: Mapped["QualityInspection"] = relationship(back_populates="defects")
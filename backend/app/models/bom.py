from decimal import Decimal
from enum import Enum
from sqlalchemy import String, Numeric, Integer, ForeignKey, Boolean, Text, Enum as SAEnum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class BomStatus(str, Enum):
    DRAFT = "Draft"
    ACTIVE = "Active"
    SUPERSEDED = "Superseded"
    OBSOLETE = "Obsolete"


class GarmentBom(TimestampMixin, Base):
    __tablename__ = "garment_boms"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    style_id: Mapped[int] = mapped_column(ForeignKey("styles.id"), nullable=False)
    bom_name: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[BomStatus] = mapped_column(SAEnum(BomStatus, name="bom_status", native_enum=False), nullable=False, default=BomStatus.DRAFT)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    notes: Mapped[str | None] = mapped_column(Text)

    __table_args__ = (UniqueConstraint("style_id", "version", name="uq_style_bom_version"),)

    style: Mapped["Style"] = relationship()
    items: Mapped[list["GarmentBomItem"]] = relationship(back_populates="bom", cascade="all, delete-orphan")


class GarmentBomItem(TimestampMixin, Base):
    __tablename__ = "garment_bom_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    bom_id: Mapped[int] = mapped_column(ForeignKey("garment_boms.id"), nullable=False)
    material_id: Mapped[int] = mapped_column(ForeignKey("materials.id"), nullable=False)
    quantity_per_garment: Mapped[Decimal] = mapped_column(Numeric(12, 4), nullable=False)
    uom: Mapped[str] = mapped_column(String(20), nullable=False)
    wastage_percent: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False, default=Decimal("0.00"))
    is_mandatory: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    color_id: Mapped[int | None] = mapped_column(ForeignKey("colors.id"))
    size_id: Mapped[int | None] = mapped_column(ForeignKey("sizes.id"))
    notes: Mapped[str | None] = mapped_column(Text)

    bom: Mapped["GarmentBom"] = relationship(back_populates="items")
    material: Mapped["Material"] = relationship()
    color: Mapped["Color | None"] = relationship()
    size: Mapped["Size | None"] = relationship()
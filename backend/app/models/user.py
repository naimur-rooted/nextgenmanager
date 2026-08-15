from enum import Enum
from sqlalchemy import String, Enum as SAEnum, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class Role(str, Enum):
    ADMIN = "Admin"
    MERCHANDISER = "Merchandiser"
    PRODUCTION_MANAGER = "Production Manager"
    PLANNER = "Planner"
    INVENTORY_MANAGER = "Inventory Manager"
    PURCHASE_MANAGER = "Purchase Manager"
    QUALITY_INSPECTOR = "Quality Inspector"
    WAREHOUSE_MANAGER = "Warehouse Manager"
    MANAGEMENT = "Management"


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[Role] = mapped_column(SAEnum(Role, name="role", native_enum=False), nullable=False, default=Role.MERCHANDISER)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
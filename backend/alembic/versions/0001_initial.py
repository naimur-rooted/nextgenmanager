"""initial migration

Revision ID: 0001
Revises:
Create Date: 2026-08-15

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # -- Users & Roles --
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("username", sa.String(100), nullable=False, unique=True),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("role", sa.String(50), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"])
    op.create_index("ix_users_username", "users", ["username"])

    # -- Master Data --
    op.create_table(
        "buyers",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("code", sa.String(50), nullable=False, unique=True),
        sa.Column("contact_person", sa.String(255)),
        sa.Column("email", sa.String(255)),
        sa.Column("phone", sa.String(50)),
        sa.Column("address", sa.String(500)),
        sa.Column("country", sa.String(100)),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "suppliers",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("code", sa.String(50), nullable=False, unique=True),
        sa.Column("contact_person", sa.String(255)),
        sa.Column("email", sa.String(255)),
        sa.Column("phone", sa.String(50)),
        sa.Column("address", sa.String(500)),
        sa.Column("payment_terms", sa.String(255)),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "colors",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(100), nullable=False, unique=True),
        sa.Column("code", sa.String(50)),
        sa.Column("hex_code", sa.String(7)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "sizes",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(50), nullable=False, unique=True),
        sa.Column("code", sa.String(20)),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "materials",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("code", sa.String(50), nullable=False, unique=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("category", sa.String(100), nullable=False, server_default="Fabric"),
        sa.Column("uom", sa.String(20), nullable=False),
        sa.Column("unit_cost", sa.Numeric(12, 2), server_default="0"),
        sa.Column("currency", sa.String(10), nullable=False, server_default="USD"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "styles",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("style_no", sa.String(100), nullable=False, unique=True),
        sa.Column("description", sa.String(500)),
        sa.Column("buyer_id", sa.Integer(), sa.ForeignKey("buyers.id")),
        sa.Column("category", sa.String(100)),
        sa.Column("image_url", sa.String(500)),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "style_variants",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("style_id", sa.Integer(), sa.ForeignKey("styles.id"), nullable=False),
        sa.Column("style_no", sa.String(100)),
        sa.Column("color_id", sa.Integer(), sa.ForeignKey("colors.id"), nullable=False),
        sa.Column("size_id", sa.Integer(), sa.ForeignKey("sizes.id"), nullable=False),
        sa.Column("variant_code", sa.String(150), nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("style_id", "color_id", "size_id", name="uq_style_color_size"),
    )

    # -- Orders --
    op.create_table(
        "buyer_orders",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("po_number", sa.String(100), nullable=False, unique=True),
        sa.Column("buyer_id", sa.Integer(), sa.ForeignKey("buyers.id"), nullable=False),
        sa.Column("style_id", sa.Integer(), sa.ForeignKey("styles.id"), nullable=False),
        sa.Column("order_date", sa.Date(), nullable=False),
        sa.Column("delivery_date", sa.Date(), nullable=False),
        sa.Column("currency", sa.String(10), nullable=False, server_default="USD"),
        sa.Column("status", sa.String(50), nullable=False, server_default="Draft"),
        sa.Column("remarks", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_buyer_orders_po_number", "buyer_orders", ["po_number"])

    op.create_table(
        "buyer_order_items",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("buyer_orders.id"), nullable=False),
        sa.Column("style_variant_id", sa.Integer(), sa.ForeignKey("style_variants.id"), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("unit_price", sa.Numeric(12, 4), nullable=False, server_default="0"),
        sa.Column("color_id", sa.Integer(), sa.ForeignKey("colors.id")),
        sa.Column("size_id", sa.Integer(), sa.ForeignKey("sizes.id")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # -- BOM --
    op.create_table(
        "garment_boms",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("style_id", sa.Integer(), sa.ForeignKey("styles.id"), nullable=False),
        sa.Column("bom_name", sa.String(255), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("status", sa.String(50), nullable=False, server_default="Draft"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("notes", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("style_id", "version", name="uq_style_bom_version"),
    )

    op.create_table(
        "garment_bom_items",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("bom_id", sa.Integer(), sa.ForeignKey("garment_boms.id"), nullable=False),
        sa.Column("material_id", sa.Integer(), sa.ForeignKey("materials.id"), nullable=False),
        sa.Column("quantity_per_garment", sa.Numeric(12, 4), nullable=False),
        sa.Column("uom", sa.String(20), nullable=False),
        sa.Column("wastage_percent", sa.Numeric(5, 2), nullable=False, server_default="0"),
        sa.Column("is_mandatory", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("color_id", sa.Integer(), sa.ForeignKey("colors.id")),
        sa.Column("size_id", sa.Integer(), sa.ForeignKey("sizes.id")),
        sa.Column("notes", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # -- Material Requirements --
    op.create_table(
        "material_requirements",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("buyer_orders.id"), nullable=False),
        sa.Column("material_id", sa.Integer(), sa.ForeignKey("materials.id"), nullable=False),
        sa.Column("bom_item_id", sa.Integer(), sa.ForeignKey("garment_bom_items.id")),
        sa.Column("total_order_qty", sa.Integer(), nullable=False),
        sa.Column("consumption_per_unit", sa.Numeric(12, 4), nullable=False),
        sa.Column("wastage_percent", sa.Numeric(5, 2), nullable=False, server_default="0"),
        sa.Column("required_qty", sa.Numeric(14, 4), nullable=False),
        sa.Column("available_qty", sa.Numeric(14, 4), nullable=False, server_default="0"),
        sa.Column("reserved_qty", sa.Numeric(14, 4), nullable=False, server_default="0"),
        sa.Column("incoming_qty", sa.Numeric(14, 4), nullable=False, server_default="0"),
        sa.Column("shortage_qty", sa.Numeric(14, 4), nullable=False, server_default="0"),
        sa.Column("status", sa.String(50), nullable=False, server_default="Open"),
        sa.Column("notes", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("order_id", "material_id", name="uq_order_material"),
    )
    op.create_index("ix_material_requirements_order_id", "material_requirements", ["order_id"])

    # -- Inventory --
    op.create_table(
        "stock_balances",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("material_id", sa.Integer(), sa.ForeignKey("materials.id")),
        sa.Column("style_variant_id", sa.Integer(), sa.ForeignKey("style_variants.id")),
        sa.Column("category", sa.String(50), nullable=False, server_default="Raw Material"),
        sa.Column("quantity", sa.Numeric(14, 4), nullable=False, server_default="0"),
        sa.Column("reserved_qty", sa.Numeric(14, 4), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_stock_balances_material_id", "stock_balances", ["material_id"])
    op.create_index("ix_stock_balances_style_variant_id", "stock_balances", ["style_variant_id"])

    op.create_table(
        "inventory_transactions",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("transaction_date", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("transaction_type", sa.String(50), nullable=False),
        sa.Column("material_id", sa.Integer(), sa.ForeignKey("materials.id")),
        sa.Column("style_variant_id", sa.Integer(), sa.ForeignKey("style_variants.id")),
        sa.Column("category", sa.String(50), nullable=False, server_default="Raw Material"),
        sa.Column("quantity", sa.Numeric(14, 4), nullable=False),
        sa.Column("balance_after", sa.Numeric(14, 4), nullable=False),
        sa.Column("reference_type", sa.String(100)),
        sa.Column("reference_id", sa.Integer()),
        sa.Column("remarks", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_inventory_transactions_material_id", "inventory_transactions", ["material_id"])
    op.create_index("ix_inventory_transactions_style_variant_id", "inventory_transactions", ["style_variant_id"])
    op.create_index("ix_inventory_transactions_transaction_date", "inventory_transactions", ["transaction_date"])

    # -- Procurement --
    op.create_table(
        "purchase_requisitions",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("pr_number", sa.String(100), nullable=False, unique=True),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("buyer_orders.id")),
        sa.Column("requested_by", sa.String(255)),
        sa.Column("required_date", sa.Date()),
        sa.Column("status", sa.String(50), nullable=False, server_default="Draft"),
        sa.Column("notes", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "purchase_requisition_items",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("requisition_id", sa.Integer(), sa.ForeignKey("purchase_requisitions.id"), nullable=False),
        sa.Column("material_id", sa.Integer(), sa.ForeignKey("materials.id"), nullable=False),
        sa.Column("quantity", sa.Numeric(14, 4), nullable=False),
        sa.Column("uom", sa.String(20), nullable=False),
        sa.Column("requirement_id", sa.Integer(), sa.ForeignKey("material_requirements.id")),
        sa.Column("notes", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "purchase_orders",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("po_number", sa.String(100), nullable=False, unique=True),
        sa.Column("supplier_id", sa.Integer(), sa.ForeignKey("suppliers.id"), nullable=False),
        sa.Column("requisition_id", sa.Integer(), sa.ForeignKey("purchase_requisitions.id")),
        sa.Column("order_date", sa.Date(), nullable=False),
        sa.Column("expected_date", sa.Date()),
        sa.Column("currency", sa.String(10), nullable=False, server_default="USD"),
        sa.Column("status", sa.String(50), nullable=False, server_default="Draft"),
        sa.Column("notes", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "purchase_order_items",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("purchase_order_id", sa.Integer(), sa.ForeignKey("purchase_orders.id"), nullable=False),
        sa.Column("material_id", sa.Integer(), sa.ForeignKey("materials.id"), nullable=False),
        sa.Column("quantity", sa.Numeric(14, 4), nullable=False),
        sa.Column("received_qty", sa.Numeric(14, 4), nullable=False, server_default="0"),
        sa.Column("unit_price", sa.Numeric(12, 4), nullable=False, server_default="0"),
        sa.Column("uom", sa.String(20), nullable=False),
        sa.Column("notes", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "goods_receipts",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("gr_number", sa.String(100), nullable=False, unique=True),
        sa.Column("purchase_order_id", sa.Integer(), sa.ForeignKey("purchase_orders.id"), nullable=False),
        sa.Column("receipt_date", sa.Date(), nullable=False),
        sa.Column("status", sa.String(50), nullable=False, server_default="Draft"),
        sa.Column("received_by", sa.String(255)),
        sa.Column("notes", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "goods_receipt_items",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("goods_receipt_id", sa.Integer(), sa.ForeignKey("goods_receipts.id"), nullable=False),
        sa.Column("po_item_id", sa.Integer(), sa.ForeignKey("purchase_order_items.id"), nullable=False),
        sa.Column("material_id", sa.Integer(), sa.ForeignKey("materials.id"), nullable=False),
        sa.Column("received_qty", sa.Numeric(14, 4), nullable=False),
        sa.Column("accepted_qty", sa.Numeric(14, 4), nullable=False),
        sa.Column("rejected_qty", sa.Numeric(14, 4), nullable=False, server_default="0"),
        sa.Column("uom", sa.String(20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # -- Production --
    op.create_table(
        "production_plans",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("plan_number", sa.String(100), nullable=False, unique=True),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("buyer_orders.id"), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("status", sa.String(50), nullable=False, server_default="Draft"),
        sa.Column("notes", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "work_orders",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("wo_number", sa.String(100), nullable=False, unique=True),
        sa.Column("plan_id", sa.Integer(), sa.ForeignKey("production_plans.id"), nullable=False),
        sa.Column("style_variant_id", sa.Integer(), sa.ForeignKey("style_variants.id"), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("produced_qty", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("rejected_qty", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("status", sa.String(50), nullable=False, server_default="Planned"),
        sa.Column("notes", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "cutting_entries",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("work_order_id", sa.Integer(), sa.ForeignKey("work_orders.id"), nullable=False),
        sa.Column("entry_date", sa.Date(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("rejection_qty", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("alteration_qty", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("waste_qty", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("shift", sa.String(50)),
        sa.Column("operator", sa.String(255)),
        sa.Column("remarks", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "sewing_entries",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("work_order_id", sa.Integer(), sa.ForeignKey("work_orders.id"), nullable=False),
        sa.Column("entry_date", sa.Date(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("rejection_qty", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("alteration_qty", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("waste_qty", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("shift", sa.String(50)),
        sa.Column("operator", sa.String(255)),
        sa.Column("remarks", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "finishing_entries",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("work_order_id", sa.Integer(), sa.ForeignKey("work_orders.id"), nullable=False),
        sa.Column("entry_date", sa.Date(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("rejection_qty", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("alteration_qty", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("waste_qty", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("shift", sa.String(50)),
        sa.Column("operator", sa.String(255)),
        sa.Column("remarks", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # -- Quality --
    op.create_table(
        "quality_inspections",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("inspection_number", sa.String(100), nullable=False, unique=True),
        sa.Column("qc_type", sa.String(50), nullable=False),
        sa.Column("status", sa.String(50), nullable=False, server_default="Pending"),
        sa.Column("work_order_id", sa.Integer(), sa.ForeignKey("work_orders.id")),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("buyer_orders.id")),
        sa.Column("style_variant_id", sa.Integer(), sa.ForeignKey("style_variants.id")),
        sa.Column("material_id", sa.Integer(), sa.ForeignKey("materials.id")),
        sa.Column("inspected_qty", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("passed_qty", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("rejected_qty", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("inspector", sa.String(255)),
        sa.Column("inspection_date", sa.Date(), nullable=False),
        sa.Column("remarks", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "defects",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("inspection_id", sa.Integer(), sa.ForeignKey("quality_inspections.id"), nullable=False),
        sa.Column("defect_type", sa.String(100), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("remarks", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # -- Packing & Shipment --
    op.create_table(
        "packing_lists",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("packing_number", sa.String(100), nullable=False, unique=True),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("buyer_orders.id"), nullable=False),
        sa.Column("style_variant_id", sa.Integer(), sa.ForeignKey("style_variants.id"), nullable=False),
        sa.Column("packing_date", sa.Date(), nullable=False),
        sa.Column("total_cartons", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("total_quantity", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status", sa.String(50), nullable=False, server_default="Draft"),
        sa.Column("warehouse", sa.String(255)),
        sa.Column("remarks", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "packing_list_items",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("packing_list_id", sa.Integer(), sa.ForeignKey("packing_lists.id"), nullable=False),
        sa.Column("carton_no", sa.String(50), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("size_id", sa.Integer(), sa.ForeignKey("sizes.id")),
        sa.Column("color_id", sa.Integer(), sa.ForeignKey("colors.id")),
        sa.Column("gross_weight", sa.Numeric(10, 2)),
        sa.Column("net_weight", sa.Numeric(10, 2)),
        sa.Column("carton_dimensions", sa.String(100)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "shipments",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("shipment_number", sa.String(100), nullable=False, unique=True),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("buyer_orders.id"), nullable=False),
        sa.Column("packing_list_id", sa.Integer(), sa.ForeignKey("packing_lists.id")),
        sa.Column("shipment_date", sa.Date(), nullable=False),
        sa.Column("carrier", sa.String(255)),
        sa.Column("tracking_number", sa.String(255)),
        sa.Column("port_of_loading", sa.String(255)),
        sa.Column("port_of_discharge", sa.String(255)),
        sa.Column("status", sa.String(50), nullable=False, server_default="Planned"),
        sa.Column("remarks", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "shipment_items",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("shipment_id", sa.Integer(), sa.ForeignKey("shipments.id"), nullable=False),
        sa.Column("style_variant_id", sa.Integer(), sa.ForeignKey("style_variants.id"), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("cartons", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # -- TNA --
    op.create_table(
        "tna_plans",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("buyer_orders.id"), nullable=False),
        sa.Column("plan_name", sa.String(255), nullable=False),
        sa.Column("notes", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "tna_milestones",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("tna_plan_id", sa.Integer(), sa.ForeignKey("tna_plans.id"), nullable=False),
        sa.Column("milestone_name", sa.String(255), nullable=False),
        sa.Column("planned_date", sa.Date(), nullable=False),
        sa.Column("actual_date", sa.Date()),
        sa.Column("status", sa.String(50), nullable=False, server_default="Pending"),
        sa.Column("responsible_person", sa.String(255)),
        sa.Column("remarks", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("tna_milestones")
    op.drop_table("tna_plans")
    op.drop_table("shipment_items")
    op.drop_table("shipments")
    op.drop_table("packing_list_items")
    op.drop_table("packing_lists")
    op.drop_table("defects")
    op.drop_table("quality_inspections")
    op.drop_table("finishing_entries")
    op.drop_table("sewing_entries")
    op.drop_table("cutting_entries")
    op.drop_table("work_orders")
    op.drop_table("production_plans")
    op.drop_table("goods_receipt_items")
    op.drop_table("goods_receipts")
    op.drop_table("purchase_order_items")
    op.drop_table("purchase_orders")
    op.drop_table("purchase_requisition_items")
    op.drop_table("purchase_requisitions")
    op.drop_table("inventory_transactions")
    op.drop_table("stock_balances")
    op.drop_table("material_requirements")
    op.drop_table("garment_bom_items")
    op.drop_table("garment_boms")
    op.drop_table("buyer_order_items")
    op.drop_table("buyer_orders")
    op.drop_table("style_variants")
    op.drop_table("styles")
    op.drop_table("materials")
    op.drop_table("sizes")
    op.drop_table("colors")
    op.drop_table("suppliers")
    op.drop_table("buyers")
    op.drop_table("users")
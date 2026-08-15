"""
Seed comprehensive, production-ready demonstration dataset for NextGen Garments Ltd.
(Dhaka, Bangladesh).
Idempotent: safe to run multiple times without duplicating data.
"""
from datetime import date
from decimal import Decimal
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.user import Role, User
from app.models.master import Buyer, Supplier, Color, Size, Material, Style, StyleVariant
from app.models.order import BuyerOrder, BuyerOrderItem, OrderStatus
from app.models.tna import TNAPlan, TNAMilestone
from app.models.bom import GarmentBom, GarmentBomItem
from app.models.material_requirement import MaterialRequirement
from app.models.procurement import (
    PurchaseRequisition,
    PurchaseRequisitionItem,
    PurchaseOrder,
    PurchaseOrderItem,
    GoodsReceipt,
    GoodsReceiptItem,
)
from app.models.inventory import StockBalance, InventoryTransaction
from app.models.production import ProductionPlan, WorkOrder, CuttingEntry, SewingEntry, FinishingEntry
from app.models.quality import QualityInspection, Defect
from app.models.packing import PackingList, PackingListItem
from app.models.shipment import Shipment, ShipmentItem


def seed_users(db: Session):
    print("--> Seeding Role-Specific Demo Users...")
    users_data = [
        ("admin", "admin123", "admin@nextgen.com", "System Administrator", Role.ADMIN),
        ("merchandiser", "demo123", "merch@nextgen.com", "Sarah Ahmed (Sr. Merchandiser)", Role.MERCHANDISER),
        ("production", "demo123", "prod@nextgen.com", "Tariqul Islam (Production Manager)", Role.PRODUCTION_MANAGER),
        ("cutting", "demo123", "cutting@nextgen.com", "Kamal Hosain (Cutting Supervisor)", Role.CUTTING_SUPERVISOR),
        ("sewing", "demo123", "sewing@nextgen.com", "Nasrin Akter (Sewing Line Supervisor)", Role.SEWING_SUPERVISOR),
        ("finishing", "demo123", "finishing@nextgen.com", "Rafiqul Alam (Finishing Supervisor)", Role.FINISHING_SUPERVISOR),
        ("quality", "demo123", "quality@nextgen.com", "Monir Hossain (Chief Quality Inspector)", Role.QUALITY_INSPECTOR),
        ("inventory", "demo123", "inventory@nextgen.com", "Abul Kalam (Store & Inventory Officer)", Role.STORE_OFFICER),
        ("procurement", "demo123", "procurement@nextgen.com", "Farhana Yasmin (Procurement Officer)", Role.PROCUREMENT_OFFICER),
    ]

    for username, password, email, full_name, role in users_data:
        existing = db.query(User).filter(User.username == username).first()
        if not existing:
            user = User(
                username=username,
                email=email,
                full_name=full_name,
                hashed_password=get_password_hash(password),
                role=role,
                is_active=True,
            )
            db.add(user)
    db.commit()


def seed_garment_demo_workflow(db: Session):
    print("--> Seeding NextGen Garments Ltd. Connected Demo Workflow...")

    # 1. Buyer
    buyer = db.query(Buyer).filter(Buyer.code == "BUY-001").first()
    if not buyer:
        buyer = Buyer(
            code="BUY-001",
            name="H&M Demo Buyer",
            contact_person="Anna Andersson",
            email="anna.demo@hm.com",
            phone="+46 8 796 5500",
            country="Sweden",
            address="Mäster Samuelsgatan 46A, Stockholm",
            is_active=True,
        )
        db.add(buyer)
        db.commit()
        db.refresh(buyer)

    # 2. Suppliers
    suppliers = {}
    sup_data = [
        ("SUP-001", "ABC Textile Mills Ltd.", "Rahim Textile", "rahim@abctextile.com", "Dhaka, Bangladesh", "30 Days Net"),
        ("SUP-002", "Dhaka Accessories & Trims Ltd.", "Kamal Hosain", "kamal@dhakaacc.com", "Gazipur, Bangladesh", "Cash on Delivery"),
        ("SUP-003", "Global Packaging Solutions Ltd.", "Tariqul Islam", "tariq@globalpkg.com", "Narayanganj, Bangladesh", "15 Days Net"),
    ]
    for code, name, contact, email, address, terms in sup_data:
        sup = db.query(Supplier).filter(Supplier.code == code).first()
        if not sup:
            sup = Supplier(code=code, name=name, contact_person=contact, email=email, address=address, payment_terms=terms, is_active=True)
            db.add(sup)
            db.commit()
            db.refresh(sup)
        suppliers[code] = sup

    # 3. Colors & Sizes
    navy = db.query(Color).filter(Color.name == "Navy Blue").first()
    if not navy:
        navy = Color(name="Navy Blue", code="NAVY", hex_code="#000080")
        db.add(navy)
        db.commit()
        db.refresh(navy)

    white = db.query(Color).filter(Color.name == "White").first()
    if not white:
        white = Color(name="White", code="WHITE", hex_code="#FFFFFF")
        db.add(white)
        db.commit()
        db.refresh(white)

    sizes = {}
    for code, name, sort_order in [("S", "S", 1), ("M", "M", 2), ("L", "L", 3), ("XL", "XL", 4)]:
        sz = db.query(Size).filter(Size.name == name).first()
        if not sz:
            sz = Size(name=name, code=code, sort_order=sort_order)
            db.add(sz)
            db.commit()
            db.refresh(sz)
        sizes[code] = sz

    # 4. Materials
    materials_data = [
        ("MAT-FAB-001", "100% Cotton Pique Fabric (220 GSM)", "Fabric", "kg", Decimal("5.50")),
        ("MAT-THR-001", "40/2 Polyester Sewing Thread (Navy)", "Thread", "roll", Decimal("1.20")),
        ("MAT-BTN-001", "18L 3-Hole Pearl Buttons", "Button", "pcs", Decimal("0.05")),
        ("MAT-LBL-001", "H&M Main Woven Brand Label", "Label", "pcs", Decimal("0.10")),
        ("MAT-LBL-002", "Size Woven Label (S-XL)", "Label", "pcs", Decimal("0.02")),
        ("MAT-LBL-003", "Care & Composition Printed Label", "Label", "pcs", Decimal("0.03")),
        ("MAT-TAG-001", "H&M Price Hang Tag", "Accessory", "pcs", Decimal("0.08")),
        ("MAT-PKG-001", "Self-Adhesive Individual Poly Bag", "Packaging", "pcs", Decimal("0.04")),
        ("MAT-PKG-002", "7-Ply Heavy Duty Export Carton (60x40x40 cm)", "Packaging", "pcs", Decimal("1.50")),
    ]
    mat_map = {}
    for code, name, cat, uom, cost in materials_data:
        m = db.query(Material).filter(Material.code == code).first()
        if not m:
            m = Material(code=code, name=name, category=cat, uom=uom, unit_cost=cost, currency="USD", is_active=True)
            db.add(m)
            db.commit()
            db.refresh(m)
        mat_map[code] = m

    # 5. Style & Style Variants
    style = db.query(Style).filter(Style.style_no == "NG-POLO-001").first()
    if not style:
        style = Style(
            style_no="NG-POLO-001",
            description="Men's Classic Cotton Pique Polo Shirt with 3-Button Placket",
            buyer_id=buyer.id,
            category="Knitwear",
            is_active=True,
        )
        db.add(style)
        db.commit()
        db.refresh(style)

    variants = {}
    for size_code in ["S", "M", "L", "XL"]:
        v_code = f"NG-POLO-001-NAVY-{size_code}"
        var = db.query(StyleVariant).filter(StyleVariant.variant_code == v_code).first()
        if not var:
            var = StyleVariant(
                style_id=style.id,
                style_no=style.style_no,
                color_id=navy.id,
                size_id=sizes[size_code].id,
                variant_code=v_code,
            )
            db.add(var)
            db.commit()
            db.refresh(var)
        variants[size_code] = var

    # 6. Garment BOM
    bom = db.query(GarmentBom).filter(GarmentBom.style_id == style.id).first()
    if not bom:
        bom = GarmentBom(
            style_id=style.id,
            bom_name="Standard Polo Shirt BOM V1.0",
            version=1,
            status="Active",
            is_active=True,
            notes="Standard Polo Shirt BOM for H&M Spring Collection",
        )
        db.add(bom)
        db.commit()
        db.refresh(bom)

        bom_items = [
            (mat_map["MAT-FAB-001"].id, Decimal("0.2500"), "kg", Decimal("5.00")),
            (mat_map["MAT-THR-001"].id, Decimal("0.0500"), "roll", Decimal("2.00")),
            (mat_map["MAT-BTN-001"].id, Decimal("3.0000"), "pcs", Decimal("2.00")),
            (mat_map["MAT-LBL-001"].id, Decimal("1.0000"), "pcs", Decimal("1.00")),
            (mat_map["MAT-LBL-002"].id, Decimal("1.0000"), "pcs", Decimal("1.00")),
            (mat_map["MAT-LBL-003"].id, Decimal("1.0000"), "pcs", Decimal("1.00")),
            (mat_map["MAT-TAG-001"].id, Decimal("1.0000"), "pcs", Decimal("1.00")),
            (mat_map["MAT-PKG-001"].id, Decimal("1.0000"), "pcs", Decimal("2.00")),
            (mat_map["MAT-PKG-002"].id, Decimal("0.0100"), "pcs", Decimal("0.00")),
        ]
        for mat_id, qty, uom, wastage in bom_items:
            item = GarmentBomItem(bom_id=bom.id, material_id=mat_id, quantity_per_garment=qty, uom=uom, wastage_percent=wastage)
            db.add(item)
        db.commit()

    # 7. Buyer Order
    order = db.query(BuyerOrder).filter(BuyerOrder.po_number == "PO-2026-001").first()
    if not order:
        order = BuyerOrder(
            po_number="PO-2026-001",
            buyer_id=buyer.id,
            style_id=style.id,
            order_date=date(2026, 1, 10),
            delivery_date=date(2026, 4, 15),
            currency="USD",
            status=OrderStatus.IN_PRODUCTION,
            remarks="10,000 Pcs Men's Navy Polo Shirt Order for H&M Spring Collection",
        )
        db.add(order)
        db.commit()
        db.refresh(order)

        for size_code in ["S", "M", "L", "XL"]:
            item = BuyerOrderItem(
                order_id=order.id,
                style_variant_id=variants[size_code].id,
                quantity=2500,
                unit_price=Decimal("6.5000"),
                color_id=navy.id,
                size_id=sizes[size_code].id,
            )
            db.add(item)
        db.commit()

    # 8. TNA Plan
    tna = db.query(TNAPlan).filter(TNAPlan.order_id == order.id).first()
    if not tna:
        tna = TNAPlan(order_id=order.id, plan_name="TNA Milestone Plan for Order PO-2026-001", notes="Master TNA schedule for H&M order")
        db.add(tna)
        db.commit()
        db.refresh(tna)

        milestones = [
            ("Order Confirmation", date(2026, 1, 10), date(2026, 1, 10), "Completed"),
            ("Fabric Booking", date(2026, 1, 15), date(2026, 1, 15), "Completed"),
            ("Fabric In-house", date(2026, 2, 10), date(2026, 2, 8), "Completed"),
            ("Trims In-house", date(2026, 2, 15), date(2026, 2, 12), "Completed"),
            ("PP Sample Approval", date(2026, 2, 20), date(2026, 2, 20), "Completed"),
            ("Cutting Start", date(2026, 2, 25), date(2026, 2, 25), "Completed"),
            ("Sewing Start", date(2026, 3, 1), date(2026, 3, 1), "Completed"),
            ("Finishing Start", date(2026, 3, 20), date(2026, 3, 20), "Completed"),
            ("Final QC Inspection", date(2026, 4, 5), date(2026, 4, 5), "Completed"),
            ("Ex-Factory Shipment", date(2026, 4, 10), date(2026, 4, 10), "On Track"),
        ]
        for name, p_date, a_date, st in milestones:
            m = TNAMilestone(tna_plan_id=tna.id, milestone_name=name, planned_date=p_date, actual_date=a_date, status=st)
            db.add(m)
        db.commit()

    # 9. Material Requirements (MRP)
    mrp_items = [
        (mat_map["MAT-FAB-001"].id, Decimal("0.2500"), Decimal("5.00"), Decimal("2625.0000")),
        (mat_map["MAT-THR-001"].id, Decimal("0.0500"), Decimal("2.00"), Decimal("510.0000")),
        (mat_map["MAT-BTN-001"].id, Decimal("3.0000"), Decimal("2.00"), Decimal("30600.0000")),
        (mat_map["MAT-LBL-001"].id, Decimal("1.0000"), Decimal("1.00"), Decimal("10100.0000")),
        (mat_map["MAT-PKG-001"].id, Decimal("1.0000"), Decimal("2.00"), Decimal("10200.0000")),
        (mat_map["MAT-PKG-002"].id, Decimal("0.0100"), Decimal("0.00"), Decimal("100.0000")),
    ]
    for m_id, cons, wastage, req_qty in mrp_items:
        mr = db.query(MaterialRequirement).filter(MaterialRequirement.order_id == order.id, MaterialRequirement.material_id == m_id).first()
        if not mr:
            mr = MaterialRequirement(
                order_id=order.id,
                material_id=m_id,
                total_order_qty=10000,
                consumption_per_unit=cons,
                wastage_percent=wastage,
                required_qty=req_qty,
                available_qty=req_qty,
                reserved_qty=req_qty,
                incoming_qty=Decimal("0.0000"),
                shortage_qty=Decimal("0.0000"),
                status="Fulfilled",
            )
            db.add(mr)
    db.commit()

    # 10. Procurement (PR, PO, GR)
    pr = db.query(PurchaseRequisition).filter(PurchaseRequisition.pr_number == "PR-2026-001").first()
    if not pr:
        pr = PurchaseRequisition(
            pr_number="PR-2026-001",
            order_id=order.id,
            requested_by="Sarah Ahmed",
            required_date=date(2026, 2, 10),
            status="Approved",
            notes="Raw materials procurement for H&M Order PO-2026-001",
        )
        db.add(pr)
        db.commit()
        db.refresh(pr)

        pr_item = PurchaseRequisitionItem(requisition_id=pr.id, material_id=mat_map["MAT-FAB-001"].id, quantity=Decimal("2700.0000"), uom="kg")
        db.add(pr_item)
        db.commit()

    po_pur = db.query(PurchaseOrder).filter(PurchaseOrder.po_number == "PO-PUR-001").first()
    if not po_pur:
        po_pur = PurchaseOrder(
            po_number="PO-PUR-001",
            supplier_id=suppliers["SUP-001"].id,
            requisition_id=pr.id,
            order_date=date(2026, 1, 18),
            expected_date=date(2026, 2, 8),
            currency="USD",
            status="Received",
            notes="100% Cotton Pique Fabric purchase from ABC Textile Mills",
        )
        db.add(po_pur)
        db.commit()
        db.refresh(po_pur)

        po_item = PurchaseOrderItem(
            purchase_order_id=po_pur.id,
            material_id=mat_map["MAT-FAB-001"].id,
            quantity=Decimal("2700.0000"),
            received_qty=Decimal("2700.0000"),
            unit_price=Decimal("5.5000"),
            uom="kg",
        )
        db.add(po_item)
        db.commit()

    gr = db.query(GoodsReceipt).filter(GoodsReceipt.gr_number == "GR-2026-001").first()
    if not gr:
        gr = GoodsReceipt(
            gr_number="GR-2026-001",
            purchase_order_id=po_pur.id,
            receipt_date=date(2026, 2, 8),
            status="Received",
            received_by="Abul Kalam",
            notes="Fabric inspected and received into warehouse stock",
        )
        db.add(gr)
        db.commit()
        db.refresh(gr)

        gr_item = GoodsReceiptItem(
            goods_receipt_id=gr.id,
            po_item_id=po_pur.items[0].id,
            material_id=mat_map["MAT-FAB-001"].id,
            received_qty=Decimal("2700.0000"),
            accepted_qty=Decimal("2700.0000"),
            rejected_qty=Decimal("0.0000"),
            uom="kg",
        )
        db.add(gr_item)
        db.commit()

    # 11. Inventory Stock Balances
    for code, m in mat_map.items():
        stk = db.query(StockBalance).filter(StockBalance.material_id == m.id).first()
        if not stk:
            qty = Decimal("2700.0000") if code == "MAT-FAB-001" else Decimal("35000.0000") if "BTN" in code else Decimal("12000.0000")
            stk = StockBalance(
                material_id=m.id,
                category="Raw Material",
                quantity=qty,
                reserved_qty=Decimal("0.0000"),
            )
            db.add(stk)
            txn = InventoryTransaction(
                material_id=m.id,
                category="Raw Material",
                transaction_type="Purchase Receipt",
                quantity=qty,
                balance_after=qty,
                reference_type="GOODS_RECEIPT",
                reference_id=gr.id if gr else 1,
                remarks="Initial goods receipt stock entry into warehouse",
            )
            db.add(txn)
    db.commit()

    # 12. Production Plan & Work Orders
    prod_plan = db.query(ProductionPlan).filter(ProductionPlan.plan_number == "PLAN-2026-001").first()
    if not prod_plan:
        prod_plan = ProductionPlan(
            plan_number="PLAN-2026-001",
            order_id=order.id,
            start_date=date(2026, 2, 25),
            end_date=date(2026, 4, 5),
            status="In Progress",
            notes="Main floor production plan for PO-2026-001 (10,000 pcs)",
        )
        db.add(prod_plan)
        db.commit()
        db.refresh(prod_plan)

        for size_code in ["S", "M", "L", "XL"]:
            wo = WorkOrder(
                wo_number=f"WO-2026-001-{size_code}",
                plan_id=prod_plan.id,
                style_variant_id=variants[size_code].id,
                quantity=2500,
                produced_qty=2425,
                rejected_qty=75,
                start_date=date(2026, 3, 1),
                end_date=date(2026, 3, 25),
                status="Completed",
            )
            db.add(wo)
        db.commit()

    work_orders = db.query(WorkOrder).filter(WorkOrder.plan_id == prod_plan.id).all()

    # 13. Cutting Entries
    for wo in work_orders:
        cut_exist = db.query(CuttingEntry).filter(CuttingEntry.work_order_id == wo.id).first()
        if not cut_exist:
            c_entry = CuttingEntry(
                work_order_id=wo.id,
                entry_date=date(2026, 2, 26),
                quantity=2550,
                rejection_qty=50,
                operator="Kamal Hosain (Cutting Supervisor)",
            )
            db.add(c_entry)
    db.commit()

    # 14. Sewing Entries
    for wo in work_orders:
        sew_exist = db.query(SewingEntry).filter(SewingEntry.work_order_id == wo.id).first()
        if not sew_exist:
            s_entry = SewingEntry(
                work_order_id=wo.id,
                entry_date=date(2026, 3, 10),
                quantity=2462,
                rejection_qty=38,
                operator="Nasrin Akter (Sewing Line 01)",
            )
            db.add(s_entry)
    db.commit()

    # 15. Finishing Entries
    for wo in work_orders:
        fin_exist = db.query(FinishingEntry).filter(FinishingEntry.work_order_id == wo.id).first()
        if not fin_exist:
            f_entry = FinishingEntry(
                work_order_id=wo.id,
                entry_date=date(2026, 3, 25),
                quantity=2425,
                rejection_qty=37,
                operator="Rafiqul Alam (Finishing Supervisor)",
            )
            db.add(f_entry)
    db.commit()

    # 16. Quality Inspection & Defects
    qc = db.query(QualityInspection).filter(QualityInspection.inspection_number == "QC-2026-001").first()
    if not qc:
        qc = QualityInspection(
            inspection_number="QC-2026-001",
            qc_type="Final",
            status="Passed",
            work_order_id=work_orders[0].id if work_orders else None,
            order_id=order.id,
            style_variant_id=variants["M"].id,
            inspected_qty=9700,
            passed_qty=9450,
            rejected_qty=250,
            inspector="Monir Hossain (Chief Quality Inspector)",
            inspection_date=date(2026, 4, 5),
            remarks="AQL 2.5 Final Garment Inspection Passed for Export Packing",
        )
        db.add(qc)
        db.commit()
        db.refresh(qc)

        defects_data = [
            ("Open Seam at Shoulder", 80, "Reworked"),
            ("Oil Stain on Front Panel", 60, "Rejected"),
            ("Broken Stitch at Bottom Hem", 50, "Reworked"),
            ("Measurement Out of Spec (+1cm)", 40, "Rejected"),
            ("Wrong Placement of Care Label", 20, "Reworked"),
        ]
        for defect_type, qty, rem in defects_data:
            d = Defect(inspection_id=qc.id, defect_type=defect_type, quantity=qty, remarks=rem)
            db.add(d)
        db.commit()

    # 17. Packing List & Items
    packing = db.query(PackingList).filter(PackingList.packing_number == "PACK-2026-001").first()
    if not packing:
        packing = PackingList(
            packing_number="PACK-2026-001",
            order_id=order.id,
            style_variant_id=variants["M"].id,
            packing_date=date(2026, 4, 8),
            total_cartons=95,
            total_quantity=9450,
            status="Packed",
            warehouse="Main Export Warehouse - Chittagong Gate",
            remarks="9,450 Pcs packed in 95 solid-size 7-ply export cartons",
        )
        db.add(packing)
        db.commit()
        db.refresh(packing)

        for i in range(1, 96):
            item = PackingListItem(
                packing_list_id=packing.id,
                carton_no=f"CTN-{i:03d}",
                quantity=100,
                size_id=sizes["M"].id,
                color_id=navy.id,
                gross_weight=Decimal("22.50"),
                net_weight=Decimal("20.00"),
                carton_dimensions="60x40x40 cm",
            )
            db.add(item)
        db.commit()

    # 18. Shipment & Shipment Items
    shipment = db.query(Shipment).filter(Shipment.shipment_number == "SHIP-2026-001").first()
    if not shipment:
        shipment = Shipment(
            shipment_number="SHIP-2026-001",
            order_id=order.id,
            packing_list_id=packing.id,
            shipment_date=date(2026, 4, 10),
            carrier="Maersk Line (Container Vessel)",
            tracking_number="MSK-DHAKA-2026-001",
            port_of_loading="Chittagong Port, Bangladesh",
            port_of_discharge="Gothenburg Port, Sweden",
            status="In Transit",
            remarks="Containers loaded and dispatched for ocean freight to Sweden",
        )
        db.add(shipment)
        db.commit()
        db.refresh(shipment)

        for size_code in ["S", "M", "L", "XL"]:
            s_item = ShipmentItem(
                shipment_id=shipment.id,
                style_variant_id=variants[size_code].id,
                quantity=2362,
                cartons=24,
            )
            db.add(s_item)
        db.commit()

    print("--> NextGen Garments Ltd. Connected Demo Workflow Seeded Successfully!")


def main():
    db = SessionLocal()
    try:
        seed_users(db)
        seed_garment_demo_workflow(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
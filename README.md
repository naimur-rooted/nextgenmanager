# BloomWorks Garment ERP

An Enterprise Resource Planning (ERP) software system designed for garment manufacturing and export factories (RMG sector). Built with FastAPI (Python 3.13), PostgreSQL, SQLAlchemy 2.0, and React (Vite, Tailwind CSS).

---

## 🌟 Key Features & Operational Modules

- **User Management & RBAC:** Role-Based Access Control (RBAC) supporting 9 distinct garment factory roles. Account provisioning managed exclusively by System Administrators.
- **Master Data Management:** Buyers, Suppliers, Styles, Style Variants, Colors, Sizes, Materials.
- **Merchandising & Order Management:** Buyer Orders, Time & Action (TNA) Milestone Tracking.
- **BOM & Material Requirements (MRP):** Garment Bill of Materials, automated material consumption and shortage calculations.
- **Procurement & Goods Receipt:** Purchase Requisitions (PR), Vendor Purchase Orders (PO), Goods Receipts (GR), Inventory Stock Balances.
- **Production Line Floor Tracking:** Production Planning, Work Orders, Line Execution for **Cutting**, **Sewing**, and **Finishing**.
- **Quality Control (QC):** Inspection Auditing (AQL 2.5), Defect Logging (Open Seams, Oil Stains, Broken Stitches), Pass/Fail Ratios.
- **Packing & Logistics:** Packing Lists, Carton Assortment, Export Shipping & Vessel Tracking.

---

## 👥 Role-Specific Demo Credentials at a Glance

All demo accounts use the standard password `demo123` (except System Administrator, which uses `admin123`).

| Role Name | System Username | Password | Full Name & Title | Responsibilities & Access |
| :--- | :--- | :--- | :--- | :--- |
| **System Administrator** | `admin` | `admin123` | System Administrator | User Management (`/users`), Master Config, Full Access |
| **Merchandiser** | `merchandiser` | `demo123` | Sarah Ahmed (Sr. Merchandiser) | Buyers, Orders, TNA, Styles, BOM, MRP |
| **Production Manager** | `production` | `demo123` | Tariqul Islam (Production Mgr) | Production Plans, Work Orders, Floor Progress |
| **Cutting Supervisor** | `cutting` | `demo123` | Kamal Hosain (Cutting Supv) | Work Orders, Cutting Output, Cut Loss Logs |
| **Sewing Supervisor** | `sewing` | `demo123` | Nasrin Akter (Sewing Line Supv) | Work Orders, Sewing Output, Line Efficiency |
| **Finishing Supervisor** | `finishing` | `demo123` | Rafiqul Alam (Finishing Supv) | Work Orders, Ironing, Folding, Finishing Output |
| **Quality Inspector** | `quality` | `demo123` | Monir Hossain (Chief QC Inspector)| QC Inspections, Defect Logging, AQL Audits |
| **Store / Inventory Officer**| `inventory` | `demo123` | Abul Kalam (Store Officer) | Stock Balances, Material Issues, Warehouse |
| **Procurement Officer** | `procurement` | `demo123` | Farhana Yasmin (Procurement) | Purchase Requisitions, Supplier POs, GR |

---

## 🛠️ Technology Stack

- **Backend:** Python 3.13, FastAPI, SQLAlchemy 2.0, Alembic, Passlib (Bcrypt), PyJWT, Uvicorn, Gunicorn.
- **Database:** PostgreSQL (Render Managed) / SQLite (Local Development).
- **Frontend:** React 18, Vite 6, Tailwind CSS, Lucide Icons, Axios, React Router v6.
- **Deployment:** Render Cloud Platform (Backend Web Service + Static Site Frontend + PostgreSQL).

---

## 🚀 Connected Garment Export Order Lifecycle Workflow

```
[1. BUYER]           H&M Demo Buyer (Code: BUY-001, Sweden)
      │
[2. STYLE]           NG-POLO-001 — Men's Classic Cotton Pique Polo Shirt
      │
[3. BUYER ORDER]     PO-2026-001 (10,000 Pcs @ $6.50/pc = $65,000 USD)
      │
[4. TNA PLAN]        10 Milestones (Booking -> Fabric -> Trims -> Cutting -> Sewing -> Shipment)
      │
[5. GARMENT BOM]     0.25 kg Pique Fabric, 3 Buttons, Labels, Poly Bag, Carton
      │
[6. MRP CALC]        2,625 kg Fabric, 30,600 Buttons, 10,100 Labels, 10,200 Poly Bags
      │
[7. PROCUREMENT]     PR-2026-001 -> PO-PUR-001 (ABC Textile Mills) & PO-PUR-002 (Dhaka Accessories)
      │
[8. GOODS RECEIPT]   GR-2026-001 (2,700 kg Fabric Received & Inspected into Stock)
      │
[9. INVENTORY]       Stock Balances updated (2,700 kg Fabric, 35,000 Buttons, 105 Cartons)
      │
[10. PRODUCTION]     PLAN-2026-001 -> 4 Work Orders (WO-2026-001-S to XL)
      │
[11. CUTTING]        10,200 Pcs Cut, 200 Rejected (Net 10,000 Pcs Cut Output)
      │
[12. SEWING]         9,850 Pcs Sewn across Sewing Line 01
      │
[13. FINISHING]      9,700 Pcs Finished, Ironed & Folded
      │
[14. QUALITY (QC)]   QC-2026-001 (9,700 Inspected, 9,450 Passed, 250 Failed/Defect Logged)
      │
[15. PACKING]        PACK-2026-001 (9,450 Pcs packed into 95 7-Ply Export Cartons)
      │
[16. SHIPMENT]       SHIP-2026-001 (Maersk Line Vessel, Chittagong Port -> Gothenburg, Sweden)
```

---

## 💻 Local Development Setup

### 1. Backend Setup
```bash
cd backend
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
python -m alembic upgrade head
python seed.py
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 🌐 Live Deployment URLs
- **Frontend App:** [https://nextgenmanagerui.onrender.com/login](https://nextgenmanagerui.onrender.com/login)
- **Backend API Docs:** [https://nextgenmanagerdb.onrender.com/docs](https://nextgenmanagerdb.onrender.com/docs)

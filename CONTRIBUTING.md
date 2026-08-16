# Contributing to BloomWorks Garment ERP

Thank you for your interest in contributing to BloomWorks Garment ERP! This guide will help you get started with our codebase, architecture, and development workflow.

---

## 🚀 Getting Started

1. **Fork** the repository on GitHub:
   `https://github.com/naimur-rooted/BloomWorks_Garment_ERP`
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/naimur-rooted/BloomWorks_Garment_ERP.git
   cd BloomWorks_Garment_ERP
   ```
3. **Create a branch** for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

---

## 🛠️ Local Development Setup

Refer to `README.md` for full stack details. Quick start:

```bash
# Backend Setup (Python 3.13 / FastAPI)
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m alembic upgrade head
python seed.py
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Frontend Setup (React / Vite / Tailwind CSS) - in a separate terminal
cd ../frontend
npm install
npm run dev
```

---

## 📐 Architecture & Code Guidelines

### 1. Backend Architecture (Python 3.13 + FastAPI)
- **Pattern:** Follow the existing modular structure: **Model $\rightarrow$ Schema $\rightarrow$ Service $\rightarrow$ Router $\rightarrow$ Dependencies**.
- **Database:** SQLAlchemy 2.0 ORM with PostgreSQL. All models extend `TimestampMixin` and `Base`.
- **Validation:** Pydantic 2.0 schemas for request/response DTOs.
- **Authentication:** OAuth2 Password bearer token flow with JWT.
- **Role-Based Access Control (RBAC):** Use `require_roles(*roles: Role)` dependency on routers to enforce administrative and operational permission boundaries.
- **Audit & Account Security:** Deactivate accounts via `is_active = False` rather than hard-deleting records.

### 2. Database & Migrations
- All database schema changes **MUST** be managed via Alembic in `backend/alembic/versions/`.
- Never modify existing migration files—always create a new sequential migration:
  ```bash
  python -m alembic revision -m "add_new_feature_table"
  ```
- Keep all migrations compatible with both PostgreSQL and SQLite (used for in-memory testing).

### 3. Frontend Architecture (React 18 + Vite 6 + Tailwind CSS)
- **UI Components:** Modular components in `src/components/` and `src/components/ui/` (DataTable, Modal, etc.).
- **Pages:** Module views in `src/pages/`.
- **API Services:** Axios client with base interceptors in `src/services/api.js`.
- **Icons:** Use `lucide-react` icons exclusively.

---

## 🧪 Submitting Changes

1. Verify backend submodules import cleanly:
   ```powershell
   python -c "import pkgutil, importlib, app; [importlib.import_module(n) for _, n, _ in pkgutil.walk_packages(app.__path__, 'app.')]; print('OK')"
   ```
2. Run database seed to verify idempotency:
   ```bash
   python seed.py
   ```
3. Verify frontend production build:
   ```bash
   cd frontend
   npm run build
   ```
4. Commit your changes with clear, descriptive messages and open a Pull Request.

---

Thank you for helping build **BloomWorks Garment ERP**!</tool_call>
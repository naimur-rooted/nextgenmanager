"""Seed initial data: default admin user."""
from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.user import Role, User


def main():
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.username == "admin").first()
        if existing:
            print("Admin user already exists.")
            return

        admin = User(
            email="admin@nextgen.com",
            username="admin",
            full_name="System Administrator",
            hashed_password=get_password_hash("admin123"),
            role=Role.ADMIN,
        )
        db.add(admin)
        db.commit()
        print("Created default admin user: admin / admin123")
    finally:
        db.close()


if __name__ == "__main__":
    main()
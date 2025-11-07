from app.core.database import SessionLocal, Base, engine
from app.core.security import get_password_hash
from app.models.user import User, UserRole

# Drop all tables and recreate
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Create only admin user
db = SessionLocal()
try:
    admin = User(
        email="admin@faithschool.rw",
        hashed_password=get_password_hash("Admin2024"),
        full_name="System Administrator",
        role=UserRole.ADMIN,
        phone="+250788000000",
        is_active=True
    )
    db.add(admin)
    db.commit()
    print("Database reset complete. Admin user created.")
    print("Email: admin@faithschool.rw")
    print("Password: Admin2024")
except Exception as e:
    print(f"Error: {e}")
    db.rollback()
finally:
    db.close()

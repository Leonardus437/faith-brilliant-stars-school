from app.core.database import SessionLocal, Base, engine
from app.core.security import get_password_hash
from app.models import *
from app.models.user import UserRole
from app.models.student import EnrollmentStatus
from app.models.fee import PaymentCategory, InvoiceStatus
from app.models.guardian import student_guardians
from app.models.attendance import AttendanceStatus
from datetime import date, datetime, timedelta
import random

db = SessionLocal()

try:
    print("Checking database status...")
    
    # Check existing data
    user_count = db.query(User).count()
    student_count = db.query(Student).count()
    invoice_count = db.query(Invoice).count()
    attendance_count = db.query(Attendance).count()
    
    print(f"Current database contains:")
    print(f"   • {user_count} users")
    print(f"   • {student_count} students")
    print(f"   • {invoice_count} invoices")
    print(f"   • {attendance_count} attendance records")
    
    if user_count >= 4 and student_count >= 60:
        print("\n[SUCCESS] Database already has sufficient data!")
        print("[READY] System is ready to use with existing data.")
        print("\n[LOGIN] CREDENTIALS:")
        print("Head Teacher: head@faithschool.rw / Head2024")
        print("Teacher: teacher@faithschool.rw / Teacher2024")
        print("Accountant: accounts@faithschool.rw / Accounts2024")
        print("Parent: parent@faithschool.rw / Parent2024")
    else:
        print("\n[WARNING] Database needs basic seeding. Run seed_direct.py first.")
    
except Exception as e:
    print(f"Error checking database: {e}")
finally:
    db.close()
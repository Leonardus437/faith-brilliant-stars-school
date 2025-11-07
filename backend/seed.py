from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models import *
from app.models.user import UserRole
from app.models.student import EnrollmentStatus
from app.models.fee import PaymentCategory, InvoiceStatus
from app.models.guardian import student_guardians
from datetime import date, datetime, timedelta
import random

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # Check if already seeded
        if db.query(User).first():
            print("Database already seeded")
            return
        
        print("Seeding database...")
        
        # Create users
        users_data = [
            {"email": "admin@faithschool.rw", "password": "Admin2024", "full_name": "System Admin", "role": UserRole.ADMIN, "phone": "+250788000001"},
            {"email": "head@faithschool.rw", "password": "Head2024", "full_name": "Head Teacher", "role": UserRole.HEAD_TEACHER, "phone": "+250788000002"},
            {"email": "teacher@faithschool.rw", "password": "Teacher2024", "full_name": "John Teacher", "role": UserRole.TEACHER, "phone": "+250788000003"},
            {"email": "accounts@faithschool.rw", "password": "Accounts2024", "full_name": "Mary Accountant", "role": UserRole.ACCOUNTANT, "phone": "+250788000004"},
            {"email": "parent@faithschool.rw", "password": "Parent2024", "full_name": "Jane Parent", "role": UserRole.PARENT, "phone": "+250788000005"},
        ]
        
        users = []
        for user_data in users_data:
            user = User(
                email=user_data["email"],
                hashed_password=get_password_hash(user_data["password"]),
                full_name=user_data["full_name"],
                role=user_data["role"],
                phone=user_data["phone"],
                is_active=True
            )
            db.add(user)
            users.append(user)
        db.commit()
        print(f"Created {len(users)} users")
        
        # Create subjects
        subjects_data = [
            {"name": "Mathematics", "code": "MATH"},
            {"name": "English", "code": "ENG"},
            {"name": "Kinyarwanda", "code": "KIN"},
            {"name": "Science", "code": "SCI"},
            {"name": "Social Studies", "code": "SST"},
            {"name": "Physical Education", "code": "PE"},
        ]
        
        subjects = []
        for subj_data in subjects_data:
            subject = Subject(**subj_data)
            db.add(subject)
            subjects.append(subject)
        db.commit()
        print(f"Created {len(subjects)} subjects")
        
        # Create teacher
        teacher_user = [u for u in users if u.role == UserRole.TEACHER][0]
        teacher = Teacher(
            user_id=teacher_user.id,
            employee_number="EMP001",
            first_name="John",
            last_name="Teacher",
            phone="+250788000003",
            qualification="Bachelor of Education",
            hire_date=datetime.now()
        )
        db.add(teacher)
        db.commit()
        print("Created teacher profile")
        
        # Create classes P1-P6
        classes = []
        for grade in range(1, 7):
            class_obj = Class(
                name=f"P{grade} A",
                grade_level=f"P{grade}",
                academic_year="2024",
                class_teacher_id=teacher.id,
                capacity=40,
                room_number=f"R{grade}01"
            )
            db.add(class_obj)
            classes.append(class_obj)
        db.commit()
        print(f"Created {len(classes)} classes")
        
        # Create guardian
        parent_user = [u for u in users if u.role == UserRole.PARENT][0]
        guardian = Guardian(
            user_id=parent_user.id,
            first_name="Jane",
            last_name="Parent",
            phone="+250788000005",
            email="parent@faithschool.rw",
            national_id="1198012345678901",
            occupation="Business Owner",
            address="Kigali, Gasabo"
        )
        db.add(guardian)
        db.commit()
        print("Created guardian profile")
        
        # Create students (10 per class)
        students = []
        student_count = 1
        for class_obj in classes:
            for i in range(10):
                # Create user for student
                student_user = User(
                    email=f"student{student_count}@faithschool.rw",
                    hashed_password=get_password_hash("Student2024"),
                    full_name=f"Student {student_count}",
                    role=UserRole.STUDENT,
                    is_active=True
                )
                db.add(student_user)
                db.flush()
                
                student = Student(
                    user_id=student_user.id,
                    admission_number=f"FBS{2024}{student_count:04d}",
                    first_name=f"Student{student_count}",
                    last_name="Test",
                    date_of_birth=date(2010 + random.randint(0, 5), random.randint(1, 12), random.randint(1, 28)),
                    gender=random.choice(["Male", "Female"]),
                    class_id=class_obj.id,
                    enrollment_status=EnrollmentStatus.ACTIVE,
                    enrollment_date=date(2024, 1, 15)
                )
                db.add(student)
                students.append(student)
                student_count += 1
        db.commit()
        print(f"Created {len(students)} students")
        
        # Link first 5 students to guardian
        for student in students[:5]:
            db.execute(
                student_guardians.insert().values(
                    student_id=student.id,
                    guardian_id=guardian.id,
                    relation="parent",
                    is_primary=1
                )
            )
        db.commit()
        print("Linked students to guardian")
        
        # Create fee structures
        fee_categories = [
            (PaymentCategory.TUITION, 150000, "term_1"),
            (PaymentCategory.LUNCH, 30000, "term_1"),
            (PaymentCategory.TRANSPORT, 25000, "term_1"),
        ]
        
        for category, amount, term in fee_categories:
            for class_obj in classes:
                fee_structure = FeeStructure(
                    class_id=class_obj.id,
                    category=category,
                    term=term,
                    amount=amount,
                    is_active=True
                )
                db.add(fee_structure)
        db.commit()
        print("Created fee structures")
        
        # Create sample invoices
        invoice_count = 1
        for student in students[:20]:
            invoice = Invoice(
                invoice_number=f"INV-2024-{invoice_count:05d}",
                student_id=student.id,
                category=PaymentCategory.TUITION,
                term="term_1",
                amount=150000,
                amount_paid=0,
                status=InvoiceStatus.PENDING,
                due_date=datetime.now() + timedelta(days=30),
                created_by=users[0].id
            )
            db.add(invoice)
            invoice_count += 1
        db.commit()
        print("Created sample invoices")
        
        # Create service items
        service_items = [
            {"name": "Breakfast", "category": PaymentCategory.BREAKFAST, "unit_price": 500},
            {"name": "Porridge", "category": PaymentCategory.PORRIDGE, "unit_price": 300},
            {"name": "Lunch", "category": PaymentCategory.LUNCH, "unit_price": 1000},
            {"name": "Snacks", "category": PaymentCategory.SNACKS, "unit_price": 400},
        ]
        
        for item_data in service_items:
            service_item = ServiceItem(**item_data, is_active=True)
            db.add(service_item)
        db.commit()
        print("Created service items")
        
        print("\n✅ Database seeded successfully!")
        print("\n📧 Demo Login Credentials:")
        print("=" * 50)
        for user_data in users_data:
            print(f"Role: {user_data['role']:15} | Email: {user_data['email']:25} | Password: {user_data['password']}")
        print("=" * 50)
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()

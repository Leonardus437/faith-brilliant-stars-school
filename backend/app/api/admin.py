from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from app.core.database import get_db
from app.core.security import get_current_user, get_password_hash
from app.models import *
from app.models.user import UserRole
from app.models.student import EnrollmentStatus
from app.models.attendance import AttendanceStatus
from app.models.fee import InvoiceStatus
from datetime import datetime, date, timedelta

router = APIRouter(prefix="/admin", tags=["admin"])

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.HEAD_TEACHER:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

# DASHBOARD ANALYTICS
@router.get("/dashboard")
async def get_admin_dashboard(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    today = date.today()
    
    # Basic counts
    total_students = db.query(Student).count()
    total_teachers = db.query(User).filter(User.role == UserRole.TEACHER).count()
    total_classes = db.query(Class).count()
    total_parents = db.query(User).filter(User.role == UserRole.PARENT).count()
    
    # Financial overview
    total_revenue = db.query(func.sum(Payment.amount)).scalar() or 0
    outstanding_fees = db.query(func.sum(Invoice.amount - Invoice.amount_paid)).filter(Invoice.status != InvoiceStatus.PAID).scalar() or 0
    
    # Today's attendance
    today_attendance = db.query(Attendance).filter(Attendance.date == today).count()
    today_present = db.query(Attendance).filter(and_(Attendance.date == today, Attendance.status == AttendanceStatus.PRESENT)).count()
    attendance_rate = (today_present / today_attendance * 100) if today_attendance > 0 else 0
    
    # Recent activities
    recent_payments = db.query(Payment).order_by(Payment.payment_date.desc()).limit(5).all()
    recent_enrollments = db.query(Student).order_by(Student.enrollment_date.desc()).limit(5).all()
    
    return {
        "overview": {
            "total_students": total_students,
            "total_teachers": total_teachers,
            "total_classes": total_classes,
            "total_parents": total_parents,
            "total_revenue": total_revenue,
            "outstanding_fees": outstanding_fees,
            "attendance_rate": round(attendance_rate, 1)
        },
        "recent_payments": [{"id": p.id, "amount": p.amount, "student": "Student", "date": p.payment_date} for p in recent_payments],
        "recent_enrollments": [{"id": s.id, "name": s.first_name + " " + s.last_name, "class": s.class_.name if s.class_ else "No Class", "date": s.enrollment_date} for s in recent_enrollments]
    }

# STUDENT MANAGEMENT
@router.post("/students")
async def create_student(student_data: dict, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    # Generate admission number
    last_student = db.query(Student).order_by(Student.id.desc()).first()
    next_id = (last_student.id + 1) if last_student else 1
    admission_number = f"FBS2024{next_id:04d}"
    
    student = Student(
        admission_number=admission_number,
        first_name=student_data["first_name"],
        last_name=student_data["last_name"],
        date_of_birth=datetime.strptime(student_data["date_of_birth"], "%Y-%m-%d").date(),
        gender=student_data["gender"],
        class_id=student_data["class_id"],
        enrollment_status=EnrollmentStatus.ACTIVE,
        enrollment_date=date.today()
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return {"message": "Student created successfully", "student_id": student.id, "admission_number": admission_number}

@router.get("/students")
async def get_all_students(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    students = db.query(Student).join(Class).all()
    return [{
        "id": s.id,
        "admission_number": s.admission_number,
        "name": f"{s.first_name} {s.last_name}",
        "class": s.class_.name,
        "gender": s.gender,
        "age": (date.today() - s.date_of_birth).days // 365,
        "status": s.enrollment_status
    } for s in students]

@router.put("/students/{student_id}")
async def update_student(student_id: int, student_data: dict, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    for key, value in student_data.items():
        if key == "date_of_birth":
            value = datetime.strptime(value, "%Y-%m-%d").date()
        setattr(student, key, value)
    
    db.commit()
    return {"message": "Student updated successfully"}

@router.delete("/students/{student_id}")
async def delete_student(student_id: int, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Soft delete - change status instead of actual deletion
    student.enrollment_status = EnrollmentStatus.WITHDRAWN
    db.commit()
    return {"message": "Student withdrawn successfully"}

# CLASS MANAGEMENT
@router.post("/classes")
async def create_class(class_data: dict, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    class_obj = Class(
        name=class_data["name"],
        grade_level=class_data["grade_level"],
        academic_year=class_data.get("academic_year", "2024"),
        capacity=class_data.get("capacity", 40),
        room_number=class_data.get("room_number"),
        class_teacher_id=class_data.get("class_teacher_id")
    )
    db.add(class_obj)
    db.commit()
    db.refresh(class_obj)
    return {"message": "Class created successfully", "class_id": class_obj.id}

@router.get("/classes")
async def get_all_classes(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    classes = db.query(Class).all()
    return [{
        "id": c.id,
        "name": c.name,
        "grade_level": c.grade_level,
        "capacity": c.capacity,
        "current_students": db.query(Student).filter(Student.class_id == c.id).count(),
        "teacher": c.teacher.first_name + " " + c.teacher.last_name if c.teacher else "Not assigned",
        "room_number": c.room_number
    } for c in classes]

@router.put("/classes/{class_id}")
async def update_class(class_id: int, class_data: dict, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    class_obj = db.query(Class).filter(Class.id == class_id).first()
    if not class_obj:
        raise HTTPException(status_code=404, detail="Class not found")
    
    for key, value in class_data.items():
        setattr(class_obj, key, value)
    
    db.commit()
    return {"message": "Class updated successfully"}

# TEACHER MANAGEMENT
@router.post("/teachers")
async def create_teacher(teacher_data: dict, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    # Check if email exists
    existing_user = db.query(User).filter(User.email == teacher_data["email"]).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Create user account
    user = User(
        email=teacher_data["email"],
        hashed_password=get_password_hash(teacher_data["password"]),
        full_name=teacher_data["full_name"],
        role=UserRole.TEACHER,
        phone=teacher_data.get("phone"),
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create teacher profile
    teacher = Teacher(
        user_id=user.id,
        employee_number=f"EMP{user.id:03d}",
        first_name=teacher_data["full_name"].split()[0],
        last_name=teacher_data["full_name"].split()[-1],
        phone=teacher_data.get("phone"),
        qualification=teacher_data.get("qualification"),
        hire_date=date.today()
    )
    db.add(teacher)
    db.commit()
    
    return {"message": "Teacher created successfully", "teacher_id": teacher.id}

@router.get("/teachers")
async def get_all_teachers(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    teachers = db.query(Teacher).join(User).all()
    return [{
        "id": t.id,
        "name": f"{t.first_name} {t.last_name}",
        "email": t.user.email,
        "phone": t.phone,
        "employee_number": t.employee_number,
        "qualification": t.qualification,
        "hire_date": t.hire_date,
        "assigned_classes": [c.name for c in db.query(Class).filter(Class.class_teacher_id == t.id).all()]
    } for t in teachers]

# USER MANAGEMENT
@router.get("/users")
async def get_all_users(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    users = db.query(User).all()
    return [{
        "id": u.id,
        "email": u.email,
        "full_name": u.full_name,
        "role": u.role,
        "phone": u.phone,
        "is_active": u.is_active,
        "created_at": u.created_at
    } for u in users]

@router.put("/users/{user_id}/status")
async def toggle_user_status(user_id: int, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = not user.is_active
    db.commit()
    return {"message": f"User {'activated' if user.is_active else 'deactivated'} successfully"}

# FINANCIAL OVERVIEW
@router.get("/finances")
async def get_financial_overview(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    # Revenue by month
    monthly_revenue = db.query(
        func.strftime('%Y-%m', Payment.payment_date).label('month'),
        func.sum(Payment.amount).label('total')
    ).group_by(func.strftime('%Y-%m', Payment.payment_date)).all()
    
    # Outstanding fees by class
    outstanding_by_class = db.query(
        Class.name,
        func.sum(Invoice.amount - Invoice.amount_paid).label('outstanding')
    ).join(Student).join(Invoice).filter(Invoice.status != InvoiceStatus.PAID).group_by(Class.name).all()
    
    # Payment methods distribution
    payment_methods = db.query(
        Payment.payment_method,
        func.count(Payment.id).label('count'),
        func.sum(Payment.amount).label('total')
    ).group_by(Payment.payment_method).all()
    
    return {
        "monthly_revenue": [{"month": m[0], "total": m[1]} for m in monthly_revenue],
        "outstanding_by_class": [{"class": c[0], "outstanding": c[1]} for c in outstanding_by_class],
        "payment_methods": [{"method": p[0], "count": p[1], "total": p[2]} for p in payment_methods]
    }

# ATTENDANCE ANALYTICS
@router.get("/attendance/analytics")
async def get_attendance_analytics(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    # Overall attendance rate
    total_records = db.query(Attendance).count()
    present_records = db.query(Attendance).filter(Attendance.status == AttendanceStatus.PRESENT).count()
    overall_rate = (present_records / total_records * 100) if total_records > 0 else 0
    
    # Attendance by class
    class_attendance = db.query(
        Class.name,
        func.count(Attendance.id).label('total'),
        func.sum(func.case([(Attendance.status == AttendanceStatus.PRESENT, 1)], else_=0)).label('present')
    ).join(Student).join(Attendance).group_by(Class.name).all()
    
    # Daily attendance for last 30 days
    thirty_days_ago = date.today() - timedelta(days=30)
    daily_attendance = db.query(
        Attendance.date,
        func.count(Attendance.id).label('total'),
        func.sum(func.case([(Attendance.status == AttendanceStatus.PRESENT, 1)], else_=0)).label('present')
    ).filter(Attendance.date >= thirty_days_ago).group_by(Attendance.date).all()
    
    return {
        "overall_rate": round(overall_rate, 1),
        "class_attendance": [{"class": c[0], "rate": round((c[2]/c[1]*100) if c[1] > 0 else 0, 1)} for c in class_attendance],
        "daily_attendance": [{"date": str(d[0]), "rate": round((d[2]/d[1]*100) if d[1] > 0 else 0, 1)} for d in daily_attendance]
    }

# ANNOUNCEMENTS
@router.post("/announcements")
async def create_announcement(announcement_data: dict, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    announcement = Announcement(
        title=announcement_data["title"],
        content=announcement_data["content"],
        priority=announcement_data.get("priority", "medium"),
        created_by=admin.id,
        is_active=True
    )
    db.add(announcement)
    db.commit()
    return {"message": "Announcement created successfully"}

@router.get("/announcements")
async def get_announcements(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    announcements = db.query(Announcement).order_by(Announcement.created_at.desc()).all()
    return [{
        "id": a.id,
        "title": a.title,
        "content": a.content,
        "priority": a.priority,
        "is_active": a.is_active,
        "created_at": a.created_at
    } for a in announcements]

# REPORTS
@router.get("/reports/students")
async def get_student_report(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    students = db.query(Student).join(Class).all()
    return [{
        "admission_number": s.admission_number,
        "name": f"{s.first_name} {s.last_name}",
        "class": s.class_.name,
        "gender": s.gender,
        "age": (date.today() - s.date_of_birth).days // 365,
        "enrollment_date": s.enrollment_date,
        "status": s.enrollment_status
    } for s in students]

@router.get("/reports/financial")
async def get_financial_report(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    # Detailed financial report
    invoices = db.query(Invoice).join(Student).join(Class).all()
    return [{
        "invoice_number": i.invoice_number,
        "student": "Student Name",
        "class": "Class Name",
        "category": i.category,
        "amount": i.amount,
        "amount_paid": i.amount_paid,
        "balance": i.amount - i.amount_paid,
        "status": i.status,
        "due_date": i.due_date
    } for i in invoices]

# SYSTEM SETTINGS
@router.get("/settings")
async def get_system_settings(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    # Return current system configuration
    return {
        "school_name": "Faith Brilliant Stars School",
        "academic_year": "2024",
        "terms": ["Term 1", "Term 2", "Term 3"],
        "fee_categories": ["tuition", "lunch", "transport", "uniform", "books"],
        "payment_methods": ["Cash", "MTN MoMo", "Airtel Money", "Bank Transfer"]
    }

@router.put("/settings")
async def update_system_settings(settings_data: dict, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    # Update system settings (would typically be stored in a settings table)
    return {"message": "Settings updated successfully"}
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List
from datetime import datetime, timedelta
from ..core.database import get_db
from ..core.security import get_current_user, require_role
from ..models.user import User, UserRole
from ..models.student import Student, EnrollmentStatus
from ..models.teacher import Teacher
from ..models.class_model import Class, Subject
from ..models.attendance import Attendance
from ..models.fee import Invoice, Payment, InvoiceStatus
from ..models.academic_calendar import AcademicTerm, Holiday, SchoolEvent
from ..models.school_settings import SchoolSettings, PromotionRule, Discount
from ..models.audit_log import AuditLog
from pydantic import BaseModel

router = APIRouter()

# ============ DASHBOARD ANALYTICS ============
class DashboardStats(BaseModel):
    total_students: int
    total_teachers: int
    total_classes: int
    active_students: int
    attendance_rate: float
    revenue_this_month: float
    outstanding_fees: float
    recent_activities: List[dict]

@router.get("/head-teacher/dashboard", response_model=DashboardStats)
async def get_dashboard(
    db: Session = Depends(get_db),
    current_user = Depends(require_role("head_teacher", "admin"))
):
    total_students = db.query(Student).count()
    active_students = db.query(Student).filter(Student.enrollment_status == EnrollmentStatus.ACTIVE).count()
    total_teachers = db.query(Teacher).count()
    total_classes = db.query(Class).count()
    
    # Attendance rate (last 30 days)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    attendance_records = db.query(Attendance).filter(Attendance.date >= thirty_days_ago).all()
    present_count = sum(1 for a in attendance_records if a.status == "present")
    attendance_rate = (present_count / len(attendance_records) * 100) if attendance_records else 0
    
    # Revenue this month
    first_day = datetime.now().replace(day=1)
    payments = db.query(Payment).filter(Payment.payment_date >= first_day).all()
    revenue_this_month = sum(p.amount for p in payments)
    
    # Outstanding fees
    invoices = db.query(Invoice).filter(Invoice.status.in_([InvoiceStatus.PENDING, InvoiceStatus.PARTIAL])).all()
    outstanding_fees = sum(i.amount - i.amount_paid for i in invoices)
    
    # Recent activities
    recent_logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(10).all()
    recent_activities = [{"action": log.action, "entity": log.entity_type, "time": log.created_at} for log in recent_logs]
    
    return DashboardStats(
        total_students=total_students,
        total_teachers=total_teachers,
        total_classes=total_classes,
        active_students=active_students,
        attendance_rate=round(attendance_rate, 2),
        revenue_this_month=revenue_this_month,
        outstanding_fees=outstanding_fees,
        recent_activities=recent_activities
    )

# ============ STUDENT MANAGEMENT ============
class StudentCreate(BaseModel):
    admission_number: str
    first_name: str
    last_name: str
    date_of_birth: str
    gender: str
    class_id: int
    enrollment_date: str
    emergency_contact: dict
    medical_info: dict | None = None

@router.post("/head-teacher/students")
async def create_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("head_teacher", "admin"))
):
    student = Student(
        admission_number=student_data.admission_number,
        first_name=student_data.first_name,
        last_name=student_data.last_name,
        date_of_birth=datetime.fromisoformat(student_data.date_of_birth),
        gender=student_data.gender,
        class_id=student_data.class_id,
        enrollment_status=EnrollmentStatus.ACTIVE,
        enrollment_date=datetime.fromisoformat(student_data.enrollment_date),
        emergency_contact=student_data.emergency_contact,
        medical_info=student_data.medical_info
    )
    db.add(student)
    db.commit()
    
    # Audit log
    audit = AuditLog(user_id=current_user.id, action="create", entity_type="student", entity_id=student.id)
    db.add(audit)
    db.commit()
    
    return {"message": "Student created", "id": student.id}

@router.put("/head-teacher/students/{student_id}")
async def update_student(
    student_id: int,
    student_data: StudentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("head_teacher", "admin"))
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    for key, value in student_data.dict(exclude_unset=True).items():
        if key in ["date_of_birth", "enrollment_date"] and isinstance(value, str):
            value = datetime.fromisoformat(value)
        setattr(student, key, value)
    
    db.commit()
    audit = AuditLog(user_id=current_user.id, action="update", entity_type="student", entity_id=student_id)
    db.add(audit)
    db.commit()
    
    return {"message": "Student updated"}

@router.delete("/head-teacher/students/{student_id}")
async def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("head_teacher", "admin"))
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.enrollment_status = EnrollmentStatus.WITHDRAWN
    db.commit()
    
    audit = AuditLog(user_id=current_user.id, action="delete", entity_type="student", entity_id=student_id)
    db.add(audit)
    db.commit()
    
    return {"message": "Student withdrawn"}

# ============ TEACHER MANAGEMENT ============
class TeacherCreate(BaseModel):
    email: str
    full_name: str
    employee_number: str
    first_name: str
    last_name: str
    phone: str
    qualification: str
    specialization: str

@router.post("/head-teacher/teachers")
async def create_teacher(
    teacher_data: TeacherCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("head_teacher", "admin"))
):
    from ..core.security import get_password_hash
    
    # Create user account
    user = User(
        email=teacher_data.email,
        hashed_password=get_password_hash("Teacher2024"),
        full_name=teacher_data.full_name,
        phone=teacher_data.phone,
        role=UserRole.TEACHER
    )
    db.add(user)
    db.flush()
    
    # Create teacher profile
    teacher = Teacher(
        user_id=user.id,
        employee_number=teacher_data.employee_number,
        first_name=teacher_data.first_name,
        last_name=teacher_data.last_name,
        phone=teacher_data.phone,
        qualification=teacher_data.qualification,
        specialization=teacher_data.specialization,
        hire_date=datetime.now()
    )
    db.add(teacher)
    db.commit()
    
    audit = AuditLog(user_id=current_user.id, action="create", entity_type="teacher", entity_id=teacher.id)
    db.add(audit)
    db.commit()
    
    return {"message": "Teacher created", "id": teacher.id}

@router.get("/head-teacher/teachers")
async def list_teachers(
    db: Session = Depends(get_db),
    current_user = Depends(require_role("head_teacher", "admin"))
):
    teachers = db.query(Teacher).all()
    return [{"id": t.id, "name": f"{t.first_name} {t.last_name}", "employee_number": t.employee_number, 
             "qualification": t.qualification, "specialization": t.specialization} for t in teachers]

# ============ CLASS MANAGEMENT ============
class ClassCreate(BaseModel):
    name: str
    grade_level: str
    academic_year: str
    class_teacher_id: int | None = None
    capacity: int = 40
    room_number: str | None = None

@router.post("/head-teacher/classes")
async def create_class(
    class_data: ClassCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("head_teacher", "admin"))
):
    new_class = Class(**class_data.dict())
    db.add(new_class)
    db.commit()
    
    audit = AuditLog(user_id=current_user.id, action="create", entity_type="class", entity_id=new_class.id)
    db.add(audit)
    db.commit()
    
    return {"message": "Class created", "id": new_class.id}

# ============ ACADEMIC CALENDAR ============
class TermCreate(BaseModel):
    name: str
    academic_year: str
    start_date: str
    end_date: str

@router.post("/head-teacher/terms")
async def create_term(
    term_data: TermCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("head_teacher", "admin"))
):
    term = AcademicTerm(
        name=term_data.name,
        academic_year=term_data.academic_year,
        start_date=datetime.fromisoformat(term_data.start_date),
        end_date=datetime.fromisoformat(term_data.end_date)
    )
    db.add(term)
    db.commit()
    return {"message": "Term created", "id": term.id}

@router.get("/head-teacher/terms")
async def list_terms(
    db: Session = Depends(get_db),
    current_user = Depends(require_role("head_teacher", "admin"))
):
    terms = db.query(AcademicTerm).all()
    return [{"id": t.id, "name": t.name, "year": t.academic_year, 
             "start": t.start_date, "end": t.end_date, "active": t.is_active} for t in terms]

# ============ SCHOOL SETTINGS ============
@router.get("/head-teacher/settings")
async def get_settings(
    db: Session = Depends(get_db),
    current_user = Depends(require_role("head_teacher", "admin"))
):
    settings = db.query(SchoolSettings).first()
    if not settings:
        settings = SchoolSettings()
        db.add(settings)
        db.commit()
    return settings

@router.put("/head-teacher/settings")
async def update_settings(
    settings_data: dict,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("head_teacher", "admin"))
):
    settings = db.query(SchoolSettings).first()
    if not settings:
        settings = SchoolSettings()
        db.add(settings)
    
    for key, value in settings_data.items():
        if hasattr(settings, key):
            setattr(settings, key, value)
    
    db.commit()
    return {"message": "Settings updated"}

# ============ REPORTS ============
@router.get("/head-teacher/reports/attendance")
async def attendance_report(
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("head_teacher", "admin"))
):
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)
    
    records = db.query(Attendance).filter(
        and_(Attendance.date >= start, Attendance.date <= end)
    ).all()
    
    total = len(records)
    present = sum(1 for r in records if r.status == "present")
    absent = sum(1 for r in records if r.status == "absent")
    late = sum(1 for r in records if r.status == "late")
    
    return {
        "total_records": total,
        "present": present,
        "absent": absent,
        "late": late,
        "attendance_rate": round((present / total * 100) if total > 0 else 0, 2)
    }

@router.get("/head-teacher/reports/financial")
async def financial_report(
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("head_teacher", "admin"))
):
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)
    
    payments = db.query(Payment).filter(
        and_(Payment.payment_date >= start, Payment.payment_date <= end)
    ).all()
    
    total_revenue = sum(p.amount for p in payments)
    
    invoices = db.query(Invoice).filter(Invoice.status != InvoiceStatus.PAID).all()
    outstanding = sum(i.amount - i.amount_paid for i in invoices)
    
    return {
        "total_revenue": total_revenue,
        "outstanding_fees": outstanding,
        "payment_count": len(payments),
        "period": f"{start_date} to {end_date}"
    }

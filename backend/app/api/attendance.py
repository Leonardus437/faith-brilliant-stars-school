from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import date, datetime
from ..core.database import get_db
from ..core.security import get_current_user, require_role
from ..models.user import User, UserRole
from ..models.attendance import Attendance, AttendanceStatus
from ..models.student import Student
from ..models.class_model import Class
from pydantic import BaseModel

router = APIRouter()

class AttendanceRecord(BaseModel):
    student_id: int
    status: str
    notes: str = None

class AttendanceSubmit(BaseModel):
    class_id: int
    date: str
    records: List[AttendanceRecord]

class AttendanceResponse(BaseModel):
    id: int
    student_id: int
    student_name: str
    class_id: int
    date: str
    status: str
    notes: str = None
    recorded_by: int
    recorded_at: str

    class Config:
        from_attributes = True

@router.get("/classes", dependencies=[Depends(require_role("teacher", "admin", "head_teacher"))])
def get_teacher_classes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get classes assigned to teacher"""
    if current_user.role == UserRole.ADMIN or current_user.role == UserRole.HEAD_TEACHER:
        classes = db.query(Class).all()
    else:
        from ..models.teacher import Teacher
        teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher profile not found")
        classes = db.query(Class).filter(Class.class_teacher_id == teacher.id).all()
    
    return [{
        "id": c.id,
        "name": c.name,
        "grade_level": c.grade_level,
        "student_count": db.query(Student).filter(Student.class_id == c.id).count()
    } for c in classes]

@router.get("/students/{class_id}", dependencies=[Depends(require_role("teacher", "admin", "head_teacher"))])
def get_class_students(class_id: int, db: Session = Depends(get_db)):
    """Get students in a class"""
    students = db.query(Student).filter(Student.class_id == class_id).all()
    return [{
        "id": s.id,
        "admission_number": s.admission_number,
        "first_name": s.first_name,
        "last_name": s.last_name,
        "full_name": f"{s.first_name} {s.last_name}"
    } for s in students]

@router.post("/submit", dependencies=[Depends(require_role("teacher", "admin", "head_teacher"))])
def submit_attendance(data: AttendanceSubmit, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Submit attendance for a class"""
    attendance_date = datetime.strptime(data.date, "%Y-%m-%d").date()
    
    # Delete existing attendance for this class and date
    db.query(Attendance).filter(
        Attendance.class_id == data.class_id,
        Attendance.date == attendance_date
    ).delete()
    
    # Create new attendance records
    for record in data.records:
        attendance = Attendance(
            student_id=record.student_id,
            class_id=data.class_id,
            date=attendance_date,
            status=AttendanceStatus(record.status),
            notes=record.notes,
            recorded_by=current_user.id,
            recorded_at=datetime.now()
        )
        db.add(attendance)
    
    db.commit()
    return {"message": f"Attendance recorded for {len(data.records)} students"}

@router.get("/view/{class_id}/{date}", dependencies=[Depends(require_role("teacher", "admin", "head_teacher"))])
def view_attendance(class_id: int, date: str, db: Session = Depends(get_db)):
    """View attendance for a class on a specific date"""
    attendance_date = datetime.strptime(date, "%Y-%m-%d").date()
    
    records = db.query(Attendance, Student).join(Student).filter(
        Attendance.class_id == class_id,
        Attendance.date == attendance_date
    ).all()
    
    return [{
        "id": att.id,
        "student_id": att.student_id,
        "student_name": f"{student.first_name} {student.last_name}",
        "admission_number": student.admission_number,
        "status": att.status.value,
        "notes": att.notes,
        "recorded_at": att.recorded_at.isoformat() if att.recorded_at else None
    } for att, student in records]

@router.get("/report/{class_id}", dependencies=[Depends(require_role("teacher", "admin", "head_teacher"))])
def attendance_report(class_id: int, start_date: str = None, end_date: str = None, db: Session = Depends(get_db)):
    """Get attendance report for a class"""
    query = db.query(
        Student.id,
        Student.admission_number,
        Student.first_name,
        Student.last_name,
        func.count(Attendance.id).label("total_days"),
        func.sum(func.case((Attendance.status == AttendanceStatus.PRESENT, 1), else_=0)).label("present"),
        func.sum(func.case((Attendance.status == AttendanceStatus.ABSENT, 1), else_=0)).label("absent"),
        func.sum(func.case((Attendance.status == AttendanceStatus.LATE, 1), else_=0)).label("late")
    ).outerjoin(Attendance, Student.id == Attendance.student_id).filter(Student.class_id == class_id)
    
    if start_date:
        query = query.filter(Attendance.date >= datetime.strptime(start_date, "%Y-%m-%d").date())
    if end_date:
        query = query.filter(Attendance.date <= datetime.strptime(end_date, "%Y-%m-%d").date())
    
    results = query.group_by(Student.id).all()
    
    return [{
        "student_id": r.id,
        "admission_number": r.admission_number,
        "student_name": f"{r.first_name} {r.last_name}",
        "total_days": r.total_days or 0,
        "present": r.present or 0,
        "absent": r.absent or 0,
        "late": r.late or 0,
        "attendance_rate": round((r.present or 0) / r.total_days * 100, 1) if r.total_days else 0
    } for r in results]

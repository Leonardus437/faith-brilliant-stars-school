from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List
from datetime import datetime, timedelta
from ..core.database import get_db
from ..core.security import get_current_user, require_role
from ..models.attendance import Attendance
from ..models.student import Student
from ..models.class_model import Class
from ..models.teacher import Teacher
from ..models.user import User
from pydantic import BaseModel

router = APIRouter()

# ============ TEACHER DASHBOARD ============
class TeacherDashboard(BaseModel):
    assigned_classes: List[dict]
    total_students: int
    today_attendance_rate: float
    this_week_attendance_rate: float
    students_with_low_attendance: List[dict]
    quick_stats: dict

@router.get("/teacher/dashboard", response_model=TeacherDashboard)
async def get_teacher_dashboard(
    db: Session = Depends(get_db),
    current_user = Depends(require_role("teacher"))
):
    # Get teacher profile
    teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    # Get assigned classes
    classes = db.query(Class).filter(Class.class_teacher_id == teacher.id).all()
    assigned_classes = [
        {
            "id": c.id,
            "name": c.name,
            "grade": c.grade_level,
            "student_count": len(c.students),
            "room": c.room_number
        } for c in classes
    ]
    
    # Total students
    total_students = sum(len(c.students) for c in classes)
    
    # Today's attendance
    today = datetime.now().date()
    today_records = db.query(Attendance).filter(func.date(Attendance.date) == today).all()
    today_present = sum(1 for r in today_records if r.status == "present")
    today_attendance_rate = (today_present / len(today_records) * 100) if today_records else 0
    
    # This week's attendance
    week_start = datetime.now() - timedelta(days=7)
    week_records = db.query(Attendance).filter(Attendance.date >= week_start).all()
    week_present = sum(1 for r in week_records if r.status == "present")
    week_attendance_rate = (week_present / len(week_records) * 100) if week_records else 0
    
    # Students with low attendance (< 75%)
    low_attendance_students = []
    for class_ in classes:
        for student in class_.students:
            student_records = db.query(Attendance).filter(
                and_(Attendance.student_id == student.id, Attendance.date >= week_start)
            ).all()
            if student_records:
                present_count = sum(1 for r in student_records if r.status == "present")
                rate = (present_count / len(student_records) * 100)
                if rate < 75:
                    low_attendance_students.append({
                        "name": f"{student.first_name} {student.last_name}",
                        "class": class_.name,
                        "rate": round(rate, 1)
                    })
    
    quick_stats = {
        "classes": len(classes),
        "students": total_students,
        "marked_today": len(today_records),
        "alerts": len(low_attendance_students)
    }
    
    return TeacherDashboard(
        assigned_classes=assigned_classes,
        total_students=total_students,
        today_attendance_rate=round(today_attendance_rate, 2),
        this_week_attendance_rate=round(week_attendance_rate, 2),
        students_with_low_attendance=low_attendance_students[:10],
        quick_stats=quick_stats
    )

# ============ QUICK ATTENDANCE MARKING ============
class BulkAttendanceCreate(BaseModel):
    class_id: int
    date: str
    attendance_records: List[dict]  # [{student_id, status}]

@router.post("/teacher/attendance/bulk")
async def mark_bulk_attendance(
    attendance_data: BulkAttendanceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("teacher", "head_teacher", "admin"))
):
    date = datetime.fromisoformat(attendance_data.date)
    
    created_count = 0
    for record in attendance_data.attendance_records:
        # Check if already exists
        existing = db.query(Attendance).filter(
            and_(
                Attendance.student_id == record["student_id"],
                func.date(Attendance.date) == date.date()
            )
        ).first()
        
        if existing:
            existing.status = record["status"]
        else:
            attendance = Attendance(
                student_id=record["student_id"],
                class_id=attendance_data.class_id,
                date=date,
                status=record["status"],
                marked_by=current_user.id
            )
            db.add(attendance)
            created_count += 1
    
    db.commit()
    return {"message": f"Attendance marked for {created_count} students"}

# ============ MARK ALL PRESENT ============
@router.post("/teacher/attendance/mark-all-present")
async def mark_all_present(
    class_id: int,
    date: str,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("teacher", "head_teacher", "admin"))
):
    class_ = db.query(Class).filter(Class.id == class_id).first()
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    
    attendance_date = datetime.fromisoformat(date)
    
    for student in class_.students:
        existing = db.query(Attendance).filter(
            and_(
                Attendance.student_id == student.id,
                func.date(Attendance.date) == attendance_date.date()
            )
        ).first()
        
        if not existing:
            attendance = Attendance(
                student_id=student.id,
                class_id=class_id,
                date=attendance_date,
                status="present",
                marked_by=current_user.id
            )
            db.add(attendance)
    
    db.commit()
    return {"message": f"All students marked present for {class_.name}"}

# ============ ATTENDANCE HISTORY ============
@router.get("/teacher/attendance/history")
async def get_attendance_history(
    class_id: int,
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("teacher", "head_teacher", "admin"))
):
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)
    
    records = db.query(Attendance).filter(
        and_(
            Attendance.class_id == class_id,
            Attendance.date >= start,
            Attendance.date <= end
        )
    ).all()
    
    # Group by date
    by_date = {}
    for record in records:
        date_key = record.date.strftime("%Y-%m-%d")
        if date_key not in by_date:
            by_date[date_key] = {"present": 0, "absent": 0, "late": 0, "sick": 0}
        by_date[date_key][record.status] = by_date[date_key].get(record.status, 0) + 1
    
    return {"history": by_date, "total_records": len(records)}

# ============ STUDENT ATTENDANCE PROFILE ============
@router.get("/teacher/students/{student_id}/attendance")
async def get_student_attendance_profile(
    student_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("teacher", "head_teacher", "admin"))
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Last 30 days
    thirty_days_ago = datetime.now() - timedelta(days=30)
    records = db.query(Attendance).filter(
        and_(Attendance.student_id == student_id, Attendance.date >= thirty_days_ago)
    ).all()
    
    total = len(records)
    present = sum(1 for r in records if r.status == "present")
    absent = sum(1 for r in records if r.status == "absent")
    late = sum(1 for r in records if r.status == "late")
    
    return {
        "student_name": f"{student.first_name} {student.last_name}",
        "admission_number": student.admission_number,
        "total_days": total,
        "present": present,
        "absent": absent,
        "late": late,
        "attendance_rate": round((present / total * 100) if total > 0 else 0, 2),
        "recent_records": [
            {
                "date": r.date.strftime("%Y-%m-%d"),
                "status": r.status
            } for r in sorted(records, key=lambda x: x.date, reverse=True)[:10]
        ]
    }

# ============ CLASS ROSTER ============
@router.get("/teacher/classes/{class_id}/roster")
async def get_class_roster(
    class_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("teacher", "head_teacher", "admin"))
):
    class_ = db.query(Class).filter(Class.id == class_id).first()
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    
    students = []
    for student in sorted(class_.students, key=lambda s: (s.last_name, s.first_name)):
        # Get recent attendance
        recent_records = db.query(Attendance).filter(
            Attendance.student_id == student.id
        ).order_by(Attendance.date.desc()).limit(5).all()
        
        students.append({
            "id": student.id,
            "admission_number": student.admission_number,
            "name": f"{student.first_name} {student.last_name}",
            "gender": student.gender,
            "photo_url": student.photo_url,
            "recent_attendance": [r.status for r in recent_records]
        })
    
    return {
        "class_name": class_.name,
        "grade": class_.grade_level,
        "total_students": len(students),
        "students": students
    }

# ============ ATTENDANCE REPORTS ============
@router.get("/teacher/reports/attendance-summary")
async def get_attendance_summary(
    class_id: int,
    month: str,  # YYYY-MM
    db: Session = Depends(get_db),
    current_user = Depends(require_role("teacher", "head_teacher", "admin"))
):
    # Parse month
    year, month_num = map(int, month.split("-"))
    start_date = datetime(year, month_num, 1)
    
    # Calculate end date
    if month_num == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month_num + 1, 1)
    
    records = db.query(Attendance).filter(
        and_(
            Attendance.class_id == class_id,
            Attendance.date >= start_date,
            Attendance.date < end_date
        )
    ).all()
    
    # Group by student
    by_student = {}
    for record in records:
        student_id = record.student_id
        if student_id not in by_student:
            student = db.query(Student).filter(Student.id == student_id).first()
            by_student[student_id] = {
                "name": f"{student.first_name} {student.last_name}",
                "present": 0,
                "absent": 0,
                "late": 0,
                "total": 0
            }
        
        by_student[student_id][record.status] += 1
        by_student[student_id]["total"] += 1
    
    # Calculate rates
    for student_id in by_student:
        total = by_student[student_id]["total"]
        present = by_student[student_id]["present"]
        by_student[student_id]["rate"] = round((present / total * 100) if total > 0 else 0, 2)
    
    return {
        "month": month,
        "class_id": class_id,
        "summary": list(by_student.values())
    }

# ============ OFFLINE SYNC ============
@router.post("/teacher/attendance/sync")
async def sync_offline_attendance(
    sync_data: List[dict],
    db: Session = Depends(get_db),
    current_user = Depends(require_role("teacher", "head_teacher", "admin"))
):
    """Sync attendance records marked offline"""
    synced_count = 0
    
    for record in sync_data:
        existing = db.query(Attendance).filter(
            and_(
                Attendance.student_id == record["student_id"],
                func.date(Attendance.date) == datetime.fromisoformat(record["date"]).date()
            )
        ).first()
        
        if not existing:
            attendance = Attendance(
                student_id=record["student_id"],
                class_id=record["class_id"],
                date=datetime.fromisoformat(record["date"]),
                status=record["status"],
                marked_by=current_user.id
            )
            db.add(attendance)
            synced_count += 1
    
    db.commit()
    return {"message": f"Synced {synced_count} attendance records"}

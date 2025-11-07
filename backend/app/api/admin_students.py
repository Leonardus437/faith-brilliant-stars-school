from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user, get_password_hash
from app.models import *
from app.models.user import UserRole
from datetime import datetime, date

router = APIRouter(prefix="/admin/students", tags=["admin-students"])

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.HEAD_TEACHER:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

@router.post("")
async def create_student(student_data: dict, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
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
    return {"message": "Student created successfully", "student_id": student.id}

@router.get("")
async def get_all_students(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    students = db.query(Student).join(Class).all()
    return [{
        "id": s.id,
        "admission_number": s.admission_number,
        "name": f"{s.first_name} {s.last_name}",
        "class": s.class_obj.name,
        "gender": s.gender,
        "age": (date.today() - s.date_of_birth).days // 365,
        "status": s.enrollment_status
    } for s in students]

@router.put("/{student_id}")
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

@router.delete("/{student_id}")
async def delete_student(student_id: int, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.enrollment_status = EnrollmentStatus.WITHDRAWN
    db.commit()
    return {"message": "Student withdrawn successfully"}
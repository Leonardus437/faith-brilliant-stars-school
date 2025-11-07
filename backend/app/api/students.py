from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..core.security import get_current_user, require_role
from ..models.student import Student, EnrollmentStatus
from ..models.user import User, UserRole
from ..core.security import get_password_hash
from pydantic import BaseModel
from datetime import date

router = APIRouter()

class StudentResponse(BaseModel):
    id: int
    admission_number: str
    first_name: str
    last_name: str
    date_of_birth: date
    gender: str | None
    class_id: int | None
    enrollment_status: str
    photo_url: str | None

    class Config:
        from_attributes = True

class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    gender: str
    class_id: int
    email: str

class StudentUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    date_of_birth: date | None = None
    gender: str | None = None
    class_id: int | None = None
    enrollment_status: str | None = None

@router.get("/")
async def list_students(
    skip: int = 0,
    limit: int = 100,
    class_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from ..models.class_model import Class
    query = db.query(Student)
    if class_id:
        query = query.filter(Student.class_id == class_id)
    students = query.offset(skip).limit(limit).all()
    
    result = []
    for student in students:
        class_obj = db.query(Class).filter(Class.id == student.class_id).first() if student.class_id else None
        result.append({
            "id": student.id,
            "admission_number": student.admission_number,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "date_of_birth": student.date_of_birth.isoformat() if student.date_of_birth else None,
            "gender": student.gender,
            "class_id": student.class_id,
            "class_name": class_obj.name if class_obj else None,
            "enrollment_status": student.enrollment_status.value if hasattr(student.enrollment_status, 'value') else student.enrollment_status,
            "photo_url": student.photo_url
        })
    return result

@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.post("/", response_model=StudentResponse)
async def create_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin", "head_teacher"))
):
    # Create user account
    user = User(
        email=student_data.email,
        hashed_password=get_password_hash("Student2024"),
        full_name=f"{student_data.first_name} {student_data.last_name}",
        role=UserRole.STUDENT,
        is_active=True
    )
    db.add(user)
    db.flush()
    
    # Generate admission number
    last_student = db.query(Student).order_by(Student.id.desc()).first()
    next_num = (last_student.id + 1) if last_student else 1
    admission_number = f"FBS2024{next_num:04d}"
    
    # Create student
    student = Student(
        user_id=user.id,
        admission_number=admission_number,
        first_name=student_data.first_name,
        last_name=student_data.last_name,
        date_of_birth=student_data.date_of_birth,
        gender=student_data.gender,
        class_id=student_data.class_id,
        enrollment_status=EnrollmentStatus.ACTIVE,
        enrollment_date=date.today()
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

@router.put("/{student_id}", response_model=StudentResponse)
async def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin", "head_teacher"))
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    for field, value in student_data.dict(exclude_unset=True).items():
        setattr(student, field, value)
    
    db.commit()
    db.refresh(student)
    return student

@router.delete("/{student_id}")
async def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}

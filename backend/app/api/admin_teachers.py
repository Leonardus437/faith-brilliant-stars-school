from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user, get_password_hash
from app.models import *
from app.models.user import UserRole
from datetime import date

router = APIRouter(prefix="/admin/teachers", tags=["admin-teachers"])

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.HEAD_TEACHER:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

@router.post("")
async def create_teacher(teacher_data: dict, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    existing_user = db.query(User).filter(User.email == teacher_data["email"]).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    
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

@router.get("")
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
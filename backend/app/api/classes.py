from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..core.security import get_current_user
from ..models.class_model import Class
from pydantic import BaseModel

router = APIRouter()

class ClassResponse(BaseModel):
    id: int
    name: str
    grade_level: str
    academic_year: str
    capacity: int
    room_number: str | None
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[ClassResponse])
async def list_classes(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Class).all()

@router.get("/{class_id}", response_model=ClassResponse)
async def get_class(class_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    class_ = db.query(Class).filter(Class.id == class_id).first()
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    return class_

class ClassUpdate(BaseModel):
    name: str | None = None
    capacity: int | None = None
    room_number: str | None = None

@router.put("/{class_id}", response_model=ClassResponse)
async def update_class(
    class_id: int,
    class_data: ClassUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    class_ = db.query(Class).filter(Class.id == class_id).first()
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    
    for field, value in class_data.dict(exclude_unset=True).items():
        setattr(class_, field, value)
    
    db.commit()
    db.refresh(class_)
    return class_

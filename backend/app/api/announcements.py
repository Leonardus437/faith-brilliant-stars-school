from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.security import get_current_user, require_role
from ..models.announcement import Announcement
from pydantic import BaseModel
from typing import List
from datetime import datetime

router = APIRouter()

class AnnouncementCreate(BaseModel):
    title: str
    content: str
    priority: str = "normal"
    target_roles: List[str] = []

class AnnouncementResponse(BaseModel):
    id: int
    title: str
    content: str
    priority: str
    target_roles: List[str] | None
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[AnnouncementResponse])
async def list_announcements(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    announcements = db.query(Announcement).order_by(Announcement.created_at.desc()).all()
    return announcements

@router.post("/", response_model=AnnouncementResponse)
async def create_announcement(
    announcement: AnnouncementCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("head_teacher", "admin"))
):
    new_announcement = Announcement(
        title=announcement.title,
        content=announcement.content,
        priority=announcement.priority,
        target_roles=announcement.target_roles,
        created_by=current_user.id
    )
    db.add(new_announcement)
    db.commit()
    db.refresh(new_announcement)
    return new_announcement

@router.delete("/{announcement_id}")
async def delete_announcement(
    announcement_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("head_teacher", "admin"))
):
    announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    db.delete(announcement)
    db.commit()
    return {"message": "Announcement deleted"}

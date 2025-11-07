from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from ..core.database import Base

class Announcement(Base):
    __tablename__ = "announcements"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    priority = Column(String, default="normal")
    target_roles = Column(JSON)
    created_by = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

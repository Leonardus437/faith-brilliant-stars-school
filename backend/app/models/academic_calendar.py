from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, Text
from sqlalchemy.sql import func
from ..core.database import Base

class AcademicTerm(Base):
    __tablename__ = "academic_terms"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Term 1, Term 2, Term 3
    academic_year = Column(String, nullable=False)  # 2024
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Holiday(Base):
    __tablename__ = "holidays"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SchoolEvent(Base):
    __tablename__ = "school_events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    event_type = Column(String)  # sports_day, graduation, cultural, meeting
    event_date = Column(Date, nullable=False)
    description = Column(Text)
    location = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

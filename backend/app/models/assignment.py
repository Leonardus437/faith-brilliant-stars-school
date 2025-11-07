from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, Enum, Float
from sqlalchemy.sql import func
import enum
from ..core.database import Base

class SubmissionStatus(str, enum.Enum):
    NOT_SUBMITTED = "not_submitted"
    SUBMITTED = "submitted"
    LATE = "late"
    GRADED = "graded"

class Assignment(Base):
    __tablename__ = "assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    title = Column(String, nullable=False)
    instructions = Column(String)
    materials = Column(JSON)  # [{name, url}]
    due_date = Column(DateTime(timezone=True))
    max_score = Column(Float)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Submission(Base):
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    status = Column(Enum(SubmissionStatus), default=SubmissionStatus.NOT_SUBMITTED)
    content = Column(String)
    attachments = Column(JSON)  # [{name, url}]
    score = Column(Float)
    feedback = Column(String)
    submitted_at = Column(DateTime(timezone=True))
    graded_at = Column(DateTime(timezone=True))

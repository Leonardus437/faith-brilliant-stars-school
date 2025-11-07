from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.sql import func
import enum
from ..core.database import Base

class AssessmentType(str, enum.Enum):
    QUIZ = "quiz"
    TEST = "test"
    EXAM = "exam"
    ASSIGNMENT = "assignment"
    PROJECT = "project"

class Term(str, enum.Enum):
    TERM_1 = "term_1"
    TERM_2 = "term_2"
    TERM_3 = "term_3"

class Assessment(Base):
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    term = Column(Enum(Term), nullable=False)
    type = Column(Enum(AssessmentType), nullable=False)
    title = Column(String, nullable=False)
    max_score = Column(Float, nullable=False)
    weight = Column(Float, default=1.0)  # For weighted averages
    date = Column(DateTime(timezone=True))
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Grade(Base):
    __tablename__ = "grades"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)
    score = Column(Float, nullable=False)
    comments = Column(String)
    graded_by = Column(Integer, ForeignKey("users.id"))
    graded_at = Column(DateTime(timezone=True), server_default=func.now())

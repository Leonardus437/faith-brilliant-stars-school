from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base

class_subjects = Table(
    "class_subjects",
    Base.metadata,
    Column("class_id", Integer, ForeignKey("classes.id"), primary_key=True),
    Column("subject_id", Integer, ForeignKey("subjects.id"), primary_key=True)
)

class Class(Base):
    __tablename__ = "classes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # e.g., "P1 A", "P2 B"
    grade_level = Column(String, nullable=False)  # P1, P2, P3, P4, P5, P6
    academic_year = Column(String, nullable=False)  # e.g., "2024"
    class_teacher_id = Column(Integer, ForeignKey("teachers.id"))
    capacity = Column(Integer, default=40)
    room_number = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    class_teacher = relationship("Teacher", back_populates="classes")
    students = relationship("Student", back_populates="class_")
    subjects = relationship("Subject", secondary=class_subjects, back_populates="classes")

class Subject(Base):
    __tablename__ = "subjects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    classes = relationship("Class", secondary=class_subjects, back_populates="subjects")
    teachers = relationship("Teacher", secondary="teacher_subjects", back_populates="subjects")

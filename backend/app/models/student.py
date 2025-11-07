from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..core.database import Base

class EnrollmentStatus(str, enum.Enum):
    ACTIVE = "active"
    GRADUATED = "graduated"
    TRANSFERRED = "transferred"
    WITHDRAWN = "withdrawn"

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    admission_number = Column(String, unique=True, nullable=False, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String)
    photo_url = Column(String)
    class_id = Column(Integer, ForeignKey("classes.id"))
    enrollment_status = Column(Enum(EnrollmentStatus), default=EnrollmentStatus.ACTIVE)
    enrollment_date = Column(Date, nullable=False)
    emergency_contact = Column(JSON)  # {name, phone, relation}
    medical_info = Column(JSON)  # {allergies, conditions, medications}
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", backref="student_profile")
    class_ = relationship("Class", back_populates="students")
    guardians = relationship("Guardian", secondary="student_guardians", back_populates="students")

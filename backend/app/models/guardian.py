from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base

student_guardians = Table(
    "student_guardians",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("guardian_id", Integer, ForeignKey("guardians.id"), primary_key=True),
    Column("relation", String),  # father, mother, uncle, aunt, etc.
    Column("is_primary", Integer, default=0)
)

class Guardian(Base):
    __tablename__ = "guardians"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String)
    national_id = Column(String)
    occupation = Column(String)
    address = Column(String)
    consent_sms = Column(Integer, default=1)
    consent_email = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", backref="guardian_profile")
    students = relationship("Student", secondary=student_guardians, back_populates="guardians")

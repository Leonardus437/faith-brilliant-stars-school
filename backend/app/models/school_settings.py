from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, JSON
from sqlalchemy.sql import func
from ..core.database import Base

class SchoolSettings(Base):
    __tablename__ = "school_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    school_name = Column(String, default="Faith Brilliant Stars School")
    school_motto = Column(String)
    school_logo = Column(String)
    address = Column(Text)
    phone = Column(String)
    email = Column(String)
    website = Column(String)
    currency = Column(String, default="RWF")
    academic_year = Column(String)
    current_term = Column(String)
    late_fee_percentage = Column(Float, default=5.0)
    grace_period_days = Column(Integer, default=7)
    sms_enabled = Column(Boolean, default=True)
    email_enabled = Column(Boolean, default=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class PromotionRule(Base):
    __tablename__ = "promotion_rules"
    
    id = Column(Integer, primary_key=True, index=True)
    from_grade = Column(String, nullable=False)  # P1, P2, etc.
    to_grade = Column(String, nullable=False)
    min_attendance_percentage = Column(Float, default=75.0)
    min_average_score = Column(Float, default=50.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Discount(Base):
    __tablename__ = "discounts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    discount_type = Column(String)  # sibling, scholarship, staff_child
    percentage = Column(Float, nullable=False)
    conditions = Column(JSON)  # {min_siblings: 2, etc}
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

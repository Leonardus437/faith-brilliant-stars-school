from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum, Boolean, JSON
from sqlalchemy.sql import func
import enum
from ..core.database import Base

class PaymentCategory(str, enum.Enum):
    TUITION = "tuition"
    BREAKFAST = "breakfast"
    PORRIDGE = "porridge"
    LUNCH = "lunch"
    SNACKS = "snacks"
    TRANSPORT = "transport"
    UNIFORM = "uniform"
    EXTRACURRICULAR = "extracurricular"
    TRIP = "trip"
    OTHER = "other"

class InvoiceStatus(str, enum.Enum):
    PENDING = "pending"
    PARTIAL = "partial"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"

class PaymentMethod(str, enum.Enum):
    CASH = "cash"
    BANK = "bank"
    MTN_MOMO = "mtn_momo"
    AIRTEL_MONEY = "airtel_money"
    WALLET = "wallet"

class FeeStructure(Base):
    __tablename__ = "fee_structures"
    
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"))
    category = Column(Enum(PaymentCategory), nullable=False)
    term = Column(String)  # term_1, term_2, term_3, or null for recurring
    amount = Column(Float, nullable=False)
    description = Column(String)
    is_recurring = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Invoice(Base):
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String, unique=True, nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    category = Column(Enum(PaymentCategory), nullable=False)
    term = Column(String)
    amount = Column(Float, nullable=False)
    amount_paid = Column(Float, default=0.0)
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.PENDING)
    due_date = Column(DateTime(timezone=True))
    description = Column(String)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    receipt_number = Column(String, unique=True, nullable=False, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    amount = Column(Float, nullable=False)
    payment_method = Column(String, nullable=False)
    payment_date = Column(String)
    recorded_by = Column(Integer, ForeignKey("users.id"))

class Wallet(Base):
    __tablename__ = "wallets"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), unique=True, nullable=False)
    balance = Column(Float, default=0.0)
    last_top_up = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class ServiceItem(Base):
    __tablename__ = "service_items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(Enum(PaymentCategory), nullable=False)
    unit_price = Column(Float, nullable=False)
    description = Column(String)
    is_recurring = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

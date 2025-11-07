from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..core.security import get_current_user, require_role
from ..models.fee import Invoice, Payment, InvoiceStatus, PaymentCategory, PaymentMethod
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class InvoiceResponse(BaseModel):
    id: int
    invoice_number: str
    student_id: int
    category: str
    total_amount: float
    amount_paid: float
    status: str
    due_date: datetime | None
    
    class Config:
        from_attributes = True

class InvoiceCreate(BaseModel):
    student_id: int
    category: str
    amount: float
    term: str
    due_date: datetime

class PaymentCreate(BaseModel):
    invoice_id: int
    amount: float
    method: str
    reference: str | None = None

class PaymentResponse(BaseModel):
    id: int
    receipt_number: str
    invoice_id: int
    amount: float
    payment_method: str
    payment_date: datetime
    
    class Config:
        from_attributes = True

@router.get("/invoices")
async def list_invoices(student_id: int | None = None, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    query = db.query(Invoice)
    if student_id:
        query = query.filter(Invoice.student_id == student_id)
    invoices = query.all()
    return [{"id": inv.id, "invoice_number": inv.invoice_number, "student_id": inv.student_id,
             "total_amount": inv.amount, "amount_paid": inv.amount_paid, "status": inv.status.value,
             "category": inv.category.value, "due_date": str(inv.due_date) if inv.due_date else None} for inv in invoices]

@router.post("/invoices", response_model=InvoiceResponse)
async def create_invoice(
    invoice_data: InvoiceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin", "accountant"))
):
    last_invoice = db.query(Invoice).order_by(Invoice.id.desc()).first()
    next_num = (last_invoice.id + 1) if last_invoice else 1
    invoice_number = f"INV-2024-{next_num:05d}"
    
    invoice = Invoice(
        invoice_number=invoice_number,
        student_id=invoice_data.student_id,
        category=invoice_data.category,
        term=invoice_data.term,
        amount=invoice_data.amount,
        amount_paid=0,
        status=InvoiceStatus.PENDING,
        due_date=invoice_data.due_date,
        created_by=current_user.id
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice

@router.delete("/invoices/{invoice_id}")
async def delete_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin", "accountant"))
):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    db.delete(invoice)
    db.commit()
    return {"message": "Invoice deleted"}

@router.post("/payments", response_model=PaymentResponse)
async def record_payment(
    payment_data: PaymentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin", "accountant"))
):
    invoice = db.query(Invoice).filter(Invoice.id == payment_data.invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    last_payment = db.query(Payment).order_by(Payment.id.desc()).first()
    next_num = (last_payment.id + 1) if last_payment else 1
    receipt_number = f"RCP-2024-{next_num:05d}"
    
    payment = Payment(
        receipt_number=receipt_number,
        invoice_id=payment_data.invoice_id,
        student_id=invoice.student_id,
        amount=payment_data.amount,
        method=payment_data.method,
        reference=payment_data.reference,
        received_by=current_user.id
    )
    db.add(payment)
    
    invoice.amount_paid += payment_data.amount
    if invoice.amount_paid >= invoice.amount:
        invoice.status = InvoiceStatus.PAID
    elif invoice.amount_paid > 0:
        invoice.status = InvoiceStatus.PARTIAL
    
    db.commit()
    db.refresh(payment)
    return payment

@router.get("/payments")
async def list_payments(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    payments = db.query(Payment).all()
    return [{"id": p.id, "receipt_number": p.receipt_number, "invoice_id": p.invoice_id,
             "amount": p.amount, "payment_method": p.payment_method, "payment_date": p.payment_date} for p in payments]

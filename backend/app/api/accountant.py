from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from app.core.database import get_db
from app.core.security import get_current_user
from app.models import *
from app.models.user import UserRole
from app.models.fee import PaymentCategory, InvoiceStatus
from datetime import datetime, date, timedelta
from typing import Optional

router = APIRouter(prefix="/accountant", tags=["accountant"])

def require_accountant(current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ACCOUNTANT, UserRole.HEAD_TEACHER]:
        raise HTTPException(status_code=403, detail="Accountant access required")
    return current_user

# DASHBOARD
@router.get("/dashboard")
async def get_accountant_dashboard(db: Session = Depends(get_db), user: User = Depends(require_accountant)):
    today = date.today()
    this_month_start = date(today.year, today.month, 1)
    
    # Financial overview
    total_revenue = db.query(func.sum(Payment.amount)).scalar() or 0
    monthly_revenue = db.query(func.sum(Payment.amount)).filter(Payment.payment_date >= this_month_start).scalar() or 0
    total_outstanding = db.query(func.sum(Invoice.amount - Invoice.amount_paid)).filter(Invoice.status != InvoiceStatus.PAID).scalar() or 0
    
    # Invoice statistics
    total_invoices = db.query(Invoice).count()
    paid_invoices = db.query(Invoice).filter(Invoice.status == InvoiceStatus.PAID).count()
    pending_invoices = db.query(Invoice).filter(Invoice.status == InvoiceStatus.PENDING).count()
    partial_invoices = db.query(Invoice).filter(Invoice.status == InvoiceStatus.PARTIAL).count()
    overdue_invoices = db.query(Invoice).filter(and_(Invoice.status != InvoiceStatus.PAID, Invoice.due_date < today)).count()
    
    # Recent payments
    recent_payments = db.query(Payment).order_by(Payment.id.desc()).limit(10).all()
    
    # Payment methods breakdown
    payment_methods = db.query(
        Payment.payment_method,
        func.count(Payment.id).label('count'),
        func.sum(Payment.amount).label('total')
    ).group_by(Payment.payment_method).all()
    
    return {
        "overview": {
            "total_revenue": total_revenue,
            "monthly_revenue": monthly_revenue,
            "total_outstanding": total_outstanding,
            "collection_rate": round((total_revenue / (total_revenue + total_outstanding) * 100) if (total_revenue + total_outstanding) > 0 else 0, 1)
        },
        "invoices": {
            "total": total_invoices,
            "paid": paid_invoices,
            "pending": pending_invoices,
            "partial": partial_invoices,
            "overdue": overdue_invoices
        },
        "recent_payments": [{
            "id": p.id,
            "receipt_number": p.receipt_number,
            "amount": p.amount,
            "method": p.payment_method,
            "date": p.payment_date
        } for p in recent_payments],
        "payment_methods": [{"method": pm[0], "count": pm[1], "total": pm[2]} for pm in payment_methods]
    }

# INVOICES
@router.get("/invoices")
async def get_all_invoices(
    status: Optional[str] = None,
    class_id: Optional[int] = None,
    db: Session = Depends(get_db),
    user: User = Depends(require_accountant)
):
    query = db.query(Invoice)
    
    if status:
        query = query.filter(Invoice.status == status)
    if class_id:
        query = query.filter(Invoice.student_id.in_(
            db.query(Student.id).filter(Student.class_id == class_id)
        ))
    
    invoices = query.order_by(Invoice.id.desc()).all()
    
    result = []
    for i in invoices:
        student = db.query(Student).filter(Student.id == i.student_id).first()
        if student:
            class_obj = db.query(Class).filter(Class.id == student.class_id).first()
            result.append({
                "id": i.id,
                "invoice_number": i.invoice_number,
                "student_id": i.student_id,
                "student_name": f"{student.first_name} {student.last_name}",
                "class": class_obj.name if class_obj else "N/A",
                "category": i.category,
                "term": i.term,
                "amount": i.amount,
                "amount_paid": i.amount_paid,
                "balance": i.amount - i.amount_paid,
                "status": i.status,
                "due_date": str(i.due_date) if i.due_date else None,
                "created_at": str(i.created_at) if i.created_at else None
            })
    
    return result

@router.post("/invoices")
async def create_invoice(invoice_data: dict, db: Session = Depends(get_db), user: User = Depends(require_accountant)):
    # Generate invoice number
    last_invoice = db.query(Invoice).order_by(Invoice.id.desc()).first()
    next_id = (last_invoice.id + 1) if last_invoice else 1
    invoice_number = f"INV-2024-{next_id:05d}"
    
    invoice = Invoice(
        invoice_number=invoice_number,
        student_id=invoice_data["student_id"],
        category=invoice_data["category"],
        term=invoice_data["term"],
        amount=invoice_data["amount"],
        amount_paid=0,
        status=InvoiceStatus.PENDING,
        due_date=datetime.strptime(invoice_data["due_date"], "%Y-%m-%d").date(),
        created_by=user.id
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    
    return {"message": "Invoice created successfully", "invoice_id": invoice.id, "invoice_number": invoice_number}

@router.put("/invoices/{invoice_id}")
async def update_invoice(invoice_id: int, invoice_data: dict, db: Session = Depends(get_db), user: User = Depends(require_accountant)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    if "status" in invoice_data:
        new_status = invoice_data["status"]
        # Validate status change matches payment data
        if new_status == "paid" or new_status == InvoiceStatus.PAID:
            if invoice.amount_paid < invoice.amount:
                raise HTTPException(status_code=400, detail="Cannot mark as paid: invoice not fully paid")
        invoice.status = new_status
    if "amount" in invoice_data:
        invoice.amount = invoice_data["amount"]
        # Recalculate status based on payment
        if invoice.amount_paid >= invoice.amount:
            invoice.status = InvoiceStatus.PAID
        elif invoice.amount_paid > 0:
            invoice.status = InvoiceStatus.PARTIAL
        else:
            invoice.status = InvoiceStatus.PENDING
    
    db.commit()
    return {"message": "Invoice updated successfully"}

@router.delete("/invoices/{invoice_id}")
async def delete_invoice(invoice_id: int, db: Session = Depends(get_db), user: User = Depends(require_accountant)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    db.delete(invoice)
    db.commit()
    return {"message": "Invoice deleted successfully"}

@router.post("/invoices/{invoice_id}/send")
async def send_invoice_notification(invoice_id: int, notification_data: dict, db: Session = Depends(get_db), user: User = Depends(require_accountant)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    # In production, integrate with email/SMS service
    return {"message": "Notification sent successfully", "recipient": notification_data.get("recipient")}

@router.post("/invoices/bulk")
async def create_bulk_invoices(bulk_data: dict, db: Session = Depends(get_db), user: User = Depends(require_accountant)):
    # Create invoices for multiple students
    class_id = bulk_data.get("class_id")
    category = bulk_data["category"]
    term = bulk_data["term"]
    amount = bulk_data["amount"]
    due_date = datetime.strptime(bulk_data["due_date"], "%Y-%m-%d").date()
    
    students = db.query(Student).filter(Student.class_id == class_id).all() if class_id else db.query(Student).all()
    
    last_invoice = db.query(Invoice).order_by(Invoice.id.desc()).first()
    next_id = (last_invoice.id + 1) if last_invoice else 1
    
    created_count = 0
    for student in students:
        # Check if invoice already exists
        existing = db.query(Invoice).filter(
            and_(Invoice.student_id == student.id, Invoice.category == category, Invoice.term == term)
        ).first()
        
        if not existing:
            invoice = Invoice(
                invoice_number=f"INV-2024-{next_id:05d}",
                student_id=student.id,
                category=category,
                term=term,
                amount=amount,
                amount_paid=0,
                status=InvoiceStatus.PENDING,
                due_date=due_date,
                created_by=user.id
            )
            db.add(invoice)
            next_id += 1
            created_count += 1
    
    db.commit()
    return {"message": f"Created {created_count} invoices successfully"}

# PAYMENTS
@router.get("/payments")
async def get_all_payments(db: Session = Depends(get_db), user: User = Depends(require_accountant)):
    payments = db.query(Payment).order_by(Payment.id.desc()).all()
    
    return [{
        "id": p.id,
        "receipt_number": p.receipt_number,
        "invoice_id": p.invoice_id,
        "amount": p.amount,
        "payment_method": p.payment_method,
        "payment_date": p.payment_date
    } for p in payments]

@router.post("/payments")
async def record_payment(payment_data: dict, db: Session = Depends(get_db), user: User = Depends(require_accountant)):
    invoice = db.query(Invoice).filter(Invoice.id == payment_data["invoice_id"]).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    # Generate receipt number
    last_payment = db.query(Payment).order_by(Payment.id.desc()).first()
    next_id = (last_payment.id + 1) if last_payment else 1
    receipt_number = f"RCP-2024-{next_id:05d}"
    
    payment_amount = float(payment_data["amount"])
    remaining_balance = invoice.amount - invoice.amount_paid
    
    if payment_amount > remaining_balance:
        raise HTTPException(status_code=400, detail="Payment amount exceeds remaining balance")
    
    # Create payment record
    payment = Payment(
        receipt_number=receipt_number,
        invoice_id=invoice.id,
        amount=payment_amount,
        payment_method=payment_data["payment_method"],
        payment_date=payment_data.get("payment_date", date.today().isoformat()),
        recorded_by=user.id
    )
    db.add(payment)
    
    # Update invoice
    invoice.amount_paid += payment_amount
    if invoice.amount_paid >= invoice.amount:
        invoice.status = InvoiceStatus.PAID
    elif invoice.amount_paid > 0:
        invoice.status = InvoiceStatus.PARTIAL
    
    db.commit()
    db.refresh(payment)
    
    return {
        "message": "Payment recorded successfully",
        "receipt_number": receipt_number,
        "remaining_balance": invoice.amount - invoice.amount_paid
    }

# FEE STRUCTURES
@router.get("/fee-structures")
async def get_fee_structures(db: Session = Depends(get_db), user: User = Depends(require_accountant)):
    fee_structures = db.query(FeeStructure).all()
    return [{
        "id": fs.id,
        "name": fs.name,
        "category": fs.category,
        "amount": fs.amount,
        "frequency": fs.frequency,
        "is_active": fs.is_active
    } for fs in fee_structures]

@router.post("/fee-structures")
async def create_fee_structure(fee_data: dict, db: Session = Depends(get_db), user: User = Depends(require_accountant)):
    fee_structure = FeeStructure(
        name=fee_data["name"],
        category=fee_data["category"],
        amount=fee_data["amount"],
        frequency=fee_data.get("frequency", "termly"),
        is_active=True
    )
    db.add(fee_structure)
    db.commit()
    return {"message": "Fee structure created successfully"}

# REPORTS
@router.get("/reports/revenue")
async def get_revenue_report(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
    user: User = Depends(require_accountant)
):
    query = db.query(Payment)
    
    if start_date:
        query = query.filter(Payment.payment_date >= datetime.strptime(start_date, "%Y-%m-%d").date())
    if end_date:
        query = query.filter(Payment.payment_date <= datetime.strptime(end_date, "%Y-%m-%d").date())
    
    payments = query.all()
    total_revenue = sum(p.amount for p in payments)
    
    # Group by payment method
    by_method = {}
    for p in payments:
        if p.payment_method not in by_method:
            by_method[p.payment_method] = 0
        by_method[p.payment_method] += p.amount
    
    # Group by date
    by_date = {}
    for p in payments:
        date_key = str(p.payment_date)
        if date_key not in by_date:
            by_date[date_key] = 0
        by_date[date_key] += p.amount
    
    return {
        "total_revenue": total_revenue,
        "payment_count": len(payments),
        "by_method": by_method,
        "by_date": by_date
    }

@router.get("/reports/outstanding")
async def get_outstanding_report(db: Session = Depends(get_db), user: User = Depends(require_accountant)):
    invoices = db.query(Invoice).filter(Invoice.status != InvoiceStatus.PAID).join(Student).join(Class).all()
    
    total_outstanding = sum(i.amount - i.amount_paid for i in invoices)
    
    # Group by class
    by_class = {}
    for i in invoices:
        class_name = i.student.class_obj.name
        if class_name not in by_class:
            by_class[class_name] = 0
        by_class[class_name] += (i.amount - i.amount_paid)
    
    # Group by category
    by_category = {}
    for i in invoices:
        if i.category not in by_category:
            by_category[i.category] = 0
        by_category[i.category] += (i.amount - i.amount_paid)
    
    return {
        "total_outstanding": total_outstanding,
        "invoice_count": len(invoices),
        "by_class": by_class,
        "by_category": by_category,
        "details": [{
            "student": f"{i.student.first_name} {i.student.last_name}",
            "class": i.student.class_obj.name,
            "invoice_number": i.invoice_number,
            "category": i.category,
            "amount": i.amount,
            "paid": i.amount_paid,
            "balance": i.amount - i.amount_paid,
            "due_date": i.due_date
        } for i in invoices]
    }

@router.get("/reports/collection-rate")
async def get_collection_rate(db: Session = Depends(get_db), user: User = Depends(require_accountant)):
    # Calculate collection rate by class
    classes = db.query(Class).all()
    
    results = []
    for cls in classes:
        students = db.query(Student).filter(Student.class_id == cls.id).all()
        student_ids = [s.id for s in students]
        
        total_invoiced = db.query(func.sum(Invoice.amount)).filter(Invoice.student_id.in_(student_ids)).scalar() or 0
        total_collected = db.query(func.sum(Invoice.amount_paid)).filter(Invoice.student_id.in_(student_ids)).scalar() or 0
        
        collection_rate = (total_collected / total_invoiced * 100) if total_invoiced > 0 else 0
        
        results.append({
            "class": cls.name,
            "total_invoiced": total_invoiced,
            "total_collected": total_collected,
            "outstanding": total_invoiced - total_collected,
            "collection_rate": round(collection_rate, 1)
        })
    
    return results

# STUDENT ACCOUNT
@router.get("/student-account/{student_id}")
async def get_student_account(student_id: int, db: Session = Depends(get_db), user: User = Depends(require_accountant)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Get class name
    class_obj = db.query(Class).filter(Class.id == student.class_id).first() if student.class_id else None
    
    invoices = db.query(Invoice).filter(Invoice.student_id == student_id).all()
    invoices_ids = [i.id for i in invoices]
    payments = db.query(Payment).filter(Payment.invoice_id.in_(invoices_ids)).all() if invoices_ids else []
    
    total_invoiced = sum(i.amount for i in invoices)
    total_paid = sum(i.amount_paid for i in invoices)
    total_outstanding = total_invoiced - total_paid
    
    return {
        "student": {
            "id": student.id,
            "name": f"{student.first_name} {student.last_name}",
            "admission_number": student.admission_number,
            "class": class_obj.name if class_obj else "N/A"
        },
        "summary": {
            "total_invoiced": total_invoiced,
            "total_paid": total_paid,
            "total_outstanding": total_outstanding
        },
        "invoices": [{
            "id": i.id,
            "invoice_number": i.invoice_number,
            "category": i.category.value if hasattr(i.category, 'value') else i.category,
            "term": i.term,
            "amount": i.amount,
            "amount_paid": i.amount_paid,
            "balance": i.amount - i.amount_paid,
            "status": i.status.value if hasattr(i.status, 'value') else i.status,
            "due_date": str(i.due_date) if i.due_date else None
        } for i in invoices],
        "payments": [{
            "receipt_number": p.receipt_number,
            "amount": p.amount,
            "method": p.payment_method,
            "date": p.payment_date
        } for p in payments]
    }

# MOBILE MONEY INTEGRATION
@router.post("/mobile-money/initiate")
async def initiate_mobile_money_payment(payment_data: dict, db: Session = Depends(get_db), user: User = Depends(require_accountant)):
    # Simulate mobile money payment initiation
    invoice_id = payment_data["invoice_id"]
    phone_number = payment_data["phone_number"]
    amount = payment_data["amount"]
    provider = payment_data["provider"]  # MTN MoMo, Airtel Money
    
    # In production, integrate with actual mobile money API
    transaction_id = f"MM-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    return {
        "message": "Mobile money payment initiated",
        "transaction_id": transaction_id,
        "status": "pending",
        "instructions": f"Please confirm payment on your {provider} phone {phone_number}"
    }

# DISCOUNTS
@router.post("/discounts/apply")
async def apply_discount(discount_data: dict, db: Session = Depends(get_db), user: User = Depends(require_accountant)):
    invoice_id = discount_data["invoice_id"]
    discount_amount = discount_data["discount_amount"]
    reason = discount_data.get("reason", "Discount applied")
    
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    invoice.amount -= discount_amount
    if invoice.amount_paid >= invoice.amount:
        invoice.status = InvoiceStatus.PAID
    
    db.commit()
    
    return {"message": "Discount applied successfully", "new_amount": invoice.amount}
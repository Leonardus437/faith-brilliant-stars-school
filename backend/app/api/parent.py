from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from ..core.database import get_db
from ..core.security import get_current_user, require_role
from ..models.user import User, UserRole
from ..models.student import Student
from ..models.guardian import Guardian, student_guardians
from ..models.attendance import Attendance, AttendanceStatus
from ..models.fee import Invoice, Payment

router = APIRouter()

@router.get("/children", dependencies=[Depends(require_role([UserRole.PARENT]))])
def get_my_children(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get parent's children"""
    guardian = db.query(Guardian).filter(Guardian.user_id == current_user.id).first()
    if not guardian:
        raise HTTPException(status_code=404, detail="Guardian profile not found")
    
    children = db.query(Student).join(
        student_guardians, Student.id == student_guardians.c.student_id
    ).filter(student_guardians.c.guardian_id == guardian.id).all()
    
    result = []
    for child in children:
        from ..models.class_model import Class
        class_info = db.query(Class).filter(Class.id == child.class_id).first()
        
        # Get attendance stats
        total_days = db.query(Attendance).filter(Attendance.student_id == child.id).count()
        present_days = db.query(Attendance).filter(
            Attendance.student_id == child.id,
            Attendance.status == AttendanceStatus.PRESENT
        ).count()
        
        # Get fee balance
        invoices = db.query(Invoice).filter(Invoice.student_id == child.id).all()
        total_due = sum(inv.amount for inv in invoices)
        total_paid = sum(inv.amount_paid for inv in invoices)
        
        result.append({
            "id": child.id,
            "admission_number": child.admission_number,
            "first_name": child.first_name,
            "last_name": child.last_name,
            "full_name": f"{child.first_name} {child.last_name}",
            "class_name": class_info.name if class_info else "N/A",
            "attendance_rate": round((present_days / total_days * 100) if total_days > 0 else 0, 1),
            "total_days": total_days,
            "present_days": present_days,
            "fee_balance": total_due - total_paid
        })
    
    return result

@router.get("/child/{student_id}/attendance", dependencies=[Depends(require_role([UserRole.PARENT]))])
def get_child_attendance(student_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get child's attendance history"""
    guardian = db.query(Guardian).filter(Guardian.user_id == current_user.id).first()
    if not guardian:
        raise HTTPException(status_code=404, detail="Guardian profile not found")
    
    # Verify this is parent's child
    link = db.query(student_guardians).filter(
        student_guardians.c.student_id == student_id,
        student_guardians.c.guardian_id == guardian.id
    ).first()
    
    if not link:
        raise HTTPException(status_code=403, detail="Not authorized to view this student")
    
    # Get last 30 days attendance
    thirty_days_ago = datetime.now().date() - timedelta(days=30)
    records = db.query(Attendance).filter(
        Attendance.student_id == student_id,
        Attendance.date >= thirty_days_ago
    ).order_by(Attendance.date.desc()).all()
    
    return [{
        "date": record.date.isoformat(),
        "status": record.status.value,
        "notes": record.notes
    } for record in records]

@router.get("/child/{student_id}/fees", dependencies=[Depends(require_role([UserRole.PARENT]))])
def get_child_fees(student_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get child's fee information"""
    guardian = db.query(Guardian).filter(Guardian.user_id == current_user.id).first()
    if not guardian:
        raise HTTPException(status_code=404, detail="Guardian profile not found")
    
    # Verify this is parent's child
    link = db.query(student_guardians).filter(
        student_guardians.c.student_id == student_id,
        student_guardians.c.guardian_id == guardian.id
    ).first()
    
    if not link:
        raise HTTPException(status_code=403, detail="Not authorized to view this student")
    
    invoices = db.query(Invoice).filter(Invoice.student_id == student_id).all()
    
    result = []
    for invoice in invoices:
        payments = db.query(Payment).filter(Payment.invoice_id == invoice.id).all()
        result.append({
            "invoice_number": invoice.invoice_number,
            "category": invoice.category.value,
            "term": invoice.term,
            "amount": invoice.amount,
            "amount_paid": invoice.amount_paid,
            "balance": invoice.amount - invoice.amount_paid,
            "status": invoice.status.value,
            "due_date": invoice.due_date.isoformat() if invoice.due_date else None,
            "payments": [{
                "receipt_number": p.receipt_number,
                "amount": p.amount,
                "payment_method": p.payment_method,
                "payment_date": p.payment_date.isoformat() if p.payment_date else None
            } for p in payments]
        })
    
    return result

from app.core.database import SessionLocal
from app.models.fee import Payment, Invoice, InvoiceStatus
from datetime import datetime

db = SessionLocal()

try:
    # Get first pending invoice
    invoice = db.query(Invoice).filter(Invoice.status == InvoiceStatus.PENDING).first()
    
    if invoice:
        # Create payment
        payment = Payment(
            receipt_number="RCP-2024-00001",
            invoice_id=invoice.id,
            student_id=invoice.student_id,
            amount=150000,
            method="mtn_momo",
            reference="MTN123456",
            received_by=1,
            received_at=datetime.now()
        )
        db.add(payment)
        
        # Update invoice
        invoice.amount_paid = 150000
        if invoice.amount_paid >= invoice.amount:
            invoice.status = InvoiceStatus.PAID
        else:
            invoice.status = InvoiceStatus.PARTIAL
        
        db.commit()
        print("Sample payment added successfully!")
    else:
        print("No pending invoices found")
        
except Exception as e:
    print(f"Error: {e}")
    db.rollback()
finally:
    db.close()

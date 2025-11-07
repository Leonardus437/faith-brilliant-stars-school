from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List
from datetime import datetime, timedelta
from ..core.database import get_db
from ..core.security import get_current_user, require_role
from ..models.guardian import Guardian
from ..models.student import Student
from ..models.attendance import Attendance
from ..models.fee import Invoice, Payment, InvoiceStatus
from ..models.announcement import Announcement
from ..models.communication import Message, ParentTeacherMeeting
from ..models.assessment import Assessment
from pydantic import BaseModel

router = APIRouter()

# ============ PARENT DASHBOARD ============
class ChildSummary(BaseModel):
    id: int
    name: str
    class_name: str
    photo_url: str | None
    attendance_rate: float
    outstanding_fees: float
    recent_status: str

class ParentDashboard(BaseModel):
    children: List[ChildSummary]
    total_outstanding: float
    unread_messages: int
    upcoming_meetings: List[dict]
    recent_announcements: List[dict]

@router.get("/parent/dashboard", response_model=ParentDashboard)
async def get_parent_dashboard(
    db: Session = Depends(get_db),
    current_user = Depends(require_role("parent"))
):
    # Get guardian profile
    guardian = db.query(Guardian).filter(Guardian.user_id == current_user.id).first()
    if not guardian:
        raise HTTPException(status_code=404, detail="Guardian profile not found")
    
    # Get all children
    children_summaries = []
    total_outstanding = 0
    
    for student in guardian.students:
        # Attendance rate (last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        records = db.query(Attendance).filter(
            and_(Attendance.student_id == student.id, Attendance.date >= thirty_days_ago)
        ).all()
        
        present = sum(1 for r in records if r.status == "present")
        attendance_rate = (present / len(records) * 100) if records else 0
        
        # Outstanding fees
        invoices = db.query(Invoice).filter(
            and_(
                Invoice.student_id == student.id,
                Invoice.status.in_([InvoiceStatus.PENDING, InvoiceStatus.PARTIAL])
            )
        ).all()
        outstanding = sum(i.amount - i.amount_paid for i in invoices)
        total_outstanding += outstanding
        
        # Recent status
        recent_record = db.query(Attendance).filter(
            Attendance.student_id == student.id
        ).order_by(Attendance.date.desc()).first()
        recent_status = recent_record.status if recent_record else "No data"
        
        children_summaries.append(ChildSummary(
            id=student.id,
            name=f"{student.first_name} {student.last_name}",
            class_name=student.class_.name if student.class_ else "No Class",
            photo_url=student.photo_url,
            attendance_rate=round(attendance_rate, 2),
            outstanding_fees=outstanding,
            recent_status=recent_status
        ))
    
    # Unread messages
    unread_messages = db.query(Message).filter(
        and_(Message.recipient_id == current_user.id, Message.is_read == False)
    ).count()
    
    # Upcoming meetings
    upcoming_meetings = db.query(ParentTeacherMeeting).filter(
        and_(
            ParentTeacherMeeting.parent_id == guardian.id,
            ParentTeacherMeeting.meeting_date >= datetime.now(),
            ParentTeacherMeeting.status == "scheduled"
        )
    ).limit(5).all()
    
    meetings_list = [
        {
            "id": m.id,
            "date": m.meeting_date,
            "purpose": m.purpose,
            "student_id": m.student_id
        } for m in upcoming_meetings
    ]
    
    # Recent announcements
    announcements = db.query(Announcement).filter(
        Announcement.is_active == True
    ).order_by(Announcement.created_at.desc()).limit(5).all()
    
    announcements_list = [
        {
            "id": a.id,
            "title": a.title,
            "content": a.content[:100] + "..." if len(a.content) > 100 else a.content,
            "date": a.created_at
        } for a in announcements
    ]
    
    return ParentDashboard(
        children=children_summaries,
        total_outstanding=total_outstanding,
        unread_messages=unread_messages,
        upcoming_meetings=meetings_list,
        recent_announcements=announcements_list
    )

# ============ CHILD DETAILS ============
@router.get("/parent/children/{student_id}")
async def get_child_details(
    student_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("parent"))
):
    guardian = db.query(Guardian).filter(Guardian.user_id == current_user.id).first()
    if not guardian:
        raise HTTPException(status_code=404, detail="Guardian profile not found")
    
    # Verify this is parent's child
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student or student not in guardian.students:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Get comprehensive details
    return {
        "id": student.id,
        "admission_number": student.admission_number,
        "name": f"{student.first_name} {student.last_name}",
        "date_of_birth": student.date_of_birth,
        "gender": student.gender,
        "class": student.class_.name if student.class_ else None,
        "photo_url": student.photo_url,
        "emergency_contact": student.emergency_contact,
        "medical_info": student.medical_info
    }

# ============ ATTENDANCE TRACKING ============
@router.get("/parent/children/{student_id}/attendance")
async def get_child_attendance(
    student_id: int,
    start_date: str | None = None,
    end_date: str | None = None,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("parent"))
):
    guardian = db.query(Guardian).filter(Guardian.user_id == current_user.id).first()
    student = db.query(Student).filter(Student.id == student_id).first()
    
    if not student or student not in guardian.students:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Default to last 30 days
    if not start_date:
        start = datetime.now() - timedelta(days=30)
    else:
        start = datetime.fromisoformat(start_date)
    
    if not end_date:
        end = datetime.now()
    else:
        end = datetime.fromisoformat(end_date)
    
    records = db.query(Attendance).filter(
        and_(
            Attendance.student_id == student_id,
            Attendance.date >= start,
            Attendance.date <= end
        )
    ).order_by(Attendance.date.desc()).all()
    
    # Calculate statistics
    total = len(records)
    present = sum(1 for r in records if r.status == "present")
    absent = sum(1 for r in records if r.status == "absent")
    late = sum(1 for r in records if r.status == "late")
    sick = sum(1 for r in records if r.status == "sick")
    
    return {
        "student_name": f"{student.first_name} {student.last_name}",
        "period": f"{start.date()} to {end.date()}",
        "statistics": {
            "total_days": total,
            "present": present,
            "absent": absent,
            "late": late,
            "sick": sick,
            "attendance_rate": round((present / total * 100) if total > 0 else 0, 2)
        },
        "records": [
            {
                "date": r.date.strftime("%Y-%m-%d"),
                "status": r.status,
                "notes": r.notes
            } for r in records
        ]
    }

# ============ FEE MANAGEMENT ============
@router.get("/parent/children/{student_id}/fees")
async def get_child_fees(
    student_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("parent"))
):
    guardian = db.query(Guardian).filter(Guardian.user_id == current_user.id).first()
    student = db.query(Student).filter(Student.id == student_id).first()
    
    if not student or student not in guardian.students:
        raise HTTPException(status_code=403, detail="Access denied")
    
    invoices = db.query(Invoice).filter(Invoice.student_id == student_id).all()
    
    pending_invoices = []
    paid_invoices = []
    
    for invoice in invoices:
        invoice_data = {
            "id": invoice.id,
            "invoice_number": invoice.invoice_number,
            "category": invoice.category,
            "term": invoice.term,
            "amount": invoice.amount,
            "amount_paid": invoice.amount_paid,
            "balance": invoice.amount - invoice.amount_paid,
            "status": invoice.status,
            "due_date": invoice.due_date,
            "description": invoice.description
        }
        
        if invoice.status in [InvoiceStatus.PENDING, InvoiceStatus.PARTIAL]:
            pending_invoices.append(invoice_data)
        else:
            paid_invoices.append(invoice_data)
    
    total_outstanding = sum(i["balance"] for i in pending_invoices)
    
    return {
        "student_name": f"{student.first_name} {student.last_name}",
        "total_outstanding": total_outstanding,
        "pending_invoices": pending_invoices,
        "paid_invoices": paid_invoices
    }

@router.get("/parent/children/{student_id}/payment-history")
async def get_payment_history(
    student_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("parent"))
):
    guardian = db.query(Guardian).filter(Guardian.user_id == current_user.id).first()
    student = db.query(Student).filter(Student.id == student_id).first()
    
    if not student or student not in guardian.students:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Get all payments for this student's invoices
    invoices = db.query(Invoice).filter(Invoice.student_id == student_id).all()
    invoice_ids = [i.id for i in invoices]
    
    payments = db.query(Payment).filter(Payment.invoice_id.in_(invoice_ids)).order_by(
        Payment.payment_date.desc()
    ).all()
    
    return {
        "student_name": f"{student.first_name} {student.last_name}",
        "payments": [
            {
                "receipt_number": p.receipt_number,
                "amount": p.amount,
                "payment_method": p.payment_method,
                "payment_date": p.payment_date,
                "invoice_id": p.invoice_id
            } for p in payments
        ]
    }

# ============ ACADEMIC PROGRESS ============
@router.get("/parent/children/{student_id}/academic-progress")
async def get_academic_progress(
    student_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("parent"))
):
    guardian = db.query(Guardian).filter(Guardian.user_id == current_user.id).first()
    student = db.query(Student).filter(Student.id == student_id).first()
    
    if not student or student not in guardian.students:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Get assessments
    assessments = db.query(Assessment).filter(Assessment.student_id == student_id).order_by(
        Assessment.assessment_date.desc()
    ).all()
    
    return {
        "student_name": f"{student.first_name} {student.last_name}",
        "class": student.class_.name if student.class_ else None,
        "assessments": [
            {
                "id": a.id,
                "subject": a.subject,
                "assessment_type": a.assessment_type,
                "score": a.score,
                "max_score": a.max_score,
                "percentage": round((a.score / a.max_score * 100) if a.max_score > 0 else 0, 2),
                "date": a.assessment_date,
                "teacher_comments": a.teacher_comments
            } for a in assessments
        ]
    }

# ============ MESSAGING ============
class MessageCreate(BaseModel):
    recipient_id: int
    subject: str
    message: str

@router.post("/parent/messages")
async def send_message(
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("parent"))
):
    message = Message(
        sender_id=current_user.id,
        recipient_id=message_data.recipient_id,
        subject=message_data.subject,
        message=message_data.message
    )
    db.add(message)
    db.commit()
    
    return {"message": "Message sent", "id": message.id}

@router.get("/parent/messages")
async def get_messages(
    db: Session = Depends(get_db),
    current_user = Depends(require_role("parent"))
):
    messages = db.query(Message).filter(
        or_(Message.sender_id == current_user.id, Message.recipient_id == current_user.id)
    ).order_by(Message.created_at.desc()).all()
    
    return [
        {
            "id": m.id,
            "subject": m.subject,
            "message": m.message,
            "is_read": m.is_read,
            "sender_id": m.sender_id,
            "recipient_id": m.recipient_id,
            "created_at": m.created_at
        } for m in messages
    ]

@router.put("/parent/messages/{message_id}/read")
async def mark_message_read(
    message_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("parent"))
):
    message = db.query(Message).filter(
        and_(Message.id == message_id, Message.recipient_id == current_user.id)
    ).first()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    message.is_read = True
    db.commit()
    
    return {"message": "Marked as read"}

# ============ MEETING REQUESTS ============
class MeetingRequest(BaseModel):
    teacher_id: int
    student_id: int
    preferred_date: str
    purpose: str

@router.post("/parent/meetings/request")
async def request_meeting(
    meeting_data: MeetingRequest,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("parent"))
):
    guardian = db.query(Guardian).filter(Guardian.user_id == current_user.id).first()
    
    meeting = ParentTeacherMeeting(
        parent_id=guardian.id,
        teacher_id=meeting_data.teacher_id,
        student_id=meeting_data.student_id,
        meeting_date=datetime.fromisoformat(meeting_data.preferred_date),
        purpose=meeting_data.purpose,
        status="scheduled"
    )
    db.add(meeting)
    db.commit()
    
    return {"message": "Meeting request sent", "id": meeting.id}

@router.get("/parent/meetings")
async def get_meetings(
    db: Session = Depends(get_db),
    current_user = Depends(require_role("parent"))
):
    guardian = db.query(Guardian).filter(Guardian.user_id == current_user.id).first()
    
    meetings = db.query(ParentTeacherMeeting).filter(
        ParentTeacherMeeting.parent_id == guardian.id
    ).order_by(ParentTeacherMeeting.meeting_date.desc()).all()
    
    return [
        {
            "id": m.id,
            "meeting_date": m.meeting_date,
            "purpose": m.purpose,
            "status": m.status,
            "notes": m.notes,
            "student_id": m.student_id,
            "teacher_id": m.teacher_id
        } for m in meetings
    ]

# ============ REPORT ABSENCE ============
class AbsenceReport(BaseModel):
    student_id: int
    date: str
    reason: str

@router.post("/parent/report-absence")
async def report_absence(
    absence_data: AbsenceReport,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("parent"))
):
    guardian = db.query(Guardian).filter(Guardian.user_id == current_user.id).first()
    student = db.query(Student).filter(Student.id == absence_data.student_id).first()
    
    if not student or student not in guardian.students:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Create or update attendance record
    date = datetime.fromisoformat(absence_data.date)
    attendance = db.query(Attendance).filter(
        and_(Attendance.student_id == absence_data.student_id, func.date(Attendance.date) == date.date())
    ).first()
    
    if attendance:
        attendance.status = "sick"
        attendance.notes = absence_data.reason
    else:
        attendance = Attendance(
            student_id=absence_data.student_id,
            class_id=student.class_id,
            date=date,
            status="sick",
            notes=absence_data.reason
        )
        db.add(attendance)
    
    db.commit()
    
    return {"message": "Absence reported"}

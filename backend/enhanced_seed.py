"""Enhanced seed script with all new features"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from datetime import datetime, timedelta
from app.core.database import SessionLocal, engine, Base
from app.models import *
from app.core.security import get_password_hash

def seed_enhanced_data():
    db = SessionLocal()
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Tables created")
        
        # 1. ACADEMIC CALENDAR
        print("\nSeeding Academic Calendar...")
        terms = [
            AcademicTerm(
                name="Term 1",
                academic_year="2024",
                start_date=datetime(2024, 1, 15).date(),
                end_date=datetime(2024, 4, 15).date(),
                is_active=True
            ),
            AcademicTerm(
                name="Term 2",
                academic_year="2024",
                start_date=datetime(2024, 5, 1).date(),
                end_date=datetime(2024, 8, 15).date(),
                is_active=False
            ),
            AcademicTerm(
                name="Term 3",
                academic_year="2024",
                start_date=datetime(2024, 9, 1).date(),
                end_date=datetime(2024, 12, 15).date(),
                is_active=False
            )
        ]
        db.add_all(terms)
        db.commit()
        print(f"Added {len(terms)} academic terms")
        
        # 2. HOLIDAYS
        holidays = [
            Holiday(
                name="Easter Break",
                start_date=datetime(2024, 4, 1).date(),
                end_date=datetime(2024, 4, 7).date(),
                description="Easter holiday"
            ),
            Holiday(
                name="Mid-Term Break",
                start_date=datetime(2024, 6, 15).date(),
                end_date=datetime(2024, 6, 22).date(),
                description="Mid-term break"
            )
        ]
        db.add_all(holidays)
        db.commit()
        print(f"Added {len(holidays)} holidays")
        
        # 3. SCHOOL EVENTS
        events = [
            SchoolEvent(
                title="Sports Day",
                event_type="sports_day",
                event_date=datetime(2024, 3, 15).date(),
                description="Annual sports competition",
                location="School Field"
            ),
            SchoolEvent(
                title="Parent-Teacher Conference",
                event_type="meeting",
                event_date=datetime(2024, 4, 10).date(),
                description="End of term parent meetings",
                location="School Hall"
            ),
            SchoolEvent(
                title="Cultural Day",
                event_type="cultural",
                event_date=datetime(2024, 5, 20).date(),
                description="Celebration of Rwandan culture",
                location="School Grounds"
            )
        ]
        db.add_all(events)
        db.commit()
        print(f"Added {len(events)} school events")
        
        # 4. SCHOOL SETTINGS
        settings = SchoolSettings(
            school_name="Faith Brilliant Stars School",
            school_motto="Excellence in Education",
            address="Kigali, Rwanda",
            phone="+250788123456",
            email="info@faithschool.rw",
            website="www.faithschool.rw",
            currency="RWF",
            academic_year="2024",
            current_term="Term 1",
            late_fee_percentage=5.0,
            grace_period_days=7,
            sms_enabled=True,
            email_enabled=True
        )
        db.add(settings)
        db.commit()
        print("Added school settings")
        
        # 5. PROMOTION RULES
        promotion_rules = [
            PromotionRule(
                from_grade="P1",
                to_grade="P2",
                min_attendance_percentage=75.0,
                min_average_score=50.0,
                is_active=True
            ),
            PromotionRule(
                from_grade="P2",
                to_grade="P3",
                min_attendance_percentage=75.0,
                min_average_score=50.0,
                is_active=True
            ),
            PromotionRule(
                from_grade="P3",
                to_grade="P4",
                min_attendance_percentage=75.0,
                min_average_score=50.0,
                is_active=True
            )
        ]
        db.add_all(promotion_rules)
        db.commit()
        print(f"Added {len(promotion_rules)} promotion rules")
        
        # 6. DISCOUNTS
        discounts = [
            Discount(
                name="Sibling Discount",
                discount_type="sibling",
                percentage=10.0,
                conditions={"min_siblings": 2},
                is_active=True
            ),
            Discount(
                name="Staff Child Discount",
                discount_type="staff_child",
                percentage=25.0,
                conditions={},
                is_active=True
            ),
            Discount(
                name="Scholarship",
                discount_type="scholarship",
                percentage=50.0,
                conditions={"min_average": 85.0},
                is_active=True
            )
        ]
        db.add_all(discounts)
        db.commit()
        print(f"Added {len(discounts)} discount types")
        
        # 7. SAMPLE NOTIFICATIONS
        print("\nCreating sample notifications...")
        head_teacher = db.query(User).filter(User.role == "head_teacher").first()
        if head_teacher:
            notifications = [
                Notification(
                    user_id=head_teacher.id,
                    title="New Student Enrollment",
                    message="5 new students enrolled this week",
                    notification_type="announcement",
                    is_read=0
                ),
                Notification(
                    user_id=head_teacher.id,
                    title="Payment Received",
                    message="RWF 500,000 received today",
                    notification_type="payment",
                    is_read=0
                )
            ]
            db.add_all(notifications)
            db.commit()
            print(f"Added {len(notifications)} notifications")
        
        # 8. SAMPLE MESSAGES
        print("\nCreating sample messages...")
        teacher = db.query(User).filter(User.role == "teacher").first()
        parent = db.query(User).filter(User.role == "parent").first()
        
        if teacher and parent:
            messages = [
                Message(
                    sender_id=teacher.id,
                    recipient_id=parent.id,
                    subject="Student Progress Update",
                    message="Your child is doing well in class. Keep up the good work!",
                    is_read=False
                ),
                Message(
                    sender_id=parent.id,
                    recipient_id=teacher.id,
                    subject="Meeting Request",
                    message="I would like to schedule a meeting to discuss my child's progress.",
                    is_read=False
                )
            ]
            db.add_all(messages)
            db.commit()
            print(f"Added {len(messages)} messages")
        
        # 9. SAMPLE PARENT-TEACHER MEETINGS
        print("\nCreating sample meetings...")
        guardian = db.query(Guardian).first()
        teacher_profile = db.query(Teacher).first()
        student = db.query(Student).first()
        
        if guardian and teacher_profile and student:
            meetings = [
                ParentTeacherMeeting(
                    parent_id=guardian.id,
                    teacher_id=teacher_profile.id,
                    student_id=student.id,
                    meeting_date=datetime.now() + timedelta(days=7),
                    purpose="Discuss academic progress",
                    status="scheduled"
                ),
                ParentTeacherMeeting(
                    parent_id=guardian.id,
                    teacher_id=teacher_profile.id,
                    student_id=student.id,
                    meeting_date=datetime.now() - timedelta(days=30),
                    purpose="Term 1 review",
                    notes="Student is performing well. Needs to improve in mathematics.",
                    status="completed"
                )
            ]
            db.add_all(meetings)
            db.commit()
            print(f"Added {len(meetings)} meetings")
        
        # 10. AUDIT LOGS
        print("\nCreating audit logs...")
        if head_teacher:
            audit_logs = [
                AuditLog(
                    user_id=head_teacher.id,
                    action="create",
                    entity_type="student",
                    entity_id=1,
                    changes={"action": "Student enrolled"},
                    ip_address="192.168.1.1"
                ),
                AuditLog(
                    user_id=head_teacher.id,
                    action="update",
                    entity_type="settings",
                    entity_id=1,
                    changes={"field": "late_fee_percentage", "old": 3.0, "new": 5.0},
                    ip_address="192.168.1.1"
                )
            ]
            db.add_all(audit_logs)
            db.commit()
            print(f"Added {len(audit_logs)} audit logs")
        
        print("\nEnhanced seed data completed successfully!")
        print("\nSummary:")
        print(f"   - Academic Terms: {db.query(AcademicTerm).count()}")
        print(f"   - Holidays: {db.query(Holiday).count()}")
        print(f"   - School Events: {db.query(SchoolEvent).count()}")
        print(f"   - Promotion Rules: {db.query(PromotionRule).count()}")
        print(f"   - Discounts: {db.query(Discount).count()}")
        print(f"   - Notifications: {db.query(Notification).count()}")
        print(f"   - Messages: {db.query(Message).count()}")
        print(f"   - Meetings: {db.query(ParentTeacherMeeting).count()}")
        print(f"   - Audit Logs: {db.query(AuditLog).count()}")
        
    except Exception as e:
        print(f"\nError: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("Starting enhanced database seeding...")
    seed_enhanced_data()

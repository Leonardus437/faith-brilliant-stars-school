# 📚 API Reference - Faith Brilliant Stars School

Base URL: `http://localhost:8001/api`

## 🔐 Authentication

All endpoints require JWT token in header:
```
Authorization: Bearer <token>
```

### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@faithschool.rw",
  "password": "password"
}

Response: { "access_token": "...", "token_type": "bearer" }
```

---

## 👑 HEAD TEACHER ENDPOINTS

### Dashboard
```http
GET /head-teacher/dashboard
Authorization: Bearer <token>

Response: {
  "total_students": 60,
  "total_teachers": 5,
  "total_classes": 6,
  "attendance_rate": 92.5,
  "revenue_this_month": 500000,
  "outstanding_fees": 150000
}
```

### Student Management
```http
POST /head-teacher/students
{
  "admission_number": "2024001",
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "2015-01-15",
  "gender": "M",
  "class_id": 1,
  "enrollment_date": "2024-01-15",
  "emergency_contact": {"name": "Jane Doe", "phone": "+250788123456"}
}

PUT /head-teacher/students/{student_id}
DELETE /head-teacher/students/{student_id}
```

### Teacher Management
```http
POST /head-teacher/teachers
{
  "email": "teacher@faithschool.rw",
  "full_name": "Teacher Name",
  "employee_number": "EMP001",
  "first_name": "Teacher",
  "last_name": "Name",
  "phone": "+250788123456",
  "qualification": "Bachelor of Education",
  "specialization": "Mathematics"
}

GET /head-teacher/teachers
```

### Class Management
```http
POST /head-teacher/classes
{
  "name": "P1 A",
  "grade_level": "P1",
  "academic_year": "2024",
  "class_teacher_id": 1,
  "capacity": 40,
  "room_number": "101"
}
```

### Academic Calendar
```http
POST /head-teacher/terms
{
  "name": "Term 1",
  "academic_year": "2024",
  "start_date": "2024-01-15",
  "end_date": "2024-04-15"
}

GET /head-teacher/terms
```

### School Settings
```http
GET /head-teacher/settings
PUT /head-teacher/settings
{
  "school_name": "Faith Brilliant Stars School",
  "currency": "RWF",
  "late_fee_percentage": 5.0,
  "grace_period_days": 7
}
```

### Reports
```http
GET /head-teacher/reports/attendance?start_date=2024-01-01&end_date=2024-01-31
GET /head-teacher/reports/financial?start_date=2024-01-01&end_date=2024-01-31
```

---

## 💰 ACCOUNTANT ENDPOINTS

### Dashboard
```http
GET /accountant/dashboard

Response: {
  "total_revenue_today": 50000,
  "total_revenue_month": 500000,
  "outstanding_fees": 150000,
  "pending_invoices": 15,
  "payment_methods_breakdown": {"cash": 200000, "mtn_momo": 300000}
}
```

### Fee Structure
```http
POST /accountant/fee-structures
{
  "class_id": 1,
  "category": "tuition",
  "term": "term_1",
  "amount": 50000,
  "description": "Term 1 tuition fees"
}

GET /accountant/fee-structures
```

### Bulk Invoices
```http
POST /accountant/invoices/bulk
{
  "class_id": 1,
  "category": "tuition",
  "term": "term_1",
  "amount": 50000,
  "due_date": "2024-02-15",
  "description": "Term 1 fees"
}
```

### Payment Processing
```http
POST /accountant/payments
{
  "invoice_id": 1,
  "amount": 50000,
  "payment_method": "mtn_momo",
  "reference": "MM123456"
}
```

### Payment Plans
```http
POST /accountant/payment-plans
{
  "invoice_id": 1,
  "installments": 3,
  "start_date": "2024-02-01"
}
```

### Discounts
```http
POST /accountant/discounts
{
  "name": "Sibling Discount",
  "discount_type": "sibling",
  "percentage": 10.0,
  "conditions": {"min_siblings": 2}
}
```

### Reports
```http
GET /accountant/reports/revenue?start_date=2024-01-01&end_date=2024-01-31
GET /accountant/reports/outstanding
GET /accountant/reports/collection-rate?term=term_1
```

### Mobile Money
```http
POST /accountant/mobile-money/initiate
{
  "invoice_id": 1,
  "phone_number": "+250788123456",
  "provider": "mtn_momo"
}
```

---

## 👨🏫 TEACHER ENDPOINTS

### Dashboard
```http
GET /teacher/dashboard

Response: {
  "assigned_classes": [...],
  "total_students": 40,
  "today_attendance_rate": 95.0,
  "this_week_attendance_rate": 92.5,
  "students_with_low_attendance": [...]
}
```

### Bulk Attendance
```http
POST /teacher/attendance/bulk
{
  "class_id": 1,
  "date": "2024-01-15",
  "attendance_records": [
    {"student_id": 1, "status": "present"},
    {"student_id": 2, "status": "absent"}
  ]
}
```

### Mark All Present
```http
POST /teacher/attendance/mark-all-present?class_id=1&date=2024-01-15
```

### Attendance History
```http
GET /teacher/attendance/history?class_id=1&start_date=2024-01-01&end_date=2024-01-31
```

### Student Attendance Profile
```http
GET /teacher/students/{student_id}/attendance
```

### Class Roster
```http
GET /teacher/classes/{class_id}/roster
```

### Reports
```http
GET /teacher/reports/attendance-summary?class_id=1&month=2024-01
```

### Offline Sync
```http
POST /teacher/attendance/sync
[
  {
    "student_id": 1,
    "class_id": 1,
    "date": "2024-01-15",
    "status": "present"
  }
]
```

---

## 👨👩👧👦 PARENT ENDPOINTS

### Dashboard
```http
GET /parent/dashboard

Response: {
  "children": [...],
  "total_outstanding": 100000,
  "unread_messages": 3,
  "upcoming_meetings": [...],
  "recent_announcements": [...]
}
```

### Child Details
```http
GET /parent/children/{student_id}
```

### Attendance Tracking
```http
GET /parent/children/{student_id}/attendance?start_date=2024-01-01&end_date=2024-01-31
```

### Fee Management
```http
GET /parent/children/{student_id}/fees
GET /parent/children/{student_id}/payment-history
```

### Academic Progress
```http
GET /parent/children/{student_id}/academic-progress
```

### Messaging
```http
POST /parent/messages
{
  "recipient_id": 2,
  "subject": "Meeting Request",
  "message": "I would like to schedule a meeting..."
}

GET /parent/messages
PUT /parent/messages/{message_id}/read
```

### Meeting Requests
```http
POST /parent/meetings/request
{
  "teacher_id": 1,
  "student_id": 1,
  "preferred_date": "2024-02-15T10:00:00",
  "purpose": "Discuss academic progress"
}

GET /parent/meetings
```

### Report Absence
```http
POST /parent/report-absence
{
  "student_id": 1,
  "date": "2024-01-15",
  "reason": "Sick with flu"
}
```

---

## 📊 Common Response Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Server Error

---

## 🔄 Pagination

For list endpoints:
```http
GET /endpoint?page=1&limit=20
```

---

## 🔍 Filtering

```http
GET /students?class_id=1&status=active
GET /invoices?status=pending&term=term_1
```

---

## 📝 Notes

- All dates in ISO 8601 format: `YYYY-MM-DD` or `YYYY-MM-DDTHH:MM:SS`
- Currency amounts in RWF (Rwandan Francs)
- Phone numbers in international format: `+250788123456`
- File uploads use `multipart/form-data`

---

## 🧪 Testing

Use the interactive API documentation:
- **Swagger UI:** http://localhost:8001/docs
- **ReDoc:** http://localhost:8001/redoc

---

## 📞 Support

For API support: info@faithschool.rw

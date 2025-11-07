# 🚀 Quick Reference Guide

## 📋 Table of Contents
- [Getting Started](#getting-started)
- [User Roles](#user-roles)
- [Common Tasks](#common-tasks)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Getting Started

### 1. Start the System
```bash
# Standard start
START.bat

# Enhanced start (with all new features)
START_ENHANCED.bat
```

### 2. Access the System
- **Frontend:** http://localhost:5174
- **Backend API:** http://localhost:8001
- **API Docs:** http://localhost:8001/docs

### 3. Login
Use one of the test accounts (see User Roles below)

---

## 👥 User Roles

### 👑 Head Teacher
**Email:** head@faithschool.rw  
**Password:** Head2024  
**Dashboard:** `/head-teacher`

**Can Do:**
- ✅ Manage students (add, edit, remove)
- ✅ Manage teachers (hire, assign)
- ✅ Create and organize classes
- ✅ Set academic calendar
- ✅ Configure school settings
- ✅ View all reports and analytics
- ✅ Manage system users

### 💰 Accountant
**Email:** accounts@faithschool.rw  
**Password:** Accounts2024  
**Dashboard:** `/accountant`

**Can Do:**
- ✅ Create fee structures
- ✅ Generate invoices (single & bulk)
- ✅ Process payments
- ✅ Create payment plans
- ✅ Manage discounts
- ✅ View financial reports
- ✅ Initiate mobile money payments

### 👨🏫 Teacher
**Email:** teacher@faithschool.rw  
**Password:** Teacher2024  
**Dashboard:** `/teacher` (API)

**Can Do:**
- ✅ Mark attendance (daily)
- ✅ Bulk mark attendance
- ✅ Mark all present
- ✅ View class roster
- ✅ View student profiles
- ✅ Generate attendance reports
- ✅ Sync offline attendance

### 👨👩👧👦 Parent
**Email:** parent@faithschool.rw  
**Password:** Parent2024  
**Dashboard:** `/parent` (API)

**Can Do:**
- ✅ View children's attendance
- ✅ Check fee balances
- ✅ View payment history
- ✅ See academic progress
- ✅ Message teachers
- ✅ Request meetings
- ✅ Report absences

---

## 📝 Common Tasks

### For Head Teacher

#### Add a New Student
```http
POST /api/head-teacher/students
{
  "admission_number": "2024001",
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "2015-01-15",
  "gender": "M",
  "class_id": 1,
  "enrollment_date": "2024-01-15",
  "emergency_contact": {
    "name": "Jane Doe",
    "phone": "+250788123456"
  }
}
```

#### Hire a New Teacher
```http
POST /api/head-teacher/teachers
{
  "email": "newteacher@faithschool.rw",
  "full_name": "New Teacher",
  "employee_number": "EMP002",
  "first_name": "New",
  "last_name": "Teacher",
  "phone": "+250788123456",
  "qualification": "Bachelor of Education",
  "specialization": "Science"
}
```

#### Create a New Class
```http
POST /api/head-teacher/classes
{
  "name": "P2 B",
  "grade_level": "P2",
  "academic_year": "2024",
  "capacity": 40,
  "room_number": "102"
}
```

### For Accountant

#### Create Bulk Invoices
```http
POST /api/accountant/invoices/bulk
{
  "class_id": 1,
  "category": "tuition",
  "term": "term_1",
  "amount": 50000,
  "due_date": "2024-02-15"
}
```

#### Record a Payment
```http
POST /api/accountant/payments
{
  "invoice_id": 1,
  "amount": 50000,
  "payment_method": "mtn_momo",
  "reference": "MM123456"
}
```

#### Create a Discount
```http
POST /api/accountant/discounts
{
  "name": "Sibling Discount",
  "discount_type": "sibling",
  "percentage": 10.0
}
```

### For Teacher

#### Mark Attendance (Bulk)
```http
POST /api/teacher/attendance/bulk
{
  "class_id": 1,
  "date": "2024-01-15",
  "attendance_records": [
    {"student_id": 1, "status": "present"},
    {"student_id": 2, "status": "absent"},
    {"student_id": 3, "status": "late"}
  ]
}
```

#### Mark All Present
```http
POST /api/teacher/attendance/mark-all-present?class_id=1&date=2024-01-15
```

### For Parent

#### View Child's Attendance
```http
GET /api/parent/children/1/attendance?start_date=2024-01-01&end_date=2024-01-31
```

#### Send Message to Teacher
```http
POST /api/parent/messages
{
  "recipient_id": 2,
  "subject": "Question about homework",
  "message": "Could you please clarify..."
}
```

#### Report Child Absence
```http
POST /api/parent/report-absence
{
  "student_id": 1,
  "date": "2024-01-15",
  "reason": "Sick with flu"
}
```

---

## 🔗 API Endpoints Quick List

### Authentication
- `POST /api/auth/login` - Login
- `POST /api/auth/register` - Register
- `GET /api/auth/me` - Get current user

### Head Teacher
- `GET /api/head-teacher/dashboard` - Dashboard stats
- `POST /api/head-teacher/students` - Add student
- `POST /api/head-teacher/teachers` - Add teacher
- `POST /api/head-teacher/classes` - Create class
- `POST /api/head-teacher/terms` - Create term
- `GET /api/head-teacher/settings` - Get settings
- `GET /api/head-teacher/reports/attendance` - Attendance report
- `GET /api/head-teacher/reports/financial` - Financial report

### Accountant
- `GET /api/accountant/dashboard` - Dashboard stats
- `POST /api/accountant/fee-structures` - Create fee structure
- `POST /api/accountant/invoices/bulk` - Bulk invoices
- `POST /api/accountant/payments` - Record payment
- `POST /api/accountant/payment-plans` - Create payment plan
- `POST /api/accountant/discounts` - Create discount
- `GET /api/accountant/reports/revenue` - Revenue report
- `GET /api/accountant/reports/outstanding` - Outstanding report

### Teacher
- `GET /api/teacher/dashboard` - Dashboard stats
- `POST /api/teacher/attendance/bulk` - Bulk attendance
- `POST /api/teacher/attendance/mark-all-present` - Mark all present
- `GET /api/teacher/attendance/history` - Attendance history
- `GET /api/teacher/classes/{id}/roster` - Class roster
- `GET /api/teacher/reports/attendance-summary` - Attendance summary

### Parent
- `GET /api/parent/dashboard` - Dashboard stats
- `GET /api/parent/children/{id}` - Child details
- `GET /api/parent/children/{id}/attendance` - Child attendance
- `GET /api/parent/children/{id}/fees` - Child fees
- `GET /api/parent/children/{id}/academic-progress` - Academic progress
- `POST /api/parent/messages` - Send message
- `POST /api/parent/meetings/request` - Request meeting
- `POST /api/parent/report-absence` - Report absence

---

## 🔧 Troubleshooting

### Backend Not Starting
```bash
# Check if port 8001 is in use
netstat -ano | findstr :8001

# Kill the process if needed
taskkill /PID <process_id> /F

# Restart backend
cd backend
python -m uvicorn app.main:app --reload --port 8001
```

### Frontend Not Starting
```bash
# Check if port 5174 is in use
netstat -ano | findstr :5174

# Kill the process if needed
taskkill /PID <process_id> /F

# Restart frontend
cd frontend
npm run dev -- --port 5174
```

### Database Issues
```bash
# Reset database
cd backend
python reset_db.py

# Run enhanced seed
python enhanced_seed.py
```

### Login Issues
```bash
# Check user credentials
cd backend
python check_users.py

# Fix passwords if needed
python fix_passwords.py
```

### API Not Responding
1. Check backend is running: http://localhost:8001/health
2. Check API docs: http://localhost:8001/docs
3. Verify token in localStorage
4. Check CORS settings

### 401 Unauthorized
- Token expired - login again
- Token missing - check localStorage
- Wrong role - verify user permissions

### 404 Not Found
- Check endpoint URL
- Verify API is running
- Check route exists in docs

---

## 📊 Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request (check input)
- `401` - Unauthorized (login required)
- `403` - Forbidden (wrong role)
- `404` - Not Found (check URL)
- `500` - Server Error (check logs)

---

## 🎯 Best Practices

### For Developers
1. Always check API docs first
2. Use proper authentication headers
3. Validate input data
4. Handle errors gracefully
5. Log important actions

### For Users
1. Logout when done
2. Keep credentials secure
3. Report issues promptly
4. Use correct role account
5. Check notifications regularly

---

## 📞 Need Help?

- **Documentation:** See ENHANCED_FEATURES.md
- **API Reference:** See API_REFERENCE.md
- **Email:** info@faithschool.rw
- **Phone:** +250788123456

---

## 🔄 Quick Commands

```bash
# Start system
START_ENHANCED.bat

# Stop system
STOP.bat

# Check system status
CHECK_SYSTEM.bat

# Reset database
cd backend && python reset_db.py

# Run tests
cd backend && pytest

# View logs
cd backend && tail -f app.log
```

---

*Last Updated: 2024*
*Version: 2.0.0*

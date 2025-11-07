# 🧪 TEST ADMIN FEATURES - QUICK GUIDE

## 🚀 START THE SYSTEM

```bash
# Double-click START.bat or run:
cd "T:\Faith Brilliant Stars School"
START.bat
```

## 👤 LOGIN AS ADMIN

```
URL: http://localhost:5174/login
Email: head@faithschool.rw
Password: Head2024
```

## 📊 TEST DASHBOARD

1. After login, you'll see the admin dashboard
2. Verify these cards display:
   - Total Students (should show 62+)
   - Total Teachers (should show 4+)
   - Total Revenue (should show amount in RWF)
   - Attendance Rate (should show percentage)

## 🧑‍🎓 TEST STUDENT MANAGEMENT

### View All Students:
```
GET http://localhost:8001/api/admin/students
```

### Create New Student:
```
POST http://localhost:8001/api/admin/students
Body: {
  "first_name": "Test",
  "last_name": "Student",
  "date_of_birth": "2015-01-15",
  "gender": "Male",
  "class_id": 1
}
```

## 👨‍🏫 TEST TEACHER MANAGEMENT

### View All Teachers:
```
GET http://localhost:8001/api/admin/teachers
```

### Create New Teacher:
```
POST http://localhost:8001/api/admin/teachers
Body: {
  "full_name": "New Teacher",
  "email": "newteacher@faithschool.rw",
  "password": "Teacher2024",
  "phone": "+250788999999",
  "qualification": "Bachelor of Education"
}
```

## 🏫 TEST CLASS MANAGEMENT

### View All Classes:
```
GET http://localhost:8001/api/admin/classes
```

### Create New Class:
```
POST http://localhost:8001/api/admin/classes
Body: {
  "name": "P1 B",
  "grade_level": "P1",
  "capacity": 40,
  "room_number": "R102"
}
```

## 💰 TEST FINANCIAL ANALYTICS

### View Financial Overview:
```
GET http://localhost:8001/api/admin/finances
```

Expected Response:
- Monthly revenue breakdown
- Outstanding fees by class
- Payment methods distribution

## ✅ TEST ATTENDANCE ANALYTICS

### View Attendance Analytics:
```
GET http://localhost:8001/api/admin/attendance/analytics
```

Expected Response:
- Overall attendance rate
- Class-wise attendance rates
- Daily attendance trends (last 30 days)

## 📢 TEST ANNOUNCEMENTS

### Create Announcement:
```
POST http://localhost:8001/api/admin/announcements
Body: {
  "title": "Test Announcement",
  "content": "This is a test announcement",
  "priority": "high"
}
```

### View All Announcements:
```
GET http://localhost:8001/api/admin/announcements
```

## 📋 TEST REPORTS

### Student Report:
```
GET http://localhost:8001/api/admin/reports/students
```

### Financial Report:
```
GET http://localhost:8001/api/admin/reports/financial
```

## 👥 TEST USER MANAGEMENT

### View All Users:
```
GET http://localhost:8001/api/admin/users
```

### Toggle User Status:
```
PUT http://localhost:8001/api/admin/users/5/status
```

## 🔍 VERIFY FEATURES WORK

### ✅ Checklist:
- [ ] Dashboard loads with correct statistics
- [ ] Can view all students
- [ ] Can create new student
- [ ] Can view all teachers
- [ ] Can create new teacher
- [ ] Can view all classes
- [ ] Can create new class
- [ ] Financial analytics display correctly
- [ ] Attendance analytics display correctly
- [ ] Can create announcements
- [ ] Can view all users
- [ ] Can toggle user status
- [ ] Reports generate correctly

## 🐛 TROUBLESHOOTING

### If Dashboard Doesn't Load:
1. Check backend is running on port 8001
2. Check frontend is running on port 5174
3. Verify you're logged in as head_teacher role
4. Check browser console for errors

### If API Returns 403 Forbidden:
- Verify you're logged in with admin credentials
- Check JWT token is valid
- Ensure role is 'head_teacher'

### If Data Doesn't Display:
- Check database has data (run enhanced_seed_safe.py)
- Verify API endpoints are responding
- Check network tab in browser dev tools

## 📊 EXPECTED DATA

After running seed scripts, you should have:
- 62+ students across 6 classes
- 4+ teachers
- 242+ invoices
- 300+ attendance records
- Multiple users with different roles

## 🎯 SUCCESS CRITERIA

Admin features are working if:
1. ✅ Dashboard displays all statistics
2. ✅ Can perform CRUD operations on students
3. ✅ Can perform CRUD operations on teachers
4. ✅ Can perform CRUD operations on classes
5. ✅ Financial analytics show data
6. ✅ Attendance analytics show data
7. ✅ Can create and view announcements
8. ✅ Can manage users
9. ✅ Reports generate successfully
10. ✅ All API endpoints respond correctly

**All admin features are implemented and ready for testing!**

import sqlite3
from datetime import datetime, timedelta, date
import random
import bcrypt

# Connect to database
conn = sqlite3.connect('faithschool.db')
cursor = conn.cursor()

# Drop all tables
cursor.execute("DROP TABLE IF EXISTS attendance")
cursor.execute("DROP TABLE IF EXISTS payments")
cursor.execute("DROP TABLE IF EXISTS invoices")
cursor.execute("DROP TABLE IF EXISTS student_guardians")
cursor.execute("DROP TABLE IF EXISTS students")
cursor.execute("DROP TABLE IF EXISTS guardians")
cursor.execute("DROP TABLE IF EXISTS classes")
cursor.execute("DROP TABLE IF EXISTS teachers")
cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("DROP TABLE IF EXISTS subjects")
cursor.execute("DROP TABLE IF EXISTS fee_structures")
cursor.execute("DROP TABLE IF EXISTS service_items")

# Create tables
cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    full_name TEXT NOT NULL,
    phone TEXT,
    role TEXT NOT NULL,
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    employee_number TEXT,
    first_name TEXT,
    last_name TEXT,
    phone TEXT,
    qualification TEXT,
    hire_date TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

cursor.execute("""
CREATE TABLE classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    grade_level TEXT,
    academic_year TEXT,
    class_teacher_id INTEGER,
    capacity INTEGER,
    room_number TEXT,
    FOREIGN KEY (class_teacher_id) REFERENCES teachers(id)
)
""")

cursor.execute("""
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    admission_number TEXT UNIQUE,
    first_name TEXT,
    last_name TEXT,
    date_of_birth TEXT,
    gender TEXT,
    class_id INTEGER,
    enrollment_status TEXT DEFAULT 'active',
    enrollment_date TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (class_id) REFERENCES classes(id)
)
""")

cursor.execute("""
CREATE TABLE guardians (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    first_name TEXT,
    last_name TEXT,
    phone TEXT,
    email TEXT,
    national_id TEXT,
    occupation TEXT,
    address TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

cursor.execute("""
CREATE TABLE student_guardians (
    student_id INTEGER,
    guardian_id INTEGER,
    relation TEXT,
    is_primary INTEGER,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (guardian_id) REFERENCES guardians(id)
)
""")

cursor.execute("""
CREATE TABLE attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    class_id INTEGER,
    date TEXT,
    status TEXT,
    notes TEXT,
    recorded_by INTEGER,
    recorded_at TEXT,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (class_id) REFERENCES classes(id),
    FOREIGN KEY (recorded_by) REFERENCES users(id)
)
""")

cursor.execute("""
CREATE TABLE invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_number TEXT UNIQUE,
    student_id INTEGER,
    category TEXT,
    term TEXT,
    amount REAL,
    amount_paid REAL DEFAULT 0,
    status TEXT,
    due_date TEXT,
    created_by INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (created_by) REFERENCES users(id)
)
""")

cursor.execute("""
CREATE TABLE payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    receipt_number TEXT UNIQUE,
    invoice_id INTEGER,
    amount REAL,
    payment_method TEXT,
    payment_date TEXT,
    recorded_by INTEGER,
    FOREIGN KEY (invoice_id) REFERENCES invoices(id),
    FOREIGN KEY (recorded_by) REFERENCES users(id)
)
""")

# Insert users with proper password hashing
users = [
    (1, 'head@faithschool.rw', bcrypt.hashpw(b'Head2024', bcrypt.gensalt()).decode(), 'Dr. Sarah Mugisha', '+250788000001', 'head_teacher', 1),
    (2, 'teacher@faithschool.rw', bcrypt.hashpw(b'Teacher2024', bcrypt.gensalt()).decode(), 'John Uwimana', '+250788000002', 'teacher', 1),
    (3, 'accounts@faithschool.rw', bcrypt.hashpw(b'Accounts2024', bcrypt.gensalt()).decode(), 'Mary Kamikazi', '+250788000003', 'accountant', 1),
    (4, 'parent@faithschool.rw', bcrypt.hashpw(b'Parent2024', bcrypt.gensalt()).decode(), 'Jane Uwase', '+250788000004', 'parent', 1)
]

cursor.executemany("INSERT INTO users (id, email, hashed_password, full_name, phone, role, is_active) VALUES (?, ?, ?, ?, ?, ?, ?)", users)

# Insert teacher
cursor.execute("INSERT INTO teachers (id, user_id, employee_number, first_name, last_name, phone, qualification, hire_date) VALUES (1, 2, 'EMP001', 'John', 'Uwimana', '+250788000002', 'Bachelor of Education', ?)", (datetime.now().isoformat(),))

# Insert classes
classes = [(i, f'P{i} A', f'P{i}', '2024', 1, 40, f'R{i}01') for i in range(1, 7)]
cursor.executemany("INSERT INTO classes (id, name, grade_level, academic_year, class_teacher_id, capacity, room_number) VALUES (?, ?, ?, ?, ?, ?, ?)", classes)

# Insert guardian
cursor.execute("INSERT INTO guardians (id, user_id, first_name, last_name, phone, email, national_id, occupation, address) VALUES (1, 4, 'Jane', 'Uwase', '+250788000004', 'parent@faithschool.rw', '1198012345678901', 'Business Owner', 'Kigali, Gasabo')")

# Insert students
student_id = 1
for class_id in range(1, 7):
    for i in range(10):
        cursor.execute("""
            INSERT INTO students (id, admission_number, first_name, last_name, date_of_birth, gender, class_id, enrollment_status, enrollment_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'active', '2024-01-15')
        """, (student_id, f'FBS2024{student_id:04d}', f'Student{student_id}', 'Test', f'2010-0{random.randint(1,9)}-{random.randint(10,28)}', random.choice(['Male', 'Female']), class_id))
        student_id += 1

# Link first 3 students to guardian
for student_id in range(1, 4):
    cursor.execute("INSERT INTO student_guardians (student_id, guardian_id, relation, is_primary) VALUES (?, 1, 'parent', 1)", (student_id,))

# Insert invoices
for student_id in range(1, 21):
    status = 'partial' if student_id <= 3 else 'pending'
    amount_paid = 50000 if student_id <= 3 else 0
    due_date = (datetime.now() + timedelta(days=30)).isoformat()
    cursor.execute("""
        INSERT INTO invoices (invoice_number, student_id, category, term, amount, amount_paid, status, due_date, created_by)
        VALUES (?, ?, 'tuition', 'term_1', 150000, ?, ?, ?, 1)
    """, (f'INV-2024-{student_id:05d}', student_id, amount_paid, status, due_date))

# Insert payments for first 3 students
for i in range(1, 4):
    payment_date = (datetime.now() - timedelta(days=i)).isoformat()
    cursor.execute("""
        INSERT INTO payments (receipt_number, invoice_id, amount, payment_method, payment_date, recorded_by)
        VALUES (?, ?, 50000, 'MTN MoMo', ?, 3)
    """, (f'RCP-2024-{i:05d}', i, payment_date))

# Insert attendance for last 5 days
for day in range(5):
    attendance_date = (date.today() - timedelta(days=day)).isoformat()
    for student_id in range(1, 61):
        class_id = ((student_id - 1) // 10) + 1
        status = 'present'
        if random.random() < 0.1:
            status = 'absent'
        elif random.random() < 0.05:
            status = 'late'
        
        cursor.execute("""
            INSERT INTO attendance (student_id, class_id, date, status, recorded_by, recorded_at)
            VALUES (?, ?, ?, ?, 2, ?)
        """, (student_id, class_id, attendance_date, status, datetime.now().isoformat()))

conn.commit()
conn.close()

print("Database seeded successfully!")
print("Created:")
print("   - 4 Users (Head Teacher, Teacher, Accountant, Parent)")
print("   - 60 Students across 6 classes")
print("   - 3 Students linked to parent")
print("   - 20 Invoices with payments")
print("   - 5 days of attendance records")

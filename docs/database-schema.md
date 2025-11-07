# Database Schema

## Overview
The database uses PostgreSQL with SQLAlchemy ORM. All tables include timestamps for audit trails.

## Core Tables

### users
Primary authentication and user management table.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| email | String | Unique email address |
| hashed_password | String | Bcrypt hashed password |
| full_name | String | User's full name |
| phone | String | Contact phone number |
| role | Enum | admin, head_teacher, teacher, accountant, parent, student |
| is_active | Boolean | Account status |
| photo_url | String | Profile photo URL |
| language_preference | String | en or rw |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

### students
Student profile information.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| user_id | Integer | FK to users (unique) |
| admission_number | String | Unique admission number |
| first_name | String | Student first name |
| last_name | String | Student last name |
| date_of_birth | Date | Birth date |
| gender | String | Male/Female |
| photo_url | String | Student photo |
| class_id | Integer | FK to classes |
| enrollment_status | Enum | active, graduated, transferred, withdrawn |
| enrollment_date | Date | Enrollment date |
| emergency_contact | JSON | Emergency contact details |
| medical_info | JSON | Medical information |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

### guardians
Guardian/parent information.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| user_id | Integer | FK to users (unique) |
| first_name | String | Guardian first name |
| last_name | String | Guardian last name |
| phone | String | Contact phone |
| email | String | Email address |
| national_id | String | National ID number |
| occupation | String | Occupation |
| address | String | Physical address |
| consent_sms | Boolean | SMS consent |
| consent_email | Boolean | Email consent |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

### student_guardians
Many-to-many relationship between students and guardians.

| Column | Type | Description |
|--------|------|-------------|
| student_id | Integer | FK to students |
| guardian_id | Integer | FK to guardians |
| relation | String | father, mother, uncle, aunt, etc. |
| is_primary | Boolean | Primary guardian flag |

### teachers
Teacher profile information.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| user_id | Integer | FK to users (unique) |
| employee_number | String | Unique employee number |
| first_name | String | Teacher first name |
| last_name | String | Teacher last name |
| phone | String | Contact phone |
| qualification | String | Educational qualification |
| specialization | String | Subject specialization |
| hire_date | DateTime | Hire date |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

### classes
Class/section information.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| name | String | Class name (e.g., "P1 A") |
| grade_level | String | P1, P2, P3, P4, P5, P6 |
| academic_year | String | Academic year (e.g., "2024") |
| class_teacher_id | Integer | FK to teachers |
| capacity | Integer | Maximum students |
| room_number | String | Classroom number |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

### subjects
Subject definitions.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| name | String | Subject name |
| code | String | Unique subject code |
| description | String | Subject description |
| created_at | DateTime | Creation timestamp |

### class_subjects
Many-to-many: classes and subjects.

| Column | Type | Description |
|--------|------|-------------|
| class_id | Integer | FK to classes |
| subject_id | Integer | FK to subjects |

### teacher_subjects
Many-to-many: teachers and subjects.

| Column | Type | Description |
|--------|------|-------------|
| teacher_id | Integer | FK to teachers |
| subject_id | Integer | FK to subjects |

## Attendance Tables

### attendance
Daily attendance records.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| student_id | Integer | FK to students |
| class_id | Integer | FK to classes |
| date | Date | Attendance date |
| status | Enum | present, absent, late, excused |
| notes | String | Additional notes |
| recorded_by | Integer | FK to users |
| recorded_at | DateTime | Recording timestamp |
| synced | Boolean | Sync status for offline |
| synced_at | DateTime | Sync timestamp |

## Assessment Tables

### assessments
Assessment definitions.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| class_id | Integer | FK to classes |
| subject_id | Integer | FK to subjects |
| term | Enum | term_1, term_2, term_3 |
| type | Enum | quiz, test, exam, assignment, project |
| title | String | Assessment title |
| max_score | Float | Maximum score |
| weight | Float | Weight for averaging |
| date | DateTime | Assessment date |
| created_by | Integer | FK to users |
| created_at | DateTime | Creation timestamp |

### grades
Student grades for assessments.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| student_id | Integer | FK to students |
| assessment_id | Integer | FK to assessments |
| score | Float | Score achieved |
| comments | String | Teacher comments |
| graded_by | Integer | FK to users |
| graded_at | DateTime | Grading timestamp |

## Financial Tables

### fee_structures
Fee definitions by class and category.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| class_id | Integer | FK to classes |
| category | Enum | tuition, breakfast, lunch, transport, etc. |
| term | String | term_1, term_2, term_3, or null |
| amount | Float | Fee amount in RWF |
| description | String | Fee description |
| is_recurring | Boolean | Recurring fee flag |
| is_active | Boolean | Active status |
| created_at | DateTime | Creation timestamp |

### invoices
Student invoices.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| invoice_number | String | Unique invoice number |
| student_id | Integer | FK to students |
| category | Enum | Payment category |
| term | String | Academic term |
| amount | Float | Invoice amount |
| amount_paid | Float | Amount paid so far |
| status | Enum | pending, partial, paid, overdue, cancelled |
| due_date | DateTime | Payment due date |
| description | String | Invoice description |
| created_by | Integer | FK to users |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

### payments
Payment records.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| receipt_number | String | Unique receipt number |
| invoice_id | Integer | FK to invoices |
| student_id | Integer | FK to students |
| amount | Float | Payment amount |
| method | Enum | cash, bank, mtn_momo, airtel_money, wallet |
| reference | String | Transaction reference |
| notes | String | Payment notes |
| received_by | Integer | FK to users |
| received_at | DateTime | Payment timestamp |
| metadata | JSON | Additional payment details |

### wallets
Student prepaid wallets.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| student_id | Integer | FK to students (unique) |
| balance | Float | Current balance |
| last_top_up | DateTime | Last top-up timestamp |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

### service_items
Service catalog for payments.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| name | String | Service name |
| category | Enum | Payment category |
| unit_price | Float | Price per unit |
| description | String | Service description |
| is_recurring | Boolean | Recurring service |
| is_active | Boolean | Active status |
| created_at | DateTime | Creation timestamp |

## Inventory Tables

### inventory_items
Inventory item definitions.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| name | String | Item name |
| category | String | food, stationery, equipment |
| unit | String | kg, liters, pieces |
| quantity | Float | Current quantity |
| threshold | Float | Low stock threshold |
| unit_cost | Float | Cost per unit |
| supplier | String | Supplier name |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

### stock_transactions
Stock movement records.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| item_id | Integer | FK to inventory_items |
| type | Enum | stock_in, stock_out, adjustment |
| quantity | Float | Transaction quantity |
| notes | String | Transaction notes |
| user_id | Integer | FK to users |
| timestamp | DateTime | Transaction timestamp |

## Communication Tables

### announcements
School announcements.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| title | String | Announcement title |
| body | String | Announcement content |
| audience | JSON | Target audience (roles, classes, students) |
| channels | JSON | Delivery channels (email, sms, push, portal) |
| priority | String | low, normal, high, urgent |
| is_published | Boolean | Publication status |
| published_at | DateTime | Publication timestamp |
| posted_by | Integer | FK to users |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

## LMS Tables

### assignments
Assignment definitions.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| class_id | Integer | FK to classes |
| subject_id | Integer | FK to subjects |
| title | String | Assignment title |
| instructions | String | Assignment instructions |
| materials | JSON | Attached materials |
| due_date | DateTime | Submission due date |
| max_score | Float | Maximum score |
| created_by | Integer | FK to users |
| created_at | DateTime | Creation timestamp |

### submissions
Student assignment submissions.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| assignment_id | Integer | FK to assignments |
| student_id | Integer | FK to students |
| status | Enum | not_submitted, submitted, late, graded |
| content | String | Submission content |
| attachments | JSON | Attached files |
| score | Float | Score received |
| feedback | String | Teacher feedback |
| submitted_at | DateTime | Submission timestamp |
| graded_at | DateTime | Grading timestamp |

## Transport Tables

### routes
Transport routes.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| name | String | Route name |
| description | String | Route description |
| pickup_points | String | JSON string of locations |
| monthly_fee | Float | Monthly transport fee |
| is_active | Boolean | Active status |
| created_at | DateTime | Creation timestamp |

### buses
School buses.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| plate_number | String | Unique plate number |
| capacity | Integer | Seating capacity |
| route_id | Integer | FK to routes |
| is_active | Boolean | Active status |
| created_at | DateTime | Creation timestamp |

### drivers
Bus drivers.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| name | String | Driver name |
| phone | String | Contact phone |
| license_number | String | Driver's license |
| bus_id | Integer | FK to buses |
| is_active | Boolean | Active status |
| created_at | DateTime | Creation timestamp |

### transport_attendance
Transport boarding records.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| student_id | Integer | FK to students |
| bus_id | Integer | FK to buses |
| date | DateTime | Attendance date |
| boarded | Boolean | Boarded status |
| dropped | Boolean | Dropped status |
| recorded_by | Integer | FK to users |
| created_at | DateTime | Creation timestamp |

## Indexes

Key indexes for performance:
- users: email (unique)
- students: admission_number (unique), class_id
- attendance: student_id, date, class_id
- invoices: invoice_number (unique), student_id, status
- payments: receipt_number (unique), invoice_id
- grades: student_id, assessment_id

## Relationships

- User → Student (1:1)
- User → Guardian (1:1)
- User → Teacher (1:1)
- Student ↔ Guardian (M:N via student_guardians)
- Class → Students (1:M)
- Class → Teacher (M:1)
- Class ↔ Subject (M:N via class_subjects)
- Teacher ↔ Subject (M:N via teacher_subjects)
- Student → Attendance (1:M)
- Student → Grade (1:M)
- Assessment → Grade (1:M)
- Student → Invoice (1:M)
- Invoice → Payment (1:M)
- Student → Wallet (1:1)

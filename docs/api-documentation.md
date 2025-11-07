# API Documentation

## Base URL
- Development: `http://localhost:8000`
- Production: `https://api.faithschool.rw`

## Authentication

All authenticated endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <access_token>
```

### POST /api/auth/login
Login with email and password.

**Request Body:**
```json
{
  "username": "admin@faithschool.rw",
  "password": "Admin@2024"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "admin@faithschool.rw",
    "full_name": "System Admin",
    "role": "admin"
  }
}
```

### GET /api/auth/me
Get current user information.

**Response:**
```json
{
  "id": 1,
  "email": "admin@faithschool.rw",
  "full_name": "System Admin",
  "role": "admin",
  "phone": "+250788000001"
}
```

## Students

### GET /api/students/
List all students with optional filters.

**Query Parameters:**
- `skip` (int): Pagination offset (default: 0)
- `limit` (int): Number of records (default: 100)
- `class_id` (int): Filter by class

**Response:**
```json
[
  {
    "id": 1,
    "admission_number": "FBS20240001",
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "2015-03-15",
    "gender": "Male",
    "class_id": 1,
    "enrollment_status": "active"
  }
]
```

### GET /api/students/{student_id}
Get student details by ID.

## Classes

### GET /api/classes/
List all classes.

**Response:**
```json
[
  {
    "id": 1,
    "name": "P1 A",
    "grade_level": "P1",
    "academic_year": "2024",
    "capacity": 40,
    "room_number": "R101"
  }
]
```

## Attendance

### GET /api/attendance/
Get attendance records.

**Query Parameters:**
- `class_id` (int, required): Class ID
- `date` (date, required): Date in YYYY-MM-DD format

**Response:**
```json
[
  {
    "id": 1,
    "student_id": 1,
    "class_id": 1,
    "date": "2024-01-15",
    "status": "present"
  }
]
```

## Fees & Payments

### GET /api/fees/invoices
List invoices with optional filters.

**Query Parameters:**
- `student_id` (int): Filter by student

**Response:**
```json
[
  {
    "id": 1,
    "invoice_number": "INV-2024-00001",
    "student_id": 1,
    "category": "tuition",
    "amount": 150000,
    "amount_paid": 0,
    "status": "pending",
    "due_date": "2024-02-15T00:00:00Z"
  }
]
```

## Error Responses

All endpoints may return the following error responses:

**401 Unauthorized**
```json
{
  "detail": "Invalid token"
}
```

**403 Forbidden**
```json
{
  "detail": "Insufficient permissions"
}
```

**404 Not Found**
```json
{
  "detail": "Resource not found"
}
```

**422 Validation Error**
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## Rate Limiting

API requests are rate-limited to:
- 100 requests per minute for authenticated users
- 20 requests per minute for unauthenticated users

## Interactive Documentation

Visit `/docs` for interactive Swagger UI documentation.
Visit `/redoc` for ReDoc documentation.

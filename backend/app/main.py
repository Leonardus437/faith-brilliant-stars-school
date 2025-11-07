from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .core.config import settings
from .core.database import engine, Base
import os

# Import routers first
try:
    from .api import (
        auth, students, classes, attendance, assessments, fees, inventory, 
        announcements, assignments, transport, analytics, parent, admin, 
        admin_students, admin_teachers, head_teacher, accountant, 
        teacher_enhanced, parent_enhanced
    )
except ImportError as e:
    print(f"Warning: Could not import all routers: {e}")

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Faith Brilliant Stars School API",
    description="School Management System API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS - Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://127.0.0.1:5174", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Create upload directory
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# Mount static files
if os.path.exists(settings.UPLOAD_DIR):
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "environment": settings.ENVIRONMENT}

# Include routers
try:
    app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
    app.include_router(students.router, prefix="/api/students", tags=["Students"])
    app.include_router(classes.router, prefix="/api/classes", tags=["Classes"])
    app.include_router(attendance.router, prefix="/api/attendance", tags=["Attendance"])
    app.include_router(assessments.router, prefix="/api/assessments", tags=["Assessments"])
    app.include_router(fees.router, prefix="/api/fees", tags=["Fees & Payments"])
    app.include_router(inventory.router, prefix="/api/inventory", tags=["Inventory"])
    app.include_router(announcements.router, prefix="/api/announcements", tags=["Announcements"])
    app.include_router(assignments.router, prefix="/api/assignments", tags=["Assignments"])
    app.include_router(transport.router, prefix="/api/transport", tags=["Transport"])
    app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
    app.include_router(parent.router, prefix="/api/parent", tags=["Parent Portal"])
    app.include_router(admin.router, prefix="/api", tags=["Admin"])
    app.include_router(admin_students.router, prefix="/api", tags=["Admin Students"])
    app.include_router(admin_teachers.router, prefix="/api", tags=["Admin Teachers"])
    
    # New enhanced role-specific routers
    app.include_router(head_teacher.router, prefix="/api", tags=["Head Teacher"])
    app.include_router(accountant.router, prefix="/api", tags=["Accountant"])
    app.include_router(teacher_enhanced.router, prefix="/api", tags=["Teacher Enhanced"])
    app.include_router(parent_enhanced.router, prefix="/api", tags=["Parent Enhanced"])
except Exception as e:
    print(f"Warning: Could not include all routers: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

# Project Structure

```
Faith Brilliant Stars School/
│
├── 📁 backend/                          # FastAPI Backend
│   ├── 📁 alembic/                      # Database migrations
│   │   └── versions/                    # Migration files
│   ├── 📁 app/
│   │   ├── 📁 api/                      # API Routes
│   │   │   ├── auth.py                  # Authentication endpoints
│   │   │   ├── students.py              # Student management
│   │   │   ├── classes.py               # Class management
│   │   │   ├── attendance.py            # Attendance tracking
│   │   │   ├── assessments.py           # Assessments & grades
│   │   │   ├── fees.py                  # Fees & payments
│   │   │   ├── inventory.py             # Inventory management
│   │   │   ├── announcements.py         # Announcements
│   │   │   ├── assignments.py           # LMS assignments
│   │   │   ├── transport.py             # Transport management
│   │   │   └── analytics.py             # Analytics & reports
│   │   ├── 📁 core/                     # Core functionality
│   │   │   ├── config.py                # Configuration management
│   │   │   ├── database.py              # Database connection
│   │   │   └── security.py              # Auth & security
│   │   ├── 📁 models/                   # SQLAlchemy models
│   │   │   ├── user.py                  # User model
│   │   │   ├── student.py               # Student model
│   │   │   ├── guardian.py              # Guardian model
│   │   │   ├── teacher.py               # Teacher model
│   │   │   ├── class_model.py           # Class & Subject models
│   │   │   ├── attendance.py            # Attendance model
│   │   │   ├── assessment.py            # Assessment & Grade models
│   │   │   ├── fee.py                   # Fee & Payment models
│   │   │   ├── inventory.py             # Inventory models
│   │   │   ├── announcement.py          # Announcement model
│   │   │   ├── assignment.py            # Assignment models
│   │   │   └── transport.py             # Transport models
│   │   ├── 📁 schemas/                  # Pydantic schemas
│   │   ├── 📁 services/                 # Business logic
│   │   └── main.py                      # FastAPI application
│   ├── 📁 tests/                        # Backend tests
│   │   └── test_auth.py                 # Authentication tests
│   ├── .env.example                     # Environment template
│   ├── alembic.ini                      # Alembic configuration
│   ├── Dockerfile                       # Backend Docker image
│   ├── pytest.ini                       # Pytest configuration
│   ├── requirements.txt                 # Python dependencies
│   └── seed.py                          # Database seeding script
│
├── 📁 frontend/                         # SvelteKit Frontend
│   ├── 📁 src/
│   │   ├── 📁 lib/
│   │   │   ├── 📁 stores/               # Svelte stores
│   │   │   │   └── auth.js              # Auth state management
│   │   │   └── 📁 utils/                # Utilities
│   │   │       ├── api.js               # API client
│   │   │       └── db.js                # IndexedDB (offline)
│   │   ├── 📁 routes/                   # SvelteKit pages
│   │   │   ├── +layout.svelte           # Main layout
│   │   │   ├── +page.svelte             # Landing page
│   │   │   ├── 📁 login/
│   │   │   │   └── +page.svelte         # Login page
│   │   │   ├── 📁 dashboard/
│   │   │   │   └── +page.svelte         # Dashboard
│   │   │   ├── 📁 students/
│   │   │   │   └── +page.svelte         # Students list
│   │   │   ├── 📁 classes/
│   │   │   │   └── +page.svelte         # Classes list
│   │   │   ├── 📁 attendance/
│   │   │   │   └── +page.svelte         # Attendance tracking
│   │   │   └── 📁 fees/
│   │   │       └── +page.svelte         # Fees & payments
│   │   ├── app.css                      # Global styles
│   │   └── app.html                     # HTML template
│   ├── 📁 static/                       # Static assets
│   │   └── service-worker.js            # Offline support
│   ├── .env.example                     # Environment template
│   ├── Dockerfile                       # Frontend Docker image
│   ├── package.json                     # Node dependencies
│   ├── postcss.config.js                # PostCSS config
│   ├── svelte.config.js                 # SvelteKit config
│   ├── tailwind.config.js               # Tailwind CSS config
│   └── vite.config.js                   # Vite config
│
├── 📁 docs/                             # Documentation
│   ├── api-documentation.md             # API reference
│   ├── database-schema.md               # Database structure
│   ├── deployment.md                    # Deployment guide
│   ├── features.md                      # Features list
│   └── user-guide.md                    # User manual
│
├── 📁 .github/                          # GitHub configuration
│   └── 📁 workflows/
│       └── ci.yml                       # CI/CD pipeline
│
├── .gitignore                           # Git ignore rules
├── docker-compose.yml                   # Docker orchestration
├── PROJECT_STRUCTURE.md                 # This file
├── PROJECT_SUMMARY.md                   # Project overview
├── README.md                            # Main documentation
├── SETUP_CHECKLIST.md                   # Setup guide
└── start.bat                            # Quick start script (Windows)
```

## Key Directories Explained

### Backend Structure

**`app/api/`** - API route handlers
- Each file contains endpoints for a specific module
- Uses FastAPI's APIRouter for modular routing
- Includes request validation and response models

**`app/core/`** - Core application logic
- `config.py`: Environment variables and settings
- `database.py`: Database connection and session management
- `security.py`: Authentication, authorization, JWT handling

**`app/models/`** - Database models
- SQLAlchemy ORM models
- Defines database schema
- Includes relationships and constraints

**`app/schemas/`** - Pydantic schemas
- Request/response validation
- Data serialization
- Type checking

**`app/services/`** - Business logic
- Reusable business logic functions
- Separates concerns from API routes
- Database operations and complex logic

### Frontend Structure

**`src/lib/stores/`** - State management
- Svelte stores for global state
- Auth state, user info, etc.

**`src/lib/utils/`** - Utility functions
- API client with interceptors
- IndexedDB for offline storage
- Helper functions

**`src/routes/`** - Pages and routing
- File-based routing (SvelteKit)
- Each folder = route
- `+page.svelte` = page component
- `+layout.svelte` = shared layout

**`static/`** - Static assets
- Images, fonts, icons
- Service worker for offline support
- Favicon and manifest

### Documentation Structure

**`docs/`** - Comprehensive documentation
- API documentation with examples
- Database schema with relationships
- Deployment guides for production
- Feature documentation
- User guides for all roles

## File Naming Conventions

### Backend (Python)
- `snake_case` for files and functions
- `PascalCase` for classes
- `UPPER_CASE` for constants

### Frontend (JavaScript/Svelte)
- `kebab-case` for files
- `camelCase` for variables and functions
- `PascalCase` for components

## Configuration Files

| File | Purpose |
|------|---------|
| `.env` | Environment variables (not in git) |
| `.env.example` | Environment template |
| `alembic.ini` | Database migration config |
| `docker-compose.yml` | Multi-container Docker setup |
| `pytest.ini` | Python testing config |
| `package.json` | Node.js dependencies |
| `tailwind.config.js` | Tailwind CSS customization |
| `vite.config.js` | Vite build configuration |
| `.gitignore` | Git ignore patterns |

## Module Organization

### Backend Modules
1. **Authentication** (`api/auth.py`)
2. **Students** (`api/students.py`, `models/student.py`)
3. **Classes** (`api/classes.py`, `models/class_model.py`)
4. **Attendance** (`api/attendance.py`, `models/attendance.py`)
5. **Assessments** (`api/assessments.py`, `models/assessment.py`)
6. **Fees** (`api/fees.py`, `models/fee.py`)
7. **Inventory** (`api/inventory.py`, `models/inventory.py`)
8. **Announcements** (`api/announcements.py`, `models/announcement.py`)
9. **Assignments** (`api/assignments.py`, `models/assignment.py`)
10. **Transport** (`api/transport.py`, `models/transport.py`)
11. **Analytics** (`api/analytics.py`)

### Frontend Pages
1. **Landing** (`routes/+page.svelte`)
2. **Login** (`routes/login/+page.svelte`)
3. **Dashboard** (`routes/dashboard/+page.svelte`)
4. **Students** (`routes/students/+page.svelte`)
5. **Classes** (`routes/classes/+page.svelte`)
6. **Attendance** (`routes/attendance/+page.svelte`)
7. **Fees** (`routes/fees/+page.svelte`)

## Data Flow

```
User Request
    ↓
Frontend (SvelteKit)
    ↓
API Client (axios)
    ↓
Backend API (FastAPI)
    ↓
Business Logic (services)
    ↓
Database (PostgreSQL via SQLAlchemy)
    ↓
Response
    ↓
Frontend Update
    ↓
User Interface
```

## Offline Data Flow

```
User Action (Offline)
    ↓
IndexedDB (Local Storage)
    ↓
Sync Queue
    ↓
[Internet Connection Restored]
    ↓
Automatic Sync
    ↓
Backend API
    ↓
Database Update
    ↓
Confirmation to User
```

## Development Workflow

1. **Backend Development**
   - Create/modify models in `app/models/`
   - Generate migration: `alembic revision --autogenerate -m "description"`
   - Apply migration: `alembic upgrade head`
   - Create API endpoints in `app/api/`
   - Write tests in `tests/`

2. **Frontend Development**
   - Create pages in `src/routes/`
   - Add components in `src/lib/`
   - Update stores for state management
   - Style with Tailwind CSS classes

3. **Testing**
   - Backend: `pytest`
   - Frontend: `npm run check`
   - Integration: Manual testing or E2E tests

4. **Deployment**
   - Push to GitHub
   - CI/CD runs automatically
   - Deploy backend to Render
   - Deploy frontend to Cloudflare Pages

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend Framework | SvelteKit | UI and routing |
| Styling | Tailwind CSS | Responsive design |
| State Management | Svelte Stores | Global state |
| Offline Storage | IndexedDB (Dexie) | Local data |
| Backend Framework | FastAPI | REST API |
| Database | PostgreSQL | Data persistence |
| ORM | SQLAlchemy | Database abstraction |
| Migrations | Alembic | Schema versioning |
| Authentication | JWT | Secure auth |
| Containerization | Docker | Deployment |
| CI/CD | GitHub Actions | Automation |

---

This structure provides:
- ✅ Clear separation of concerns
- ✅ Modular and maintainable code
- ✅ Easy to navigate and understand
- ✅ Scalable architecture
- ✅ Production-ready organization

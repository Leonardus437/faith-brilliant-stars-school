# Setup Checklist

## Prerequisites Installation

### Required Software
- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed
- [ ] PostgreSQL 15+ installed (or Docker)
- [ ] Git installed
- [ ] Code editor (VS Code recommended)

### Optional but Recommended
- [ ] Docker Desktop installed
- [ ] Postman or similar API testing tool

## Initial Setup

### 1. Database Setup

**Option A: Docker (Recommended)**
```bash
docker-compose up -d db
```

**Option B: Local PostgreSQL**
```bash
# Create database
psql -U postgres
CREATE DATABASE faithschool_db;
CREATE USER faithschool WITH PASSWORD 'faithschool_dev_2024';
GRANT ALL PRIVILEGES ON DATABASE faithschool_db TO faithschool;
\q
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Edit .env with your settings
# Minimum required:
# - DATABASE_URL
# - SECRET_KEY (generate a strong one)

# Run migrations
alembic upgrade head

# Seed database with demo data
python seed.py

# Start backend server
uvicorn app.main:app --reload
```

**Verify Backend:**
- [ ] Backend running at http://localhost:8000
- [ ] API docs accessible at http://localhost:8000/docs
- [ ] Health check returns {"status": "healthy"}

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Start development server
npm run dev
```

**Verify Frontend:**
- [ ] Frontend running at http://localhost:5173
- [ ] Landing page loads correctly
- [ ] Can navigate to login page

### 4. Test Login

- [ ] Navigate to http://localhost:5173/login
- [ ] Login with: admin@faithschool.rw / Admin@2024
- [ ] Dashboard loads successfully
- [ ] Navigation menu appears
- [ ] Can access different pages

## Feature Testing

### Authentication
- [ ] Login works with demo credentials
- [ ] Invalid credentials show error
- [ ] Logout works correctly
- [ ] Token persists on page refresh

### Students Module
- [ ] Can view students list
- [ ] Students data loads from API
- [ ] Table displays correctly
- [ ] Pagination works (if implemented)

### Classes Module
- [ ] Can view classes list
- [ ] Classes display in grid
- [ ] Class details show correctly

### Attendance Module
- [ ] Can select class
- [ ] Can select date
- [ ] Roll call interface loads
- [ ] Can mark attendance

### Fees Module
- [ ] Can view invoices
- [ ] Invoice data loads correctly
- [ ] Currency formatting works (RWF)
- [ ] Status badges display correctly

## API Testing

### Using API Docs (http://localhost:8000/docs)

1. **Test Authentication**
   - [ ] POST /api/auth/login returns token
   - [ ] GET /api/auth/me returns user info

2. **Test Students API**
   - [ ] GET /api/students/ returns student list
   - [ ] GET /api/students/{id} returns student details

3. **Test Classes API**
   - [ ] GET /api/classes/ returns classes list

4. **Test Fees API**
   - [ ] GET /api/fees/invoices returns invoices

## Database Verification

```bash
# Connect to database
psql -U faithschool -d faithschool_db

# Check tables exist
\dt

# Verify demo data
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM students;
SELECT COUNT(*) FROM classes;
SELECT COUNT(*) FROM invoices;

# Should see:
# - 5+ users
# - 60 students
# - 6 classes
# - 20 invoices
```

## Docker Setup (Alternative)

```bash
# Build and start all services
docker-compose up --build

# Verify containers running
docker-compose ps

# Check logs
docker-compose logs backend
docker-compose logs frontend

# Stop services
docker-compose down
```

**Verify Docker Setup:**
- [ ] All containers running
- [ ] Backend accessible at http://localhost:8000
- [ ] Frontend accessible at http://localhost:5173
- [ ] Database container healthy

## Mobile Testing

### Responsive Design
- [ ] Open http://localhost:5173 on mobile device
- [ ] Or use browser DevTools mobile emulation
- [ ] Test on various screen sizes:
  - [ ] 320px (small phone)
  - [ ] 375px (iPhone)
  - [ ] 768px (tablet)
  - [ ] 1024px (desktop)

### Touch Interactions
- [ ] Buttons are easily tappable
- [ ] Forms work on mobile
- [ ] Navigation menu works
- [ ] No horizontal scrolling

## Offline Testing

1. **Enable Offline Mode**
   - [ ] Open DevTools → Network tab
   - [ ] Set throttling to "Offline"

2. **Test Offline Features**
   - [ ] Previously loaded pages still accessible
   - [ ] Service Worker caches assets
   - [ ] Appropriate offline messages shown

## Performance Testing

### Lighthouse Audit
1. Open Chrome DevTools
2. Go to Lighthouse tab
3. Run audit for:
   - [ ] Performance ≥ 90
   - [ ] Accessibility ≥ 90
   - [ ] Best Practices ≥ 90
   - [ ] SEO ≥ 90

## Security Checklist

- [ ] .env files not committed to git
- [ ] Strong SECRET_KEY in production
- [ ] Database credentials secure
- [ ] CORS configured correctly
- [ ] API endpoints require authentication
- [ ] Passwords are hashed (bcrypt)

## Common Issues & Solutions

### Backend won't start
- Check DATABASE_URL is correct
- Ensure PostgreSQL is running
- Verify all dependencies installed
- Check Python version (3.11+)

### Frontend won't start
- Delete node_modules and reinstall
- Check Node version (18+)
- Verify .env file exists
- Clear npm cache: `npm cache clean --force`

### Database connection error
- Check PostgreSQL is running
- Verify database exists
- Check credentials in .env
- Test connection: `psql -U faithschool -d faithschool_db`

### API returns 401 Unauthorized
- Check token is valid
- Re-login to get fresh token
- Verify Authorization header format

### Seed script fails
- Drop and recreate database
- Run migrations: `alembic upgrade head`
- Check for existing data conflicts

## Production Deployment Checklist

See `docs/deployment.md` for detailed guide.

### Pre-Deployment
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Database backup created
- [ ] SSL certificates ready
- [ ] Domain configured

### Deployment
- [ ] Backend deployed to Render
- [ ] Frontend deployed to Cloudflare Pages
- [ ] Database on Supabase
- [ ] Environment variables set
- [ ] Migrations run on production DB

### Post-Deployment
- [ ] Health check passes
- [ ] Can login to production
- [ ] All features working
- [ ] Mobile testing on real devices
- [ ] Performance monitoring active
- [ ] Error tracking (Sentry) configured

## Support

If you encounter issues:

1. Check this checklist thoroughly
2. Review error messages carefully
3. Check logs:
   - Backend: Terminal output
   - Frontend: Browser console
   - Database: PostgreSQL logs

4. Consult documentation:
   - README.md
   - docs/user-guide.md
   - docs/api-documentation.md

5. Common commands:
```bash
# Restart backend
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload

# Restart frontend
cd frontend
npm run dev

# Reset database
cd backend
alembic downgrade base
alembic upgrade head
python seed.py

# Docker restart
docker-compose down
docker-compose up --build
```

## Success Criteria

✅ **Setup is complete when:**
- Backend API is running and accessible
- Frontend is running and responsive
- Can login with demo credentials
- Dashboard loads with data
- All main pages are accessible
- Database has seed data
- No console errors
- Mobile view works correctly

---

**Congratulations! Your Faith Brilliant Stars School Management System is ready! 🎉**

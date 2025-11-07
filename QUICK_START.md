# 🚀 Quick Start - One Click Launch

## Instant Launch (Recommended)

Simply double-click: **`LAUNCH.bat`**

That's it! The script will:
1. ✅ Check for Docker or set up manually
2. ✅ Install all dependencies
3. ✅ Create database and seed data
4. ✅ Start backend and frontend servers
5. ✅ Open your browser automatically

## What You'll See

After 10-15 seconds, your browser will open to:
**http://localhost:5173**

## Login Credentials

| Role | Email | Password |
|------|-------|----------|
| **Admin** | admin@faithschool.rw | Admin@2024 |
| Teacher | teacher@faithschool.rw | Teacher@2024 |
| Accountant | accounts@faithschool.rw | Accounts@2024 |
| Parent | parent@faithschool.rw | Parent@2024 |

## Access Points

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Troubleshooting

### If browser doesn't open automatically:
Manually navigate to: http://localhost:5173

### If you see errors:
1. Make sure Python 3.11+ is installed
2. Make sure Node.js 18+ is installed
3. Close any programs using ports 5173 or 8000
4. Run `LAUNCH.bat` again

### To stop the servers:
- Press Ctrl+C in the terminal windows
- Or close the terminal windows

## Manual Alternative

If automated setup doesn't work:

```bash
# Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
python seed.py
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

Then open: http://localhost:5173

---

**Enjoy your Faith Brilliant Stars School Management System! 🎉**

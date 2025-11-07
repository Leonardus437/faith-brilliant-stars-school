# Faith Brilliant Stars School - Management System

A production-ready, responsive school management platform optimized for Rwanda's primary schools.

## 🚀 Live Demo
- **Frontend**: [Deployed on Cloudflare Pages](https://faith-brilliant-stars-school.pages.dev)
- **Backend**: [Deployed on Render](https://faith-brilliant-stars-school-backend.onrender.com)

## 🚀 Quick Start

### Local Development
1. **Backend Setup**:
   ```bash
   cd backend
   pip install -r requirements.txt
   python full_seed.py
   uvicorn app.main:app --reload --port 8001
   ```

2. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

### Production Deployment
- **Frontend**: Auto-deploys to Cloudflare Pages on push to `main`
- **Backend**: Auto-deploys to Render on push to `main`

## 👥 User Roles & Credentials

### 1. HEAD TEACHER (Administrator)
- **Email:** head@faithschool.rw
- **Password:** Head2024

### 2. TEACHER
- **Email:** teacher@faithschool.rw
- **Password:** Teacher2024

### 3. ACCOUNTANT
- **Email:** accounts@faithschool.rw
- **Password:** Accounts2024

### 4. PARENT
- **Email:** parent@faithschool.rw
- **Password:** Parent2024

## 🛠 Tech Stack
- **Frontend**: SvelteKit + Tailwind CSS
- **Backend**: FastAPI (Python)
- **Database**: SQLite
- **Deployment**: Cloudflare Pages + Render

## 📊 Features
- Modern responsive UI with glass morphism design
- Role-based access control
- Attendance management
- Fee management with mobile money integration
- Financial reporting and analytics
- Parent portal
- Real-time notifications

## 🔧 Environment Variables

### Backend (.env)
```
DATABASE_URL=sqlite:///./faithschool.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (.env)
```
VITE_API_URL=https://faith-brilliant-stars-school-backend.onrender.com
```
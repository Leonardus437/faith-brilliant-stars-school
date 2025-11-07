# Repository Quick Reference

## Overview
- **Project Name**: Faith Brilliant Stars School Management System
- **Domain**: Primary school management platform tailored for Rwanda
- **Tech Stack**:
  - **Frontend**: SvelteKit + Tailwind CSS
  - **Backend**: FastAPI (Python)
  - **Database**: SQLite (with Alembic migrations)
  - **Auth**: JWT-based + RBAC

## Key Entry Points
1. **Startup Scripts**
   - `START.bat`: seeds sample data, launches backend (port 8001) and frontend (port 5174), opens browser
   - `STOP.bat`: stops all running services started by the project scripts
   - Additional helper scripts for various reset/restart flows are in the repository root

2. **Backend** (`backend/`)
   - FastAPI application in `backend/app`
   - Database seeding scripts: `full_seed.py`, `seed.py`, etc.
   - Virtual environment under `backend/venv`
   - Tests in `backend/tests`
   - Configuration: `.env`, `alembic.ini`

3. **Frontend** (`frontend/`)
   - SvelteKit source in `frontend/src`
   - Tailwind configuration via `tailwind.config.js`
   - Environment variables: `.env`

4. **Documentation** (`docs/`)
   - `features.md`: feature breakdown
   - `user-guide.md`: role-based walkthrough
   - `api-documentation.md`: API endpoints
   - `database-schema.md`: ERD and schema notes

## Primary User Roles
- **Head Teacher**: full admin privileges
- **Teacher**: attendance and class management tools
- **Accountant**: payment and financial modules
- **Parent**: child monitoring, payments, communication

Default credentials listed in `README.md` for rapid testing. Ensure passwords are updated in production.

## Common Tasks
1. **Run the full system**
   ```powershell
   .\START.bat
   ```
2. **Stop services**
   ```powershell
   .\STOP.bat
   ```
3. **Backend-only**
   ```powershell
   Set-Location "t:\Faith Brilliant Stars School\backend"
   .\venv\Scripts\activate
   uvicorn app.main:app --reload --port 8001
   ```
4. **Frontend-only**
   ```powershell
   Set-Location "t:\Faith Brilliant Stars School\frontend"
   npm install
   npm run dev -- --port 5174
   ```

## Testing & Quality
- Backend tests: `pytest` within `backend/`
- Frontend: refer to SvelteKit testing strategy if present (not currently included)

## Security & Configuration Notes
- JWT signing keys and secrets in `.env` files; keep them secure
- SQLite database (`faithschool.db`) ships with sample data; reset via `full_seed.py` if needed

## Additional Resources
- `PROJECT_STRUCTURE.md` and `QUICK_START.md` for deeper walkthroughs
- Numerous helper `.txt` files in the root provide troubleshooting steps (e.g., `BACKEND_IS_WORKING.txt`, `CORS_FIXED.txt`)

Keep this guide updated as the repository evolves to ensure fast onboarding and troubleshooting.
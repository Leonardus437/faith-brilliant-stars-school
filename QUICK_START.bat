@echo off
echo ========================================
echo FAITH BRILLIANT STARS SCHOOL
echo Quick Start (No Database Seeding)
echo ========================================

echo.
echo [1/2] Starting Backend Server...
start "Backend Server" cmd /k "cd /d \"T:\Faith Brilliant Stars School\backend\" && python -m uvicorn app.main:app --reload --port 8001"

timeout /t 3 /nobreak >nul

echo.
echo [2/2] Starting Frontend Server...
start "Frontend Server" cmd /k "cd /d \"T:\Faith Brilliant Stars School\frontend\" && npm run dev"

timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo System Started Successfully!
echo ========================================
echo.
echo Backend:  http://localhost:8001/docs
echo Frontend: http://localhost:5174
echo.
echo Opening browser in 5 seconds...
timeout /t 5 /nobreak >nul

start http://localhost:5174

echo.
echo Press any key to close this window...
pause >nul
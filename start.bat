@echo off
echo ========================================
echo FAITH BRILLIANT STARS SCHOOL
echo Starting System...
echo ========================================

cd /d "T:\Faith Brilliant Stars School\backend"

echo.
echo [1/3] Checking Database...
python enhanced_seed_safe.py
if %errorlevel% neq 0 (
    echo ERROR: Database check failed!
    pause
    exit /b 1
)

echo.
echo [2/3] Starting Backend Server...
start "Backend Server" cmd /k "cd /d \"T:\Faith Brilliant Stars School\backend\" && python -m uvicorn app.main:app --reload --port 8001"

timeout /t 3 /nobreak >nul

echo.
echo [3/3] Starting Frontend Server...
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

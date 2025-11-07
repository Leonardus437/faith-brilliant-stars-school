@echo off
echo ========================================
echo FAITH BRILLIANT STARS SCHOOL
echo FIX AND START
echo ========================================

cd /d "T:\Faith Brilliant Stars School\backend"

echo.
echo [1/4] Stopping any running servers...
taskkill /FI "WINDOWTITLE eq Backend Server*" /T /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Frontend Server*" /T /F >nul 2>&1
timeout /t 2 /nobreak >nul

echo.
echo [2/4] Re-seeding Database...
python seed_direct.py
if %errorlevel% neq 0 (
    echo ERROR: Database seeding failed!
    pause
    exit /b 1
)

echo.
echo [3/4] Fixing Passwords...
python fix_passwords.py
if %errorlevel% neq 0 (
    echo ERROR: Password fix failed!
    pause
    exit /b 1
)

echo.
echo [4/4] Starting Servers...
start "Backend Server" cmd /k "cd /d T:\Faith Brilliant Stars School\backend && python -m uvicorn app.main:app --reload --port 8001"
timeout /t 3 /nobreak >nul

start "Frontend Server" cmd /k "cd /d T:\Faith Brilliant Stars School\frontend && npm run dev"
timeout /t 5 /nobreak >nul

echo.
echo ========================================
echo System Fixed and Started!
echo ========================================
echo.
echo Backend:  http://localhost:8001/docs
echo Frontend: http://localhost:5174
echo.
echo Opening browser...
timeout /t 3 /nobreak >nul
start http://localhost:5174

echo.
echo ========================================
echo LOGIN CREDENTIALS:
echo ========================================
echo.
echo HEAD TEACHER:
echo   Email: head@faithschool.rw
echo   Password: Head2024
echo.
echo TEACHER:
echo   Email: teacher@faithschool.rw
echo   Password: Teacher2024
echo.
echo ACCOUNTANT:
echo   Email: accounts@faithschool.rw
echo   Password: Accounts2024
echo.
echo PARENT:
echo   Email: parent@faithschool.rw
echo   Password: Parent2024
echo.
echo ========================================
echo TIP: Use the quick login buttons!
echo ========================================
echo.
pause

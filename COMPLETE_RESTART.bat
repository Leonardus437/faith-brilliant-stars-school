@echo off
echo ========================================
echo COMPLETE SYSTEM RESTART
echo ========================================

echo.
echo [1/5] Stopping all servers...
taskkill /FI "WINDOWTITLE eq Backend Server*" /T /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Frontend Server*" /T /F >nul 2>&1
taskkill /F /IM node.exe >nul 2>&1
taskkill /F /IM python.exe >nul 2>&1
timeout /t 3 /nobreak >nul

echo.
echo [2/5] Reseeding database...
cd /d "T:\Faith Brilliant Stars School\backend"
python seed_direct.py
python fix_passwords.py

echo.
echo [3/5] Starting Backend...
start "Backend Server" cmd /k "cd /d T:\Faith Brilliant Stars School\backend && python -m uvicorn app.main:app --reload --port 8001"
timeout /t 5 /nobreak >nul

echo.
echo [4/5] Starting Frontend...
start "Frontend Server" cmd /k "cd /d T:\Faith Brilliant Stars School\frontend && npm run dev"
timeout /t 8 /nobreak >nul

echo.
echo [5/5] Opening browser...
start http://localhost:5174

echo.
echo ========================================
echo SYSTEM READY!
echo ========================================
echo.
echo Backend:  http://localhost:8001
echo Frontend: http://localhost:5174
echo.
echo CREDENTIALS:
echo head@faithschool.rw / Head2024
echo teacher@faithschool.rw / Teacher2024
echo accounts@faithschool.rw / Accounts2024
echo parent@faithschool.rw / Parent2024
echo.
echo Click any role card, then click Sign In!
echo.
pause

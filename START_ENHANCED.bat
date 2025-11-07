@echo off
echo ========================================
echo Faith Brilliant Stars School
echo ENHANCED SYSTEM STARTUP
echo ========================================
echo.

echo [1/5] Running database seed...
cd backend
python full_seed.py
if errorlevel 1 (
    echo ERROR: Full seed failed!
    pause
    exit /b 1
)
python enhanced_seed.py
if errorlevel 1 (
    echo ERROR: Enhanced seed failed!
    pause
    exit /b 1
)
echo.

echo [2/5] Starting backend server...
start "Backend Server" cmd /k "python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001"
timeout /t 5 /nobreak >nul
echo.

echo [3/5] Starting frontend server...
cd ..\frontend
start "Frontend Server" cmd /k "npm run dev -- --port 5174"
timeout /t 5 /nobreak >nul
echo.

echo [4/5] Waiting for servers to initialize...
timeout /t 10 /nobreak >nul
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
echo API Docs: http://localhost:8001/docs
echo.
echo NEW FEATURES AVAILABLE:
echo - Head Teacher: Complete school management
echo - Accountant: Advanced payment processing
echo - Teacher: Enhanced attendance with offline sync
echo - Parent: Child monitoring and communication
echo.
echo Press any key to view system status...
pause >nul

cd ..
call CHECK_SYSTEM.bat

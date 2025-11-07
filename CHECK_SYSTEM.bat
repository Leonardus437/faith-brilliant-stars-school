@echo off
echo ========================================
echo SYSTEM CHECK
echo ========================================

echo.
echo [1] Checking Database...
cd /d "T:\Faith Brilliant Stars School\backend"
python -c "import sqlite3; conn = sqlite3.connect('faithschool.db'); cursor = conn.cursor(); users = cursor.execute('SELECT email, role FROM users').fetchall(); print('Users found:'); [print(f'  - {email} ({role})') for email, role in users]; conn.close()"

echo.
echo [2] Testing Password Verification...
python -c "import sqlite3; import bcrypt; conn = sqlite3.connect('faithschool.db'); cursor = conn.cursor(); result = cursor.execute('SELECT hashed_password FROM users WHERE email = ?', ('head@faithschool.rw',)).fetchone(); test = bcrypt.checkpw(b'Head2024', result[0].encode()); print(f'Password test: {'PASS' if test else 'FAIL'}'); conn.close()"

echo.
echo [3] Checking if Backend is Running...
curl -s http://localhost:8001/health >nul 2>&1
if %errorlevel% equ 0 (
    echo Backend: RUNNING on port 8001
) else (
    echo Backend: NOT RUNNING
    echo Please start backend with START.bat
)

echo.
echo [4] Checking if Frontend is Running...
curl -s http://localhost:5174 >nul 2>&1
if %errorlevel% equ 0 (
    echo Frontend: RUNNING on port 5174
) else (
    echo Frontend: NOT RUNNING
    echo Please start frontend with START.bat
)

echo.
echo ========================================
echo Check complete!
echo ========================================
pause

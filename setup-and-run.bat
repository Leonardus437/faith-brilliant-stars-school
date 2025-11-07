@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Faith Brilliant Stars School
echo Automated Setup and Launch
echo ========================================
echo.

cd /d "%~dp0"

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% equ 0 (
    echo Docker detected. Using Docker setup...
    echo.
    
    REM Create .env files if they don't exist
    if not exist "backend\.env" (
        echo Creating backend .env...
        copy "backend\.env.example" "backend\.env" >nul
    )
    
    if not exist "frontend\.env" (
        echo Creating frontend .env...
        copy "frontend\.env.example" "frontend\.env" >nul
    )
    
    echo Starting services with Docker...
    docker-compose up -d --build
    
    echo.
    echo Waiting for services to start...
    timeout /t 15 /nobreak >nul
    
    echo.
    echo Running database migrations...
    docker-compose exec -T backend alembic upgrade head
    
    echo.
    echo Seeding database...
    docker-compose exec -T backend python seed.py
    
    echo.
    echo ========================================
    echo Setup Complete!
    echo ========================================
    echo Opening browser...
    timeout /t 3 /nobreak >nul
    start http://localhost:5173
    
    echo.
    echo Services running:
    echo Frontend: http://localhost:5173
    echo Backend API: http://localhost:8000
    echo API Docs: http://localhost:8000/docs
    echo.
    echo Press Ctrl+C to stop services
    docker-compose logs -f
    
) else (
    echo Docker not running. Using manual setup...
    echo.
    
    REM Backend Setup
    echo Setting up Backend...
    cd backend
    
    if not exist "venv" (
        echo Creating Python virtual environment...
        python -m venv venv
    )
    
    call venv\Scripts\activate
    
    echo Installing Python dependencies...
    pip install -q -r requirements.txt
    
    if not exist ".env" (
        echo Creating backend .env...
        copy .env.example .env >nul
        
        REM Update .env with SQLite for simplicity
        echo DATABASE_URL=sqlite:///./faithschool.db > .env.temp
        echo SECRET_KEY=dev-secret-key-change-in-production-min-32-chars >> .env.temp
        echo ALGORITHM=HS256 >> .env.temp
        echo ACCESS_TOKEN_EXPIRE_MINUTES=30 >> .env.temp
        echo ENVIRONMENT=development >> .env.temp
        echo DEBUG=True >> .env.temp
        echo ALLOWED_ORIGINS=http://localhost:5173 >> .env.temp
        move /y .env.temp .env >nul
    )
    
    echo Running database migrations...
    alembic upgrade head
    
    echo Seeding database...
    python seed.py
    
    echo Starting Backend Server...
    start "Backend Server" cmd /k "cd /d %CD% && venv\Scripts\activate && uvicorn app.main:app --reload"
    
    cd ..
    
    REM Frontend Setup
    echo.
    echo Setting up Frontend...
    cd frontend
    
    if not exist "node_modules" (
        echo Installing Node dependencies...
        call npm install
    )
    
    if not exist ".env" (
        echo Creating frontend .env...
        echo VITE_API_URL=http://localhost:8000 > .env
    )
    
    echo Starting Frontend Server...
    start "Frontend Server" cmd /k "cd /d %CD% && npm run dev"
    
    cd ..
    
    echo.
    echo Waiting for servers to start...
    timeout /t 10 /nobreak >nul
    
    echo.
    echo ========================================
    echo Setup Complete!
    echo ========================================
    echo Opening browser...
    start http://localhost:5173
    
    echo.
    echo Services running:
    echo Frontend: http://localhost:5173
    echo Backend API: http://localhost:8000
    echo API Docs: http://localhost:8000/docs
    echo.
    echo Demo Login:
    echo Email: admin@faithschool.rw
    echo Password: Admin@2024
    echo ========================================
    echo.
    echo Press any key to stop servers...
    pause >nul
    
    taskkill /FI "WindowTitle eq Backend Server*" /T /F >nul 2>&1
    taskkill /FI "WindowTitle eq Frontend Server*" /T /F >nul 2>&1
)

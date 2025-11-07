@echo off
cd /d "T:\Faith Brilliant Stars School\backend"
echo Starting Backend Server on port 8001...
python -m uvicorn app.main:app --reload --port 8001
pause

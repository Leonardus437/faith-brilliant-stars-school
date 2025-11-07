@echo off
echo ========================================
echo FAITH BRILLIANT STARS SCHOOL
echo Stopping System...
echo ========================================

echo.
echo Stopping Backend Server...
taskkill /FI "WINDOWTITLE eq Backend Server*" /T /F >nul 2>&1

echo Stopping Frontend Server...
taskkill /FI "WINDOWTITLE eq Frontend Server*" /T /F >nul 2>&1

echo.
echo ========================================
echo System Stopped Successfully!
echo ========================================
echo.
pause

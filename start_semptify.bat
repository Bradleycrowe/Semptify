@echo off
title Semptify Production Server
color 0B
cls
echo.
echo ========================================
echo    SEMPTIFY - Tenant Justice Platform
echo ========================================
echo.
echo Starting production server...
echo.

cd /d "C:\Semptify\Semptify"

REM Kill existing processes
echo [1/3] Stopping old instances...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Semptify*" >nul 2>&1
timeout /t 2 /nobreak >nul

REM Start production server
echo [2/3] Starting Waitress server...
start /MIN "" ".venv\Scripts\python.exe" "run_prod.py"
timeout /t 4 /nobreak >nul

REM Open browser
echo [3/3] Opening browser...
start http://localhost:5000/hub

echo.
echo ========================================
echo    SEMPTIFY IS RUNNING!
echo ========================================
echo.
echo    Access at: http://localhost:5000
echo    GUI Hub:   http://localhost:5000/hub
echo.
echo Server running in background.
echo You can close this window.
echo.
timeout /t 5
exit

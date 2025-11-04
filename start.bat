@echo off
REM ============================================================
REM Semptify Production Web Server Launcher (Windows Batch)
REM Simple one-click startup for Windows
REM ============================================================

setlocal enabledelayedexpansion

cls
echo.
echo ============================================================
echo  SEMPTIFY PRODUCTION SERVER
echo ============================================================
echo.

REM Check if FLASK_SECRET is set
if not defined FLASK_SECRET (
    echo WARNING: FLASK_SECRET environment variable not set
    echo.
    echo To set it now, run:
    echo   set FLASK_SECRET=your-secret-key-here
    echo.
    echo Or press Ctrl+C to cancel and set it first.
    echo.
    pause
    
    REM Try to use a temporary secret (NOT FOR PRODUCTION)
    for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c%%a%%b)
    for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)
    set FLASK_SECRET=dev-temp-!mydate!!mytime!
    echo Using temporary dev secret: !FLASK_SECRET!
    echo WARNING: This is NOT secure for production!
    echo.
)

echo Starting server...
echo.

REM Call PowerShell to run the startup script
powershell -NoProfile -ExecutionPolicy Bypass -Command "& '.\Start-Production.ps1'"

REM If PowerShell exits with error, offer troubleshooting
if errorlevel 1 (
    echo.
    echo ERROR: Server failed to start
    echo.
    echo Troubleshooting:
    echo 1. Check Python is installed: python --version
    echo 2. Check FLASK_SECRET is set: echo !FLASK_SECRET!
    echo 3. Review logs/production.log for errors
    echo 4. Run .\Start-Production.ps1 directly for more details
    echo.
    pause
    exit /b 1
)

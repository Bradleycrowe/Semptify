@echo off
REM Semptify Local Server - Windows Startup Script
REM Ensures Ollama is running and starts Semptify

echo ================================================
echo    Semptify Local Server Startup
echo ================================================
echo.

REM Check if Ollama is running
echo [1/3] Checking Ollama AI service...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARN] Ollama not detected, starting...
    start "" "C:\Users\%USERNAME%\AppData\Local\Programs\Ollama\ollama app.exe"
    timeout /t 5 /nobreak >nul
) else (
    echo [OK] Ollama is running
)

REM Activate virtual environment
echo [2/3] Activating Python environment...
cd /d C:\Semptify\Semptify
call .venv\Scripts\activate.bat

REM Start Semptify
echo [3/3] Starting Semptify...
echo.
echo ================================================
echo   Semptify running at: http://localhost:5000
echo   Profiles: http://localhost:5000/profiles
echo   Press Ctrl+C to stop
echo ================================================
echo.

python Semptify.py

pause

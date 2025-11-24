@echo off
REM Semptify Launcher - Batch file wrapper
REM This allows double-clicking to start Semptify

title Semptify - Tenant Rights Protection Platform

cd /d "C:\Semptify\Semptify"
powershell.exe -ExecutionPolicy Bypass -File "C:\Semptify\Semptify\Semptify_Launcher.ps1"
pause

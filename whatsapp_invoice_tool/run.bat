@echo off
REM Batch file to run WhatsApp Invoice Tool on Windows

echo ========================================
echo   WhatsApp Invoice Tool
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

REM Run the application
echo Starting application...
echo.
python app.py

pause

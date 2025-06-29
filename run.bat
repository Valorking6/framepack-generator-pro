@echo off
title Framepack Generator Pro
echo.
echo 🎬 Framepack Generator Pro
echo ========================
echo.
echo Starting application...
echo.

cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found!
    echo Please run install.ps1 first to set up the application.
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if activation was successful
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    echo.
    pause
    exit /b 1
)

echo ✅ Virtual environment activated
echo.

REM Start the application
echo 🚀 Launching Framepack Generator Pro...
echo.
echo The application will be available at:
echo http://127.0.0.1:7861
echo.
echo Press Ctrl+C to stop the application
echo.

python app.py

REM If we get here, the application has stopped
echo.
echo 🛑 Application stopped
echo.
pause
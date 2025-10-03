@echo off
REM Zone-H Mass Mirror Launcher Script
REM For Windows systems

echo 🎯 Zone-H Mass Mirror Tool
echo ==========================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed!
    echo Please install Python 3.6 or higher
    pause
    exit /b 1
)

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip is not installed!
    echo Please install pip
    pause
    exit /b 1
)

REM Check if requirements are installed
echo 📦 Checking dependencies...
if exist "requirements.txt" (
    pip install -r requirements.txt --quiet
    echo ✅ Dependencies installed/updated
) else (
    echo ❌ requirements.txt not found!
    pause
    exit /b 1
)

REM Check if main.py exists
if not exist "main.py" (
    echo ❌ main.py not found!
    pause
    exit /b 1
)

echo.
echo 🚀 Starting Zone-H Mass Mirror Tool...
echo =====================================
echo.

REM Run the application
python main.py

REM Pause to see any error messages
pause
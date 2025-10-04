@echo off
title Zone-H Mobile Mirror Tool
color 0A

echo.
echo  📱 ZONE-H MOBILE MIRROR TOOL
echo  =============================
echo  Mobile Version with Kivy Framework
echo  Author: Hadi Ramdhani
echo.
echo  🚀 Starting mobile application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.7+ first
    pause
    exit /b 1
)

REM Navigate to mobile directory
cd /d "%~dp0"

REM Check if requirements are installed
echo 📦 Checking dependencies...
python -c "import kivy" >nul 2>&1
if errorlevel 1 (
    echo 📥 Installing required dependencies...
    pip install -r requirements_mobile.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Start the mobile application
echo.
echo 🎯 Starting Zone-H Mobile Mirror...
echo.
python run_mobile.py

echo.
echo ✅ Application closed.
echo.
pause
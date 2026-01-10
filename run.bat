@echo off
REM Quick startup script for Windows
REM AI Agent Conversational Application

echo.
echo ================================
echo   AI Agent - Startup Script
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

echo [OK] Python found

REM Check if .env exists
if not exist ".env" (
    echo [WARNING] .env file not found
    echo Please create .env file with your OpenAI API key:
    echo   OPENAI_API_KEY=sk-proj-xxxxx
    echo.
    pause
)

REM Install dependencies if needed
echo [INFO] Checking dependencies...
pip install -q openai python-dotenv
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo [OK] Dependencies ready

REM Launch the application
echo [INFO] Starting AI Agent...
echo.
python main.py

pause

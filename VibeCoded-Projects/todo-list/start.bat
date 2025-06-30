@echo off
REM Startup script for Todo List Application
REM This script sets up and runs the todo app

echo.
echo ========================================
echo    Interactive To-Do List App Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

echo ✅ Python is installed

REM Check if virtual environment exists
if not exist ".venv" (
    echo.
    echo 📦 Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
)

REM Activate virtual environment
echo.
echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies
echo.
echo 📥 Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)
echo ✅ Dependencies installed successfully

REM Initialize database
echo.
echo 🗄️ Initializing database...
python -c "from app import init_db; init_db()"
echo ✅ Database initialized

REM Start the application
echo.
echo 🚀 Starting the Todo List application...
echo.
echo The app will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py

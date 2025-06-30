@echo off
echo 🚗 Starting Automobile Parts Shopping Cart API...
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo ❌ Virtual environment not found!
    echo Please run: python -m venv .venv
    echo Then run: .venv\Scripts\pip install -r requirements.txt
    pause
    exit /b 1
)

REM Test if dependencies are installed
echo Testing dependencies...
".venv\Scripts\python.exe" -c "import fastapi, uvicorn, sqlalchemy; print('✅ All dependencies found')" 2>nul
if errorlevel 1 (
    echo ❌ Dependencies missing! Installing...
    ".venv\Scripts\pip.exe" install -r requirements.txt
)

REM Test if main.py can be imported
echo Testing main application...
".venv\Scripts\python.exe" -c "import main; print('✅ Application loads successfully')" 2>nul
if errorlevel 1 (
    echo ❌ Application has errors! Check the code.
    pause
    exit /b 1
)

echo.
echo ✅ Starting server...
echo.
echo 🌐 The application will be available at:
echo    📱 Frontend:     http://127.0.0.1:8000/frontend/index.html
echo    📚 API Docs:     http://127.0.0.1:8000/docs
echo    🔍 API Root:     http://127.0.0.1:8000/
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server
".venv\Scripts\python.exe" -m uvicorn main:app --reload --host 127.0.0.1 --port 8000

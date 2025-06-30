@echo off
echo Starting Automobile Parts Shopping Cart API...
echo.
echo The API will be available at:
echo   - API: http://localhost:8000
echo   - Documentation: http://localhost:8000/docs
echo   - Alternative docs: http://localhost:8000/redoc
echo.
echo Press Ctrl+C to stop the server
echo.

.venv\Scripts\uvicorn.exe main:app --reload --host 0.0.0.0 --port 8000

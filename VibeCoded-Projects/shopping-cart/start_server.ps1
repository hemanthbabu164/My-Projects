Write-Host "🚗 Starting Automobile Parts Shopping Cart API..." -ForegroundColor Green
Write-Host ""
Write-Host "The API will be available at:"
Write-Host "  - API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "  - Documentation: http://localhost:8000/docs" -ForegroundColor Cyan  
Write-Host "  - Alternative docs: http://localhost:8000/redoc" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

.\.venv\Scripts\uvicorn.exe main:app --reload --host 0.0.0.0 --port 8000

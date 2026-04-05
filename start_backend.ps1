# Script PowerShell pour lancer le backend FastAPI
Write-Host "Starting Human Firewall Backend API..." -ForegroundColor Green
Write-Host "Backend will run on: http://127.0.0.1:8001" -ForegroundColor Cyan
Write-Host "Swagger UI available at: http://127.0.0.1:8001/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press CTRL+C to stop the backend." -ForegroundColor Yellow
Write-Host ""

cd "c:\Users\nourb\OneDrive\Bureau\human-firewall\human-firewall"
python -m uvicorn backend.app.main:app --reload --port 8001

# Script PowerShell pour lancer le frontend Streamlit
Write-Host "Starting Human Firewall Frontend (Streamlit)..." -ForegroundColor Green
Write-Host "Frontend will run on: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "Make sure the backend is running on: http://127.0.0.1:8001" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press CTRL+C to stop the frontend." -ForegroundColor Yellow
Write-Host ""

cd "c:\Users\nourb\OneDrive\Bureau\human-firewall\human-firewall"
streamlit run frontend/app.py

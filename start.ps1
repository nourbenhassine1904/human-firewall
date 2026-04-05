param(
    [string]$Service = "all"
)

function Start-Backend {
    Write-Host "`n╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║  🚀 Starting Backend API (FastAPI)                          ║" -ForegroundColor Cyan
    Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    
    Write-Host "`n📍 Backend URL: " -NoNewline -ForegroundColor Green
    Write-Host "http://127.0.0.1:8001" -ForegroundColor Yellow
    
    Write-Host "📚 Swagger UI: " -NoNewline -ForegroundColor Green
    Write-Host "http://127.0.0.1:8001/docs" -ForegroundColor Yellow
    
    Write-Host "`n⏸️  Press [CTRL+C] to stop the backend" -ForegroundColor Gray
    Write-Host "─" * 60 -ForegroundColor Gray
    
    cd "c:\Users\nourb\OneDrive\Bureau\human-firewall\human-firewall"
    python -m uvicorn backend.app.main:app --reload --port 8001
}

function Start-Frontend {
    Write-Host "`n╔════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
    Write-Host "║  🎨 Starting Frontend UI (Streamlit)                        ║" -ForegroundColor Magenta
    Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Magenta
    
    Write-Host "`n📍 Frontend URL: " -NoNewline -ForegroundColor Green
    Write-Host "http://localhost:8501" -ForegroundColor Yellow
    
    Write-Host "🔗 Backend API: " -NoNewline -ForegroundColor Green
    Write-Host "http://127.0.0.1:8001" -ForegroundColor Yellow
    
    Write-Host "`n⏸️  Press [CTRL+C] to stop the frontend" -ForegroundColor Gray
    Write-Host "─" * 60 -ForegroundColor Gray
    
    cd "c:\Users\nourb\OneDrive\Bureau\human-firewall\human-firewall"
    streamlit run frontend/app.py
}

function Start-Both {
    Write-Host "`n" -ForegroundColor Cyan
    Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║  🔥 Human Firewall - Launching All Services               ║" -ForegroundColor Cyan
    Write-Host "║                                                            ║" -ForegroundColor Cyan
    Write-Host "║  Backend Mode: Étape 2 (QR Support)                      ║" -ForegroundColor Cyan
    Write-Host "║  Frontend Mode: Full UI with QR Analysis                  ║" -ForegroundColor Cyan
    Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    
    # Check if port 8001 is already in use
    $portInUse = (netstat -ano | Select-String ":8001" | Measure-Object).Count -gt 0
    
    if ($portInUse) {
        Write-Host "`n⚠️  Port 8001 is already in use (backend might be running)" -ForegroundColor Yellow
        $continue = Read-Host "Continue anyway? (y/n)"
        if ($continue -ne "y") {
            Write-Host "Cancelled." -ForegroundColor Red
            return
        }
    }
    
    Write-Host "`n[1/2] 🚀 Launching Backend..." -ForegroundColor Cyan
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'c:\Users\nourb\OneDrive\Bureau\human-firewall\human-firewall'; python -m uvicorn backend.app.main:app --reload --port 8001" -WindowStyle Normal
    
    Write-Host "[⏳] Waiting 3 seconds for backend to start..." -ForegroundColor Gray
    Start-Sleep -Seconds 3
    
    Write-Host "[2/2] 🎨 Launching Frontend..." -ForegroundColor Magenta
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'c:\Users\nourb\OneDrive\Bureau\human-firewall\human-firewall'; streamlit run frontend/app.py" -WindowStyle Normal
    
    Write-Host "`n╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║  ✅ Both services started in separate windows              ║" -ForegroundColor Green
    Write-Host "╠════════════════════════════════════════════════════════════╣" -ForegroundColor Green
    Write-Host "║  Backend:  http://127.0.0.1:8001                          ║" -ForegroundColor Green
    Write-Host "║  Frontend: http://localhost:8501                          ║" -ForegroundColor Green
    Write-Host "║                                                            ║" -ForegroundColor Green
    Write-Host "║  🧪 Test QR Mode:                                         ║" -ForegroundColor Green
    Write-Host "║  curl -X POST http://127.0.0.1:8001/analyze \             ║" -ForegroundColor Green
    Write-Host "║    -H 'Content-Type: application/json' \                  ║" -ForegroundColor Green
    Write-Host "║    -d '{\"text\":\"https://verify.xyz/pay\",\"mode\":\"qr\"}'   ║" -ForegroundColor Green
    Write-Host "║                                                            ║" -ForegroundColor Green
    Write-Host "║  Close this window when done                              ║" -ForegroundColor Green
    Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green
}

# Main
switch ($Service.ToLower()) {
    "backend" {
        Start-Backend
    }
    "frontend" {
        Start-Frontend
    }
    "all" {
        Start-Both
    }
    default {
        Write-Host "Usage: .\start.ps1 [backend|frontend|all]" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Examples:" -ForegroundColor Cyan
        Write-Host "  .\start.ps1 all       # Launch backend and frontend" -ForegroundColor Gray
        Write-Host "  .\start.ps1 backend   # Launch backend only" -ForegroundColor Gray
        Write-Host "  .\start.ps1 frontend  # Launch frontend only" -ForegroundColor Gray
    }
}

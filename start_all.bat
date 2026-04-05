@echo off
REM Script pour lancer backend et frontend dans des terminaux séparés
REM Placer ce fichier dans la racine du projet

cd /d "c:\Users\nourb\OneDrive\Bureau\human-firewall\human-firewall"

echo ======================================================
echo   Human Firewall - Lancement du Backend et Frontend
echo ======================================================
echo.

REM Vérifier si le backend est déjà en cours d'exécution
netstat -ano | findstr ":8001" >nul
if %errorlevel% equ 0 (
    echo [*] Port 8001 détecté comme actif (backend peut être en cours d'exécution)
    timeout /t 2
) else (
    echo [+] Port 8001 disponible - Lancement du backend...
)

REM Lancer le backend dans une nouvelle fenêtre
start "Human Firewall Backend" cmd /k "title Human Firewall Backend - FastAPI (Port 8001) & python -m uvicorn backend.app.main:app --reload --port 8001"

echo.
echo [+] Backend lancé dans une nouvelle fenêtre
echo [*] Attente de 3 secondes avant de lancer le frontend...
timeout /t 3

REM Lancer le frontend dans une nouvelle fenêtre
start "Human Firewall Frontend" cmd /k "title Human Firewall Frontend - Streamlit (Port 8501) & cd /d c:\Users\nourb\OneDrive\Bureau\human-firewall\human-firewall & streamlit run frontend/app.py"

echo.
echo ======================================================
echo   [✓] Backend lancé sur http://127.0.0.1:8001
echo   [✓] Frontend lancé sur http://localhost:8501
echo ======================================================
echo.
echo [*] Les deux services tournent dans des terminaux séparés
echo [*] Appuyez sur CTRL+C dans chaque fenêtre pour arrêter
echo.
timeout /t 2

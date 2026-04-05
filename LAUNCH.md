# Human Firewall - Guide de Lancement

## 🚀 Démarrage Rapide

### **Option 1: Lancer tout automatiquement (Recommandé)**

Double-cliquez sur:
```
start_all.bat
```

Cela va:
- ✅ Lancer le backend FastAPI sur le port 8001 (Terminal 1)
- ✅ Lancer le frontend Streamlit sur le port 8501 (Terminal 2)
- ✅ Les deux tournent indépendamment

---

### **Option 2: Lancer manuellement dans des terminaux séparés**

**Terminal 1 - Backend:**
```powershell
.\start_backend.ps1
```
Ou directement:
```powershell
cd c:\Users\nourb\OneDrive\Bureau\human-firewall\human-firewall
python -m uvicorn backend.app.main:app --reload --port 8001
```

**Terminal 2 - Frontend:**
```powershell
.\start_frontend.ps1
```
Ou directement:
```powershell
cd c:\Users\nourb\OneDrive\Bureau\human-firewall\human-firewall
streamlit run frontend/app.py
```

---

## 📍 Points d'accès

| Service | URL | Description |
|---------|-----|-------------|
| **Backend API** | http://127.0.0.1:8001 | FastAPI REST API |
| **API Docs (Swagger)** | http://127.0.0.1:8001/docs | Documentation interactive |
| **Frontend UI** | http://localhost:8501 | Interface Streamlit |

---

## ✨ Features Étape 2

### Message Mode (Défaut)
```bash
curl -X POST http://127.0.0.1:8001/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"Urgent: your account is suspended","mode":"message"}'
```

### QR Mode (Nouveau!)
```bash
curl -X POST http://127.0.0.1:8001/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"https://verify-payment.xyz/confirm","mode":"qr"}'
```

Réponse incluera:
- `analysis_mode: "qr"`
- `qr_triggers: ["phishing_keywords", "suspicious_domain"]`
- `qr_score: 0.5`
- Scoring: **0.4×ML + 0.25×rules + 0.35×QR-specific**

---

## 🧪 Test des Scénarios QR

### Scénario 1: Banking Scam
```json
{
  "text": "http://secure-payment-tnd.xyz/confirm",
  "mode": "qr"
}
```
**Attendu:** `qr_score: 0.65`, `attack_type: "banking scam"`

### Scénario 2: Shortened URL
```json
{
  "text": "https://biat-verification-alert.top/login",
  "mode": "qr"
}
```
**Attendu:** `qr_triggers: ["shortened_url"]`, `qr_score: > 0.4`

### Scénario 3: Delivery Scam
```json
{
  "text": "https://delivery-confirmation-click.shop/update-address",
  "mode": "qr"
}
```
**Attendu:** `attack_type: "delivery scam"`, `severity: "high"`

---

## 🛠️ Dépannage

### Port 8001 déjà utilisé?
```powershell
netstat -ano | findstr ":8001"
taskkill /PID <PID> /F
```

### Problèmes de connexion frontend→backend?
Vérifier que:
1. ✅ Le backend tourne sur `http://127.0.0.1:8001`
2. ✅ Le frontend peut accéder à l'API (vérifier firewall)
3. ✅ Variable d'environnement `API_BASE_URL` correcte (par défaut: `http://127.0.0.1:8001`)

### Streamlit ne démarre pas?
```powershell
pip install --upgrade streamlit
```

---

## 📊 Architecture

```
┌─────────────────────────────────────────────────────┐
│              Human Firewall System                   │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Terminal 1: Backend (FastAPI)                    │
│  ├─ Port 8001                                      │
│  ├─ /analyze (mode: message | qr)                 │
│  ├─ /decision (human validation)                  │
│  ├─ /logs (audit trail)                           │
│  └─ Swagger: http://127.0.0.1:8001/docs          │
│                                                     │
│  Terminal 2: Frontend (Streamlit)                 │
│  ├─ Port 8501                                      │
│  ├─ Section 1: Text Analysis                       │
│  ├─ Section 2a: Message (SMS/Email)               │
│  ├─ Section 2b: QR Code Analysis [NEW]            │
│  ├─ Section 3: Human Validation                    │
│  └─ Section 4: Audit Logs                         │
│                                                     │
│                 HTTP/JSON                          │
│                ←──────────→                        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## ✅ Étapes Complétées

- ✅ **Étape 1** - Dataset construction (131 messages)
- ✅ **Étape A** - Backend features (psychological + Tunisian context)
- ✅ **Étape B** - Frontend display (7 blocks)
- ✅ **Étape C** - Demo buttons (3 scenarios)
- ✅ **Étape D** - QR API foundation
- ✅ **Étape 2** - Backend QR mode support with ML + QR scoring

---

## 🎯 Prochaines Étapes Possibles

1. Intégration OCR pour lecture réelle de QR codes
2. Interface caméra pour scanner de codes QR
3. Détection automatique d'URLs raccourcies malveillantes
4. Support de multiples langues
5. Export des rapports d'analyse

---

*Last Updated: April 5, 2026*
*Human Firewall v2.0 - QR Mode Edition*

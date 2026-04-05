# URL & Threat Analysis - Demo Scenarios

## Overview
The URL Analysis section now provides 3 ready-to-test scenarios with different risk levels:
- 🔴 HIGH RISK
- 🟠 MEDIUM RISK  
- 🟢 LOW RISK

---

## Scenario 1: 🔴 HIGH RISK - Banking Scam

**URL:** `https://bit.ly/biat-verify-account`

### Why it's malicious:
- ✅ **Shortened URL** (`bit.ly`) → +0.25 QR risk
- ✅ **Phishing Keywords** (`verify`, `account`) → +0.25 QR risk
- ✅ **Tunisian Banking** (`biat`) → Detected as targeting TN citizens

### Expected Detection:
| Component | Expected Value |
|-----------|-----------------|
| **QR Risk Score** | 0.50 (from URL triggers) |
| **ML Score** | ~0.60-0.70 |
| **Final Risk Score** | **0.70-0.80 (HIGH)** |
| **Severity** | 🔴 HIGH RISK |
| **Attack Type** | Banking scam |
| **QR Triggers** | `["shortened_url", "phishing_keywords"]` |

### What to look for:
- High risk warning in 🔴 RED
- Psychological manipulation: urgency tactics detected
- Tunisian context: BIAT bank mentioned
- Recommendation: "Warn citizen" or "Escalate to analyst"

---

## Scenario 2: 🟠 MEDIUM RISK - Delivery Scam

**URL:** `https://colis-livraison.click/track-package`

### Why it's malicious:
- ✅ **Suspicious TLD** (`.click`) → +0.25 QR risk
- ✅ **Phishing Keywords** (`colis`, `livraison`) → +0.25 QR risk
- ✅ **Delivery Scam Pattern** (colis = package in French)

### Expected Detection:
| Component | Expected Value |
|-----------|-----------------|
| **QR Risk Score** | 0.50 (from URL triggers) |
| **ML Score** | ~0.40-0.50 |
| **Final Risk Score** | **0.50-0.65 (MEDIUM)** |
| **Severity** | 🟠 MEDIUM RISK |
| **Attack Type** | Delivery scam |
| **QR Triggers** | `["suspicious_domain", "phishing_keywords"]` |

### What to look for:
- Medium risk warning in 🟠 ORANGE
- Tunisian context: Detection of `colis` (delivery package)
- Rules triggered: delivery-related keywords
- Recommendation: "Escalate to analyst"

---

## Scenario 3: 🟢 LOW RISK - Safe URL

**URL:** `https://www.google.com`

### Why it's safe:
- ❌ No shortened URL
- ❌ No phishing keywords
- ❌ No suspicious TLD (`.com` is legitimate)
- ❌ No insecure HTTP
- ❌ No suspicious context

### Expected Detection:
| Component | Expected Value |
|-----------|-----------------|
| **QR Risk Score** | 0.0 (no triggers) |
| **ML Score** | ~0.05-0.15 |
| **Final Risk Score** | **<0.40 (LOW)** |
| **Severity** | 🟢 LOW RISK |
| **Attack Type** | benign |
| **QR Triggers** | `[]` (empty) |

### What to look for:
- Low risk success message in 🟢 GREEN
- No psychological manipulation detected
- No Tunisian context
- Recommendation: "No action"
- Remediation: "No immediate action required"

---

## How to Test

### Step 1: Start Backend & Frontend
```bash
# Terminal 1: Backend
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8001

# Terminal 2: Frontend
streamlit run frontend/app.py
```

### Step 2: Navigate to URL Analysis Section
- Open Streamlit UI (usually `http://localhost:8501`)
- Scroll to "URL & Threat Analysis" section

### Step 3: Test Each Scenario

**Test HIGH RISK:**
1. Click "🔴 HIGH RISK: Banking Scam" button
2. Text area auto-fills with `https://bit.ly/biat-verify-account`
3. Click "Analyze URL"
4. Observe:
   - Risk Score: Around 0.70-0.80
   - Severity: HIGH (🔴 red)
   - Attack Type: "banking scam"
   - Tunisian context confirmed

**Test MEDIUM RISK:**
1. Click "🟠 MEDIUM RISK: Delivery Scam" button
2. Text area auto-fills with `https://colis-livraison.click/track-package`
3. Click "Analyze URL"
4. Observe:
   - Risk Score: Around 0.50-0.65
   - Severity: MEDIUM (🟠 orange)
   - Attack Type: "delivery scam"
   - Keywords detected: `colis`, `livraison`

**Test LOW RISK:**
1. Click "🟢 LOW RISK: Safe URL" button
2. Text area auto-fills with `https://www.google.com`
3. Click "Analyze URL"
4. Observe:
   - Risk Score: Around 0.0-0.20
   - Severity: LOW (🟢 green)
   - Attack Type: "benign"
   - No triggers detected

### Step 4: Validate Results (Optional)
After analysis, use the "Human Decision for URL Analysis" section to:
- Approve/reject/flag for review
- Add analyst comments
- Submit decision to backend audit logs

---

## Technical Details

### QR Risk Detection (backend/app/rules.py)
The `detect_qr_risk()` function checks for:

| Trigger | Contribution | Examples |
|---------|--------------|----------|
| Shortened URL | +0.25 | bit.ly, tinyurl, t.co |
| Phishing Keywords | +0.25 | verify, login, payment, otp, colis |
| Suspicious TLD | +0.25 | .xyz, .click, .shop, .buzz |
| Insecure HTTP | +0.15 | http:// (not https://) |
| QR Context | +0.10 | contains "qr" keyword |

**Final Score Calculation (QR Mode):**
```
final_score = 0.4 × ML_score + 0.25 × rules_score + 0.35 × qr_score
```

### Expected Severity Thresholds
- 🔴 **HIGH**: >= 0.70
- 🟠 **MEDIUM**: 0.40 - 0.70
- 🟢 **LOW**: < 0.40

---

## Troubleshooting

### Issue: Backend returns 500 error
- Check backend is running on port 8001
- Check logs for Python errors
- Ensure `.venv` is activated

### Issue: URLs not appearing in text area
- Ensure `st.rerun()` is present in button code
- Clear Streamlit cache: `streamlit cache clear`
- Reload the page

### Issue: Wrong risk scores
- Verify `detect_qr_risk()` in `backend/app/rules.py`
- Check ML model is trained and loaded
- Verify scoring weights in `main.py`

---

## Next Steps

1. ✅ Test all 3 scenarios with the button demos
2. ✅ Verify risk scores match expectations
3. ✅ Log human decisions in audit trail
4. ✅ Ready for hackathon submission!


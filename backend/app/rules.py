SUSPICIOUS_KEYWORDS = [
    "urgent", "immédiatement", "cliquez", "click", "verify",
    "password", "mot de passe", "compte", "suspendu",
    "paiement", "otp", "bank", "bancaire", "livraison",
    "confirmer", "blocked", "locked", "account"
]


def detect_rules(text: str):
    text_lower = text.lower()
    triggered = [kw for kw in SUSPICIOUS_KEYWORDS if kw in text_lower]

    score = min(len(triggered) * 0.15, 1.0)

    return {
        "rules_triggered": triggered,
        "rules_score": score
    }


def recommend_action(prediction: str, risk_score: float) -> str:
    if prediction == "phishing" and risk_score >= 0.75:
        return "Warn citizen"
    if prediction == "phishing" and risk_score >= 0.50:
        return "Escalate to analyst"
    return "No action"
SUSPICIOUS_KEYWORDS = [
    "urgent", "immédiatement", "cliquez", "click", "verify",
    "password", "mot de passe", "compte", "suspendu",
    "paiement", "otp", "bank", "bancaire", "livraison",
    "confirmer", "blocked", "locked", "account", "colis",
    "adresse", "code"
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


def get_severity(risk_score: float) -> str:
    if risk_score >= 0.70:
        return "high"
    if risk_score >= 0.40:
        return "medium"
    return "low"


def get_attack_type(text: str, prediction: str) -> str:
    text_lower = text.lower()

    if any(word in text_lower for word in ["bancaire", "bank", "compte", "account", "suspendu", "verify"]):
        return "banking scam"

    if any(word in text_lower for word in ["livraison", "colis", "adresse", "delivery"]):
        return "delivery scam"

    if any(word in text_lower for word in ["otp", "password", "mot de passe", "code"]):
        return "credential theft"

    if any(word in text_lower for word in ["urgent", "immédiatement", "locked", "blocked"]):
        return "urgency scam"

    if prediction == "phishing":
        return "generic phishing"

    return "benign"


def get_remediation_tips(attack_type: str, prediction: str) -> list[str]:
    if prediction == "safe":
        return [
            "No immediate action required.",
            "Keep monitoring if the context changes."
        ]

    tips_map = {
        "banking scam": [
            "Do not click the suspicious link.",
            "Do not share credentials or OTP codes.",
            "Contact your bank using official channels."
        ],
        "delivery scam": [
            "Do not confirm your address from this message.",
            "Do not click external tracking links.",
            "Verify delivery status from the official provider website."
        ],
        "credential theft": [
            "Do not share your password or OTP.",
            "Change your password if you already responded.",
            "Enable two-factor authentication on the affected account."
        ],
        "urgency scam": [
            "Do not react under pressure.",
            "Verify the request through an official channel.",
            "Report the suspicious message to the analyst."
        ],
        "generic phishing": [
            "Do not click suspicious links.",
            "Do not share personal or financial information.",
            "Report the message as suspicious."
        ],
    }

    return tips_map.get(
        attack_type,
        [
            "Do not interact with the message.",
            "Verify the sender through trusted channels.",
            "Escalate to a human analyst."
        ]
    )
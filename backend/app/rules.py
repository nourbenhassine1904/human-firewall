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


def detect_psychological_manipulation(text: str):
    """Detect psychological manipulation tactics in text"""
    text_lower = text.lower()

    categories = {
        "urgency": [
            "urgent", "immédiatement", "now", "asap", "tout de suite", "vite"
        ],
        "fear": [
            "suspendu", "bloqué", "blocked", "locked", "expiré", "menace", "fermé"
        ],
        "pressure": [
            "dernière chance", "before midnight", "avant minuit", "sinon", "must", "obligatoire"
        ],
        "reward": [
            "gagné", "récompense", "bonus", "cadeau", "prize", "winner", "bon d'achat"
        ]
    }

    detected = []

    for category, keywords in categories.items():
        if any(keyword in text_lower for keyword in keywords):
            detected.append(category)

    if detected:
        explanation = "Psychological manipulation detected: " + ", ".join(detected)
    else:
        explanation = "No strong psychological manipulation pattern detected."

    return {
        "psychological_profile": detected,
        "psychological_explanation": explanation
    }


def detect_tunisian_context(text: str):
    """Detect Tunisian-specific phishing indicators"""
    text_lower = text.lower()

    tunisian_keywords = [
        "tunisie", "tunisia", "poste tunisienne", "ooredoo", "orange", "tunisie telecom",
        "biat", "stb", "attijari", "amen bank", "bna", "bh bank",
        "dinars", "dt", "tnd", "colis", "livraison"
    ]

    indicators = [kw for kw in tunisian_keywords if kw in text_lower]
    detected = len(indicators) > 0

    if detected:
        message = "This message matches common phishing patterns targeting Tunisian citizens."
    else:
        message = "No specific Tunisian contextual indicator detected."

    return {
        "tunisian_context_detected": detected,
        "tunisian_indicators": indicators,
        "tunisian_context_message": message
    }


def detect_qr_risk(text: str):
    """Detect QR-specific risk factors and phishing indicators"""
    text_lower = text.lower()
    triggers = []
    score = 0.0

    shorteners = ["bit.ly", "tinyurl", "t.co", "shorturl", "goo.gl"]
    suspicious_keywords = [
        "verify", "login", "update", "payment", "bank", "wallet",
        "confirm", "account", "otp", "password", "bancaire",
        "livraison", "colis"
    ]
    suspicious_tlds = [".xyz", ".top", ".click", ".shop", ".buzz"]

    if any(s in text_lower for s in shorteners):
        triggers.append("shortened_url")
        score += 0.25

    if any(k in text_lower for k in suspicious_keywords):
        triggers.append("phishing_keywords")
        score += 0.25

    if any(tld in text_lower for tld in suspicious_tlds):
        triggers.append("suspicious_domain")
        score += 0.25

    if text_lower.startswith("http://"):
        triggers.append("insecure_http")
        score += 0.15

    if "qr" in text_lower:
        triggers.append("qr_redirection_context")
        score += 0.10

    score = min(score, 1.0)

    return {
        "qr_triggers": triggers,
        "qr_score": round(score, 4)
    }
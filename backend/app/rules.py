# ==============================
# KEYWORDS
# ==============================

SUSPICIOUS_KEYWORDS = [
    "urgent", "immédiatement", "cliquez", "click", "verify",
    "password", "mot de passe", "compte", "suspendu",
    "paiement", "otp", "bank", "bancaire", "livraison",
    "confirmer", "blocked", "locked", "account", "colis",
    "adresse", "code"
]

# ==============================
# ATTACK PATTERNS
# ==============================

ATTACK_PATTERNS = {
    "banking_scam": [
        "bank", "banque", "compte bancaire", "transaction",
        "paiement", "carte", "card", "payment",
        "biat", "stb", "attijari", "amen bank", "bna", "bh bank"
    ],
    "delivery_scam": [
        "colis", "livraison", "delivery", "package",
        "shipment", "courier", "poste tunisienne"
    ],
    "credential_theft": [
        "login", "password", "mot de passe",
        "verify account", "confirm identity",
        "reset password", "identifiant"
    ],
    "otp_scam": [
        "otp", "code", "code de verification",
        "verification code", "security code"
    ],
    "tech_support_scam": [
        "support", "technical support",
        "microsoft", "apple", "virus",
        "infected", "security issue"
    ]
}

# ==============================
# PSYCHOLOGICAL PATTERNS
# ==============================

PSYCHOLOGICAL_PATTERNS = {
    "urgency": ["urgent", "immédiatement", "asap", "now"],
    "fear": ["suspendu", "bloqué", "blocked", "locked"],
    "pressure": ["avant minuit", "last chance"],
    "authority": ["banque", "support", "service client"],
    "reward": ["gagné", "bonus", "cadeau"]
}

# ==============================
# TUNISIAN CONTEXT PATTERNS
# ==============================

TUNISIAN_PATTERNS = {
    "banks": [
        "biat", "stb", "attijari", "amen bank", "bna", "bh bank", "zitouna"
    ],
    "telco": [
        "ooredoo", "orange", "tunisie telecom"
    ],
    "services": [
        "poste tunisienne", "poste", "colis", "livraison"
    ],
    "currency": [
        "tnd", "dt", "dinars"
    ],
    "common_words": [
        "tunisie", "tunisia", "citoyen", "client"
    ]
}

# ==============================
# BASE RULES
# ==============================


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


# ==============================
# ATTACK PATTERN DETECTION
# ==============================

def detect_attack_patterns(text: str):
    text_lower = text.lower()
    detected_types = {}

    for attack_type, keywords in ATTACK_PATTERNS.items():
        matches = [kw for kw in keywords if kw in text_lower]
        if matches:
            detected_types[attack_type] = matches

    return detected_types


def get_main_attack_type(detected_types: dict):
    if not detected_types:
        return "unknown"
    return max(detected_types, key=lambda k: len(detected_types[k]))


# ==============================
# ADVANCED PSYCHOLOGICAL ANALYSIS
# ==============================

def detect_psychological_patterns_advanced(text: str):
    text_lower = text.lower()
    detected = {}

    for category, keywords in PSYCHOLOGICAL_PATTERNS.items():
        matches = [kw for kw in keywords if kw in text_lower]
        if matches:
            detected[category] = matches

    return detected


def compute_psychological_score_advanced(detected: dict) -> float:
    weights = {
        "urgency": 15,
        "fear": 20,
        "pressure": 15,
        "authority": 10,
        "reward": 10
    }

    score = sum(weights.get(cat, 10) * len(matches) for cat, matches in detected.items())
    return min(score, 100)


def generate_psychological_explanation_advanced(detected: dict) -> str:
    explanations = []

    if "urgency" in detected:
        explanations.append("Urgency pressure detected")
    if "fear" in detected:
        explanations.append("Fear-based manipulation detected")
    if "pressure" in detected:
        explanations.append("Time pressure detected")
    if "authority" in detected:
        explanations.append("Fake authority detected")
    if "reward" in detected:
        explanations.append("Reward bait detected")

    return " | ".join(explanations) if explanations else "No manipulation detected"


def analyze_psychological_advanced(text: str) -> dict:
    detected = detect_psychological_patterns_advanced(text)
    score = compute_psychological_score_advanced(detected)
    explanation = generate_psychological_explanation_advanced(detected)

    return {
        "psychological_profile": list(detected.keys()),
        "psychological_score": score,
        "psychological_explanation": explanation
    }


# ==============================
# ADVANCED TUNISIAN CONTEXT ANALYSIS
# ==============================

def detect_tunisian_context_advanced(text: str) -> dict:
    text_lower = text.lower()
    detected = {}

    for category, keywords in TUNISIAN_PATTERNS.items():
        matches = [kw for kw in keywords if kw in text_lower]
        if matches:
            detected[category] = matches

    return detected


def compute_tunisian_score(detected: dict) -> float:
    weights = {
        "banks": 30,
        "telco": 25,
        "services": 20,
        "currency": 15,
        "common_words": 10
    }

    score = 0
    for category, matches in detected.items():
        score += weights.get(category, 10) * len(matches)

    return min(score, 100)


def generate_tunisian_explanation(detected: dict) -> str:
    if not detected:
        return "No Tunisian context detected."

    explanations = []

    if "banks" in detected:
        explanations.append("Tunisian bank detected")
    if "telco" in detected:
        explanations.append("Tunisian telecom operator detected")
    if "services" in detected:
        explanations.append("Local service context detected")
    if "currency" in detected:
        explanations.append("Tunisian currency detected")

    return " | ".join(explanations)


def analyze_tunisian_context_advanced(text: str) -> dict:
    detected = detect_tunisian_context_advanced(text)
    score = compute_tunisian_score(detected)
    explanation = generate_tunisian_explanation(detected)

    return {
        "tunisian_context_detected": len(detected) > 0,
        "tunisian_score": score,
        "tunisian_indicators": detected,
        "tunisian_explanation": explanation
    }


# ==============================
# QR & URL RISK DETECTION
# ==============================

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


# ==============================
# ADVANCED SECURITY SIGNALS
# ==============================

def detect_advanced_security_signals(text: str) -> list:
    """Detect advanced security signals in text"""
    text_lower = text.lower()
    signals = []

    # 🔗 Suspicious links
    if "http" in text_lower or "www" in text_lower:
        signals.append("suspicious_link")

    # 🔑 Request for sensitive info
    sensitive_keywords = [
        "password", "mot de passe",
        "code", "otp",
        "identifiant", "login"
    ]
    if any(word in text_lower for word in sensitive_keywords):
        signals.append("sensitive_info_request")

    # ⏳ Time pressure
    time_pressure = [
        "urgent", "immédiatement",
        "avant minuit", "now", "asap"
    ]
    if any(word in text_lower for word in time_pressure):
        signals.append("time_pressure")

    # 🧑‍💻 Fake support
    support_keywords = [
        "support", "technical support",
        "service client", "security team"
    ]
    if any(word in text_lower for word in support_keywords):
        signals.append("fake_support")

    # 🎁 Reward scam
    reward_keywords = [
        "gagné", "bonus", "cadeau",
        "reward", "prize"
    ]
    if any(word in text_lower for word in reward_keywords):
        signals.append("reward_trap")

    return signals
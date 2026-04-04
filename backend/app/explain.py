SUSPICIOUS_KEYWORDS = [
    "urgent", "immédiatement", "cliquez", "verify", "password",
    "mot de passe", "compte", "suspendu", "paiement", "otp",
    "bank", "bancaire", "livraison", "confirmer"
]

def explain_prediction(text: str):
    text_lower = text.lower()
    triggers = [kw for kw in SUSPICIOUS_KEYWORDS if kw in text_lower]

    if triggers:
        return {
            "rules_triggered": triggers,
            "explanation": f"Alerte levée car le message contient des indices suspects : {', '.join(triggers)}"
        }

    return {
        "rules_triggered": [],
        "explanation": "Aucun mot-clé suspect majeur détecté par les règles simples."
    }
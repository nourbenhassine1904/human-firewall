SUSPICIOUS_KEYWORDS = [
    "urgent", "immédiatement", "cliquez", "verify", "password",
    "mot de passe", "compte", "suspendu", "paiement", "otp",
    "bank", "bancaire", "livraison", "confirmer"
]

def explain_prediction(text: str, rules_triggered: list, prediction: str, risk_score: float) -> str:
    if rules_triggered:
        return (
            f"Le message a été classé comme {prediction} avec un score de risque de "
            f"{risk_score:.2f}, car il contient des indices suspects : "
            f"{', '.join(rules_triggered)}."
        )

    return (
        f"Le message a été classé comme {prediction} avec un score de risque de "
        f"{risk_score:.2f}. Aucun mot-clé suspect majeur n'a été détecté par les règles."
    )
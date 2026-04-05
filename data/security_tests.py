TEST_MESSAGES = [
    # =========================
    # PHISHING - BANKING
    # =========================
    {
        "text": "Urgent : votre compte BIAT est suspendu. Vérifiez maintenant",
        "expected": {
            "attack_type": "banking scam",
            "severity": "high",
            "psychological_profile": ["urgency", "fear"]
        }
    },

    # =========================
    # DELIVERY SCAM
    # =========================
    {
        "text": "Votre colis ne peut pas être livré. Confirmez votre adresse avant minuit",
        "expected": {
            "attack_type": "delivery scam",
            "severity": "medium",
            "psychological_profile": ["pressure"]
        }
    },

    # =========================
    # OTP SCAM
    # =========================
    {
        "text": "Envoyez votre code OTP immédiatement pour éviter le blocage",
        "expected": {
            "attack_type": "credential theft",
            "severity": "high",
            "psychological_profile": ["urgency", "fear"]
        }
    },

    # =========================
    # REWARD SCAM
    # =========================
    {
        "text": "Félicitations ! Vous avez gagné un bon d'achat. Cliquez maintenant",
        "expected": {
            "attack_type": "generic phishing",
            "severity": "medium",
            "psychological_profile": ["reward", "urgency"]
        }
    },

    # =========================
    # TECH SUPPORT SCAM
    # =========================
    {
        "text": "Microsoft security alert: your device is infected. Call support now",
        "expected": {
            "attack_type": "tech_support_scam",
            "severity": "high",
            "psychological_profile": ["fear", "authority"]
        }
    },

    # =========================
    # SAFE MESSAGES
    # =========================
    {
        "text": "Bonjour, votre rendez-vous est confirmé pour demain",
        "expected": {
            "attack_type": "benign",
            "severity": "low",
            "psychological_profile": []
        }
    },

    {
        "text": "Merci pour votre paiement. Facture disponible sur votre espace client",
        "expected": {
            "attack_type": "benign",
            "severity": "low",
            "psychological_profile": []
        }
    }
]
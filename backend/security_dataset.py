SECURITY_DATASET = [

    # 🔴 BANKING SCAM
    {
        "text": "Urgent : votre compte BIAT sera suspendu aujourd’hui. Cliquez ici pour vérifier vos informations.",
        "expected_attack": "banking scam",
        "expected_severity": "high",
        "expected_psychology": ["urgency", "fear"]
    },

    # 🔴 DELIVERY SCAM
    {
        "text": "Votre colis ne peut pas être livré. Merci de confirmer votre adresse avant minuit.",
        "expected_attack": "delivery scam",
        "expected_severity": "medium",
        "expected_psychology": ["pressure"]
    },

    # 🔴 OTP SCAM
    {
        "text": "Votre code OTP est requis immédiatement pour éviter le blocage de votre compte.",
        "expected_attack": "credential theft",
        "expected_severity": "high",
        "expected_psychology": ["urgency", "fear"]
    },

    # 🔴 TECH SUPPORT SCAM
    {
        "text": "Microsoft security alert: your device is infected. Call support now.",
        "expected_attack": "tech_support_scam",
        "expected_severity": "high",
        "expected_psychology": ["fear", "authority"]
    },

    # 🔴 REWARD SCAM
    {
        "text": "Félicitations ! Vous avez gagné un bon d'achat. Cliquez maintenant pour réclamer votre récompense.",
        "expected_attack": "generic phishing",
        "expected_severity": "medium",
        "expected_psychology": ["reward", "urgency"]
    },

    # 🔴 LINK + PASSWORD
    {
        "text": "URGENT: Click here http://secure-login.com and enter your password now",
        "expected_attack": "credential theft",
        "expected_severity": "high",
        "expected_psychology": ["urgency"]
    },

    # 🟢 SAFE MESSAGE
    {
        "text": "Bonjour, votre rendez-vous est confirmé pour demain.",
        "expected_attack": "benign",
        "expected_severity": "low",
        "expected_psychology": []
    },

    # 🟢 SAFE PAYMENT
    {
        "text": "Merci pour votre paiement. Votre facture est disponible sur votre espace client.",
        "expected_attack": "benign",
        "expected_severity": "low",
        "expected_psychology": []
    },

    # 🟢 NORMAL DELIVERY
    {
        "text": "Votre colis a été expédié et arrivera demain.",
        "expected_attack": "benign",
        "expected_severity": "low",
        "expected_psychology": []
    }
]

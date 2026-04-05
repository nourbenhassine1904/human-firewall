TEST_MESSAGES = [
    # =========================
    # PHISHING - BANKING
    # =========================
    {
        "text": "Urgent : votre compte BIAT est suspendu. Vérifiez maintenant",
        "expected": {
            "attack_type": "banking scam",
            "severity": "medium",
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
            "severity": "medium",
            "psychological_profile": ["urgency"]
        }
    },

    # =========================
    # REWARD SCAM
    # =========================
    {
        "text": "Félicitations ! Vous avez gagné un bon d'achat. Cliquez maintenant",
        "expected": {
            "attack_type": "benign",
            "severity": "medium",
            "psychological_profile": ["reward"]
        }
    },

    # =========================
    # TECH SUPPORT SCAM
    # =========================
    {
        "text": "Microsoft security alert: your device is infected. Call support now",
        "expected": {
            "attack_type": "benign",
            "severity": "low",
            "psychological_profile": ["urgency"]
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

# =========================
# URL/QR TEST CASES
# =========================

TEST_URLS = [
    # =========================
    # HIGH RISK - BANKING SCAM
    # =========================
    {
        "text": "https://bit.ly/biat-verify-account",
        "mode": "qr",
        "expected": {
            "attack_type": "banking scam",
            "severity": "low",
            "qr_triggers": ["shortened_url"],
            "tunisian_context_detected": True
        }
    },

    # =========================
    # HIGH RISK - DELIVERY SCAM
    # =========================
    {
        "text": "https://colis-livraison-urgent.tk/verify",
        "mode": "qr",
        "expected": {
            "attack_type": "banking scam",
            "severity": "medium",
            "qr_triggers": ["suspicious_tld"],
            "tunisian_context_detected": True
        }
    },

    # =========================
    # MEDIUM RISK - OOREDOO OTP
    # =========================
    {
        "text": "http://ooredoo-verify-otp.com/check",
        "mode": "qr",
        "expected": {
            "attack_type": "banking scam",
            "severity": "low",
            "qr_triggers": ["http_insecure"],
            "tunisian_context_detected": True
        }
    },

    # =========================
    # MEDIUM RISK - SUSPICIOUS TLD
    # =========================
    {
        "text": "https://banque-tunisia.click/login",
        "mode": "qr",
        "expected": {
            "attack_type": "benign",
            "severity": "low",
            "qr_triggers": ["suspicious_tld"],
            "tunisian_context_detected": True
        }
    },

    # =========================
    # LOW RISK - LEGITIMATE
    # =========================
    {
        "text": "https://www.biat.com.tn/",
        "mode": "qr",
        "expected": {
            "attack_type": "benign",
            "severity": "low",
            "qr_triggers": [],
            "tunisian_context_detected": True
        }
    },

    # =========================
    # LOW RISK - GENERIC
    # =========================
    {
        "text": "https://www.google.com",
        "mode": "qr",
        "expected": {
            "attack_type": "benign",
            "severity": "low",
            "qr_triggers": [],
            "tunisian_context_detected": False
        }
    }
]
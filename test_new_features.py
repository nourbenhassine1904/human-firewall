import requests
import json
import time

time.sleep(3)

test_cases = [
    {
        "name": "Cas 1 - Banking + Fear + Urgency",
        "text": "Urgent : votre compte BIAT sera suspendu immédiatement. Vérifiez vos informations maintenant."
    },
    {
        "name": "Cas 2 - Delivery + Pressure",
        "text": "Votre colis ne peut pas être livré. Merci de confirmer votre adresse avant minuit."
    },
    {
        "name": "Cas 3 - Reward Scam",
        "text": "Félicitations, vous avez gagné un bon d'achat exceptionnel. Cliquez vite pour réclamer votre récompense."
    }
]

for test in test_cases:
    print(f"\n{'='*70}")
    print(f"TEST: {test['name']}")
    print(f"{'='*70}")
    print(f"Input: {test['text']}\n")
    
    try:
        response = requests.post(
            "http://localhost:8001/analyze",
            json={"text": test['text']},
            timeout=5
        )
        
        if response.status_code != 200:
            print(f"❌ Error {response.status_code}: {response.text}")
            continue
            
        result = response.json()
        
        print(f"✓ attack_type: {result.get('attack_type')}")
        print(f"✓ severity: {result.get('severity')}")
        print(f"✓ prediction: {result.get('prediction')}")
        print(f"✓ risk_score: {result.get('risk_score')}")
        print(f"✓ psychological_profile: {result.get('psychological_profile')}")
        print(f"✓ psychological_explanation: {result.get('psychological_explanation')}")
        print(f"✓ tunisian_context_detected: {result.get('tunisian_context_detected')}")
        print(f"✓ tunisian_indicators: {result.get('tunisian_indicators')}")
        print(f"✓ ml_score: {result.get('ml_score')}")
        print(f"✓ rules_score: {result.get('rules_score')}")
        
    except requests.ConnectionError as e:
        print(f"❌ Connection Error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

print(f"\n{'='*70}")
print("✓ All tests completed!")
print(f"{'='*70}\n")

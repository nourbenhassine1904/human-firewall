import sys
import os
from app.rules import detect_advanced_security_signals
from security_dataset import SECURITY_DATASET


sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.rules import (
    analyze_psychological_advanced,
    detect_attack_patterns,
    get_main_attack_type
)

from data.security_tests import TEST_MESSAGES

def run_tests():
    print("=== SECURITY TESTS ===\n")

    for i, test in enumerate(TEST_MESSAGES):
        text = test["text"]
        expected = test["expected"]

        print(f"\nTest {i+1}")
        print("Message:", text)

        # Analyse
        psych = analyze_psychological_advanced(text)
        attacks = detect_attack_patterns(text)
        attack_type = get_main_attack_type(attacks)

        print("Detected attack:", attack_type)
        print("Psychological:", psych["psychological_profile"])
        print("Expected:", expected)

        print("-" * 40)

if __name__ == "__main__":
    run_tests()

print("\n=== TEST ADVANCED SECURITY SIGNALS ===")

msg = "URGENT: Click here http://fake-link.com and enter your password now"

signals = detect_advanced_security_signals(msg)

print("Message:", msg)
print("Detected signals:", signals)

print("\n=== DATASET TEST ===\n")

for i, sample in enumerate(SECURITY_DATASET, 1):
    text = sample["text"]

    print(f"Test {i}")
    print("Message:", text)

    # Analyse
    patterns = detect_attack_patterns(text)
    attack_type = get_main_attack_type(patterns)

    psych = analyze_psychological_advanced(text)

    print("Detected attack:", attack_type)
    print("Psychological:", psych["psychological_profile"])

    print("Expected:", sample)
    print("-" * 50)
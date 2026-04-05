#!/usr/bin/env python3
"""
Test Runner for Human Firewall Detection System
Validates all TEST_MESSAGES and TEST_URLS against the /analyze endpoint
"""

import requests
import json
import sys
from pathlib import Path
from data.security_tests import TEST_MESSAGES, TEST_URLS

# Configuration
API_BASE_URL = "http://127.0.0.1:8001"
ANALYZE_ENDPOINT = f"{API_BASE_URL}/analyze"

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(title):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{title:^70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")

def print_test_case(index, total, test_type):
    print(f"{Colors.CYAN}[Test {index}/{total}] {test_type}{Colors.END}")

def print_success(message):
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")

def test_message(index, total, test_case):
    """Test a message against the detection engine"""
    text = test_case["text"]
    expected = test_case["expected"]
    
    print_test_case(index, total, f"Message Test - '{text[:50]}...'")
    
    try:
        response = requests.post(ANALYZE_ENDPOINT, json={"text": text})
        response.raise_for_status()
        result = response.json()
        
        # Validate expected fields
        passed = True
        
        if "prediction" in result:
            print_success(f"Prediction: {result['prediction']}")
        
        if "attack_type" in result:
            expected_type = expected.get("attack_type", "unknown")
            actual_type = result["attack_type"]
            if actual_type.lower() == expected_type.lower():
                print_success(f"Attack Type: {actual_type} ✓")
            else:
                print_warning(f"Attack Type: Expected '{expected_type}', got '{actual_type}'")
                passed = False
        
        if "severity" in result:
            expected_severity = expected.get("severity", "low")
            actual_severity = result["severity"]
            if actual_severity.lower() == expected_severity.lower():
                print_success(f"Severity: {actual_severity} ✓")
            else:
                print_warning(f"Severity: Expected '{expected_severity}', got '{actual_severity}'")
                passed = False
        
        if "risk_score" in result:
            print_success(f"Risk Score: {result['risk_score']:.2f}")
        
        if "rules_triggered" in result and result["rules_triggered"]:
            print_success(f"Triggered Rules ({len(result['rules_triggered'])}): {', '.join(result['rules_triggered'])}")
        
        if "psychological_profile" in result and result["psychological_profile"]:
            print_success(f"Psychological Profile: {result['psychological_profile']}")
        
        if "tunisian_context_detected" in result:
            print_success(f"Tunisian Context: {result['tunisian_context_detected']}")
        
        return passed, result
    
    except requests.exceptions.ConnectionError:
        print_error(f"Cannot connect to API at {ANALYZE_ENDPOINT}")
        return False, None
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False, None

def test_url(index, total, test_case):
    """Test a URL/QR against the detection engine"""
    url = test_case["text"]
    expected = test_case["expected"]
    
    print_test_case(index, total, f"URL Test - '{url[:50]}...'")
    
    try:
        response = requests.post(ANALYZE_ENDPOINT, json={"text": url})
        response.raise_for_status()
        result = response.json()
        
        # Validate expected fields
        passed = True
        
        if "attack_type" in result:
            expected_type = expected.get("attack_type", "benign")
            actual_type = result["attack_type"]
            if actual_type.lower() == expected_type.lower():
                print_success(f"Attack Type: {actual_type} ✓")
            else:
                print_warning(f"Attack Type: Expected '{expected_type}', got '{actual_type}'")
                passed = False
        
        if "severity" in result:
            expected_severity = expected.get("severity", "low")
            actual_severity = result["severity"]
            if actual_severity.lower() == expected_severity.lower():
                print_success(f"Severity: {actual_severity} ✓")
            else:
                print_warning(f"Severity: Expected '{expected_severity}', got '{actual_severity}'")
                passed = False
        
        if "risk_score" in result:
            print_success(f"Risk Score: {result['risk_score']:.2f}")
        
        if "qr_triggers" in result and result["qr_triggers"]:
            print_success(f"QR Triggers: {result['qr_triggers']}")
        
        if "tunisian_context_detected" in result:
            status = "Detected ✓" if result["tunisian_context_detected"] else "Not Detected"
            print_success(f"Tunisian Context: {status}")
        
        return passed, result
    
    except requests.exceptions.ConnectionError:
        print_error(f"Cannot connect to API at {ANALYZE_ENDPOINT}")
        return False, None
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False, None

def run_all_tests():
    """Run all tests and generate report"""
    print_header("🔐 Human Firewall - Security Test Suite")
    
    # Test availability of API
    print(f"{Colors.CYAN}Checking API availability...{Colors.END}")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        print_success(f"API is running: {API_BASE_URL}")
    except:
        print_error(f"API is not responding at {API_BASE_URL}")
        print_warning("Make sure backend is running: python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8001")
        return
    
    # Message Tests
    print_header("📨 Testing Message Detection")
    message_passed = 0
    message_total = len(TEST_MESSAGES)
    
    for i, test_case in enumerate(TEST_MESSAGES, 1):
        passed, result = test_message(i, message_total, test_case)
        if passed:
            message_passed += 1
        print()
    
    # URL Tests
    print_header("🔗 Testing URL/QR Analysis")
    url_passed = 0
    url_total = len(TEST_URLS)
    
    for i, test_case in enumerate(TEST_URLS, 1):
        passed, result = test_url(i, url_total, test_case)
        if passed:
            url_passed += 1
        print()
    
    # Summary Report
    print_header("📊 Test Summary Report")
    
    print(f"{Colors.BOLD}Message Detection Tests:{Colors.END}")
    print(f"  Passed: {Colors.GREEN}{message_passed}/{message_total}{Colors.END}")
    print(f"  Success Rate: {(message_passed/message_total)*100:.1f}%\n")
    
    print(f"{Colors.BOLD}URL/QR Analysis Tests:{Colors.END}")
    print(f"  Passed: {Colors.GREEN}{url_passed}/{url_total}{Colors.END}")
    print(f"  Success Rate: {(url_passed/url_total)*100:.1f}%\n")
    
    total_passed = message_passed + url_passed
    total_tests = message_total + url_total
    
    print(f"{Colors.BOLD}Overall Results:{Colors.END}")
    print(f"  Total Passed: {Colors.GREEN}{total_passed}/{total_tests}{Colors.END}")
    print(f"  Overall Success Rate: {(total_passed/total_tests)*100:.1f}%\n")
    
    # Final status
    if total_passed == total_tests:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ ALL TESTS PASSED!{Colors.END}\n")
    else:
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠ Some tests did not pass. Review the output above.{Colors.END}\n")

if __name__ == "__main__":
    run_all_tests()

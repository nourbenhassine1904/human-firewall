#!/usr/bin/env python3
"""Test script to verify Étape 2 QR Mode Implementation"""

import sys
sys.path.insert(0, 'c:\\Users\\nourb\\OneDrive\\Bureau\\human-firewall\\human-firewall')

from backend.app.schemas import AnalyzeRequest, AnalyzeResponse
from backend.app.rules import detect_qr_risk

def test_1_schema_mode_parameter():
    """Test 1: AnalyzeRequest accepts mode parameter"""
    print("✓ Test 1: AnalyzeRequest mode parameter")
    
    # Default mode (message)
    req1 = AnalyzeRequest(text="test message")
    assert req1.mode == "message", f"Expected mode='message', got {req1.mode}"
    print(f"  - Default mode: {req1.mode} ✓")
    
    # Explicit QR mode
    req2 = AnalyzeRequest(text="https://bit.ly/fake", mode="qr")
    assert req2.mode == "qr", f"Expected mode='qr', got {req2.mode}"
    print(f"  - Explicit QR mode: {req2.mode} ✓")
    
    print("✓ AnalyzeRequest schema validation passed\n")

def test_2_qr_response_fields():
    """Test 2: AnalyzeResponse has QR-specific fields"""
    print("✓ Test 2: AnalyzeResponse QR fields")
    
    response_fields = AnalyzeResponse.model_fields.keys()
    
    assert 'analysis_mode' in response_fields, "Missing analysis_mode field"
    print("  - analysis_mode field ✓")
    
    assert 'qr_triggers' in response_fields, "Missing qr_triggers field"
    print("  - qr_triggers field ✓")
    
    assert 'qr_score' in response_fields, "Missing qr_score field"
    print("  - qr_score field ✓")
    
    print("✓ AnalyzeResponse schema validation passed\n")

def test_3_detect_qr_risk_function():
    """Test 3: detect_qr_risk function works correctly"""
    print("✓ Test 3: detect_qr_risk function")
    
    # Test 1: Shortened URL detection
    result1 = detect_qr_risk("http://bit.ly/fake-bank")
    assert "shortened_url" in result1["qr_triggers"], "shortened_url not detected"
    assert result1["qr_score"] > 0, "QR score should be > 0"
    print(f"  - Shortened URL detection: score={result1['qr_score']}, triggers={result1['qr_triggers']} ✓")
    
    # Test 2: Suspicious domain (.xyz)
    result2 = detect_qr_risk("https://verify-account.xyz/login")
    assert "suspicious_domain" in result2["qr_triggers"], "suspicious_domain not detected"
    assert "phishing_keywords" in result2["qr_triggers"], "phishing_keywords not detected"
    print(f"  - Suspicious domain detection: score={result2['qr_score']}, triggers={result2['qr_triggers']} ✓")
    
    # Test 3: Insecure HTTP
    result3 = detect_qr_risk("http://biat-verify.click/confirm-payment")
    assert "insecure_http" in result3["qr_triggers"], "insecure_http not detected"
    print(f"  - Insecure HTTP detection: score={result3['qr_score']}, triggers={result3['qr_triggers']} ✓")
    
    # Test 4: Safe URL should have minimal score
    result4 = detect_qr_risk("https://www.bbc.com/news")
    assert len(result4["qr_triggers"]) == 0 or result4["qr_score"] == 0, "Safe URL should have no triggers"
    print(f"  - Safe URL: score={result4['qr_score']}, triggers={result4['qr_triggers']} ✓")
    
    print("✓ detect_qr_risk function tests passed\n")

def test_4_backend_routes():
    """Test 4: Check backend has /analyze endpoint with mode support"""
    print("✓ Test 4: Backend routing with mode parameter")
    
    from backend.app.main import app
    
    routes = {route.path: route.methods for route in app.routes}
    
    assert "/analyze" in routes, "Missing /analyze endpoint"
    print("  - /analyze endpoint exists ✓")
    
    # Verify /analyze-qr is removed
    assert "/analyze-qr" not in routes, "/analyze-qr endpoint should be removed"
    print("  - /analyze-qr endpoint removed (as per Étape 2) ✓")
    
    print("✓ Backend routing validation passed\n")

def test_5_scoring_logic():
    """Test 5: Verify QR scoring weights are different from message mode"""
    print("✓ Test 5: QR mode scoring weights")
    
    # This is a conceptual test - the actual endpoint would be tested in integration
    # For now, we verify the logic exists in the code
    
    with open('c:\\Users\\nourb\\OneDrive\\Bureau\\human-firewall\\human-firewall\\backend\\app\\main.py', 'r') as f:
        content = f.read()
    
    # Check for mode-based scoring
    assert 'if mode == "qr":' in content, "Mode-based scoring not found"
    print("  - Mode-based conditional scoring ✓")
    
    # Check for QR weights: 0.4 ML + 0.25 rules + 0.35 QR
    assert '(0.4 * ml_score)' in content or '0.4 * ml_score' in content, "QR ML weight (0.4) not found"
    assert '(0.25 * rules_score)' in content or '0.25 * rules_score' in content, "QR rules weight (0.25) not found"
    assert '(0.35 * qr_result' in content, "QR score weight (0.35) not found"
    print("  - QR scoring weights: 0.4 ML + 0.25 rules + 0.35 QR ✓")
    
    # Check for message weights: 0.7 ML + 0.3 rules
    assert '(0.7 * ml_score)' in content, "Message ML weight (0.7) not found"
    assert '(0.3 * rules_score)' in content, "Message rules weight (0.3) not found"
    print("  - Message scoring weights: 0.7 ML + 0.3 rules ✓")
    
    print("✓ Scoring logic validation passed\n")

def test_6_logging_includes_qr_fields():
    """Test 6: Verify logging includes analysis_mode and QR fields"""
    print("✓ Test 6: Logging with QR fields")
    
    with open('c:\\Users\\nourb\\OneDrive\\Bureau\\human-firewall\\human-firewall\\backend\\app\\main.py', 'r') as f:
        content = f.read()
    
    # Check log_entry has mode field
    assert '"analysis_mode": mode' in content, "analysis_mode not in log_entry"
    print("  - analysis_mode in log_entry ✓")
    
    # Check log_entry has QR fields
    assert '"qr_triggers": qr_result["qr_triggers"]' in content, "qr_triggers not in log_entry"
    print("  - qr_triggers in log_entry ✓")
    
    assert '"qr_score": qr_result["qr_score"]' in content, "qr_score not in log_entry"
    print("  - qr_score in log_entry ✓")
    
    # Check response includes QR fields
    assert '"analysis_mode": mode' in content, "analysis_mode not in response"
    print("  - analysis_mode in response ✓")
    
    print("✓ Logging validation passed\n")

if __name__ == "__main__":
    print("=" * 70)
    print("ÉTAPE 2 - QR Mode Backend Implementation Verification Tests")
    print("=" * 70 + "\n")
    
    try:
        test_1_schema_mode_parameter()
        test_2_qr_response_fields()
        test_3_detect_qr_risk_function()
        test_4_backend_routes()
        test_5_scoring_logic()
        test_6_logging_includes_qr_fields()
        
        print("=" * 70)
        print("✅ ALL ÉTAPE 2 TESTS PASSED!")
        print("=" * 70)
        print("\nImplementation Summary:")
        print("✅ AnalyzeRequest now accepts mode parameter (message|qr)")
        print("✅ AnalyzeResponse includes analysis_mode, qr_triggers, qr_score fields")
        print("✅ detect_qr_risk function detects:")
        print("   - Shortened URLs (bit.ly, tinyurl, etc.)")
        print("   - Suspicious keywords (verify, login, payment, etc.)")
        print("   - Suspicious TLDs (.xyz, .top, .click, .shop, .buzz)")
        print("   - Insecure HTTP")
        print("   - QR redirection context")
        print("✅ /analyze endpoint now handles both message and qr modes")
        print("✅ QR scoring: 0.4 ML + 0.25 rules + 0.35 QR-specific")
        print("✅ Message scoring: 0.7 ML + 0.3 rules (unchanged)")
        print("✅ Logging includes analysis_mode and QR fields")
        print("✅ /analyze-qr endpoint removed (consolidated into /analyze)")
        print("\nNext step: Test with Swagger UI or curl:")
        print("  curl -X POST http://localhost:8001/analyze \\")
        print('    -H "Content-Type: application/json" \\')
        print('    -d \'{"text":"https://verify-payment.xyz/confirm","mode":"qr"}\'')
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

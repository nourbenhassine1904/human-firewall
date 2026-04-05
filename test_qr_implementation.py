#!/usr/bin/env python3
"""Test script to verify QR implementation without running full server"""

import sys
sys.path.insert(0, 'c:\\Users\\nourb\\OneDrive\\Bureau\\human-firewall\\human-firewall')

from backend.app.schemas import AnalyzeRequest, AnalyzeResponse

def test_analyze_request_with_source():
    """Test that AnalyzeRequest now accepts source parameter"""
    print("✓ Test 1: AnalyzeRequest with source parameter")
    
    # Test 1: Default source (manual)
    req1 = AnalyzeRequest(text="test message")
    assert req1.source == "manual", f"Expected source='manual', got {req1.source}"
    print(f"  - Default source: {req1.source} ✓")
    
    # Test 2: Explicit QR source
    req2 = AnalyzeRequest(text="https://bit.ly/fake", source="qr")
    assert req2.source == "qr", f"Expected source='qr', got {req2.source}"
    print(f"  - Explicit QR source: {req2.source} ✓")
    
    print("✓ AnalyzeRequest schema validation passed\n")

def test_backend_routing():
    """Test that endpoint routing is correct"""
    print("✓ Test 2: Backend routing validation")
    
    from backend.app.main import app
    
    # Check if routes exist
    routes = [route.path for route in app.routes]
    print(f"  Available routes: {[r for r in routes if '/analyze' in r]}")
    
    assert "/analyze" in routes, "Missing /analyze endpoint"
    print("  - /analyze endpoint exists ✓")
    
    assert "/analyze-qr" in routes, "Missing /analyze-qr endpoint"
    print("  - /analyze-qr endpoint exists ✓")
    
    assert "/decision" in routes, "Missing /decision endpoint"
    print("  - /decision endpoint exists ✓")
    
    assert "/logs" in routes, "Missing /logs endpoint"
    print("  - /logs endpoint exists ✓")
    
    print("✓ All required endpoints are registered\n")

def test_frontend_qr_section():
    """Test frontend file contains QR section code"""
    print("✓ Test 3: Frontend QR section validation")
    
    with open('c:\\Users\\nourb\\OneDrive\\Bureau\\human-firewall\\human-firewall\\frontend\\app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    assert '"qr_result"' in content, "QR result session state not found"
    print("  - QR result session state initialization ✓")
    
    assert '"2b. QR Code Analysis"' in content, "QR section header not found"
    print("  - QR Code Analysis section header ✓")
    
    assert 'Fake WiFi QR' in content, "Fake WiFi demo button not found"
    print("  - Fake WiFi QR demo button ✓")
    
    assert 'Shortened URL QR' in content, "Shortened URL demo button not found"
    print("  - Shortened URL QR demo button ✓")
    
    assert 'Payment QR Scam' in content, "Payment QR demo button not found"
    print("  - Payment QR Scam demo button ✓")
    
    assert '/analyze-qr' in content, "QR API endpoint call not found"
    print("  - /analyze-qr endpoint call ✓")
    
    assert 'qr_human_decision' in content, "QR human decision selectbox not found"
    print("  - QR human decision validation ✓")
    
    print("✓ Frontend QR implementation validated\n")

if __name__ == "__main__":
    print("=" * 60)
    print("QR Implementation Verification Tests")
    print("=" * 60 + "\n")
    
    try:
        test_analyze_request_with_source()
        test_backend_routing()
        test_frontend_qr_section()
        
        print("=" * 60)
        print("✅ ALL TESTS PASSED - QR Implementation is Ready!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Start the FastAPI server: python -m uvicorn backend.app.main:app --reload --port 8001")
        print("2. Start Streamlit: streamlit run frontend/app.py")
        print("3. Test QR scenarios in the UI")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

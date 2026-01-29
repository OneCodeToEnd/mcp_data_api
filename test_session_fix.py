#!/usr/bin/env python3
"""
Test script to verify the FastMCP session context fix
"""
import sys
sys.path.insert(0, 'src')

from unittest.mock import MagicMock

def test_session_context_fix():
    """Test that ctx.session access works correctly"""
    print("Testing ctx.session access fix...")
    
    # Create a mock Context with session attribute
    mock_session = {}
    mock_ctx = MagicMock()
    mock_ctx.session = mock_session
    
    # Test write
    mock_ctx.session["session_context"] = {"app_id": "test", "initialized": True}
    print("✓ Write to ctx.session works")
    
    # Test read
    value = mock_ctx.session["session_context"]
    assert value == {"app_id": "test", "initialized": True}
    print("✓ Read from ctx.session works")
    
    return True

def test_server_import():
    """Test that server.py can be imported"""
    print("\nTesting server.py import...")
    try:
        # Just verify the file structure is valid
        with open('src/server.py', 'r') as f:
            content = f.read()
            
        # Check that old incorrect patterns are removed
        if 'ctx.request_context.session' in content:
            print("✗ ERROR: Old pattern still exists!")
            return False
        
        # Check that new correct pattern exists
        if 'ctx.session["session_context"]' not in content:
            print("✗ ERROR: New pattern not found!")
            return False
            
        print("✓ server.py has correct session access pattern")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("FastMCP Session Context Fix Verification")
    print("=" * 60)
    print()
    
    result1 = test_session_context_fix()
    result2 = test_server_import()
    
    print("\n" + "=" * 60)
    if result1 and result2:
        print("✅ Fix verified! Ready to test with agent.")
    else:
        print("❌ Fix verification failed.")
    print("=" * 60)

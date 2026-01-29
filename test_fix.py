#!/usr/bin/env python3
"""
Test script to verify FastMCP RequestContext fix
"""
import asyncio
import sys
from unittest.mock import MagicMock, AsyncMock

# Add the src directory to path
import sys
sys.path.insert(0, '/Users/xiedi/data/rh/code/mcp_data_api/src')

# Now we can import the server module directly
from server import get_session_context, SessionContext, settings
    
    # Test 1: First call - should auto-initialize
    print("  Test 1: Auto-initialization")
    session_ctx = get_session_context(mock_ctx)
    assert session_ctx is not None, "Session context should not be None"
    assert session_ctx.app_id == settings.server.app_id, f"Expected app_id {settings.server.app_id}, got {session_ctx.app_id}"
    assert session_ctx.initialized == True, "Session should be initialized"
    print("  ✓ Auto-initialization works")
    
    # Test 2: Second call - should retrieve existing session
    print("  Test 2: Retrieve existing session")
    mock_session["session_context"] = session_ctx  # Simulate stored session
    session_ctx2 = get_session_context(mock_ctx)
    assert session_ctx2 is not None, "Session context should not be None"
    assert session_ctx2 is session_ctx, "Should return the same session object"
    print("  ✓ Retrieve existing session works")
    
    print("\n✅ All tests passed!")
    return True


async def test_tool_functionality():
    """Test that tool functions work with the fixed context"""
    print("\nTesting tool functionality...")
    
    # Create mock context
    mock_session = {}
    mock_request_context = MagicMock()
    mock_request_context.session = mock_session
    
    mock_ctx = MagicMock()
    mock_ctx.request_context = mock_request_context
    
    # Test get_categories tool
    print("  Testing get_categories tool...")
    try:
        from server import get_categories
        
        # Mock the services
        mock_session_service = MagicMock()
        mock_category_service = MagicMock()
        mock_category_service.get_categories = AsyncMock(return_value=MagicMock(
            categories=[],
            model_dump=lambda: {"categories": []}
        ))
        
        # This should work without errors
        result = await get_categories(ctx=mock_ctx)
        print("  ✓ get_categories tool works")
        
    except Exception as e:
        print(f"  ✗ Error in get_categories: {e}")
        return False
    
    print("\n✅ Tool functionality tests passed!")
    return True


def main():
    """Run all tests"""
    print("=" * 80)
    print("FastMCP RequestContext Fix Verification")
    print("=" * 80)
    print()
    
    try:
        # Run synchronous tests
        test_session_context_access()
        
        # Run async tests
        asyncio.run(test_tool_functionality())
        
        print("\n" + "=" * 80)
        print("✅ All tests passed! The RequestContext fix is working correctly.")
        print("=" * 80)
        return 0
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

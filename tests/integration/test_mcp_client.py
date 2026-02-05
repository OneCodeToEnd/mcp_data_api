"""
Test MCP client connection to api-data-server
"""
import asyncio
import pytest
from fastmcp import Client
from fastmcp.client.transports import SSETransport
from fastmcp.client.transports import SSETransport


class TestMCPClient:
    """Test cases for MCP client connecting to api-data-server"""

    @pytest.fixture
    def server_url(self):
        """MCP server URL"""
        return "http://127.0.0.1:32001/data/api/mcp"

    @pytest.fixture
    def headers(self):
        """Custom headers for the MCP server"""
        return {
            "app_id": "984",
            "dbName": "hc_data_center"
        }

    @pytest.mark.asyncio
    async def test_connection_with_headers(self, server_url, headers):
        """Test basic connection to MCP server with custom headers"""
        # Create transport with custom headers
        transport = SSETransport(url=server_url, headers=headers)
        client = Client(transport)

        async with client:
            # Test that connection is established
            assert client is not None
            print(f"✓ Successfully connected to {server_url}")

    @pytest.mark.asyncio
    async def test_list_tools(self, server_url, headers):
        """Test listing available tools from MCP server"""
        transport = SSETransport(url=server_url, headers=headers)
        client = Client(transport)

        async with client:
            # List available tools
            tools = await client.list_tools()
            print(f"✓ Found {len(tools)} tools")

            # Print tool details
            for tool in tools:
                print(f"  - {tool.name}: {tool.description}")

            # Verify we got some tools
            assert len(tools) > 0, "Expected at least one tool"

    @pytest.mark.asyncio
    async def test_list_resources(self, server_url, headers):
        """Test listing available resources from MCP server"""
        transport = SSETransport(url=server_url, headers=headers)
        client = Client(transport)

        async with client:
            # List available resources
            resources = await client.list_resources()
            print(f"✓ Found {len(resources)} resources")

            # Print resource details
            for resource in resources:
                print(f"  - {resource.uri}: {resource.name}")

    @pytest.mark.asyncio
    async def test_call_tool(self, server_url, headers):
        """Test calling a tool on the MCP server"""
        transport = SSETransport(url=server_url, headers=headers)
        client = Client(transport)

        async with client:
            # First, list tools to find an available one
            tools = await client.list_tools()

            if len(tools) > 0:
                # Try to call the first tool
                tool_name = tools[0].name
                print(f"✓ Attempting to call tool: {tool_name}")

                # Call the tool with empty arguments (adjust as needed)
                try:
                    result = await client.call_tool(tool_name, {})
                    print(f"✓ Tool call successful")
                    print(f"  Result: {result}")
                except Exception as e:
                    print(f"  Note: Tool call failed (may need specific arguments): {e}")


async def main():
    """Manual test runner for quick verification"""
    test = TestMCPClient()
    server_url = "http://127.0.0.1:32001/data/api/mcp"
    headers = {
        "appId": "984",
        "dbName": "hc_data_center"
    }

    print("=" * 60)
    print("Testing MCP Client Connection")
    print("=" * 60)

    try:
        print("\n1. Testing connection...")
        await test.test_connection_with_headers(server_url, headers)

        print("\n2. Testing list_tools...")
        await test.test_list_tools(server_url, headers)

        print("\n3. Testing list_resources...")
        await test.test_list_resources(server_url, headers)

        print("\n4. Testing call_tool...")
        await test.test_call_tool(server_url, headers)

        print("\n" + "=" * 60)
        print("All tests completed!")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

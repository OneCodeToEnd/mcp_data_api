# MCP Client Configuration Guide

## Configuration for Claude Desktop

Add this to your Claude Desktop MCP settings file:

**Location**:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

### Option 1: SSE Transport (Recommended for Running Server)

```json
{
  "mcpServers": {
    "api-data-server": {
      "url": "http://127.0.0.1:32001/data/api/mcp",
      "transport": "sse",
      "env": {
        "SERVER_APP_ID": "test_app"
      }
    }
  }
}
```

**Note**: The `SERVER_APP_ID` environment variable sets the app_id for the session. If not specified, defaults to "test_app".

**Prerequisites**: Server must be running first
```bash
cd /Users/xiedi/data/rh/code/mcp_data_api
python -m src.server
```

### Option 2: stdio Transport (Auto-start Server)

```json
{
  "mcpServers": {
    "api-data-server": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "/Users/xiedi/data/rh/code/mcp_data_api",
      "env": {
        "PYTHONPATH": "/Users/xiedi/data/rh/code/mcp_data_api",
        "SERVER_APP_ID": "test_app"
      }
    }
  }
}
```

**Note**:
- The `SERVER_APP_ID` environment variable sets the app_id for the session
- For stdio transport, you need to modify `src/server.py` to use stdio instead of SSE:

```python
if __name__ == "__main__":
    mcp.run(transport="stdio")  # Change from "sse"
```

## Configuration for Other MCP Clients

### Generic MCP Client Configuration

```json
{
  "servers": [
    {
      "name": "API Data Server",
      "url": "http://127.0.0.1:32001/data/api/mcp",
      "transport": "sse",
      "description": "Progressive API discovery and execution server"
    }
  ]
}
```

## Testing the Connection

### Using curl

```bash
# Test server health
curl http://127.0.0.1:32001/data/api/mcp

# Test SSE connection
curl -N -H "Accept: text/event-stream" http://127.0.0.1:32001/data/api/mcp
```

### Using MCP Inspector

```bash
# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Connect to server
mcp-inspector http://127.0.0.1:32001/data/api/mcp
```

## Available Tools After Connection

Once connected, you'll have access to these 4 tools:

1. **get_categories** - Browse API categories
2. **get_apis_by_category** - List APIs in a category
3. **get_api_details** - Get API details (batch)
4. **execute_apis** - Execute multiple APIs

**Note**: The app_id is automatically initialized from the `SERVER_APP_ID` environment variable configured in your MCP client settings.

## Example Usage Flow

```
1. get_categories()
2. get_apis_by_category(category_id="user_management")
3. get_api_details(api_names=["get_user_info"])
4. execute_apis(executions=[{
     api_name: "get_user_info",
     parameters: {user_id: "12345"}
   }])
```

**Note**: No need to call initialize_session - the session is automatically initialized with the app_id from your MCP client configuration.

## Troubleshooting

### Server Not Running
```bash
# Check if server is running
lsof -i :32001

# Start server
cd /Users/xiedi/data/rh/code/mcp_data_api
python -m src.server
```

### Connection Refused
- Ensure server is running on port 32001
- Check firewall settings
- Verify URL: http://127.0.0.1:32001/data/api/mcp

### Tools Not Showing Up
- Restart Claude Desktop after config change
- Check Claude Desktop logs for errors
- Verify JSON syntax in config file

## Production Deployment

For production, consider:

1. **Use a process manager**:
```bash
# Using systemd, supervisor, or pm2
pm2 start "python -m src.server" --name mcp-api-server
```

2. **Add authentication** (if needed):
```json
{
  "mcpServers": {
    "api-data-server": {
      "url": "http://127.0.0.1:32001/data/api/mcp",
      "transport": "sse",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN"
      }
    }
  }
}
```

3. **Use HTTPS** for remote connections:
```json
{
  "mcpServers": {
    "api-data-server": {
      "url": "https://your-domain.com/data/api/mcp",
      "transport": "sse"
    }
  }
}
```

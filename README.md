# MCP Data API

A Model Context Protocol (MCP) server that provides access to data APIs, category management, and SQL query execution capabilities.

## Overview

MCP Data API is a FastMCP-based server that exposes various data access tools through the Model Context Protocol. It enables AI agents and applications to interact with backend services for API discovery, execution, and database queries.

## Features

- **Category Management**: Browse and navigate API categories in a hierarchical structure
- **API Discovery**: Search and retrieve API definitions by category or name
- **API Execution**: Execute APIs with dynamic parameters
- **SQL Query Execution**: Run SQL queries against configured databases
- **MCP Protocol Support**: Full compatibility with MCP clients and AI agents

## Architecture

The service acts as a bridge between MCP clients and backend services:

```
MCP Client → MCP Data API Server → Backend Services
                                    ├── chatgpt-api-service
                                    ├── chatdb-visual-service
                                    └── llm-workflow-service
```

## Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd mcp_data_api
```

2. Install dependencies:
```bash
pip install -e ".[dev]"
```

3. Configure environment variables (optional):
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Configuration

The MCP server requires the following headers for authentication:

- `app_id`: Application identifier (e.g., "984")
- `dbName`: Database name (e.g., "hc_data_center")

### MCP Client Configuration

Add the following to your MCP client configuration:

```json
{
  "mcpServers": {
    "api-data-server": {
      "url": "http://127.0.0.1:32001/data/api/mcp",
      "header": {
        "app_id": "984",
        "dbName": "hc_data_center"
      }
    }
  }
}
```

## Usage

### Starting the Server

```bash
# Development mode
python -m src.main

# Production mode with uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 32001
```

### Using with MCP Clients

#### Python Client Example

```python
from fastmcp import Client
from fastmcp.client.transports import SSETransport

# Configure transport with headers
transport = SSETransport(
    url="http://127.0.0.1:32001/data/api/mcp",
    headers={
        "app_id": "984",
        "dbName": "hc_data_center"
    }
)

# Create client
client = Client(transport)

async with client:
    # List available tools
    tools = await client.list_tools()
    print(f"Available tools: {[t.name for t in tools]}")

    # Call a tool
    result = await client.call_tool("get_categories", {})
    print(result)
```

## Available Tools

### 1. get_categories

Retrieves the hierarchical list of API categories.

**Parameters:**
- None

**Returns:** List of Category objects with flattened hierarchy

### 2. get_apis_by_category

Gets all APIs belonging to a specific category.

**Parameters:**
- `category_id` (integer): The category ID

**Returns:** List of APIBasic objects

### 3. get_api_details

Retrieves detailed information for specific APIs.

**Parameters:**
- `api_names` (string): Comma-separated list of API names

**Returns:** List of detailed API objects with parameter definitions

### 4. execute_api

Executes a single API with provided parameters.

**Parameters:**
- `api_name` (string): Name of the API to execute
- `parameters` (object): JSON object containing API parameters

**Returns:** API execution result

### 5. execute_sql

Executes a SQL query against the configured database.

**Parameters:**
- `sql` (string): SQL query to execute

**Returns:** Query results in standardized format

## Testing

### Run Unit Tests

```bash
pytest tests/unit -v
```

### Run Integration Tests

```bash
# Ensure the MCP server is running first
pytest tests/integration -v
```

### Manual Testing

Run the integration test script directly:

```bash
python tests/integration/test_mcp_client.py
```

## Project Structure

```
mcp_data_api/
├── src/
│   ├── models/          # Data models
│   ├── services/        # Business logic services
│   ├── tools/           # MCP tool implementations
│   ├── data_access/     # Data access layer
│   ├── cache/           # Caching implementations
│   └── utils/           # Utility functions
├── tests/
│   ├── unit/            # Unit tests
│   ├── integration/     # Integration tests
│   └── mock_data/       # Test data
├── docs/
│   └── API_DOCUMENTATION.md  # Detailed API documentation
├── pyproject.toml       # Project configuration
└── README.md           # This file
```

## API Documentation

For detailed API documentation, see [API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md).

## Development

### Code Style

The project uses:
- **Black** for code formatting
- **Ruff** for linting
- **pytest** for testing

Format code:
```bash
black src tests
```

Lint code:
```bash
ruff check src tests
```

### Adding New Tools

1. Define the tool in `src/tools/`
2. Implement the service logic in `src/services/`
3. Add tests in `tests/unit/` and `tests/integration/`
4. Update documentation

## Troubleshooting

### Connection Issues

If you encounter connection errors:

1. Verify the MCP server is running
2. Check that the URL and port are correct
3. Ensure headers (app_id, dbName) are properly configured
4. Verify backend services are accessible

### 405 Method Not Allowed

This error typically means:
- The MCP server is not running at the specified URL
- The endpoint path is incorrect
- The server doesn't support the MCP protocol at that endpoint

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

[Specify your license here]

## Support

For issues and questions:
- Create an issue in the repository
- Contact the development team

## Changelog

### Version 0.1.0 (2026-02-05)
- Initial release
- MCP server implementation
- Category and API management tools
- SQL query execution
- Integration tests
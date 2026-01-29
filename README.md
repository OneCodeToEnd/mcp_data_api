# MCP Data API Server

A FastMCP-based server for progressive API discovery and execution with mock data support.

## Features

- **5 MCP Tools**: Session initialization, category browsing, API discovery, API details, and execution
- **Session Management**: Stateful sessions with app_id context
- **Caching**: 1-hour TTL for metadata (categories, APIs)
- **Mock Data**: Realistic mock data for development and testing
- **Layered Architecture**: Easy migration to real backend APIs

## Server Information

- **Port**: 32001
- **MCP Path**: http://127.0.0.1:32001/data/api/mcp
- **Transport**: SSE (Server-Sent Events)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python -m src.server
```

## Available Tools

### 1. initialize_session
Initialize MCP session with app_id.

**Parameters**:
- `app_id` (string): Application identifier

**Example**:
```json
{
  "app_id": "test_app"
}
```

### 2. get_categories
Get all API categories for the current session.

**Parameters**: None (uses session app_id)

### 3. get_apis_by_category
Get all APIs in a specific category.

**Parameters**:
- `category_id` (string): Category identifier

### 4. get_api_details
Get detailed information for specific APIs.

**Parameters**:
- `api_names` (array of strings): List of API names

### 5. execute_apis
Execute multiple API calls.

**Parameters**:
- `executions` (array): List of execution requests
  - `api_name` (string): API name
  - `parameters` (object): API parameters

## Mock Data

The server includes mock data for two apps:

### test_app
- **Categories**: User Management, Order Management, Product Catalog
- **APIs**:
  - `get_user_info`: Get user information
  - `create_user`: Create a new user
  - `get_orders`: Get user orders
  - `search_products`: Search products

### demo_app
- **Categories**: Demo Category
- **APIs**: `demo_api`

## Configuration

Edit `config/config.yaml` to customize:

```yaml
server:
  host: "127.0.0.1"
  port: 32001
  mcp_path: "/data/api/mcp"

cache:
  enabled: true
  ttl: 3600
  type: "memory"
```

## Migration to Real API

To switch from mock data to real backend:

1. Update `config/config.yaml` with real API URL:
```yaml
backend:
  base_url: "https://your-api.example.com"
  api_key: "${API_KEY}"
```

2. Set API key in environment:
```bash
export BACKEND_API_KEY=your_api_key
```

3. Update `src/server.py` line 17:
```python
# Change from:
data_provider = MockDataProvider()
# To:
data_provider = APIDataProvider(settings)
```

4. Implement real API endpoints in `src/data_access/api_provider.py`

## Architecture

```
Presentation Layer (MCP Tools)
    ↓
Business Logic Layer (Services)
    ↓
Data Access Layer (Providers)
    ↓
Backend API / Mock Data
```

## Project Structure

```
src/
├── server.py              # FastMCP server entry point
├── config.py              # Configuration management
├── models/                # Pydantic data models
├── data_access/           # Data providers (mock + real API)
├── services/              # Business logic
├── cache/                 # Caching layer
├── tools/                 # MCP tool implementations
└── utils/                 # Error handling

config/
├── config.yaml            # Configuration file
└── .env.example           # Environment variables template
```

## Development

### Running Tests
```bash
pytest tests/
```

### Code Quality
```bash
black src/
ruff check src/
mypy src/
```

## License

MIT

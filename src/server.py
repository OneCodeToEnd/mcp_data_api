"""FastMCP Server Entry Point"""
from fastmcp import FastMCP, Context
from typing import List, Optional
import logging
import json
from .config import Settings
from .data_access import APIDataProvider
from .cache import MemoryCache
from .services import CategoryService, APIService, ExecutionService, SQLService
from .models import ExecutionRequest

# Initialize settings
settings = Settings.from_yaml()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.logging.level.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("mcp_data_api")

# Create FastMCP instance
mcp = FastMCP(name = "API Data Server",instructions="""
工具调用参数约束:
1. 调用get_api_details工具入参api_names必须是get_apis_by_category工具返回的name参数
""")

logger.info("=" * 80)
logger.info("MCP Data API Server Initializing")
logger.info("=" * 80)

# Create dependencies
logger.info("Creating data provider: APIDataProvider")
data_provider = APIDataProvider(settings)

logger.info(f"Creating cache: MemoryCache (TTL={settings.cache.ttl}s)")
cache = MemoryCache(default_ttl=settings.cache.ttl)

# Create services
logger.info("Initializing services:")
logger.info("  - CategoryService")
category_service = CategoryService(data_provider, cache)
logger.info("  - APIService")
api_service = APIService(data_provider, cache)
logger.info("  - ExecutionService")
execution_service = ExecutionService(data_provider)
logger.info("  - SQLService")
sql_service = SQLService(data_provider)
logger.info("All services initialized successfully")


def get_app_id_from_request() -> str:
    """
    Extract app_id from HTTP request with priority order:
    1. URL query parameters (?app-id=xxx or ?app_id=xxx)
    2. HTTP headers (X-App-Id, App-Id)
    3. Fallback to config default

    Supports:
    - Query params: app-id, app_id
    - Headers: X-App-Id, App-Id (case-insensitive)
    """
    # Try query parameters first
    try:
        from fastmcp.server.dependencies import get_http_request

        request = get_http_request()
        if request and hasattr(request, 'query_params'):
            query_params = request.query_params
            app_id = query_params.get("appId") or query_params.get("app_id")
            if app_id:
                logger.info(f"✓ app_id from URL query parameter: {app_id}")
                return app_id
    except Exception as e:
        logger.error(f"Could not extract app_id from query params: {e}")

    # Try headers second
    try:
        from fastmcp.server.dependencies import get_http_headers

        headers = get_http_headers()
        if headers:
            # Try common header names for app_id
            app_id = (
                headers.get("app_id") or
                headers.get("APP_ID")
            )
            if app_id:
                logger.info(f"✓ app_id from HTTP header: {app_id}")
                return app_id
    except Exception as e:
        logger.error(f"Could not extract app_id from headers: {e}")

    # Fallback to configured default
    logger.info(f"Using default app_id from config: {settings.server.app_id}")
    return settings.server.app_id


def get_db_name_from_request() -> Optional[str]:
    """
    Extract dbName from HTTP request headers

    Supports:
    - Headers: X-DB-Name, DB-Name, dbName (case-insensitive)

    Returns:
        Database name or None if not found
    """
    # Try headers
    try:
        from fastmcp.server.dependencies import get_http_headers

        headers = get_http_headers()
        if headers:
            db_name = (
                headers.get("x-db-name") or
                headers.get("X-DB-Name") or
                headers.get("db-name") or
                headers.get("DB-Name") or
                headers.get("dbname") or
                headers.get("dbName")
            )
            if db_name:
                logger.info(f"✓ dbName from HTTP header: {db_name}")
                return db_name
    except Exception as e:
        logger.error(f"Could not extract dbName from headers: {e}")

    logger.warning("dbName not found in request")
    return None


@mcp.tool()
async def get_categories(ctx: Context) -> dict:
    """
    Get all API categories for the current session.

    Returns:
        List of available categories
    """
    logger.info("=" * 80)
    logger.info("MCP TOOL CALL: get_categories")
    logger.info("=" * 80)
    logger.info("Description: Retrieve all available API categories")
    logger.info("Parameters: None")

    from .tools import get_categories_tool

    # Try to get app_id from context first (set by middleware)
    app_id = None

    # Fallback to extracting from HTTP request if not in context
    if not app_id:
        logger.info("app_id not found in context, falling back to request extraction")
        app_id = get_app_id_from_request()

    logger.info("Executing tool logic...")
    result = await get_categories_tool(app_id, category_service)

    logger.info(f"✓ Tool execution completed successfully")
    logger.info(f"  Result: Found {len(result.categories)} categories")
    logger.debug(f"  Categories: {[cat.name for cat in result.categories]}")
    logger.info("=" * 80)

    return result.model_dump()


@mcp.tool()
async def get_apis_by_category(category_id: str, ctx: Context) -> dict:
    """
    Get all APIs in a specific category.

    Args:
        category_id: Category identifier

    Returns:
        List of APIs with basic information
    """
    logger.info("=" * 80)
    logger.info("MCP TOOL CALL: get_apis_by_category")
    logger.info("=" * 80)
    logger.info("Description: Retrieve all APIs in a specific category")
    logger.info(f"Parameters:")
    logger.info(f"  - category_id: {category_id}")

    from .tools import get_apis_by_category_tool

    # Try to get app_id from context first (set by middleware)
    app_id = None

    # Fallback to extracting from HTTP request if not in context
    if not app_id:
        logger.info("app_id not found in context, falling back to request extraction")
        app_id = get_app_id_from_request()

    logger.info("Executing tool logic...")
    result = await get_apis_by_category_tool(app_id, api_service, category_id)

    logger.info(f"✓ Tool execution completed successfully")
    logger.info(f"  Result: Found {len(result.apis)} APIs in category '{category_id}'")
    logger.debug(f"  APIs: {[api.name for api in result.apis]}")
    logger.info("=" * 80)

    return result.model_dump()


@mcp.tool()
async def get_api_details(api_names: List[str], ctx: Context) -> dict:
    """
    Get detailed information for specific APIs.

    Args:
        api_names: List of API names to get details (请注意使用get_apis_by_category工具中的 name 字段中的值，而不是description字段)

    Returns:
        Detailed API information including parameters
    """
    logger.info("=" * 80)
    logger.info("MCP TOOL CALL: get_api_details")
    logger.info("=" * 80)
    logger.info("Description: Retrieve detailed information for specific APIs")
    logger.info(f"Parameters:")
    logger.info(f"  - api_names: {api_names} (count: {len(api_names)})")

    from .tools import get_api_details_tool

    # Try to get app_id from context first (set by middleware)
    app_id = None

    # Fallback to extracting from HTTP request if not in context
    if not app_id:
        logger.info("app_id not found in context, falling back to request extraction")
        app_id = get_app_id_from_request()

    logger.info("Executing tool logic...")
    result = await get_api_details_tool(app_id, api_service, api_names)

    logger.info(f"✓ Tool execution completed successfully")
    logger.info(f"  Result: Retrieved details for {len(result.apis)} APIs")
    for api in result.apis:
        logger.debug(f"    - {api.name}: {len(api.parameters)} parameters")
    logger.info("=" * 80)

    return result.model_dump()


@mcp.tool()
async def execute_apis(executions: List[dict], ctx: Context) -> dict:
    """
    Execute multiple API calls.

    Args:
        executions: List of API execution requests (each with api_name and parameters)

    Returns:
        Execution results for all APIs
    """
    logger.info("=" * 80)
    logger.info("MCP TOOL CALL: execute_apis")
    logger.info("=" * 80)
    logger.info("Description: Execute multiple API calls")
    logger.info(f"Parameters:")
    logger.info(f"  - executions: {len(executions)} API call(s)")
    for i, ex in enumerate(executions, 1):
        logger.info(f"    [{i}] api_name: {ex.get('api_name')}")
        logger.debug(f"        parameters: {json.dumps(ex.get('parameters', {}), indent=10)}")

    from .tools import execute_apis_tool

    # Try to get app_id from context first (set by middleware)
    app_id = None

    # Fallback to extracting from HTTP request if not in context
    if not app_id:
        logger.info("app_id not found in context, falling back to request extraction")
        app_id = get_app_id_from_request()

    # Convert dict to ExecutionRequest objects
    logger.info("Converting execution requests to ExecutionRequest objects...")
    execution_requests = [ExecutionRequest(**ex) for ex in executions]

    logger.info("Executing tool logic...")
    result = await execute_apis_tool(
        app_id, execution_service, execution_requests
    )

    logger.info(f"✓ Tool execution completed")
    logger.info(f"  Result: Executed {len(result.results)} API call(s)")
    for i, res in enumerate(result.results, 1):
        status = "✓ SUCCESS" if res.success else "✗ FAILED"
        logger.info(f"    [{i}] {res.api_name}: {status}")
        if not res.success:
            logger.warning(f"        Error: {res.error}")
        else:
            logger.debug(f"        Response: {json.dumps(res.data, indent=10)}")
    logger.info("=" * 80)

    return result.model_dump()


@mcp.tool()
async def get_sql_tables(ctx: Context) -> dict:
    """
    Get list of all tables in the database with their comments.

    Returns:
        List of tables with names and comments
    """
    logger.info("=" * 80)
    logger.info("MCP TOOL CALL: get_sql_tables")
    logger.info("=" * 80)

    from .tools import get_sql_tables_tool

    app_id = ctx.get_state('app_id') or get_app_id_from_request()
    db_name = get_db_name_from_request()

    logger.info(f"✓ app_id: {app_id}")
    if db_name:
        logger.info(f"✓ dbName: {db_name}")
    else:
        logger.warning("✗ dbName not found")

    result = await get_sql_tables_tool(app_id, sql_service, db_name)

    logger.info(f"✓ Found {len(result.tables)} tables")
    logger.info("=" * 80)

    return result.model_dump()


@mcp.tool()
async def get_sql_table_fields(table_names: List[str], ctx: Context) -> dict:
    """
    Get detailed field information for specified tables.

    Args:
        table_names: List of table names to get field information for

    Returns:
        Field information for each table
    """
    logger.info("=" * 80)
    logger.info("MCP TOOL CALL: get_sql_table_fields")
    logger.info("=" * 80)
    logger.info(f"Parameters: table_names={table_names}")

    from .tools import get_sql_table_fields_tool

    app_id = ctx.get_state('app_id') or get_app_id_from_request()
    db_name = get_db_name_from_request()

    logger.info(f"✓ app_id: {app_id}")
    if db_name:
        logger.info(f"✓ dbName: {db_name}")
    else:
        logger.warning("✗ dbName not found")

    result = await get_sql_table_fields_tool(app_id, sql_service, db_name, table_names)

    logger.info(f"✓ Retrieved fields for {len(result.table_fields)} tables")
    logger.info("=" * 80)

    return result.model_dump()


@mcp.tool()
async def execute_sql(sql: str, ctx: Context) -> dict:
    """
    Execute an arbitrary SQL query against the database.

    Args:
        sql: SQL query to execute

    Returns:
        Query results with data and schema information
    """
    logger.info("=" * 80)
    logger.info("MCP TOOL CALL: execute_sql")
    logger.info("=" * 80)
    logger.info(f"SQL: {sql[:100]}..." if len(sql) > 100 else f"SQL: {sql}")

    from .tools import execute_sql_tool

    app_id = ctx.get_state('app_id') or get_app_id_from_request()
    db_name = get_db_name_from_request()

    logger.info(f"✓ app_id: {app_id}")
    if db_name:
        logger.info(f"✓ dbName: {db_name}")
    else:
        logger.warning("✗ dbName not found")

    result = await execute_sql_tool(app_id, sql_service, db_name, sql)

    if result.result.success:
        logger.info(f"✓ Success - {len(result.result.data or [])} rows")
    else:
        logger.warning(f"✗ Failed - {result.result.error}")
    logger.info("=" * 80)

    return result.model_dump()


if __name__ == "__main__":
    logger.info("=" * 80)
    logger.info("Starting MCP Data API Server")
    logger.info(f"  Transport: SSE")
    logger.info(f"  Host: {settings.server.host}")
    logger.info(f"  Port: {settings.server.port}")
    logger.info(f"  Path: {settings.server.mcp_path}")
    logger.info(f"  Default App ID: {settings.server.app_id}")
    logger.info("=" * 80)

    mcp.run(
        transport="sse",
        host=settings.server.host,
        port=settings.server.port,
        path="/data/api/mcp"
    )

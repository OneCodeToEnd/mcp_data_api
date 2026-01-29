"""FastMCP Server Entry Point"""
from fastmcp import FastMCP, Context
from typing import List
import logging
import json
import contextvars
from urllib.parse import urlparse, parse_qs
from .config import Settings
from .data_access import MockDataProvider
from .cache import MemoryCache
from .services import SessionService, CategoryService, APIService, ExecutionService
from .models import SessionContext, ExecutionRequest

# Context variable to store app_id for current request
current_app_id = contextvars.ContextVar("current_app_id", default=None)

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
mcp = FastMCP("API Data Server")
logger.info("=" * 80)
logger.info("MCP Data API Server Initializing")
logger.info("=" * 80)

# Create dependencies
logger.info("Creating data provider: MockDataProvider")
data_provider = MockDataProvider()

logger.info(f"Creating cache: MemoryCache (TTL={settings.cache.ttl}s)")
cache = MemoryCache(default_ttl=settings.cache.ttl)

# Create services
logger.info("Initializing services:")
logger.info("  - SessionService")
session_service = SessionService(data_provider)
logger.info("  - CategoryService")
category_service = CategoryService(data_provider, cache)
logger.info("  - APIService")
api_service = APIService(data_provider, cache)
logger.info("  - ExecutionService")
execution_service = ExecutionService(data_provider)
logger.info("All services initialized successfully")


def get_app_id_from_request() -> str:
    """
    Extract app_id from HTTP request headers using get_http_headers().

    Supports headers:
    - X-App-Id (case-insensitive)
    - App-Id (case-insensitive)
    """
    try:
        from fastmcp.server.dependencies import get_http_headers

        headers = get_http_headers()
        if headers:
            # Try common header names for app_id
            app_id = (
                headers.get("x-app-id") or
                headers.get("X-App-Id") or
                headers.get("app-id") or
                headers.get("App-Id")
            )
            if app_id:
                logger.info(f"✓ app_id extracted from HTTP header: {app_id}")
                return app_id
    except Exception as e:
        logger.debug(f"Could not extract app_id from headers: {e}")

    # Fallback to configured default
    logger.info(f"Using default app_id from config: {settings.server.app_id}")
    return settings.server.app_id


def get_session_context(ctx: Context) -> SessionContext:
    """
    Get session context from FastMCP context.

    Auto-initializes from HTTP header X-App-Id if not already set.

    Args:
        ctx: FastMCP context

    Returns:
        Session context
    """
    logger.debug("-" * 60)
    logger.debug("CONTEXT RETRIEVAL: Getting session context")

    # Use FastMCP's state management (set_state/get_state)
    session_ctx = ctx.get_state("session_context")

    if session_ctx is not None:
        logger.info(f"✓ Session context found - app_id: {session_ctx.app_id}, initialized: {session_ctx.initialized}")
        logger.debug(f"  Session details: {session_ctx.model_dump()}")
        return session_ctx

    # No existing session context - auto-initialize from request headers
    logger.info("✗ No existing session context found, auto-initializing from HTTP header...")

    # Extract app_id from request headers
    app_id = get_app_id_from_request()

    # Create and store initialized session context
    session_ctx = SessionContext(
        app_id=app_id,
        initialized=True
    )
    ctx.set_state("session_context", session_ctx)

    logger.info(f"✓ Session auto-initialized with app_id: {app_id}")
    logger.debug(f"  Session details: {session_ctx.model_dump()}")
    logger.debug("-" * 60)
    return session_ctx


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

    # Get session context
    session_ctx = get_session_context(ctx)

    logger.info("Executing tool logic...")
    result = await get_categories_tool(session_ctx, session_service, category_service)

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

    # Get session context
    session_ctx = get_session_context(ctx)

    logger.info("Executing tool logic...")
    result = await get_apis_by_category_tool(
        session_ctx, session_service, api_service, category_id
    )

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
        api_names: List of API names to get details for

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

    # Get session context
    session_ctx = get_session_context(ctx)

    logger.info("Executing tool logic...")
    result = await get_api_details_tool(
        session_ctx, session_service, api_service, api_names
    )

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

    # Get session context
    session_ctx = get_session_context(ctx)

    # Convert dict to ExecutionRequest objects
    logger.info("Converting execution requests to ExecutionRequest objects...")
    execution_requests = [ExecutionRequest(**ex) for ex in executions]

    logger.info("Executing tool logic...")
    result = await execute_apis_tool(
        session_ctx, session_service, execution_service, execution_requests
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
        path=settings.server.mcp_path
    )

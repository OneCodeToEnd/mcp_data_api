"""FastMCP Server Entry Point"""
from fastmcp import FastMCP, Context
from typing import List
from .config import Settings
from .data_access import MockDataProvider
from .cache import MemoryCache
from .services import SessionService, CategoryService, APIService, ExecutionService
from .models import SessionContext, ExecutionRequest

# Initialize settings
settings = Settings.from_yaml()

# Create FastMCP instance
mcp = FastMCP("API Data Server")

# Create dependencies
data_provider = MockDataProvider()
cache = MemoryCache(default_ttl=settings.cache.ttl)

# Create services
session_service = SessionService(data_provider)
category_service = CategoryService(data_provider, cache)
api_service = APIService(data_provider, cache)
execution_service = ExecutionService(data_provider)


def get_session_context(ctx: Context) -> SessionContext:
    """Get or create session context from FastMCP context"""
    if "session_context" not in ctx.request_context.session:
        ctx.request_context.session["session_context"] = SessionContext()
    return ctx.request_context.session["session_context"]


@mcp.tool()
async def initialize_session(app_id: str, ctx: Context) -> dict:
    """
    Initialize MCP session with app_id.

    Args:
        app_id: Application identifier

    Returns:
        Initialization result with success status
    """
    from .tools import initialize_session_tool

    session_ctx = get_session_context(ctx)
    result = await initialize_session_tool(session_ctx, session_service, app_id)
    return result.model_dump()


@mcp.tool()
async def get_categories(ctx: Context) -> dict:
    """
    Get all API categories for the current session.

    Returns:
        List of available categories
    """
    from .tools import get_categories_tool

    session_ctx = get_session_context(ctx)
    result = await get_categories_tool(session_ctx, session_service, category_service)
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
    from .tools import get_apis_by_category_tool

    session_ctx = get_session_context(ctx)
    result = await get_apis_by_category_tool(
        session_ctx, session_service, api_service, category_id
    )
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
    from .tools import get_api_details_tool

    session_ctx = get_session_context(ctx)
    result = await get_api_details_tool(
        session_ctx, session_service, api_service, api_names
    )
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
    from .tools import execute_apis_tool

    session_ctx = get_session_context(ctx)

    # Convert dict to ExecutionRequest objects
    execution_requests = [ExecutionRequest(**ex) for ex in executions]

    result = await execute_apis_tool(
        session_ctx, session_service, execution_service, execution_requests
    )
    return result.model_dump()


if __name__ == "__main__":
    # Run the MCP server
    mcp.run(
        transport="sse",
        host=settings.server.host,
        port=settings.server.port,
        path=settings.server.mcp_path
    )

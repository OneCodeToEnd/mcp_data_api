"""API tools"""
from typing import List
from ..models import SessionContext, APIsResponse, APIDetailsResponse
from ..services import SessionService, APIService


async def get_apis_by_category_tool(
    session_ctx: SessionContext,
    session_service: SessionService,
    api_service: APIService,
    category_id: str
) -> APIsResponse:
    """
    Get all APIs in a specific category

    Args:
        session_ctx: Session context
        session_service: Session service instance
        api_service: API service instance
        category_id: Category identifier

    Returns:
        List of APIs with basic information
    """
    session_service.validate_session(session_ctx)

    apis = await api_service.get_apis_by_category(session_ctx, category_id)

    return APIsResponse(apis=apis)


async def get_api_details_tool(
    session_ctx: SessionContext,
    session_service: SessionService,
    api_service: APIService,
    api_names: List[str]
) -> APIDetailsResponse:
    """
    Get detailed information for specific APIs

    Args:
        session_ctx: Session context
        session_service: Session service instance
        api_service: API service instance
        api_names: List of API names

    Returns:
        Detailed API information including parameters
    """
    session_service.validate_session(session_ctx)

    apis = await api_service.get_api_details(session_ctx, api_names)

    return APIDetailsResponse(apis=apis)

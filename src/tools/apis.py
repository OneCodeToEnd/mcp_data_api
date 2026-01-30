"""API tools"""
from typing import List
from ..models import APIsResponse, APIDetailsResponse
from ..services import APIService


async def get_apis_by_category_tool(
    app_id: str,
    api_service: APIService,
    category_id: str
) -> APIsResponse:
    """
    Get all APIs in a specific category

    Args:
        app_id: Application identifier
        api_service: API service instance
        category_id: Category identifier

    Returns:
        List of APIs with basic information
    """
    apis = await api_service.get_apis_by_category(app_id, category_id)

    return APIsResponse(apis=apis)


async def get_api_details_tool(
    app_id: str,
    api_service: APIService,
    api_names: List[str]
) -> APIDetailsResponse:
    """
    Get detailed information for specific APIs

    Args:
        app_id: Application identifier
        api_service: API service instance
        api_names: List of API names

    Returns:
        Detailed API information including parameters
    """
    apis = await api_service.get_api_details(app_id, api_names)

    return APIDetailsResponse(apis=apis)

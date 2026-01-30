"""Categories tool"""
from ..models import CategoriesResponse
from ..services import CategoryService


async def get_categories_tool(
    app_id: str,
    category_service: CategoryService
) -> CategoriesResponse:
    """
    Get all API categories for the current session

    Args:
        app_id: Application identifier
        category_service: Category service instance

    Returns:
        List of categories
    """

    # Get categories
    categories = await category_service.get_categories(app_id)

    return CategoriesResponse(categories=categories)

"""Categories tool"""
from ..models import SessionContext, CategoriesResponse
from ..services import SessionService, CategoryService


async def get_categories_tool(
    session_ctx: SessionContext,
    session_service: SessionService,
    category_service: CategoryService
) -> CategoriesResponse:
    """
    Get all API categories for the current session

    Args:
        session_ctx: Session context
        session_service: Session service instance
        category_service: Category service instance

    Returns:
        List of categories
    """
    # Validate session
    session_service.validate_session(session_ctx)

    # Get categories
    categories = await category_service.get_categories(session_ctx)

    return CategoriesResponse(categories=categories)

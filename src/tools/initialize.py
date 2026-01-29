"""Initialize session tool"""
from ..models import SessionContext, InitializeResponse
from ..services import SessionService


async def initialize_session_tool(
    session_ctx: SessionContext,
    session_service: SessionService,
    app_id: str
) -> InitializeResponse:
    """
    Initialize MCP session with app_id

    Args:
        session_ctx: Session context
        session_service: Session service instance
        app_id: Application identifier

    Returns:
        Initialization result
    """
    # Initialize session
    updated_ctx = await session_service.initialize_session(session_ctx, app_id)

    return InitializeResponse(
        success=True,
        message="Session initialized successfully",
        app_id=app_id
    )

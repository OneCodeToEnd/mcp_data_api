"""Session management service"""
from ..models import SessionContext
from ..data_access import DataProvider
from ..utils.errors import InvalidAppIdError, SessionNotInitializedError


class SessionService:
    """Service for managing session state"""

    def __init__(self, data_provider: DataProvider):
        """
        Initialize session service

        Args:
            data_provider: Data provider instance
        """
        self._data_provider = data_provider

    async def initialize_session(
        self, context: SessionContext, app_id: str
    ) -> SessionContext:
        """
        Initialize session with app_id

        Args:
            context: Session context
            app_id: Application identifier

        Returns:
            Updated session context

        Raises:
            InvalidAppIdError: If app_id is invalid
        """
        # Validate app_id
        is_valid = await self._data_provider.validate_app_id(app_id)
        if not is_valid:
            raise InvalidAppIdError(app_id)

        # Update context
        context.app_id = app_id
        context.initialized = True
        return context

    def validate_session(self, context: SessionContext) -> None:
        """
        Validate that session is initialized

        Args:
            context: Session context

        Raises:
            SessionNotInitializedError: If session is not initialized
        """
        if not context or not context.is_initialized():
            raise SessionNotInitializedError()

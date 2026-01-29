"""Custom exception classes for MCP Data API"""


class MCPDataAPIError(Exception):
    """Base exception for all MCP Data API errors"""
    def __init__(self, code: str, message: str, details: dict = None):
        self.code = code
        self.message = message
        self.details = details or {}
        super().__init__(message)

    def to_dict(self) -> dict:
        """Convert error to dictionary format"""
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.details
            }
        }


class SessionNotInitializedError(MCPDataAPIError):
    """Raised when session is not initialized"""
    def __init__(self):
        super().__init__(
            code="SESSION_NOT_INITIALIZED",
            message="Session not initialized. Call initialize_session first."
        )


class InvalidAppIdError(MCPDataAPIError):
    """Raised when app_id is invalid"""
    def __init__(self, app_id: str):
        super().__init__(
            code="INVALID_APP_ID",
            message=f"Invalid app_id: {app_id}",
            details={"app_id": app_id}
        )


class CategoryNotFoundError(MCPDataAPIError):
    """Raised when category is not found"""
    def __init__(self, category_id: str):
        super().__init__(
            code="CATEGORY_NOT_FOUND",
            message=f"Category not found: {category_id}",
            details={"category_id": category_id}
        )


class APINotFoundError(MCPDataAPIError):
    """Raised when API is not found"""
    def __init__(self, api_name: str):
        super().__init__(
            code="API_NOT_FOUND",
            message=f"API not found: {api_name}",
            details={"api_name": api_name}
        )


class APIExecutionError(MCPDataAPIError):
    """Raised when API execution fails"""
    def __init__(self, api_name: str, error: str):
        super().__init__(
            code="API_EXECUTION_ERROR",
            message=f"API execution failed: {api_name}",
            details={"api_name": api_name, "error": error}
        )


class ParameterValidationError(MCPDataAPIError):
    """Raised when parameter validation fails"""
    def __init__(self, api_name: str, parameter: str, error: str):
        super().__init__(
            code="PARAMETER_VALIDATION_ERROR",
            message=f"Parameter validation failed for {api_name}.{parameter}: {error}",
            details={"api_name": api_name, "parameter": parameter, "error": error}
        )

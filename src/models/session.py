from pydantic import BaseModel
from typing import Optional


class SessionContext(BaseModel):
    """Session context for storing app_id and state"""
    app_id: Optional[str] = None
    initialized: bool = False

    def is_initialized(self) -> bool:
        """Check if session is initialized"""
        return self.initialized and self.app_id is not None

from pydantic import BaseModel
from typing import Any, Optional


class ExecutionRequest(BaseModel):
    """API execution request"""
    api_name: str
    parameters: dict


class ExecutionResult(BaseModel):
    """API execution result"""
    api_name: str
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None

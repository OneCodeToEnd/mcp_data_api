from pydantic import BaseModel
from typing import List, Any, Optional


class Parameter(BaseModel):
    """API parameter model"""
    name: str
    type: str  # string, number, boolean, object, array
    required: bool
    description: str
    default: Optional[Any] = None


class APIBasic(BaseModel):
    """Basic API information (name and description only)"""
    name: str
    description: str
    category_id: str


class APIDetail(APIBasic):
    """Detailed API information including parameters"""
    parameters: List[Parameter]
    response_schema: dict

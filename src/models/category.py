from pydantic import BaseModel


class Category(BaseModel):
    """API category model"""
    id: str
    name: str
    description: str

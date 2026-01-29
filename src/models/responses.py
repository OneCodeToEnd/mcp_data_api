from pydantic import BaseModel
from typing import List
from .category import Category
from .api import APIBasic, APIDetail
from .execution import ExecutionResult


class InitializeResponse(BaseModel):
    """Response for initialize_session tool"""
    success: bool
    message: str
    app_id: str


class CategoriesResponse(BaseModel):
    """Response for get_categories tool"""
    categories: List[Category]


class APIsResponse(BaseModel):
    """Response for get_apis_by_category tool"""
    apis: List[APIBasic]


class APIDetailsResponse(BaseModel):
    """Response for get_api_details tool"""
    apis: List[APIDetail]


class ExecutionResponse(BaseModel):
    """Response for execute_apis tool"""
    results: List[ExecutionResult]

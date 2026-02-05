from pydantic import BaseModel
from typing import List, Optional
from .category import Category
from .api import APIBasic, APIDetail
from .execution import ExecutionResult
from .sql import TableInfo, TableFieldsInfo, SQLExecutionResult


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


class TablesResponse(BaseModel):
    """Response for get_sql_tables tool"""
    tables: List[TableInfo]
    database_name: Optional[str] = None


class TableFieldsResponse(BaseModel):
    """Response for get_sql_table_fields tool"""
    table_fields: List[TableFieldsInfo]


class SQLExecutionResponse(BaseModel):
    """Response for execute_sql tool"""
    result: SQLExecutionResult

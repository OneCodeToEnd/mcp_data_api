"""SQL-related data models"""
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Any


class TableInfo(BaseModel):
    """Database table information"""
    name: str = Field(description="Table name")
    comment: Optional[str] = Field(default="", description="Table comment")


class FieldInfo(BaseModel):
    """Database field/column information"""
    name: str = Field(description="Field name")
    type: str = Field(description="Data type")
    comment: Optional[str] = Field(default="", description="Field comment")
    nullable: bool = Field(default=True, description="Whether field can be NULL")
    default_value: Optional[str] = Field(default=None, description="Default value")
    key_type: Optional[str] = Field(default="", description="Key type (PRI, UNI, MUL)")


class TableFieldsInfo(BaseModel):
    """Field information for a specific table"""
    table_name: str = Field(description="Table name")
    fields: List[FieldInfo] = Field(description="List of fields")


class SQLExecutionResult(BaseModel):
    """SQL execution result"""
    model_config = ConfigDict(populate_by_name=True)

    success: bool = Field(description="Whether execution succeeded")
    data: Optional[List[dict]] = Field(default=None, description="Query result data")
    result_schema: Optional[List[dict]] = Field(default=None, description="Result schema", alias="schema")
    error: Optional[str] = Field(default=None, description="Error message if failed")


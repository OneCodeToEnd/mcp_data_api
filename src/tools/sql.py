"""SQL tools"""
import logging
from typing import List, Optional
from ..models import TablesResponse, TableFieldsResponse, SQLExecutionResponse, SQLExecutionResult
from ..services import SQLService

logger = logging.getLogger(__name__)


async def get_sql_tables_tool(
    app_id: str,
    sql_service: SQLService,
    db_name: Optional[str]
) -> TablesResponse:
    """Get list of database tables with comments"""
    if not db_name:
        logger.warning("dbName not configured, returning empty table list")
        return TablesResponse(tables=[], database_name=None)

    tables = await sql_service.get_tables(app_id, db_name)
    return TablesResponse(tables=tables, database_name=db_name)


async def get_sql_table_fields_tool(
    app_id: str,
    sql_service: SQLService,
    db_name: Optional[str],
    table_names: List[str]
) -> TableFieldsResponse:
    """Get field information for specified tables"""
    if not db_name:
        logger.warning("dbName not configured, returning empty fields list")
        return TableFieldsResponse(table_fields=[])

    if not table_names:
        logger.warning("No table names provided")
        return TableFieldsResponse(table_fields=[])

    table_fields = await sql_service.get_table_fields(app_id, db_name, table_names)
    return TableFieldsResponse(table_fields=table_fields)


async def execute_sql_tool(
    app_id: str,
    sql_service: SQLService,
    db_name: Optional[str],
    sql: str
) -> SQLExecutionResponse:
    """Execute arbitrary SQL query"""
    if not db_name:
        return SQLExecutionResponse(
            result=SQLExecutionResult(
                success=False,
                error="dbName not configured in request headers"
            )
        )

    if not sql or not sql.strip():
        return SQLExecutionResponse(
            result=SQLExecutionResult(
                success=False,
                error="SQL query is empty"
            )
        )

    result = await sql_service.execute_sql(app_id, db_name, sql)
    return SQLExecutionResponse(result=result)

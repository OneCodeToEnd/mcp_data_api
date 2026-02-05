"""SQL service for database operations"""
import asyncio
import logging
from typing import List
from ..data_access import DataProvider
from ..models import TableInfo, FieldInfo, TableFieldsInfo, SQLExecutionResult

logger = logging.getLogger(__name__)


class SQLService:
    """Service for SQL operations"""

    def __init__(self, data_provider: DataProvider):
        self._data_provider = data_provider

    async def get_tables(self, app_id: str, db_name: str) -> List[TableInfo]:
        """Get table list using information_schema"""
        sql = """
        SELECT table_name AS name, table_comment AS comment
        FROM information_schema.tables
        WHERE table_schema = DATABASE() AND table_type = 'BASE TABLE'
        ORDER BY table_name
        """

        try:
            response = await self._data_provider.execute_sql(app_id, sql, db_name)
            data, _ = self._parse_sql_response(response.get("data", []))
            return [TableInfo(**row) for row in data]
        except Exception as e:
            logger.error(f"Error getting tables: {e}")
            return []

    async def get_table_fields(
        self, app_id: str, db_name: str, table_names: List[str]
    ) -> List[TableFieldsInfo]:
        """Get fields for multiple tables concurrently"""
        tasks = [
            self._get_single_table_fields(app_id, db_name, table)
            for table in table_names
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [r for r in results if isinstance(r, TableFieldsInfo)]

    async def _get_single_table_fields(
        self, app_id: str, db_name: str, table_name: str
    ) -> TableFieldsInfo:
        """Get fields for a single table"""
        sql = f"""
        SELECT column_name AS name, data_type AS type, column_comment AS comment,
               is_nullable AS nullable, column_default AS default_value,
               column_key AS key_type
        FROM information_schema.columns
        WHERE table_schema = DATABASE() AND table_name = '{table_name}'
        ORDER BY ordinal_position
        """

        try:
            response = await self._data_provider.execute_sql(app_id, sql, db_name)
            data, _ = self._parse_sql_response(response.get("data", []))
            fields = [FieldInfo(**row) for row in data]
            return TableFieldsInfo(table_name=table_name, fields=fields)
        except Exception as e:
            logger.error(f"Error getting fields for table {table_name}: {e}")
            return TableFieldsInfo(table_name=table_name, fields=[])

    async def execute_sql(
        self, app_id: str, db_name: str, sql: str
    ) -> SQLExecutionResult:
        """Execute arbitrary SQL"""
        try:
            response = await self._data_provider.execute_sql(app_id, sql, db_name)
            data, schema = self._parse_sql_response(response.get("data", []))
            return SQLExecutionResult(success=True, data=data, result_schema=schema)
        except Exception as e:
            logger.error(f"Error executing SQL: {e}")
            return SQLExecutionResult(success=False, error=str(e))

    def _parse_sql_response(self, response_data: List[dict]) -> tuple:
        """Extract output_standard_chart and output_json_schema"""
        data, schema = [], []
        for item in response_data:
            if isinstance(item, dict):
                if item.get("name") == "output_standard_chart":
                    data = item.get("value", [])
                elif item.get("name") == "output_json_schema":
                    schema = item.get("value", [])
        return data, schema


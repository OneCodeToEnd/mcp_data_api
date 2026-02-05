"""Abstract base class for data providers"""
from abc import ABC, abstractmethod
from typing import List
from ..models import Category, APIBasic, APIDetail, ExecutionRequest, ExecutionResult


class DataProvider(ABC):
    """Abstract base class for data providers"""

    @abstractmethod
    async def validate_app_id(self, app_id: str) -> bool:
        """
        Validate if app_id is valid

        Args:
            app_id: Application identifier

        Returns:
            True if valid, False otherwise
        """
        pass

    @abstractmethod
    async def get_categories(self, app_id: str) -> List[Category]:
        """
        Get all categories for an app

        Args:
            app_id: Application identifier

        Returns:
            List of categories
        """
        pass

    @abstractmethod
    async def get_apis_by_category(
        self, app_id: str, category_id: str
    ) -> List[APIBasic]:
        """
        Get all APIs in a category

        Args:
            app_id: Application identifier
            category_id: Category identifier

        Returns:
            List of basic API information
        """
        pass

    @abstractmethod
    async def get_api_details(
        self, app_id: str, api_names: List[str]
    ) -> List[APIDetail]:
        """
        Get detailed information for specific APIs

        Args:
            app_id: Application identifier
            api_names: List of API names

        Returns:
            List of detailed API information
        """
        pass

    @abstractmethod
    async def execute_api(
        self, app_id: str, execution: ExecutionRequest
    ) -> ExecutionResult:
        """
        Execute a single API call

        Args:
            app_id: Application identifier
            execution: Execution request

        Returns:
            Execution result
        """
        pass

    @abstractmethod
    async def execute_sql(self, app_id: str, sql: str, source_name: str) -> dict:
        """
        Execute SQL query

        Args:
            app_id: Application identifier
            sql: SQL query to execute
            source_name: Database name (from dbName header)

        Returns:
            Raw backend response
        """
        pass

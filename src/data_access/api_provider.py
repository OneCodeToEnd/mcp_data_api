"""Real API data provider - connects to backend (Phase 2)"""
import httpx
import logging
from typing import List
from .base import DataProvider
from ..models import Category, APIBasic, APIDetail, ExecutionRequest, ExecutionResult, Parameter
from ..config import Settings
from ..utils.errors import InvalidAppIdError, CategoryNotFoundError, APINotFoundError, APIExecutionError

logger = logging.getLogger(__name__)


class APIDataProvider(DataProvider):
    """Real API data provider - connects to backend"""

    def __init__(self, settings: Settings):
        """
        Initialize API data provider with two separate HTTP clients

        Args:
            settings: Application settings
        """
        self._settings = settings

        # Client for chatgpt-api-service (categories)
        self._chatgpt_client = httpx.AsyncClient(
            base_url=settings.backend.chatgpt_service_url,
            timeout=settings.backend.timeout
        )

        # Client for chatdb-visual-service (APIs and execution)
        self._chatdb_client = httpx.AsyncClient(
            base_url=settings.backend.chatdb_service_url,
            timeout=settings.backend.timeout
        )

        self._workflow_client = httpx.AsyncClient(
            base_url=settings.backend.workflow_service_url,
            timeout=settings.backend.timeout
        )

    async def validate_app_id(self, app_id: str) -> bool:
        """Validate app_id with backend by attempting to get categories"""
        try:
            response = await self._chatgpt_client.get(
                "/file/directory",
                params={"appId": app_id, "source": "API"}
            )
            response.raise_for_status()
            data = response.json()

            # Check if response is successful
            return data.get("message", {}).get("code") == 0

        except (httpx.HTTPStatusError, httpx.RequestError) as e:
            logger.error(f"Error validating app_id {app_id}: {e}")
            return False

    async def get_categories(self, app_id: str) -> List[Category]:
        """Get categories from backend and flatten the tree structure"""
        try:
            response = await self._chatgpt_client.get(
                "/file/directory",
                params={"appId": app_id, "source": "API"}
            )
            response.raise_for_status()
            data = response.json()

            # Check response status
            if data.get("message", {}).get("code") != 0:
                error_msg = data.get("message", {}).get("message", "Unknown error")
                raise Exception(f"Failed to get categories: {error_msg}")

            # Flatten the category tree
            categories_data = data.get("data", [])
            return self._flatten_categories(categories_data)

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error getting categories for app {app_id}: {e}")
            if e.response.status_code == 404:
                raise InvalidAppIdError(app_id)
            raise Exception(f"Failed to get categories: {e}")
        except httpx.RequestError as e:
            logger.error(f"Request error getting categories for app {app_id}: {e}")
            raise Exception(f"Failed to connect to backend: {e}")

    def _flatten_categories(self, categories: List[dict], parent_name: str = "") -> List[Category]:
        """
        Recursively flatten category tree structure

        Args:
            categories: List of category dictionaries with potential children
            parent_name: Parent category name for building hierarchical names

        Returns:
            Flattened list of Category objects
        """
        result = []
        for cat in categories:
            # Build full name with parent prefix
            full_name = f"{parent_name}>{cat['name']}" if parent_name else cat['name']

            # Add current category
            result.append(Category(
                id=str(cat['id']),
                name=full_name,
                description=""
            ))

            # Recursively process children
            if cat.get('children'):
                result.extend(self._flatten_categories(cat['children'], full_name))

        return result

    async def get_apis_by_category(
        self, app_id: str, category_id: str
    ) -> List[APIBasic]:
        """Get APIs by category from backend"""
        try:
            response = await self._chatdb_client.get(
                "/agent/queryByNames",
                params={"appId": app_id, "treeId": category_id}
            )
            response.raise_for_status()
            data = response.json()

            # Check response status
            if data.get("message", {}).get("code") != 0:
                error_msg = data.get("message", {}).get("message", "Unknown error")
                raise Exception(f"Failed to get APIs: {error_msg}")

            # Transform to APIBasic objects
            apis_data = data.get("data", [])
            return [
                APIBasic(
                    name=api["name"],
                    # description=api.get("description", ""),
                    category_id=category_id
                )
                for api in apis_data
            ]

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error getting APIs for category {category_id}: {e}")
            raise Exception(f"Failed to get APIs: {e}")
        except httpx.RequestError as e:
            logger.error(f"Request error getting APIs for category {category_id}: {e}")
            raise Exception(f"Failed to connect to backend: {e}")

    async def get_api_details(
        self, app_id: str, api_names: List[str]
    ) -> List[APIDetail]:
        """Get API details from backend"""
        try:
            # Join API names with commas
            names_param = ",".join(api_names)

            response = await self._chatdb_client.get(
                "/agent/queryByNames",
                params={"appId": app_id, "names": names_param}
            )
            response.raise_for_status()
            data = response.json()

            # Check response status
            if data.get("message", {}).get("code") != 0:
                error_msg = data.get("message", {}).get("message", "Unknown error")
                raise Exception(f"Failed to get API details: {error_msg}")

            # Transform to APIDetail objects
            apis_data = data.get("data", [])
            return [self._transform_to_api_detail(api) for api in apis_data]

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error getting API details: {e}")
            raise Exception(f"Failed to get API details: {e}")
        except httpx.RequestError as e:
            logger.error(f"Request error getting API details: {e}")
            raise Exception(f"Failed to connect to backend: {e}")

    def _transform_to_api_detail(self, api_data: dict) -> APIDetail:
        """
        Transform API data from backend to APIDetail model

        Args:
            api_data: Raw API data from backend

        Returns:
            APIDetail object
        """
        # Transform queryParams to Parameter objects
        parameters = [
            Parameter(
                name=p.get("name", ""),
                type=p.get("type") or "string",
                required=p.get("isNecessary") == "是",
                description=p.get("desc", ""),
                default=p.get("content")
            )
            for p in api_data.get("queryParams", [])
        ]

        return APIDetail(
            name=api_data["name"],
            description=api_data.get("description", ""),
            category_id=str(api_data.get("id", "")),
            parameters=parameters,
            response_schema={}  # Not provided in API response
        )

    async def execute_api(
        self, app_id: str, execution: ExecutionRequest
    ) -> ExecutionResult:
        """Execute API via backend"""
        try:
            # Build request body
            request_body = {
                "apiName": execution.api_name,
                "appId": app_id,
                "reqMap": execution.parameters
            }

            response = await self._chatdb_client.post(
                "/dataApiInfo/callApi",
                json=request_body
            )
            response.raise_for_status()
            data = response.json()

            # Check response status
            if data.get("status") != 200:
                error_msg = data.get("message", {}).get("message", "Unknown error")
                return ExecutionResult(
                    api_name=execution.api_name,
                    success=False,
                    data=None,
                    error=error_msg
                )

            # Return successful result
            return ExecutionResult(
                api_name=execution.api_name,
                success=True,
                data=data.get("data"),
                error=None
            )

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error executing API {execution.api_name}: {e}")
            return ExecutionResult(
                api_name=execution.api_name,
                success=False,
                data=None,
                error=f"HTTP error: {e}"
            )
        except httpx.RequestError as e:
            logger.error(f"Request error executing API {execution.api_name}: {e}")
            return ExecutionResult(
                api_name=execution.api_name,
                success=False,
                data=None,
                error=f"Connection error: {e}"
            )
        except Exception as e:
            logger.error(f"Unexpected error executing API {execution.api_name}: {e}")
            return ExecutionResult(
                api_name=execution.api_name,
                success=False,
                data=None,
                error=f"Unexpected error: {e}"
            )

    async def execute_sql(self, app_id: str, sql: str, source_name: str) -> dict:
        """Execute SQL via /sqlQuery/execSql endpoint"""
        try:
            request_body = {
                "appId": app_id,
                "sql": sql,
                "sourceName": source_name
            }

            response = await self._workflow_client.post(
                "/sqlQuery/execSql",
                json=request_body
            )
            response.raise_for_status()
            data = response.json()

            if data.get("message", {}).get("code") != 0:
                error_msg = data.get("message", {}).get("message", "Unknown error")
                raise Exception(f"SQL execution failed: {error_msg}")

            return data

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error executing SQL: {e}")
            raise Exception(f"Failed to execute SQL: {e}")
        except httpx.RequestError as e:
            logger.error(f"Request error executing SQL: {e}")
            raise Exception(f"Failed to connect to backend: {e}")

    async def close(self):
        """Close HTTP clients"""
        await self._chatgpt_client.aclose()
        await self._chatdb_client.aclose()

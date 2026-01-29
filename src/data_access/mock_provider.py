"""Mock data provider for development and testing"""
from typing import List, Dict
from .base import DataProvider
from ..models import Category, APIBasic, APIDetail, Parameter, ExecutionRequest, ExecutionResult
from ..utils.errors import InvalidAppIdError, CategoryNotFoundError, APINotFoundError


class MockDataProvider(DataProvider):
    """Mock data provider with realistic test data"""

    def __init__(self):
        """Initialize with mock data"""
        self._mock_data = self._initialize_mock_data()

    def _initialize_mock_data(self) -> Dict:
        """Initialize comprehensive mock data"""
        return {
            "test_app": {
                "categories": [
                    Category(
                        id="user_management",
                        name="User Management",
                        description="APIs for user operations"
                    ),
                    Category(
                        id="order_management",
                        name="Order Management",
                        description="APIs for order operations"
                    ),
                    Category(
                        id="product_catalog",
                        name="Product Catalog",
                        description="APIs for product information"
                    )
                ],
                "apis": {
                    "user_management": [
                        APIDetail(
                            name="get_user_info",
                            description="Get user information by user ID",
                            category_id="user_management",
                            parameters=[
                                Parameter(
                                    name="user_id",
                                    type="string",
                                    required=True,
                                    description="User ID"
                                )
                            ],
                            response_schema={
                                "type": "object",
                                "properties": {
                                    "user_id": {"type": "string"},
                                    "name": {"type": "string"},
                                    "email": {"type": "string"},
                                    "created_at": {"type": "string"}
                                }
                            }
                        ),
                        APIDetail(
                            name="create_user",
                            description="Create a new user",
                            category_id="user_management",
                            parameters=[
                                Parameter(
                                    name="name",
                                    type="string",
                                    required=True,
                                    description="User name"
                                ),
                                Parameter(
                                    name="email",
                                    type="string",
                                    required=True,
                                    description="User email"
                                )
                            ],
                            response_schema={
                                "type": "object",
                                "properties": {
                                    "user_id": {"type": "string"},
                                    "name": {"type": "string"},
                                    "email": {"type": "string"}
                                }
                            }
                        )
                    ],
                    "order_management": [
                        APIDetail(
                            name="get_orders",
                            description="Get orders for a user",
                            category_id="order_management",
                            parameters=[
                                Parameter(
                                    name="user_id",
                                    type="string",
                                    required=True,
                                    description="User ID"
                                ),
                                Parameter(
                                    name="status",
                                    type="string",
                                    required=False,
                                    description="Order status filter",
                                    default="all"
                                )
                            ],
                            response_schema={
                                "type": "object",
                                "properties": {
                                    "orders": {"type": "array"}
                                }
                            }
                        )
                    ],
                    "product_catalog": [
                        APIDetail(
                            name="search_products",
                            description="Search products by keyword",
                            category_id="product_catalog",
                            parameters=[
                                Parameter(
                                    name="keyword",
                                    type="string",
                                    required=True,
                                    description="Search keyword"
                                ),
                                Parameter(
                                    name="limit",
                                    type="number",
                                    required=False,
                                    description="Maximum results",
                                    default=10
                                )
                            ],
                            response_schema={
                                "type": "object",
                                "properties": {
                                    "products": {"type": "array"},
                                    "total": {"type": "number"}
                                }
                            }
                        )
                    ]
                }
            },
            "demo_app": {
                "categories": [
                    Category(
                        id="demo_category",
                        name="Demo Category",
                        description="Demo APIs for testing"
                    )
                ],
                "apis": {
                    "demo_category": [
                        APIDetail(
                            name="demo_api",
                            description="Demo API for testing",
                            category_id="demo_category",
                            parameters=[],
                            response_schema={
                                "type": "object",
                                "properties": {
                                    "message": {"type": "string"}
                                }
                            }
                        )
                    ]
                }
            }
        }

    async def validate_app_id(self, app_id: str) -> bool:
        """Validate if app_id exists"""
        return app_id in self._mock_data

    async def get_categories(self, app_id: str) -> List[Category]:
        """Get all categories for an app"""
        if app_id not in self._mock_data:
            raise InvalidAppIdError(app_id)
        return self._mock_data[app_id]["categories"]

    async def get_apis_by_category(
        self, app_id: str, category_id: str
    ) -> List[APIBasic]:
        """Get all APIs in a category"""
        if app_id not in self._mock_data:
            raise InvalidAppIdError(app_id)

        if category_id not in self._mock_data[app_id]["apis"]:
            raise CategoryNotFoundError(category_id)

        apis = self._mock_data[app_id]["apis"][category_id]
        return [
            APIBasic(
                name=api.name,
                description=api.description,
                category_id=api.category_id
            )
            for api in apis
        ]

    async def get_api_details(
        self, app_id: str, api_names: List[str]
    ) -> List[APIDetail]:
        """Get detailed information for specific APIs"""
        if app_id not in self._mock_data:
            raise InvalidAppIdError(app_id)

        results = []
        for category_apis in self._mock_data[app_id]["apis"].values():
            for api in category_apis:
                if api.name in api_names:
                    results.append(api)

        if len(results) != len(api_names):
            found_names = {api.name for api in results}
            missing = set(api_names) - found_names
            raise APINotFoundError(", ".join(missing))

        return results

    async def execute_api(
        self, app_id: str, execution: ExecutionRequest
    ) -> ExecutionResult:
        """Execute a single API call (mock execution)"""
        # Mock execution - return fake but realistic data
        if execution.api_name == "get_user_info":
            return ExecutionResult(
                api_name=execution.api_name,
                success=True,
                data={
                    "user_id": execution.parameters.get("user_id"),
                    "name": "John Doe",
                    "email": "john@example.com",
                    "created_at": "2024-01-01T00:00:00Z"
                }
            )
        elif execution.api_name == "create_user":
            return ExecutionResult(
                api_name=execution.api_name,
                success=True,
                data={
                    "user_id": "user_12345",
                    "name": execution.parameters.get("name"),
                    "email": execution.parameters.get("email")
                }
            )
        elif execution.api_name == "get_orders":
            return ExecutionResult(
                api_name=execution.api_name,
                success=True,
                data={
                    "orders": [
                        {
                            "order_id": "order_1",
                            "user_id": execution.parameters.get("user_id"),
                            "status": "completed",
                            "total": 99.99
                        },
                        {
                            "order_id": "order_2",
                            "user_id": execution.parameters.get("user_id"),
                            "status": "pending",
                            "total": 149.99
                        }
                    ]
                }
            )
        elif execution.api_name == "search_products":
            return ExecutionResult(
                api_name=execution.api_name,
                success=True,
                data={
                    "products": [
                        {
                            "product_id": "prod_1",
                            "name": f"Product matching {execution.parameters.get('keyword')}",
                            "price": 29.99
                        }
                    ],
                    "total": 1
                }
            )
        else:
            # Default mock response
            return ExecutionResult(
                api_name=execution.api_name,
                success=True,
                data={"message": "Mock execution successful", "parameters": execution.parameters}
            )

"""Real API data provider - connects to backend (Phase 2)"""
import httpx
from typing import List
from .base import DataProvider
from ..models import Category, APIBasic, APIDetail, ExecutionRequest, ExecutionResult
from ..config import Settings


class APIDataProvider(DataProvider):
    """Real API data provider - connects to backend"""

    def __init__(self, settings: Settings):
        """
        Initialize API data provider

        Args:
            settings: Application settings
        """
        self._settings = settings
        self._client = httpx.AsyncClient(
            base_url=settings.backend.base_url,
            timeout=settings.backend.timeout,
            headers={"Authorization": f"Bearer {settings.backend.api_key}"}
        )

    async def validate_app_id(self, app_id: str) -> bool:
        """Validate app_id with backend"""
        # TODO: Implement real validation
        # response = await self._client.get(f"/apps/{app_id}/validate")
        # return response.status_code == 200
        raise NotImplementedError("Real API provider not implemented yet")

    async def get_categories(self, app_id: str) -> List[Category]:
        """Get categories from backend"""
        # TODO: Implement real API call
        # response = await self._client.get(f"/apps/{app_id}/categories")
        # response.raise_for_status()
        # data = response.json()
        # return [Category(**cat) for cat in data["categories"]]
        raise NotImplementedError("Real API provider not implemented yet")

    async def get_apis_by_category(
        self, app_id: str, category_id: str
    ) -> List[APIBasic]:
        """Get APIs by category from backend"""
        # TODO: Implement real API call
        raise NotImplementedError("Real API provider not implemented yet")

    async def get_api_details(
        self, app_id: str, api_names: List[str]
    ) -> List[APIDetail]:
        """Get API details from backend"""
        # TODO: Implement real API call
        raise NotImplementedError("Real API provider not implemented yet")

    async def execute_api(
        self, app_id: str, execution: ExecutionRequest
    ) -> ExecutionResult:
        """Execute API via backend"""
        # TODO: Implement real API execution
        raise NotImplementedError("Real API provider not implemented yet")

    async def close(self):
        """Close HTTP client"""
        await self._client.aclose()

"""API management service"""
from typing import List
from ..models import APIBasic, APIDetail, SessionContext
from ..data_access import DataProvider
from ..cache import CacheProvider


class APIService:
    """Service for managing API metadata"""

    def __init__(self, data_provider: DataProvider, cache: CacheProvider):
        """
        Initialize API service

        Args:
            data_provider: Data provider instance
            cache: Cache provider instance
        """
        self._data_provider = data_provider
        self._cache = cache

    async def get_apis_by_category(
        self, context: SessionContext, category_id: str
    ) -> List[APIBasic]:
        """
        Get APIs by category with caching

        Args:
            context: Session context
            category_id: Category identifier

        Returns:
            List of basic API information
        """
        cache_key = f"apis:{context.app_id}:{category_id}"

        cached = await self._cache.get(cache_key)
        if cached:
            return cached

        apis = await self._data_provider.get_apis_by_category(
            context.app_id, category_id
        )

        await self._cache.set(cache_key, apis)
        return apis

    async def get_api_details(
        self, context: SessionContext, api_names: List[str]
    ) -> List[APIDetail]:
        """
        Get API details with caching

        Args:
            context: Session context
            api_names: List of API names

        Returns:
            List of detailed API information
        """
        # Try to get from cache first
        cached_results = []
        uncached_names = []

        for name in api_names:
            cache_key = f"api_detail:{context.app_id}:{name}"
            cached = await self._cache.get(cache_key)
            if cached:
                cached_results.append(cached)
            else:
                uncached_names.append(name)

        # Fetch uncached APIs
        if uncached_names:
            fetched = await self._data_provider.get_api_details(
                context.app_id, uncached_names
            )

            # Cache individual results
            for api in fetched:
                cache_key = f"api_detail:{context.app_id}:{api.name}"
                await self._cache.set(cache_key, api)

            cached_results.extend(fetched)

        return cached_results

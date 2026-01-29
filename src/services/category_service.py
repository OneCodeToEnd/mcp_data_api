"""Category management service"""
from typing import List
from ..models import Category, SessionContext
from ..data_access import DataProvider
from ..cache import CacheProvider


class CategoryService:
    """Service for managing categories"""

    def __init__(self, data_provider: DataProvider, cache: CacheProvider):
        """
        Initialize category service

        Args:
            data_provider: Data provider instance
            cache: Cache provider instance
        """
        self._data_provider = data_provider
        self._cache = cache

    async def get_categories(self, context: SessionContext) -> List[Category]:
        """
        Get categories with caching

        Args:
            context: Session context

        Returns:
            List of categories
        """
        cache_key = f"categories:{context.app_id}"

        # Try cache first
        cached = await self._cache.get(cache_key)
        if cached:
            return cached

        # Fetch from data provider
        categories = await self._data_provider.get_categories(context.app_id)

        # Cache the result
        await self._cache.set(cache_key, categories)

        return categories

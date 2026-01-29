"""Abstract base class for cache providers"""
from abc import ABC, abstractmethod
from typing import Any, Optional


class CacheProvider(ABC):
    """Abstract cache provider interface"""

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found/expired
        """
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: int = None) -> None:
        """
        Set value in cache with optional TTL

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (None = use default)
        """
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        """
        Delete value from cache

        Args:
            key: Cache key
        """
        pass

    @abstractmethod
    async def clear(self) -> None:
        """Clear all cache"""
        pass

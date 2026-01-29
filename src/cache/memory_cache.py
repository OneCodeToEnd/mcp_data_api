"""In-memory cache implementation with TTL support"""
import time
from typing import Any, Optional, Dict, Tuple
from .base import CacheProvider


class MemoryCache(CacheProvider):
    """In-memory cache with TTL support"""

    def __init__(self, default_ttl: int = 3600):
        """
        Initialize memory cache

        Args:
            default_ttl: Default time to live in seconds (default: 1 hour)
        """
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._default_ttl = default_ttl

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if key not in self._cache:
            return None

        value, expiry = self._cache[key]

        # Check if expired
        if time.time() > expiry:
            del self._cache[key]
            return None

        return value

    async def set(self, key: str, value: Any, ttl: int = None) -> None:
        """Set value in cache with TTL"""
        ttl = ttl or self._default_ttl
        expiry = time.time() + ttl
        self._cache[key] = (value, expiry)

    async def delete(self, key: str) -> None:
        """Delete value from cache"""
        self._cache.pop(key, None)

    async def clear(self) -> None:
        """Clear all cache"""
        self._cache.clear()

    def get_stats(self) -> dict:
        """Get cache statistics"""
        total_keys = len(self._cache)
        expired_keys = sum(
            1 for _, expiry in self._cache.values()
            if time.time() > expiry
        )
        return {
            "total_keys": total_keys,
            "active_keys": total_keys - expired_keys,
            "expired_keys": expired_keys
        }

"""
Simple in-memory cache manager
For production, consider Redis or similar
"""
from typing import Any, Optional, Dict
from datetime import datetime, timedelta


class CacheEntry:
    """Cache entry with expiration"""
    
    def __init__(self, value: Any, ttl_seconds: int = 300):
        self.value = value
        self.expires_at = datetime.utcnow() + timedelta(seconds=ttl_seconds)
    
    def is_expired(self) -> bool:
        """Check if entry is expired"""
        return datetime.utcnow() > self.expires_at


class CacheManager:
    """
    Simple in-memory cache manager
    O(1) get/set operations
    """
    
    def __init__(self):
        self._cache: Dict[str, CacheEntry] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache - O(1)"""
        entry = self._cache.get(key)
        if entry is None:
            return None
        
        if entry.is_expired():
            del self._cache[key]
            return None
        
        return entry.value
    
    def set(self, key: str, value: Any, ttl_seconds: int = 300):
        """Set value in cache - O(1)"""
        self._cache[key] = CacheEntry(value, ttl_seconds)
    
    def delete(self, key: str):
        """Delete key from cache - O(1)"""
        if key in self._cache:
            del self._cache[key]
    
    def clear(self):
        """Clear all cache"""
        self._cache.clear()
    
    def cleanup_expired(self):
        """Remove expired entries - O(n)"""
        expired_keys = [
            key for key, entry in self._cache.items()
            if entry.is_expired()
        ]
        for key in expired_keys:
            del self._cache[key]


# Global cache instance
cache_manager = CacheManager()


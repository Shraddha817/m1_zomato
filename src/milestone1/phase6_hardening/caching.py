"""
Caching strategies for Phase 6 hardening.
"""

import hashlib
import json
import time
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class CacheEntry:
    """Cache entry with metadata."""
    data: Any
    timestamp: datetime
    ttl_seconds: int
    access_count: int = 0
    size_bytes: int = 0


class CacheManager:
    """Manages caching for backend services."""
    
    def __init__(self, max_size_mb: int = 100):
        self.cache: Dict[str, CacheEntry] = {}
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.current_size_bytes = 0
        self.hits = 0
        self.misses = 0
    
    def _generate_key(self, prefix: str, **kwargs) -> str:
        """Generate cache key from prefix and parameters."""
        key_data = json.dumps(kwargs, sort_keys=True)
        return f"{prefix}:{hashlib.md5(key_data.encode()).hexdigest()}"
    
    def _is_expired(self, entry: CacheEntry) -> bool:
        """Check if cache entry is expired."""
        return datetime.now() > entry.timestamp + timedelta(seconds=entry.ttl_seconds)
    
    def _should_evict(self) -> bool:
        """Check if cache should evict entries."""
        return self.current_size_bytes > self.max_size_bytes
    
    def _evict_expired(self) -> int:
        """Remove expired entries and return count."""
        expired_keys = [
            key for key, entry in self.cache.items()
            if self._is_expired(entry)
        ]
        
        for key in expired_keys:
            if key in self.cache:
                self.current_size_bytes -= self.cache[key].size_bytes
                del self.cache[key]
        
        return len(expired_keys)
    
    def _evict_lru(self, count: int = 1) -> None:
        """Remove least recently used entries."""
        if not self.cache:
            return
        
        # Sort by access count and timestamp
        sorted_items = sorted(
            self.cache.items(),
            key=lambda item: (item[1].access_count, item[1].timestamp)
        )
        
        for key, _ in sorted_items[:count]:
            if key in self.cache:
                self.current_size_bytes -= self.cache[key].size_bytes
                del self.cache[key]
    
    def get(self, prefix: str, **kwargs) -> Optional[Any]:
        """Get item from cache."""
        key = self._generate_key(prefix, **kwargs)
        
        if key in self.cache:
            entry = self.cache[key]
            
            if self._is_expired(entry):
                self.current_size_bytes -= entry.size_bytes
                del self.cache[key]
                self.misses += 1
                return None
            else:
                entry.access_count += 1
                self.hits += 1
                return entry.data
        else:
            self.misses += 1
            return None
    
    def put(self, prefix: str, data: Any, ttl_seconds: int = 3600, **kwargs) -> None:
        """Put item in cache."""
        key = self._generate_key(prefix, **kwargs)
        
        # Calculate size
        data_bytes = len(json.dumps(data).encode())
        
        # Evict if necessary
        self._evict_expired()
        if self._should_evict():
            self._evict_lru()
        
        # Store entry
        self.cache[key] = CacheEntry(
            data=data,
            timestamp=datetime.now(),
            ttl_seconds=ttl_seconds,
            size_bytes=data_bytes
        )
        
        self.current_size_bytes += data_bytes
    
    def clear(self, prefix: Optional[str] = None) -> None:
        """Clear cache entries."""
        if prefix:
            keys_to_remove = [k for k in self.cache.keys() if k.startswith(prefix)]
        else:
            keys_to_remove = list(self.cache.keys())
        
        for key in keys_to_remove:
            if key in self.cache:
                self.current_size_bytes -= self.cache[key].size_bytes
                del self.cache[key]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate_percent": round(hit_rate, 2),
            "entries": len(self.cache),
            "size_bytes": self.current_size_bytes,
            "max_size_bytes": self.max_size_bytes
        }


class RestaurantCache(CacheManager):
    """Specialized cache for restaurant data."""
    
    def __init__(self, max_size_mb: int = 50):
        super().__init__(max_size_mb)
    
    def get_restaurants(self, limit: int = 1000) -> Optional[List[Any]]:
        """Get cached restaurants."""
        return self.get("restaurants", limit=limit)
    
    def put_restaurants(self, restaurants: List[Any], ttl_seconds: int = 3600) -> None:
        """Cache restaurant data."""
        self.put("restaurants", restaurants, ttl_seconds=ttl_seconds)
    
    def get_recommendations(self, prefs_hash: str) -> Optional[List[Any]]:
        """Get cached recommendations."""
        return self.get("recommendations", prefs_hash=prefs_hash)
    
    def put_recommendations(self, prefs_hash: str, recommendations: List[Any], ttl_seconds: int = 1800) -> None:
        """Cache recommendation results."""
        self.put("recommendations", recommendations, ttl_seconds=ttl_seconds, prefs_hash=prefs_hash)
    
    def get_locations(self) -> Optional[List[str]]:
        """Get cached locations."""
        return self.get("locations")
    
    def put_locations(self, locations: List[str], ttl_seconds: int = 7200) -> None:
        """Cache locations list."""
        self.put("locations", locations, ttl_seconds=ttl_seconds)


class LLMResponseCache(CacheManager):
    """Specialized cache for LLM responses."""
    
    def __init__(self, max_size_mb: int = 25):
        super().__init__(max_size_mb)
    
    def get_response(self, prompt_hash: str) -> Optional[Dict[str, Any]]:
        """Get cached LLM response."""
        return self.get("llm_response", prompt_hash=prompt_hash)
    
    def put_response(self, prompt_hash: str, response: Dict[str, Any], ttl_seconds: int = 1800) -> None:
        """Cache LLM response."""
        self.put("llm_response", response, ttl_seconds=ttl_seconds, prompt_hash=prompt_hash)
    
    def clear_expired(self) -> int:
        """Clear expired entries."""
        return self._evict_expired()


class CacheStrategy:
    """Strategy for cache eviction and management."""
    
    @staticmethod
    def choose_ttl(data_type: str) -> int:
        """Choose TTL based on data type."""
        ttl_map = {
            "restaurants": 3600,      # 1 hour
            "recommendations": 1800,    # 30 minutes
            "llm_response": 1800,      # 30 minutes
            "locations": 7200,          # 2 hours
            "user_preferences": 3600     # 1 hour
        }
        return ttl_map.get(data_type, 1800)
    
    @staticmethod
    def should_cache(key: str, data_size: int, max_size: int = 1024*1024) -> bool:
        """Determine if data should be cached."""
        # Don't cache very large items
        return data_size <= max_size
    
    @staticmethod
    def get_cache_key_components(user_input: Dict[str, Any]) -> Dict[str, str]:
        """Extract components for cache key generation."""
        return {
            "location": user_input.get("location", ""),
            "budget_band": user_input.get("budget_band", ""),
            "cuisines": ",".join(sorted(user_input.get("cuisines", []))),
            "min_rating": str(user_input.get("min_rating", "")),
            "additional_text": user_input.get("additional_preferences_text", "")
        }

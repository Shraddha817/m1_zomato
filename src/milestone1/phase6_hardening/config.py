"""
Production configuration and dataset pinning for Phase 6 hardening.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class ProductionConfig:
    """Production configuration settings."""
    # Dataset configuration
    dataset_name: str = "ManikaSaini/zomato-restaurant-recommendation"
    dataset_revision: Optional[str] = None  # Pin to specific revision
    dataset_cache_dir: Optional[str] = None
    
    # Performance controls
    candidate_cap: int = 25  # Maximum candidates for LLM context
    cache_ttl_restaurants: int = 3600  # 1 hour
    cache_ttl_recommendations: int = 1800  # 30 minutes
    cache_ttl_locations: int = 7200  # 2 hours
    
    # API rate limiting
    api_rate_limit_per_minute: int = 60
    api_rate_limit_per_hour: int = 1000
    user_rate_limit_per_hour: int = 100
    
    # Model configuration
    xai_model: str = "grok-beta"
    xai_timeout_seconds: float = 30.0
    xai_max_tokens: int = 600
    xai_temperature: float = 0.3
    
    # Monitoring configuration
    enable_performance_monitoring: bool = True
    enable_structured_logging: bool = True
    log_level: str = "INFO"
    log_retention_days: int = 7
    
    # Feature flags
    enable_caching: bool = True
    enable_api_metrics: bool = True
    enable_user_analytics: bool = False  # Privacy-focused
    
    @classmethod
    def from_env(cls) -> 'ProductionConfig':
        """Create configuration from environment variables."""
        return cls(
            dataset_name=os.environ.get("HF_DATASET_NAME", cls.dataset_name),
            dataset_revision=os.environ.get("HF_DATASET_REVISION"),
            dataset_cache_dir=os.environ.get("HF_DATASET_CACHE_DIR"),
            candidate_cap=int(os.environ.get("CANDIDATE_CAP", str(cls.candidate_cap))),
            cache_ttl_restaurants=int(os.environ.get("CACHE_TTL_RESTAURANTS", str(cls.cache_ttl_restaurants))),
            cache_ttl_recommendations=int(os.environ.get("CACHE_TTL_RECOMMENDATIONS", str(cls.cache_ttl_recommendations))),
            cache_ttl_locations=int(os.environ.get("CACHE_TTL_LOCATIONS", str(cls.cache_ttl_locations))),
            api_rate_limit_per_minute=int(os.environ.get("API_RATE_LIMIT_PER_MINUTE", str(cls.api_rate_limit_per_minute))),
            api_rate_limit_per_hour=int(os.environ.get("API_RATE_LIMIT_PER_HOUR", str(cls.api_rate_limit_per_hour))),
            user_rate_limit_per_hour=int(os.environ.get("USER_RATE_LIMIT_PER_HOUR", str(cls.user_rate_limit_per_hour))),
            xai_model=os.environ.get("XAI_MODEL", cls.xai_model),
            xai_timeout_seconds=float(os.environ.get("XAI_TIMEOUT_SECONDS", str(cls.xai_timeout_seconds))),
            xai_max_tokens=int(os.environ.get("XAI_MAX_TOKENS", str(cls.xai_max_tokens))),
            xai_temperature=float(os.environ.get("XAI_TEMPERATURE", str(cls.xai_temperature))),
            enable_performance_monitoring=os.environ.get("ENABLE_PERFORMANCE_MONITORING", "true").lower() == "true",
            enable_structured_logging=os.environ.get("ENABLE_STRUCTURED_LOGGING", "true").lower() == "true",
            log_level=os.environ.get("LOG_LEVEL", cls.log_level),
            log_retention_days=int(os.environ.get("LOG_RETENTION_DAYS", str(cls.log_retention_days))),
            enable_caching=os.environ.get("ENABLE_CACHING", "true").lower() == "true",
            enable_api_metrics=os.environ.get("ENABLE_API_METRICS", "true").lower() == "true",
            enable_user_analytics=os.environ.get("ENABLE_USER_ANALYTICS", "false").lower() == "false"
        )
    
    def validate(self) -> list[str]:
        """Validate configuration and return list of issues."""
        issues = []
        
        if self.candidate_cap <= 0:
            issues.append("candidate_cap must be positive")
        
        if self.cache_ttl_restaurants <= 0:
            issues.append("cache_ttl_restaurants must be positive")
        
        if self.xai_timeout_seconds <= 0:
            issues.append("xai_timeout_seconds must be positive")
        
        return issues
    
    def to_dict(self) -> dict:
        """Convert to dictionary for logging."""
        return {
            "dataset_name": self.dataset_name,
            "dataset_revision": self.dataset_revision,
            "candidate_cap": self.candidate_cap,
            "cache_ttl_restaurants": self.cache_ttl_restaurants,
            "cache_ttl_recommendations": self.cache_ttl_recommendations,
            "api_rate_limit_per_minute": self.api_rate_limit_per_minute,
            "xai_model": self.xai_model,
            "enable_performance_monitoring": self.enable_performance_monitoring,
            "enable_caching": self.enable_caching
        }


@dataclass
class DatasetPinning:
    """Dataset version pinning information."""
    name: str
    revision: str
    url: str
    download_date: str
    size_mb: Optional[float] = None
    checksum: Optional[str] = None
    
    @classmethod
    def create(cls, config: ProductionConfig) -> 'DatasetPinning':
        """Create dataset pinning information."""
        return cls(
            name=config.dataset_name,
            revision=config.dataset_revision or "latest",
            url=f"https://huggingface.co/datasets/{config.dataset_name}",
            download_date=datetime.now().isoformat(),
            size_mb=None,  # Would be populated during download
            checksum=None  # Would be calculated during download
        )

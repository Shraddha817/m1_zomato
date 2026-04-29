# Backend API Specification

## Overview

This document defines the backend API interfaces for the restaurant recommendation system. The backend is organized into logical phases, each providing specific functionality to the frontend.

## Architecture Layers

### Layer 1: Data Access Layer (Phase 1)
### Layer 2: Business Logic Layer (Phases 2-4)
### Layer 3: Service Integration Layer (Phase 4)
### Layer 4: API Facade Layer (Backend-Frontend Interface)

---

## Phase 1: Data Access API

### Restaurant Data Service

```python
# Interface Definition
class RestaurantDataService:
    """Provides access to normalized restaurant data."""
    
    def load_restaurants(self, limit: int = 1000) -> List[Restaurant]:
        """Load restaurants from the dataset.
        
        Args:
            limit: Maximum number of restaurants to load
            
        Returns:
            List of normalized Restaurant objects
            
        Raises:
            DataLoadError: If dataset cannot be loaded
        """
    
    def get_restaurant_by_id(self, restaurant_id: str) -> Optional[Restaurant]:
        """Get a specific restaurant by ID.
        
        Args:
            restaurant_id: Unique restaurant identifier
            
        Returns:
            Restaurant object or None if not found
        """
    
    def get_available_locations(self) -> List[str]:
        """Get list of all available locations.
        
        Returns:
            List of unique location names
        """
    
    def get_dataset_stats(self) -> DatasetStats:
        """Get statistics about the loaded dataset.
        
        Returns:
            Dataset statistics object
        """
```

### Data Models

```python
@dataclass
class Restaurant:
    """Canonical restaurant model."""
    id: str
    name: str
    location: str
    cuisines: Tuple[str, ...]
    rating: Optional[float]
    cost: Optional[float]
    budget_band: Optional[str]
    raw: Optional[Dict[str, Any]]

@dataclass
class DatasetStats:
    """Dataset statistics."""
    total_restaurants: int
    locations_count: int
    avg_rating: Optional[float]
    budget_distribution: Dict[str, int]
    cuisine_distribution: Dict[str, int]
```

---

## Phase 2: Preferences API

### Preferences Service

```python
class PreferencesService:
    """Handles user preference validation and normalization."""
    
    def validate_preferences(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate user preference data.
        
        Args:
            data: Raw user preference data
            
        Returns:
            ValidationResult with validation status and errors
        """
    
    def normalize_preferences(self, data: Dict[str, Any]) -> UserPreferences:
        """Normalize and create UserPreferences object.
        
        Args:
            data: Validated preference data
            
        Returns:
            Normalized UserPreferences object
        """
    
    def get_allowed_budget_bands(self) -> List[str]:
        """Get list of allowed budget band values.
        
        Returns:
            List of budget band options
        """
    
    def validate_location(self, location: str) -> bool:
        """Check if location is valid/supported.
        
        Args:
            location: Location string to validate
            
        Returns:
            True if location is valid
        """
```

### Data Models

```python
@dataclass
class UserPreferences:
    """User preference model."""
    location: str
    budget_band: Optional[str]
    cuisines: Tuple[str, ...]
    min_rating: Optional[float]
    additional_preferences_text: Optional[str]

@dataclass
class ValidationResult:
    """Validation result."""
    valid: bool
    errors: List[str]
    warnings: List[str]
```

---

## Phase 3: Integration API

### Filtering Service

```python
class FilteringService:
    """Handles restaurant filtering and candidate selection."""
    
    def filter_candidates(
        self, 
        restaurants: List[Restaurant], 
        prefs: UserPreferences,
        limit: int = 50
    ) -> FilterResult:
        """Filter restaurants based on user preferences.
        
        Args:
            restaurants: List of all restaurants
            prefs: User preferences
            limit: Maximum number of candidates to return
            
        Returns:
            FilterResult with candidates and metadata
        """
    
    def get_filter_stats(self, restaurants: List[Restaurant], prefs: UserPreferences) -> FilterStats:
        """Get filtering statistics without actually filtering.
        
        Args:
            restaurants: List of restaurants
            prefs: User preferences
            
        Returns:
            Filter statistics
        """
```

### Prompt Service

```python
class PromptService:
    """Handles LLM prompt construction."""
    
    def build_prompt_payload(
        self, 
        candidates: List[Restaurant], 
        prefs: UserPreferences
    ) -> PromptPayload:
        """Build prompt payload for LLM.
        
        Args:
            candidates: Filtered restaurant candidates
            prefs: User preferences
            
        Returns:
            PromptPayload for LLM
        """
    
    def validate_prompt_payload(self, payload: PromptPayload) -> bool:
        """Validate prompt payload structure.
        
        Args:
            payload: Prompt payload to validate
            
        Returns:
            True if payload is valid
        """
```

### Data Models

```python
@dataclass
class FilterResult:
    """Result of filtering operation."""
    candidates: List[Restaurant]
    total_filtered: int
    filter_applied: Dict[str, Any]
    processing_time: float

@dataclass
class FilterStats:
    """Filtering statistics."""
    total_restaurants: int
    matching_location: int
    matching_budget: int
    matching_rating: int
    matching_cuisines: int
    final_candidates: int

@dataclass
class PromptPayload:
    """LLM prompt payload."""
    system_message: str
    user_message: str
    candidate_count: int
```

---

## Phase 4: Recommendation API

### Recommendation Service

```python
class RecommendationService:
    """Handles LLM-based recommendations."""
    
    def get_recommendations(
        self, 
        prompt_payload: PromptPayload, 
        candidates: List[Restaurant],
        top_k: int = 5
    ) -> RecommendationResult:
        """Get AI-powered restaurant recommendations.
        
        Args:
            prompt_payload: LLM prompt payload
            candidates: Restaurant candidates
            top_k: Number of recommendations to return
            
        Returns:
            RecommendationResult with recommendations and metadata
        """
    
    def get_fallback_recommendations(
        self, 
        candidates: List[Restaurant], 
        top_k: int = 5
    ) -> List[Recommendation]:
        """Get deterministic fallback recommendations.
        
        Args:
            candidates: Restaurant candidates
            top_k: Number of recommendations
            
        Returns:
            List of fallback recommendations
        """
    
    def get_service_health(self) -> ServiceHealth:
        """Check recommendation service health.
        
        Returns:
            Service health status
        """
```

### LLM Client Interface

```python
class LLMClient:
    """Interface for LLM API clients."""
    
    def generate_completion(
        self, 
        messages: List[Dict[str, str]], 
        response_format: Optional[Dict] = None
    ) -> LLMResponse:
        """Generate completion from LLM.
        
        Args:
            messages: Chat messages
            response_format: Expected response format
            
        Returns:
            LLM response
        """
    
    def validate_api_key(self) -> bool:
        """Validate LLM API key.
        
        Returns:
            True if API key is valid
        """
```

### Data Models

```python
@dataclass
class Recommendation:
    """Restaurant recommendation."""
    restaurant: Restaurant
    rank: int
    explanation: str
    confidence: Optional[float] = None

@dataclass
class RecommendationResult:
    """Result of recommendation operation."""
    recommendations: List[Recommendation]
    processing_time: float
    used_fallback: bool
    llm_metadata: Optional[LLMMetadata]

@dataclass
class LLMMetadata:
    """LLLM operation metadata."""
    model: str
    tokens_used: Optional[int]
    response_time: float
    api_calls: int

@dataclass
class ServiceHealth:
    """Service health status."""
    healthy: bool
    llm_available: bool
    data_available: bool
    last_check: datetime
```

---

## Backend-Frontend API Facade

### Main Recommendation API

```python
class RecommendationAPI:
    """Main API facade for frontend consumption."""
    
    def __init__(self):
        self.data_service = RestaurantDataService()
        self.preferences_service = PreferencesService()
        self.filtering_service = FilteringService()
        self.prompt_service = PromptService()
        self.recommendation_service = RecommendationService()
    
    async def get_recommendations(
        self, 
        user_input: Dict[str, Any]
    ) -> APIResponse[RecommendationResponse]:
        """Main endpoint for getting recommendations.
        
        Args:
            user_input: User preference data from frontend
            
        Returns:
            API response with recommendations
        """
    
    def get_locations(self) -> APIResponse[List[str]]:
        """Get available locations.
        
        Returns:
            API response with location list
        """
    
    def validate_input(self, data: Dict[str, Any]) -> APIResponse[ValidationResult]:
        """Validate user input.
        
        Args:
            data: User input data
            
        Returns:
            API response with validation result
        """
    
    def get_system_status(self) -> APIResponse[SystemStatus]:
        """Get system status and health.
        
        Returns:
            API response with system status
        """
```

### API Response Models

```python
@dataclass
class APIResponse(Generic[T]):
    """Standard API response wrapper."""
    success: bool
    data: Optional[T]
    error: Optional[APIError]
    metadata: Optional[Dict[str, Any]]

@dataclass
class APIError:
    """API error information."""
    code: str
    message: str
    details: Optional[Dict[str, Any]]
    retryable: bool

@dataclass
class RecommendationResponse:
    """Complete recommendation response."""
    recommendations: List[Recommendation]
    user_preferences: UserPreferences
    processing_stats: ProcessingStats
    system_info: SystemInfo

@dataclass
class ProcessingStats:
    """Processing statistics."""
    total_time: float
    data_load_time: float
    filtering_time: float
    llm_time: float
    candidates_found: int
    recommendations_returned: int

@dataclass
class SystemInfo:
    """System information."""
    dataset_version: str
    model_version: str
    api_version: str
    timestamp: datetime
```

---

## Error Handling

### Error Types

```python
class RecommendationAPIError(Exception):
    """Base API error."""
    pass

class DataLoadError(RecommendationAPIError):
    """Data loading failed."""
    pass

class ValidationError(RecommendationAPIError):
    """Input validation failed."""
    pass

class FilteringError(RecommendationAPIError):
    """Filtering operation failed."""
    pass

class LLMError(RecommendationAPIError):
    """LLM operation failed."""
    pass

class ServiceUnavailableError(RecommendationAPIError):
    """Service temporarily unavailable."""
    pass
```

### Error Response Format

```python
# Standard error response
{
    "success": false,
    "data": null,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid location provided",
        "details": {
            "field": "location",
            "value": "InvalidLocation",
            "valid_options": ["Banashankari", "BTM", "JP Nagar"]
        },
        "retryable": true
    },
    "metadata": {
        "timestamp": "2026-04-28T13:00:00Z",
        "request_id": "req_123456"
    }
}
```

---

## Performance and Caching

### Caching Strategy

```python
class CacheManager:
    """Manages caching for backend services."""
    
    def cache_restaurants(self, restaurants: List[Restaurant], ttl: int = 3600):
        """Cache restaurant data."""
        pass
    
    def cache_recommendations(
        self, 
        prefs_hash: str, 
        recommendations: List[Recommendation], 
        ttl: int = 1800
    ):
        """Cache recommendation results."""
        pass
    
    def get_cached_recommendations(self, prefs_hash: str) -> Optional[List[Recommendation]]:
        """Get cached recommendations."""
        pass
```

### Rate Limiting

```python
class RateLimiter:
    """Rate limiting for API calls."""
    
    def check_llm_rate_limit(self) -> bool:
        """Check if LLM API call is allowed."""
        pass
    
    def check_user_rate_limit(self, user_id: str) -> bool:
        """Check user-specific rate limits."""
        pass
```

---

## Configuration

### Environment Variables

```bash
# Data Configuration
HF_DATASET_NAME=ManikaSaini/zomato-restaurant-recommendation
HF_DATASET_CACHE_DIR=./cache
HF_TOKEN=your_hf_token

# LLM Configuration
XAI_API_KEY=your_xai_api_key
XAI_BASE_URL=https://api.x.ai/v1
XAI_MODEL=grok-beta
XAI_TIMEOUT_SECONDS=30
XAI_MAX_TOKENS=600
XAI_TEMPERATURE=0.3

# API Configuration
API_RATE_LIMIT_PER_MINUTE=60
CACHE_TTL_RESTAURANTS=3600
CACHE_TTL_RECOMMENDATIONS=1800
CANDIDATE_CAP=25

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

---

## Testing Interfaces

### Mock Services

```python
class MockRestaurantDataService(RestaurantDataService):
    """Mock service for testing."""
    
    def load_restaurants(self, limit: int = 1000) -> List[Restaurant]:
        """Return mock restaurant data."""
        return generate_mock_restaurants(limit)

class MockLLMClient(LLMClient):
    """Mock LLM client for testing."""
    
    def generate_completion(self, messages: List[Dict[str, str]]) -> LLMResponse:
        """Return mock LLM response."""
        return generate_mock_llm_response(messages)
```

### Test Fixtures

```python
@pytest.fixture
def sample_restaurants():
    """Sample restaurant data for testing."""
    return load_test_restaurants()

@pytest.fixture
def sample_preferences():
    """Sample user preferences for testing."""
    return UserPreferences(
        location="Banashankari",
        budget_band="medium",
        cuisines=("North Indian", "Chinese"),
        min_rating=4.0
    )

@pytest.fixture
def mock_api():
    """Mock API for testing."""
    return RecommendationAPI(
        data_service=MockRestaurantDataService(),
        recommendation_service=MockRecommendationService()
    )
```

This backend API specification provides a comprehensive interface for frontend integration while maintaining clear separation of concerns and enabling independent testing and development of each component.

## Updated Architecture — AI Restaurant Recommendation (Post-Phase 5)

### Purpose
This document defines the **updated architecture** after Phase 5 implementation, reflecting proper backend/frontend separation and the complete system structure.

---

## System Architecture Overview

### Backend Services (Phases 1-4)
- **Data Layer**: Restaurant ingestion and normalization
- **Business Logic**: Filtering, preference validation, LLM integration
- **API Layer**: Clean interfaces for frontend consumption

### Frontend Application (Phase 5)
- **UI Components**: React-like component structure in Streamlit
- **State Management**: Session state and user journey handling
- **Presentation Layer**: User interface and experience

---

## Phase 0 — Foundation and Contracts

### Backend Components
- **Configuration Management**: Environment variables, `.env.example`
- **Dependency Management**: `requirements.txt`, package versions
- **Dataset Contract**: `docs/dataset-contract.md`
- **API Contracts**: Interface definitions between phases

### Frontend Components
- **UI Framework**: Streamlit configuration and setup
- **Component Contracts**: Props and interfaces for UI components
- **State Contracts**: Session state structure and transitions

---

## Phase 1 — Data Ingestion Layer (Backend)

### Backend Implementation
```python
# src/milestone1/ingestion/
├── models.py              # Restaurant dataclass
├── ingest.py              # Main ingestion functions
├── normalize.py           # Data normalization logic
├── hf_loader.py           # Hugging Face integration
└── config.py              # Configuration management
```

### API Interface
```python
def load_restaurants(limit: int = 1000) -> List[Restaurant]
def iter_restaurants(cfg: IngestionConfig) -> Iterable[Restaurant]
def restaurant_to_dict(restaurant: Restaurant) -> Dict[str, Any]
```

### Frontend Integration
- **Data Service**: Wrapper functions for loading restaurant data
- **Caching**: Session-based caching for performance
- **Error Handling**: Graceful fallback for data loading failures

---

## Phase 2 — User Preferences (Backend)

### Backend Implementation
```python
# src/milestone1/phase2_preferences/
├── models.py              # UserPreferences, BudgetBand
├── validation.py           # Validation logic
└── allowed_locations.py    # Location validation
```

### API Interface
```python
@dataclass
class UserPreferences:
    location: str
    budget_band: Optional[str]
    cuisines: Tuple[str, ...]
    min_rating: Optional[float]
    additional_preferences_text: Optional[str]

def validate_preferences(data: Dict) -> ValidationResult
def normalize_cuisines(cuisines: List[str]) -> Tuple[str, ...]
```

### Frontend Integration
- **Form Components**: Input validation and user feedback
- **State Models**: Frontend representation of preferences
- **Validation UI**: Real-time validation feedback

---

## Phase 3 — Integration Layer (Backend)

### Backend Implementation
```python
# src/milestone1/phase3_integration/
├── filtering.py            # Candidate filtering logic
├── prompting.py            # LLM prompt construction
└── models.py               # PromptPayload dataclass
```

### API Interface
```python
def filter_candidates(
    restaurants: List[Restaurant],
    prefs: UserPreferences,
    limit: int = 50
) -> List[Restaurant]

def build_prompt_payload(
    candidates: List[Restaurant],
    prefs: UserPreferences
) -> PromptPayload
```

### Frontend Integration
- **Service Layer**: Backend service calls
- **Loading States**: Progress indicators during processing
- **Error Boundaries**: Error handling and user feedback

---

## Phase 4 — Recommendation Engine (Backend)

### Backend Implementation
```python
# src/milestone1/phase4_recommendation/
├── client.py               # LLM client and API calls
├── models.py               # Recommendation dataclass
└── fallback.py             # Deterministic fallback logic
```

### API Interface
```python
def get_recommendations(
    prompt_payload: PromptPayload,
    candidates: List[Restaurant],
    top_k: int = 5
) -> List[Recommendation]

@dataclass
class Recommendation:
    restaurant: Restaurant
    rank: int
    explanation: str
```

### Frontend Integration
- **Recommendation Service**: API wrapper for recommendations
- **Result Processing**: Data transformation for UI
- **Fallback UI**: Display fallback recommendations

---

## Phase 5 — Frontend Application

### Frontend Architecture
```python
# src/milestone1/phase5_ui/
├── models.py               # UI state and data models
├── components.py           # UI rendering functions
├── app.py                  # Main Streamlit application
└── services.py             # Backend service integration
```

### Component Structure
```python
# UI Components
def render_input_form() -> Dict[str, Any]
def render_results(recommendations: List[Recommendation]) -> None
def render_empty_state(message: str) -> None
def render_error_state(error: UIError) -> None
def render_loading_state(message: str) -> None
```

### State Management
```python
# UI States
class UIState(Enum):
    INPUT = "input"
    LOADING = "loading"
    RESULTS = "results"
    ERROR = "error"
    EMPTY = "empty"

# Session State Structure
st.session_state.ui_state = UIState.INPUT
st.session_state.recommendations = []
st.session_state.error = None
st.session_state.user_input_data = None
```

### Backend Integration Layer
```python
# Service Functions
async def get_restaurant_recommendations(user_input: UserInput) -> List[Recommendation]
def get_available_locations() -> List[str]
def validate_user_input(data: Dict) -> ValidationResult
```

---

## Updated File Structure

```
milestone1/
├── Backend Services (Phases 1-4)
│   ├── ingestion/                    # Phase 1
│   ├── phase2_preferences/           # Phase 2
│   ├── phase3_integration/           # Phase 3
│   └── phase4_recommendation/        # Phase 4
│
├── Frontend Application (Phase 5)
│   └── phase5_ui/                    # Phase 5
│       ├── models.py                 # UI models
│       ├── components.py             # UI components
│       ├── app.py                    # Main app
│       └── services.py               # Backend integration
│
├── Shared Components
│   ├── preferences/                   # Shared preference models
│   └── llm/                          # LLM client utilities
│
└── Web Application Entry Point
    └── apps/web/app.py               # Streamlit entry point
```

---

## API Contracts Between Backend and Frontend

### 1. Restaurant Data API
```python
# Backend → Frontend
interface RestaurantData {
    id: string
    name: string
    location: string
    cuisines: string[]
    rating: number | null
    cost: number | null
    budget_band: "low" | "medium" | "high" | null
}
```

### 2. Preferences API
```python
# Frontend → Backend
interface UserPreferencesInput {
    location: string
    budget_band?: string
    cuisines?: string[]
    min_rating?: number
    additional_preferences_text?: string
}

# Backend → Frontend
interface ValidationResult {
    valid: boolean
    errors: string[]
}
```

### 3. Recommendations API
```python
# Frontend → Backend
interface RecommendationRequest {
    preferences: UserPreferencesInput
}

# Backend → Frontend
interface RecommendationResponse {
    recommendations: Recommendation[]
    processing_time: number
    candidate_count: number
    used_fallback: boolean
}

interface Recommendation {
    restaurant: RestaurantData
    rank: number
    explanation: string
}
```

---

## Deployment Architecture

### Backend Deployment
- **Service Container**: Python backend with all phases
- **Environment Variables**: API keys, configuration
- **Data Storage**: In-memory with optional caching
- **External Dependencies**: Hugging Face, xAI API

### Frontend Deployment
- **Web Server**: Streamlit built-in server
- **Static Assets**: CSS, JavaScript, images
- **Session Management**: In-memory session state
- **API Communication**: Direct backend imports

### Production Considerations
- **Scaling**: Horizontal scaling of backend services
- **Caching**: Redis for session and data caching
- **Load Balancing**: Multiple frontend instances
- **Monitoring**: Logging and metrics collection

---

## Phase 6 — Hardening and Production Readiness

### Backend Hardening
- **API Rate Limiting**: Prevent abuse of LLM calls
- **Data Caching**: Restaurant data and recommendation caching
- **Error Monitoring**: Structured logging and alerting
- **Performance Monitoring**: Request timing and resource usage

### Frontend Hardening
- **Error Boundaries**: Graceful error handling
- **Loading States**: Proper loading indicators
- **Accessibility**: Screen reader support and keyboard navigation
- **Performance**: Optimized rendering and state management

### Testing Strategy
- **Backend Tests**: Unit tests for all phases
- **Integration Tests**: API contract testing
- **Frontend Tests**: Component testing and E2E tests
- **Performance Tests**: Load testing and optimization

---

## Updated Dependency Rules

### Backend Independence
- **Phase 1**: Pure data processing, no UI dependencies
- **Phase 2**: Business logic only, no presentation
- **Phase 3**: Integration logic, no UI concerns
- **Phase 4**: LLM integration, no frontend dependencies

### Frontend Independence
- **Phase 5**: Pure UI and presentation
- **Backend Communication**: Through well-defined interfaces
- **State Management**: Isolated from backend implementation
- **Error Handling**: UI-specific error handling

### Cross-Cutting Concerns
- **Logging**: Structured logging across all phases
- **Configuration**: Centralized configuration management
- **Testing**: Comprehensive test coverage
- **Documentation**: API documentation and user guides

---

## Future Enhancements

### Backend Evolution
- **Microservices**: Separate services for each phase
- **API Gateway**: Centralized API management
- **Event Streaming**: Real-time data updates
- **Machine Learning**: Custom model training

### Frontend Evolution
- **Progressive Web App**: Mobile-first design
- **Real-time Updates**: WebSocket integration
- **Offline Support**: Service worker implementation
- **Advanced UI**: Interactive maps and visualizations

---

## Conclusion

The updated architecture provides:
- **Clear Separation**: Backend logic and frontend presentation
- **Scalable Design**: Independent scaling of components
- **Maintainable Code**: Well-defined interfaces and contracts
- **Production Ready**: Comprehensive testing and monitoring

This architecture supports the current Phase 5 implementation while providing a clear path for future enhancements and production deployment.

# Frontend Architecture Specification

## Overview

This document defines the frontend architecture for the restaurant recommendation system. The frontend is built using Streamlit and provides a complete user interface for the recommendation pipeline.

## Architecture Principles

### 1. Component-Based Design
- Modular UI components with clear responsibilities
- Reusable components across different screens
- Props-based data flow between components

### 2. State Management
- Centralized state using Streamlit session state
- Clear state transitions and lifecycle management
- Error state handling and recovery

### 3. Service Integration
- Clean separation between UI and backend services
- Async service calls with proper error handling
- Loading states and user feedback

### 4. User Experience
- Progressive disclosure of information
- Clear visual hierarchy and navigation
- Responsive and accessible design

---

## Frontend Layer Structure

```
src/milestone1/phase5_ui/
├── models.py                   # Data models and enums
├── components.py               # UI rendering functions
├── app.py                      # Main application logic
├── services.py                 # Backend service integration
├── styles.py                   # CSS and styling
└── utils.py                    # Utility functions
```

---

## Data Models and State

### UI State Models

```python
@dataclass(frozen=True, slots=True)
class UIState(Enum):
    """Application UI states."""
    INPUT = "input"           # Showing input form
    LOADING = "loading"       # Processing request
    RESULTS = "results"       # Showing recommendations
    ERROR = "error"          # Showing error state
    EMPTY = "empty"          # No results found

@dataclass(frozen=True, slots=True)
class UserInput:
    """User input from form."""
    location: str
    budget_band: str | None = None
    cuisines: list[str] | None = None
    min_rating: float | None = None
    additional_preferences_text: str | None = None
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for API calls."""
        return {
            "location": self.location,
            "budget_band": self.budget_band,
            "cuisines": self.cuisines or [],
            "min_rating": self.min_rating,
            "additional_preferences_text": self.additional_preferences_text
        }

@dataclass(frozen=True, slots=True)
class UIError:
    """UI error representation."""
    title: str
    message: str
    is_retryable: bool = True
    error_code: str | None = None

@dataclass(frozen=True, slots=True)
class LoadingInfo:
    """Loading state information."""
    message: str
    step_description: str | None = None
    progress: int | None = None
```

### Session State Structure

```python
# Global session state initialization
def init_session_state():
    """Initialize Streamlit session state."""
    if "ui_state" not in st.session_state:
        st.session_state.ui_state = UIState.INPUT
    
    if "recommendations" not in st.session_state:
        st.session_state.recommendations = []
    
    if "error" not in st.session_state:
        st.session_state.error = None
    
    if "user_input_data" not in st.session_state:
        st.session_state.user_input_data = None
    
    if "processing_time" not in st.session_state:
        st.session_state.processing_time = 0.0
    
    if "candidate_count" not in st.session_state:
        st.session_state.candidate_count = 0
    
    if "using_fallback" not in st.session_state:
        st.session_state.using_fallback = False
```

---

## UI Components Architecture

### Component Hierarchy

```
App (main)
├── Header
├── InputForm
│   ├── LocationInput
│   ├── BudgetSelector
│   ├── RatingSlider
│   ├── CuisineInput
│   └── AdditionalPreferences
├── LoadingState
├── ResultsView
│   ├── RecommendationCard (repeated)
│   │   ├── RestaurantInfo
│   │   ├── CuisineTags
│   │   ├── MetricsRow
│   │   └── ExplanationSection
│   └── SidebarStats
├── EmptyState
└── ErrorState
```

### Component Specifications

#### 1. Input Form Component

```python
def render_input_form() -> dict[str, Any] | None:
    """Render the main input form.
    
    Returns:
        User input data if form submitted, None otherwise
        
    Features:
        - Real-time validation
        - Location autocomplete
        - Budget band helper text
        - Cuisine tag suggestions
        - Form state persistence
    """
    
    with st.form("recommendation_form"):
        # Location input with autocomplete
        location = render_location_input()
        
        # Budget and rating in columns
        col1, col2 = st.columns(2)
        with col1:
            budget_band = render_budget_selector()
        with col2:
            min_rating = render_rating_slider()
        
        # Cuisine input with tag suggestions
        cuisines = render_cuisine_input()
        
        # Additional preferences
        additional_text = render_additional_preferences()
        
        # Submit button
        submitted = st.form_submit_button("Get Recommendations", type="primary")
        
        if submitted:
            return validate_and_process_form_data({
                "location": location,
                "budget_band": budget_band,
                "cuisines": cuisines,
                "min_rating": min_rating,
                "additional_preferences_text": additional_text
            })
    
    return None
```

#### 2. Results View Component

```python
def render_results(recommendations: list[Recommendation]) -> None:
    """Render the recommendations results view.
    
    Args:
        recommendations: List of recommendation objects
        
    Features:
        - Restaurant cards with rich information
        - Expandable AI explanations
        - Visual budget and rating indicators
        - Sidebar with processing statistics
        - Detailed analysis modal
    """
    
    st.header("🎉 Your Restaurant Recommendations")
    
    # Summary section
    render_results_summary(recommendations)
    
    # Fallback notification
    if st.session_state.get("using_fallback", False):
        render_fallback_message()
    
    # Main results grid
    for i, rec in enumerate(recommendations, 1):
        render_recommendation_card(rec, i)
    
    # Sidebar statistics
    render_sidebar_stats()
    
    # Action buttons
    render_action_buttons()
```

#### 3. Recommendation Card Component

```python
def render_recommendation_card(rec: Recommendation, rank: int) -> None:
    """Render a single recommendation card.
    
    Args:
        rec: Recommendation object
        rank: Display rank (1-based)
        
    Features:
        - Restaurant name and rank
        - Key metrics (rating, cost, location)
        - Cuisine tags with truncation
        - Expandable AI explanation
        - Budget band indicator
        - Visual hierarchy
    """
    
    with st.container():
        st.markdown("---")
        
        # Header with rank
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(f"### #{rank}")
        with col2:
            st.markdown(f"### {rec.restaurant.name}")
        
        # Metrics row
        col1, col2, col3 = st.columns(3)
        with col1:
            render_rating_metric(rec.restaurant.rating)
        with col2:
            render_cost_metric(rec.restaurant.cost)
        with col3:
            render_location_metric(rec.restaurant.location)
        
        # Cuisine tags
        render_cuisine_tags(rec.restaurant.cuisines)
        
        # AI explanation (expandable)
        if rec.explanation:
            with st.expander("🤖 Why this restaurant?", expanded=True):
                st.markdown(rec.explanation)
        
        # Budget badge
        if rec.restaurant.budget_band:
            render_budget_badge(rec.restaurant.budget_band)
```

#### 4. Loading State Component

```python
def render_loading_state(message: str = "Finding the best restaurants for you...") -> None:
    """Render loading state with progress indication.
    
    Args:
        message: Loading message to display
        
    Features:
        - Spinner animation
        - Progress message
        - Step-by-step progress
        - Cancel option (if applicable)
    """
    
    st.info("🔄 Processing your request...")
    
    with st.spinner(message):
        # This will be replaced by actual processing
        st.empty()
```

#### 5. Error State Component

```python
def render_error_state(error: UIError) -> None:
    """Render error state with recovery options.
    
    Args:
        error: Error object with details
        
    Features:
        - Clear error message
        - Retry button if applicable
        - Error details (expandable)
        - Help suggestions
    """
    
    st.error(f"❌ {error.title}")
    st.warning(error.message)
    
    if error.is_retryable:
        if st.button("🔄 Try Again"):
            st.session_state.ui_state = UIState.INPUT
            st.rerun()
    
    # Error details (for debugging)
    if error.error_code:
        with st.expander("Error Details"):
            st.code(f"Error Code: {error.error_code}")
```

---

## Service Integration Layer

### Service Interface

```python
class RecommendationService:
    """Frontend service for backend integration."""
    
    def __init__(self):
        self.backend_api = RecommendationAPI()
    
    async def get_recommendations(self, user_input: UserInput) -> ServiceResult:
        """Get recommendations from backend.
        
        Args:
            user_input: Validated user input
            
        Returns:
            Service result with recommendations or error
        """
        try:
            response = await self.backend_api.get_recommendations(user_input.to_dict())
            
            if response.success:
                return ServiceResult(
                    success=True,
                    data=response.data,
                    processing_time=response.data.processing_stats.total_time
                )
            else:
                return ServiceResult(
                    success=False,
                    error=UIError(
                        title="API Error",
                        message=response.error.message,
                        is_retryable=response.error.retryable
                    )
                )
                
        except Exception as e:
            return ServiceResult(
                success=False,
                error=UIError(
                    title="Connection Error",
                    message="Unable to connect to the service. Please try again.",
                    is_retryable=True
                )
            )
    
    def get_available_locations(self) -> List[str]:
        """Get available locations from backend."""
        try:
            response = self.backend_api.get_locations()
            return response.data if response.success else []
        except Exception:
            return []
    
    def validate_input(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate input using backend validation."""
        try:
            response = self.backend_api.validate_input(data)
            return response.data if response.success else ValidationResult(False, ["Validation service unavailable"])
        except Exception:
            return ValidationResult(False, ["Validation service unavailable"])
```

### Service Result Models

```python
@dataclass
class ServiceResult:
    """Result from service call."""
    success: bool
    data: Any | None = None
    error: UIError | None = None
    processing_time: float | None = None

@dataclass
class ValidationResult:
    """Input validation result."""
    valid: bool
    errors: List[str]
    warnings: List[str] = None
```

---

## State Management Patterns

### State Transitions

```python
class StateManager:
    """Manages UI state transitions."""
    
    @staticmethod
    def transition_to_loading(user_input: Dict[str, Any]):
        """Transition from INPUT to LOADING state."""
        st.session_state.ui_state = UIState.LOADING
        st.session_state.user_input_data = user_input
        st.session_state.error = None
    
    @staticmethod
    def transition_to_results(recommendations: List[Recommendation], stats: Dict):
        """Transition from LOADING to RESULTS state."""
        st.session_state.ui_state = UIState.RESULTS
        st.session_state.recommendations = recommendations
        st.session_state.processing_time = stats.get("processing_time", 0.0)
        st.session_state.candidate_count = stats.get("candidate_count", 0)
        st.session_state.using_fallback = stats.get("used_fallback", False)
    
    @staticmethod
    def transition_to_error(error: UIError):
        """Transition to ERROR state."""
        st.session_state.ui_state = UIState.ERROR
        st.session_state.error = error
    
    @staticmethod
    def transition_to_empty():
        """Transition to EMPTY state."""
        st.session_state.ui_state = UIState.EMPTY
    
    @staticmethod
    def reset_to_input():
        """Reset to INPUT state."""
        st.session_state.ui_state = UIState.INPUT
        st.session_state.recommendations = []
        st.session_state.error = None
        st.session_state.user_input_data = None
```

### State Persistence

```python
class StatePersistence:
    """Handles state persistence and recovery."""
    
    @staticmethod
    def save_user_preferences(prefs: UserInput):
        """Save user preferences to session state."""
        st.session_state.saved_preferences = prefs.to_dict()
    
    @staticmethod
    def load_user_preferences() -> Dict[str, Any]:
        """Load saved user preferences."""
        return st.session_state.get("saved_preferences", {})
    
    @staticmethod
    def save_search_history(search: Dict[str, Any]):
        """Save search to history."""
        if "search_history" not in st.session_state:
            st.session_state.search_history = []
        
        st.session_state.search_history.append({
            **search,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only last 10 searches
        if len(st.session_state.search_history) > 10:
            st.session_state.search_history = st.session_state.search_history[-10:]
```

---

## Styling and Theming

### CSS Architecture

```python
# styles.py
def get_custom_css() -> str:
    """Return custom CSS for the application."""
    return """
    /* Main theme colors */
    :root {
        --primary-color: #FF6B6B;
        --secondary-color: #4ECDC4;
        --accent-color: #45B7D1;
        --success-color: #96CEB4;
        --warning-color: #FFEAA7;
        --error-color: #FD79A8;
        --text-primary: #2D3436;
        --text-secondary: #636E72;
        --background: #F8F9FA;
        --surface: #FFFFFF;
        --border: #E1E8ED;
    }
    
    /* Component styles */
    .recommendation-card {
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 16px;
        margin: 8px 0;
        background: var(--surface);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        text-align: center;
        padding: 12px;
        border-radius: 6px;
        background: var(--background);
    }
    
    .cuisine-tag {
        display: inline-block;
        background: var(--accent-color);
        color: white;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 12px;
        margin: 2px;
    }
    
    .budget-badge {
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
    }
    
    .budget-low { background: #96CEB4; color: white; }
    .budget-medium { background: #FFEAA7; color: #2D3436; }
    .budget-high { background: #FD79A8; color: white; }
    
    /* Loading states */
    .loading-container {
        text-align: center;
        padding: 40px;
    }
    
    /* Error states */
    .error-container {
        border-left: 4px solid var(--error-color);
        padding: 16px;
        margin: 16px 0;
        background: #FFF5F5;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .recommendation-card {
            padding: 12px;
        }
        
        .metric-card {
            padding: 8px;
            font-size: 14px;
        }
    }
    """

def apply_custom_styles():
    """Apply custom CSS to Streamlit app."""
    st.markdown(f"<style>{get_custom_css()}</style>", unsafe_allow_html=True)
```

---

## Accessibility and UX

### Accessibility Features

```python
def render_accessible_input(label: str, help_text: str = None, **kwargs):
    """Render accessible input component."""
    return st.text_input(
        label=label,
        help=help_text,
        **kwargs
    )

def add_aria_labels():
    """Add ARIA labels for screen readers."""
    st.markdown("""
    <script>
    // Add ARIA labels dynamically
    document.addEventListener('DOMContentLoaded', function() {
        // Add labels to recommendation cards
        const cards = document.querySelectorAll('.recommendation-card');
        cards.forEach((card, index) => {
            card.setAttribute('aria-label', `Restaurant recommendation ${index + 1}`);
        });
        
        // Add labels to metric displays
        const metrics = document.querySelectorAll('.metric-card');
        metrics.forEach(metric => {
            const label = metric.querySelector('div').textContent;
            metric.setAttribute('aria-label', label);
        });
    });
    </script>
    """, unsafe_allow_html=True)
```

### UX Enhancements

```python
def add_progressive_disclosure():
    """Add progressive disclosure patterns."""
    # Start with essential information
    # Allow users to expand for more details
    pass

def add_micro_interactions():
    """Add subtle micro-interactions."""
    # Hover effects, transitions, etc.
    st.markdown("""
    <style>
    .recommendation-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        transition: all 0.2s ease;
    }
    
    .cuisine-tag:hover {
        transform: scale(1.05);
        transition: transform 0.1s ease;
    }
    </style>
    """, unsafe_allow_html=True)
```

---

## Performance Optimization

### Component Optimization

```python
@st.cache_data(ttl=3600)
def get_location_suggestions() -> List[str]:
    """Get cached location suggestions."""
    return get_available_locations()

@st.cache_data(ttl=1800)
def get_cached_recommendations(prefs_hash: str) -> Optional[List[Recommendation]]:
    """Get cached recommendations if available."""
    # Implementation for caching
    pass

def optimize_rendering():
    """Optimize component rendering performance."""
    # Use memoization for expensive operations
    # Lazy load components
    # Optimize re-renders
    pass
```

### Loading Optimization

```python
def render_progressive_loading():
    """Render components progressively for better perceived performance."""
    # Show skeleton screens while loading
    # Load critical content first
    # Defer non-critical content
    pass
```

---

## Testing Strategy

### Component Testing

```python
def test_input_form_validation():
    """Test input form validation."""
    # Test required fields
    # Test format validation
    # Test error messages
    pass

def test_results_display():
    """Test results display functionality."""
    # Test empty results
    # Test single result
    # Test multiple results
    # Test fallback display
    pass

def test_state_transitions():
    """Test state machine transitions."""
    # Test all valid transitions
    # Test invalid transitions
    # Test error recovery
    pass
```

### Integration Testing

```python
def test_backend_integration():
    """Test backend service integration."""
    # Test API calls
    # Test error handling
    # Test timeout handling
    pass

def test_end_to_end_flow():
    """Test complete user journey."""
    # Test happy path
    # Test error paths
    # Test edge cases
    pass
```

This frontend architecture provides a comprehensive, maintainable, and scalable foundation for the restaurant recommendation system's user interface.

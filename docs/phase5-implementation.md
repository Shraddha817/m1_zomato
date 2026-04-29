# Phase 5 Implementation - Web UI

## Overview

Phase 5 provides a complete web-based user interface for the restaurant recommendation system. It implements the full user journey from preference input to AI-powered recommendations, with proper error handling and observability.

## Architecture

### Components

1. **Models** (`src/milestone1/phase5_ui/models.py`)
   - `UIState`: Enum representing UI states (input, loading, results, error, empty)
   - `UserInput`: Dataclass for form input validation
   - `UIError`: Structured error representation
   - `LoadingInfo`: Loading state information

2. **Components** (`src/milestone1/phase5_ui/components.py`)
   - `render_input_form()`: User preference input form
   - `render_results()`: Recommendation results display
   - `render_empty_state()`: No results found state
   - `render_error_state()`: Error display with retry options
   - `render_loading_state()`: Loading spinner with progress
   - `render_fallback_message()`: Fallback recommendation notice
   - `get_available_locations()`: Location autocomplete suggestions

3. **App** (`src/milestone1/phase5_ui/app.py`)
   - `create_app()`: Main Streamlit application
   - State management with session state
   - End-to-end request processing
   - Integration with all previous phases

## Features

### Input Form
- **Location**: Required text input with autocomplete suggestions
- **Budget Band**: Optional dropdown (low/medium/high)
- **Minimum Rating**: Optional slider (1.0-5.0)
- **Cuisines**: Optional comma-separated input
- **Additional Preferences**: Optional free text area

### Results Display
- **Restaurant Cards**: Rank, name, rating, cost, location
- **Cuisine Tags**: Visual cuisine representation
- **AI Explanations**: Expandable LLM-generated reasoning
- **Budget Badges**: Visual budget band indicators
- **Processing Metrics**: Sidebar with timing and statistics

### Error Handling
- **Graceful Degradation**: Falls back to deterministic recommendations
- **User-Friendly Messages**: Clear error descriptions
- **Retry Mechanisms**: Easy retry buttons on failures
- **Empty State**: Helpful suggestions when no results found

### Observability
- **Processing Time**: Request timing measurement
- **Candidate Counts**: Filter statistics
- **LLM Status**: Fallback vs AI recommendations
- **Logging**: Structured error and progress logging

## File Structure

```
src/milestone1/phase5_ui/
├── __init__.py              # Package exports
├── models.py                # Data models and enums
├── components.py            # UI rendering functions
└── app.py                   # Main Streamlit application

apps/web/
└── app.py                   # Updated to use Phase 5

requirements-phase5.txt      # Phase 5 dependencies
test_phase5_ui.py           # Comprehensive test suite
```

## Installation & Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements-phase5.txt
   ```

2. **Environment Setup**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run the Application**:
   ```bash
   cd apps/web
   streamlit run app.py
   ```

## User Journey

### 1. Input Phase
- User fills preference form
- Validation ensures required fields
- Submit triggers processing

### 2. Processing Phase
- Loading state with spinner
- Data ingestion from Hugging Face
- Candidate filtering based on preferences
- LLM recommendation generation
- Fallback if LLM fails

### 3. Results Phase
- Display top 5 recommendations
- AI explanations for each choice
- Detailed restaurant information
- Processing statistics in sidebar

### 4. Error/Empty States
- Clear error messages with retry options
- Helpful suggestions for no results
- Graceful fallback notifications

## Integration Points

### Phase 1 - Data Ingestion
```python
from milestone1.ingestion import load_restaurants
restaurants = load_restaurants(limit=1000)
```

### Phase 2 - User Preferences
```python
from milestone1.phase2_preferences.models import UserPreferences
prefs = UserPreferences(...)
```

### Phase 3 - Filtering & Prompting
```python
from milestone1.phase3_integration.filtering import filter_candidates
from milestone1.phase3_integration.prompting import build_prompt_payload
```

### Phase 4 - LLM Recommendations
```python
from milestone1.phase4_recommendation.client import get_recommendations
recommendations = get_recommendations(prompt_payload, candidates, top_k=5)
```

## Testing

Run the comprehensive test suite:

```bash
python test_phase5_ui.py
```

Tests cover:
- ✅ Component imports
- ✅ Model functionality
- ✅ Phase integration
- ✅ UI functionality

## Configuration

### Environment Variables
- `XAI_API_KEY`: xAI Grok API key (for LLM recommendations)
- `XAI_MODEL`: Model name (default: grok-beta)
- `HF_TOKEN`: Hugging Face token (for rate limits)
- `CANDIDATE_CAP`: Max candidates for LLM context

### UI Customization
- Modify `components.py` for visual changes
- Update `models.py` for new data structures
- Extend `app.py` for additional features

## Performance Considerations

- **Data Loading**: Limited to 1000 restaurants for responsiveness
- **Candidate Capping**: Maximum 50 candidates, 20 sent to LLM
- **Timeout Settings**: 30-second LLM timeout with fallback
- **Caching**: Streamlit's built-in session state caching

## Future Enhancements

### Phase 6 (Hardening)
- [ ] Add comprehensive test fixtures
- [ ] Implement caching strategies
- [ ] Add performance monitoring
- [ ] Pin dataset revisions
- [ ] Document limitations

### Additional Features
- [ ] Restaurant detail pages
- [ ] User preference saving
- [ ] Map integration
- [ ] Review aggregation
- [ ] Mobile responsiveness improvements

## Troubleshooting

### Common Issues

1. **LLM API Errors**: System automatically falls back to deterministic recommendations
2. **Data Loading Issues**: Check Hugging Face connectivity and token
3. **Import Errors**: Ensure all dependencies installed and paths correct
4. **UI Not Rendering**: Check Streamlit version and browser compatibility

### Debug Mode

Enable debug logging by setting:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Security Considerations

- API keys loaded from environment variables only
- No user data logged beyond necessary metrics
- Input validation on all form fields
- Safe fallback when external services fail

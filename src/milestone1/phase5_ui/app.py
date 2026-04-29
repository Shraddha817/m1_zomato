"""Main Streamlit application for Phase 5 UI."""

import logging
import time
from typing import Any

import streamlit as st

from milestone1.ingestion import load_restaurants
from milestone1.phase2_preferences.models import UserPreferences
from milestone1.phase3_integration.filtering import filter_candidates
from milestone1.phase3_integration.prompting import build_prompt_payload
from milestone1.phase4_recommendation.client import get_recommendations

from .components import (
    render_empty_state,
    render_error_state,
    render_input_form,
    render_loading_state,
    render_results,
    render_fallback_message,
)
from .models import UIError, UIState, UserInput

logger = logging.getLogger(__name__)


def create_app() -> None:
    """Create and configure the Streamlit application."""
    # Configure page
    st.set_page_config(
        page_title="Restaurant Recommender (Milestone 1)",
        page_icon="🍽️",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize session state
    _init_session_state()
    
    # Main app logic
    _run_app()


def _init_session_state() -> None:
    """Initialize Streamlit session state variables."""
    if "ui_state" not in st.session_state:
        st.session_state.ui_state = UIState.INPUT
    
    if "recommendations" not in st.session_state:
        st.session_state.recommendations = []
    
    if "error" not in st.session_state:
        st.session_state.error = None
    
    if "processing_time" not in st.session_state:
        st.session_state.processing_time = 0.0
    
    if "candidate_count" not in st.session_state:
        st.session_state.candidate_count = 0
    
    if "user_input_data" not in st.session_state:
        st.session_state.user_input_data = None


def _run_app() -> None:
    """Main application logic."""
    # Handle different states
    if st.session_state.ui_state == UIState.INPUT:
        _handle_input_state()
    elif st.session_state.ui_state == UIState.LOADING:
        _handle_loading_state()
    elif st.session_state.ui_state == UIState.RESULTS:
        _handle_results_state()
    elif st.session_state.ui_state == UIState.ERROR:
        _handle_error_state()
    elif st.session_state.ui_state == UIState.EMPTY:
        _handle_empty_state()


def _handle_input_state() -> None:
    """Handle the input form state."""
    user_input_data = render_input_form()
    
    if user_input_data:
        # Store user input in session state
        st.session_state.user_input_data = user_input_data
        # Transition to loading state
        st.session_state.ui_state = UIState.LOADING
        st.session_state.error = None
        st.rerun()


def _handle_loading_state() -> None:
    """Handle the loading state and process the request."""
    render_loading_state("Finding the best restaurants for you...")
    
    try:
        # Get user input from previous form submission
        user_input_data = _get_user_input_from_form()
        
        # Process the recommendation request
        start_time = time.time()
        recommendations = _process_recommendation_request(user_input_data)
        processing_time = time.time() - start_time
        
        # Store results
        st.session_state.recommendations = recommendations
        st.session_state.processing_time = processing_time
        
        # Determine next state
        if not recommendations:
            st.session_state.ui_state = UIState.EMPTY
        else:
            st.session_state.ui_state = UIState.RESULTS
        
        st.rerun()
        
    except Exception as e:
        logger.exception(f"Error processing recommendation request: {e}")
        st.session_state.error = UIError(
            title="Processing Error",
            message="We encountered an error while processing your request. Please try again.",
            is_retryable=True
        )
        st.session_state.ui_state = UIState.ERROR
        st.rerun()


def _handle_results_state() -> None:
    """Handle the results display state."""
    recommendations = st.session_state.recommendations
    processing_time = st.session_state.processing_time
    candidate_count = st.session_state.candidate_count
    
    # Check if using fallback
    using_fallback = any(
        "We couldn't generate a personalized reason" in rec.explanation 
        for rec in recommendations
    )
    
    if using_fallback:
        render_fallback_message()
    
    # Render results
    render_results(recommendations)
    
    # Show processing info in sidebar
    with st.sidebar:
        st.markdown("### 📊 Processing Info")
        st.metric("⏱️ Processing Time", f"{processing_time:.2f}s")
        st.metric("🔍 Candidates Found", candidate_count)
        st.metric("🎯 Recommendations", len(recommendations))
        
        if using_fallback:
            st.warning("⚠️ Used fallback recommendations")
    
    # Action buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 New Search", type="primary"):
            st.session_state.ui_state = UIState.INPUT
            st.session_state.recommendations = []
            st.rerun()
    
    with col2:
        if st.button("📊 View Details"):
            _show_detailed_analysis()


def _handle_error_state() -> None:
    """Handle the error state."""
    error = st.session_state.error
    if error:
        render_error_state(error)
    else:
        # Generic error
        render_error_state(UIError(
            title="Unknown Error",
            message="An unexpected error occurred. Please try again.",
            is_retryable=True
        ))


def _handle_empty_state() -> None:
    """Handle the empty results state."""
    render_empty_state("No restaurants match your criteria. Try adjusting your filters.")
    
    if st.button("🔄 Try Again"):
        st.session_state.ui_state = UIState.INPUT
        st.rerun()


def _get_user_input_from_form() -> dict[str, Any]:
    """Extract user input from the previous form submission."""
    return st.session_state.get("user_input_data", {
        "location": "Banashankari",  # Default fallback
        "budget_band": "high",
        "cuisines": [],
        "min_rating": None,
        "additional_preferences_text": None
    })


def _process_recommendation_request(user_input_data: dict[str, Any]) -> list[Any]:
    """Process the recommendation request and return recommendations."""
    from .models import UserInput
    
    # Create UserInput object
    user_input = UserInput(
        location=user_input_data["location"],
        budget_band=user_input_data.get("budget_band"),
        cuisines=user_input_data.get("cuisines"),
        min_rating=user_input_data.get("min_rating"),
        additional_preferences_text=user_input_data.get("additional_preferences_text")
    )
    
    # Convert to UserPreferences
    prefs = UserPreferences(
        location=user_input.location,
        budget_band=user_input.budget_band,
        cuisines=tuple(user_input.cuisines) if user_input.cuisines else (),
        min_rating=user_input.min_rating,
        additional_preferences_text=user_input.additional_preferences_text
    )
    
    # Load restaurants
    logger.info("Loading restaurant data...")
    restaurants = load_restaurants(limit=1000)
    
    # Filter candidates
    logger.info(f"Filtering candidates for location: {prefs.location}")
    candidates = filter_candidates(restaurants, prefs, limit=50)
    st.session_state.candidate_count = len(candidates)
    
    if not candidates:
        logger.warning("No candidates found after filtering")
        return []
    
    # Get recommendations
    logger.info(f"Getting recommendations from LLM with {len(candidates)} candidates")
    prompt_payload = build_prompt_payload(candidates[:20], prefs)
    recommendations = get_recommendations(prompt_payload, candidates[:20], top_k=5)
    
    logger.info(f"Generated {len(recommendations)} recommendations")
    return recommendations


def _show_detailed_analysis() -> None:
    """Show detailed analysis of the recommendations."""
    st.markdown("### 📊 Detailed Analysis")
    
    recommendations = st.session_state.recommendations
    
    if not recommendations:
        st.warning("No recommendations to analyze.")
        return
    
    # Statistics
    with st.expander("📈 Recommendation Statistics", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_cost = sum(r.restaurant.cost for r in recommendations if r.restaurant.cost) / len([r for r in recommendations if r.restaurant.cost]) if recommendations else 0
            st.metric("💰 Average Cost", f"Rs.{avg_cost:.0f}")
        
        with col2:
            avg_rating = sum(r.restaurant.rating for r in recommendations if r.restaurant.rating) / len([r for r in recommendations if r.restaurant.rating]) if recommendations else 0
            st.metric("⭐ Average Rating", f"{avg_rating:.1f}/5.0" if avg_rating > 0 else "N/A")
        
        with col3:
            budget_counts = {}
            for rec in recommendations:
                band = rec.restaurant.budget_band
                if band:
                    budget_counts[band] = budget_counts.get(band, 0) + 1
            most_common = max(budget_counts.items(), key=lambda x: x[1])[0] if budget_counts else "N/A"
            st.metric("🎯 Most Common Budget", most_common.title())
    
    # Cuisine analysis
    with st.expander("🍽️ Cuisine Analysis", expanded=False):
        all_cuisines = []
        for rec in recommendations:
            all_cuisines.extend(rec.restaurant.cuisines)
        
        if all_cuisines:
            cuisine_counts = {}
            for cuisine in all_cuisines:
                cuisine_counts[cuisine] = cuisine_counts.get(cuisine, 0) + 1
            
            # Sort by frequency
            sorted_cuisines = sorted(cuisine_counts.items(), key=lambda x: x[1], reverse=True)
            
            for cuisine, count in sorted_cuisines[:10]:  # Top 10
                st.write(f"**{cuisine}:** {count} restaurant(s)")
        else:
            st.write("No cuisine data available.")


if __name__ == "__main__":
    create_app()

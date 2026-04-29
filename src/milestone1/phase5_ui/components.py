"""UI components for the restaurant recommendation web application."""

import streamlit as st
from typing import Any

from milestone1.phase2_preferences.models import UserPreferences
from milestone1.phase4_recommendation.models import Recommendation

from .models import UIError, UIState


def render_input_form() -> dict[str, Any] | None:
    """Render the input form and return user data when submitted."""
    st.header("🍽️ Restaurant Recommendations")
    st.subheader("Tell us your preferences")
    
    with st.form("recommendation_form"):
        # Location (required)
        location = st.text_input(
            "Location *",
            placeholder="e.g., Banashankari, BTM, JP Nagar",
            help="Enter the area or locality where you want to find restaurants"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Budget band
            budget_band = st.selectbox(
                "Budget Band",
                options=["", "low", "medium", "high"],
                format_func=lambda x: {
                    "": "No preference",
                    "low": "Low (≤ Rs.300)",
                    "medium": "Medium (Rs.301-700)", 
                    "high": "High (> Rs.700)"
                }.get(x, x),
                help="Filter by price range"
            )
        
        with col2:
            # Minimum rating
            min_rating = st.slider(
                "Minimum Rating",
                min_value=1.0,
                max_value=5.0,
                value=3.0,
                step=0.5,
                help="Minimum restaurant rating (optional)"
            )
        
        # Cuisines
        cuisines_text = st.text_input(
            "Cuisines (optional)",
            placeholder="e.g., North Indian, Chinese, Italian",
            help="Comma-separated list of preferred cuisines"
        )
        
        # Additional preferences
        additional_text = st.text_area(
            "Additional Preferences (optional)",
            placeholder="Any specific requirements or preferences...",
            help="Tell us more about what you're looking for"
        )
        
        # Submit button
        submitted = st.form_submit_button("Get Recommendations", type="primary")
        
        if submitted:
            # Validate required field
            if not location.strip():
                st.error("Please enter a location")
                return None
            
            # Process cuisines
            cuisines = []
            if cuisines_text.strip():
                cuisines = [c.strip() for c in cuisines_text.split(",") if c.strip()]
            
            # Process budget band
            budget_band_value = budget_band if budget_band else None
            
            # Process rating
            min_rating_value = min_rating if min_rating > 0 else None
            
            # Process additional text
            additional_text_value = additional_text.strip() if additional_text.strip() else None
            
            return {
                "location": location.strip(),
                "budget_band": budget_band_value,
                "cuisines": cuisines,
                "min_rating": min_rating_value,
                "additional_preferences_text": additional_text_value
            }
    
    return None


def render_loading_state(message: str = "Finding the best restaurants for you...") -> None:
    """Render loading state with spinner."""
    st.info("🔄 Processing your request...")
    
    with st.spinner(message):
        st.empty()  # This will be replaced by the actual processing


def render_results(recommendations: list[Recommendation]) -> None:
    """Render the recommendations results."""
    st.header("🎉 Your Restaurant Recommendations")
    
    if not recommendations:
        st.warning("No recommendations available.")
        return
    
    # Summary
    st.success(f"Found {len(recommendations)} great restaurants for you!")
    
    # Render each recommendation
    for i, rec in enumerate(recommendations, 1):
        restaurant = rec.restaurant
        
        with st.container():
            # Restaurant card
            st.markdown("---")
            
            # Header with rank and name
            col1, col2 = st.columns([1, 4])
            
            with col1:
                st.markdown(f"### #{rec.rank}")
            
            with col2:
                st.markdown(f"### {restaurant.name}")
            
            # Restaurant details
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if restaurant.rating:
                    st.metric("⭐ Rating", f"{restaurant.rating}/5.0")
                else:
                    st.metric("⭐ Rating", "Not rated")
            
            with col2:
                if restaurant.cost:
                    st.metric("💰 Cost", f"Rs.{restaurant.cost:.0f}")
                else:
                    st.metric("💰 Cost", "Not available")
            
            with col3:
                st.metric("📍 Location", restaurant.location)
            
            # Cuisines
            if restaurant.cuisines:
                cuisine_tags = " ".join([f"`{c}`" for c in restaurant.cuisines[:5]])
                if len(restaurant.cuisines) > 5:
                    cuisine_tags += f" +{len(restaurant.cuisines)-5} more"
                st.markdown(f"**Cuisines:** {cuisine_tags}")
            
            # AI explanation
            if rec.explanation:
                with st.expander("🤖 Why this restaurant?", expanded=True):
                    st.markdown(rec.explanation)
            
            # Budget band badge
            if restaurant.budget_band:
                color = {
                    "low": "🟢",
                    "medium": "🟡", 
                    "high": "🔴"
                }.get(restaurant.budget_band, "⚪")
                st.caption(f"{color} Budget: {restaurant.budget_band.title()}")


def render_empty_state(message: str = "No restaurants match your criteria") -> None:
    """Render empty state when no results are found."""
    st.warning("😔 No Results Found")
    st.info(message)
    
    st.markdown("### Suggestions:")
    st.markdown("""
    - Try a different location
    - Adjust your budget preferences
    - Lower the minimum rating requirement
    - Remove cuisine filters
    """)
    
    if st.button("🔄 Try Again"):
        st.rerun()


def render_error_state(error: UIError) -> None:
    """Render error state."""
    st.error(f"❌ {error.title}")
    st.warning(error.message)
    
    if error.is_retryable:
        if st.button("🔄 Try Again"):
            st.rerun()


def render_fallback_message() -> None:
    """Render message when using fallback recommendations."""
    st.info("🤖 **AI recommendations unavailable** - Showing top-rated matches based on your filters")


def get_available_locations() -> list[str]:
    """Get list of available locations from the dataset (for autocomplete suggestions)."""
    try:
        from milestone1.ingestion import load_restaurants
        
        # Load a small sample to get locations
        restaurants = load_restaurants(limit=100)
        locations = list(set(r.location for r in restaurants if r.location))
        return sorted(locations)
    except Exception:
        return []  # Return empty list if loading fails

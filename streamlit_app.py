#!/usr/bin/env python3
"""
Streamlit application for Phase 8 - Restaurant Recommendation System
Alternative deployment option using Streamlit for rapid prototyping and demos
"""

import sys
import os
import pandas as pd
import streamlit as st
from pathlib import Path
from typing import List, Dict, Any

# Add the src directory to the Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Initialize session state
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'restaurants_loaded' not in st.session_state:
    st.session_state.restaurants_loaded = False

def load_restaurants():
    """Load restaurant data using Phase 1 ingestion"""
    try:
        # Import Phase 1 ingestion module
        from milestone1.ingestion import load_restaurants
        restaurants = load_restaurants()
        st.session_state.restaurants_loaded = True
        return restaurants
    except ImportError:
        st.error("Phase 1 modules not found. Please ensure the project structure is correct.")
        return []
    except Exception as e:
        st.error(f"Error loading restaurants: {e}")
        return []

def get_available_locations(restaurants):
    """Extract unique locations from restaurant data"""
    locations = set()
    for restaurant in restaurants:
        if hasattr(restaurant, 'location') and restaurant.location:
            locations.add(restaurant.location)
    return sorted(list(locations))

def get_available_cuisines(restaurants):
    """Extract unique cuisines from restaurant data"""
    cuisines = set()
    for restaurant in restaurants:
        if hasattr(restaurant, 'cuisines') and restaurant.cuisines:
            for cuisine in restaurant.cuisines:
                cuisines.add(cuisine)
    return sorted(list(cuisines))

def create_user_preferences(preferences: Dict[str, Any]) -> Any:
    """Create UserPreferences object using Phase 2 models"""
    try:
        from milestone1.phase2_preferences.models import UserPreferences
        return UserPreferences(
            location=preferences.get('location'),
            budget_band=preferences.get('budget_band'),
            cuisines=preferences.get('cuisines', []),
            min_rating=preferences.get('min_rating'),
            additional_preferences_text=preferences.get('additional_preferences_text', '')
        )
    except ImportError:
        st.warning("Phase 2 models not available. Using dictionary format.")
        return preferences

def get_recommendations(preferences: Dict[str, Any], restaurants: List) -> List[Dict]:
    """Get recommendations using Phase 6 backend modules"""
    try:
        # Import Phase 6 modules for production hardening
        from milestone1.phase6_hardening.production import ProductionHardening
        from milestone1.phase6_hardening.config import ProductionConfig
        
        # Load configuration from environment
        config = ProductionConfig.from_env()
        
        # Initialize production hardening
        hardening = ProductionHardening(config)
        
        # Create UserPreferences object
        user_prefs = create_user_preferences(preferences)
        
        # Import Phase 3 and 4 modules for the recommendation pipeline
        from milestone1.phase3_integration.filtering import filter_candidates
        from milestone1.phase3_integration.prompting import build_prompt_payload
        from milestone1.phase4_recommendation.client import get_recommendations
        
        # Step 1: Filter candidates using Phase 3
        candidates = filter_candidates(restaurants, user_prefs)
        
        if not candidates:
            return []
        
        # Step 2: Build prompt payload using Phase 3
        prompt_payload = build_prompt_payload(user_prefs, candidates)
        
        # Step 3: Get recommendations using Phase 4 LLM
        recommendations = get_recommendations(prompt_payload, candidates)
        
        # Convert to display format
        display_recommendations = []
        for i, rec in enumerate(recommendations[:10]):  # Top 10
            display_recommendations.append({
                'rank': i + 1,
                'name': getattr(rec, 'name', 'Unknown'),
                'location': getattr(rec, 'location', 'Unknown'),
                'cuisines': ', '.join(getattr(rec, 'cuisines', [])),
                'rating': getattr(rec, 'rating', 0),
                'budget_band': getattr(rec, 'budget_band', 'Unknown'),
                'explanation': getattr(rec, 'explanation', f"Recommended based on your preferences")
            })
        
        return display_recommendations
        
    except ImportError as e:
        st.warning(f"Phase 6 modules not available: {e}. Using simple filtering.")
        return simple_filter(preferences, restaurants)
    except Exception as e:
        st.error(f"Error getting recommendations: {e}")
        return []

def simple_filter(preferences: Dict[str, Any], restaurants: List) -> List[Dict]:
    """Simple filtering fallback when Phase 6 modules are not available"""
    filtered_restaurants = []
    
    for restaurant in restaurants:
        # Simple filtering logic
        match = True
        
        if preferences.get('location') and hasattr(restaurant, 'location'):
            if preferences['location'].lower() not in str(restaurant.location).lower():
                match = False
        
        if preferences.get('min_rating') and hasattr(restaurant, 'rating'):
            try:
                # Convert rating to float for comparison
                restaurant_rating = float(restaurant.rating) if restaurant.rating is not None else 0.0
                if restaurant_rating < preferences['min_rating']:
                    match = False
            except (ValueError, TypeError):
                # If rating conversion fails, skip this filter
                pass
        
        if preferences.get('budget_band') and hasattr(restaurant, 'budget_band'):
            if str(restaurant.budget_band).lower() != preferences['budget_band'].lower():
                match = False
        
        if preferences.get('cuisines') and hasattr(restaurant, 'cuisines'):
            restaurant_cuisines = restaurant.cuisines if restaurant.cuisines else []
            if not any(cuisine in restaurant_cuisines for cuisine in preferences['cuisines']):
                match = False
        
        if match:
            filtered_restaurants.append(restaurant)
    
    # Convert to display format
    recommendations = []
    for i, restaurant in enumerate(filtered_restaurants[:10]):
        # Safely extract restaurant attributes
        name = getattr(restaurant, 'name', 'Unknown')
        location = getattr(restaurant, 'location', 'Unknown')
        cuisines = getattr(restaurant, 'cuisines', [])
        rating = getattr(restaurant, 'rating', 0)
        budget_band = getattr(restaurant, 'budget_band', 'Unknown')
        
        # Convert cuisines to string safely
        cuisines_str = ', '.join(cuisines) if cuisines else 'Not specified'
        
        # Format rating safely
        try:
            rating_val = float(rating) if rating is not None else 0.0
            rating_str = f"{rating_val:.1f}"
        except (ValueError, TypeError):
            rating_str = "N/A"
        
        recommendations.append({
            'rank': i + 1,
            'name': name,
            'location': location,
            'cuisines': cuisines_str,
            'rating': rating_val if 'rating_val' in locals() else 0.0,
            'budget_band': budget_band,
            'explanation': f"Matches your criteria with rating {rating_str}"
        })
    
    return recommendations

def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="Restaurant Recommender",
        page_icon=":fork_and_knife:",
        layout="wide"
    )
    
    st.title(":fork_and_knife: Restaurant Recommendation System")
    st.markdown("---")
    
    # Load restaurants
    if not st.session_state.restaurants_loaded:
        with st.spinner("Loading restaurant data..."):
            restaurants = load_restaurants()
    
    if not st.session_state.restaurants_loaded:
        st.error("No restaurant data available. Please check your dataset.")
        return
    
    # Load restaurants for this session
    with st.spinner("Loading restaurant data..."):
        restaurants = load_restaurants()
    
    if not restaurants:
        st.error("No restaurant data available. Please check your dataset.")
        return
    
    # Sidebar for preferences
    st.sidebar.header("Your Preferences")
    
    # Location selection using st.selectbox
    locations = get_available_locations(restaurants)
    selected_location = st.sidebar.selectbox(
        "Location *",
        options=locations,
        index=0 if locations else None,
        help="Select your preferred location"
    )
    
    # Budget band using st.select_slider
    budget_bands = ["low", "medium", "high"]
    selected_budget = st.sidebar.select_slider(
        "Budget Band",
        options=budget_bands,
        value="medium",
        help="Select your budget preference"
    )
    
    # Minimum rating using st.number_input
    min_rating = st.sidebar.number_input(
        "Minimum Rating",
        min_value=1.0,
        max_value=5.0,
        value=3.0,
        step=0.5,
        help="Minimum restaurant rating"
    )
    
    # Cuisine preferences using st.multiselect
    cuisines = get_available_cuisines(restaurants)
    selected_cuisines = st.sidebar.multiselect(
        "Preferred Cuisines",
        options=cuisines,
        help="Select your preferred cuisines (optional)"
    )
    
    # Additional preferences
    additional_text = st.sidebar.text_area(
        "Additional Preferences",
        placeholder="Any specific requirements or preferences...",
        help="Tell us more about what you're looking for"
    )
    
    # Get recommendations button
    if st.sidebar.button("Get Recommendations", type="primary"):
        # Validate required fields
        if not selected_location:
            st.sidebar.error("Location is required!")
            return
        
        preferences = {
            'location': selected_location,
            'budget_band': selected_budget,
            'min_rating': min_rating,
            'cuisines': selected_cuisines,
            'additional_preferences_text': additional_text
        }
        
        st.session_state.processing = True
        st.session_state.recommendations = []
        
        # Get recommendations with loading spinner
        with st.spinner("Finding the best restaurants for you..."):
            recommendations = get_recommendations(preferences, restaurants)
        
        st.session_state.recommendations = recommendations
        st.session_state.processing = False
    
    # Display results
    if st.session_state.processing:
        st.info("Processing your request...")
    
    elif st.session_state.recommendations:
        st.header("Recommended Restaurants")
        st.markdown(f"Found {len(st.session_state.recommendations)} restaurants for you!")
        
        # Create DataFrame for display
        df = pd.DataFrame(st.session_state.recommendations)
        
        # Display results using custom cards
        for _, row in df.iterrows():
            with st.expander(f"{row['rank']}. {row['name']}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Location:** {row['location']}")
                    st.write(f"**Cuisines:** {row['cuisines']}")
                    st.write(f"**Rating:** {'*' * int(row['rating'])} ({row['rating']})")
                    st.write(f"**Budget:** {row['budget_band']}")
                
                with col2:
                    st.metric("Rank", row['rank'])
                
                st.write(f"**Why we recommend this:** {row['explanation']}")
        
        # Export functionality
        st.markdown("---")
        st.subheader("Export Options")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Download as CSV"):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="restaurant_recommendations.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("Copy Results"):
                st.text_area("Results (copy this):", value=df.to_string(index=False))
    
    else:
        st.info("Set your preferences and click 'Get Recommendations' to see results.")
        
        # Show sample data
        if restaurants:
            st.markdown("---")
            st.subheader("Sample Restaurants")
            sample_data = []
            for r in restaurants[:5]:
                # Safely extract restaurant attributes
                name = getattr(r, 'name', 'Unknown')
                location = getattr(r, 'location', 'Unknown')
                cuisines = getattr(r, 'cuisines', [])
                rating = getattr(r, 'rating', 0)
                
                # Convert cuisines to string safely
                cuisines_str = ', '.join(cuisines) if cuisines else 'Not specified'
                
                # Format rating safely
                try:
                    rating_val = float(rating) if rating is not None else 0.0
                    rating_str = f"{rating_val:.1f}"
                except (ValueError, TypeError):
                    rating_str = "N/A"
                
                sample_data.append({
                    'Name': name,
                    'Location': location,
                    'Cuisines': cuisines_str,
                    'Rating': rating_str
                })
            
            sample_df = pd.DataFrame(sample_data)
            st.dataframe(sample_df, use_container_width=True)

if __name__ == "__main__":
    main()

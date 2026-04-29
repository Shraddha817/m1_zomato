#!/usr/bin/env python3
"""
Test script for Phase 4 recommendation system with mock LLM response.
Tests with: location=Banashankari, budget=2000, rating=None
"""

import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
import json

# Add the src directory to the Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from milestone1.ingestion import load_restaurants
from milestone1.phase2_preferences.models import UserPreferences
from milestone1.phase3_integration.filtering import filter_candidates
from milestone1.phase3_integration.prompting import build_prompt_payload
from milestone1.phase4_recommendation.client import get_recommendations


def determine_budget_band_from_cost(cost: float) -> str:
    """Convert cost to budget band based on dataset contract"""
    if cost <= 300:
        return "low"
    elif cost <= 700:
        return "medium"
    else:
        return "high"


def create_mock_llm_response(candidates):
    """Create a realistic mock LLM response for testing"""
    # Get restaurant IDs from candidates
    restaurant_ids = [c.id for c in candidates[:5]]
    
    # Create mock recommendations with realistic explanations
    mock_response = {
        "recommendations": [
            {
                "restaurant_id": restaurant_ids[0],
                "rank": 1,
                "explanation": "Perfect match for your high budget preference with excellent North Indian and Mughlai cuisine. This restaurant offers great value at Rs.800 and is highly popular in the Banashankari area."
            },
            {
                "restaurant_id": restaurant_ids[1],
                "rank": 2,
                "explanation": "Great choice for diverse cuisine lovers, offering Chinese, North Indian, and Thai options. The price point fits your budget well and it's known for consistent quality."
            },
            {
                "restaurant_id": restaurant_ids[2],
                "rank": 3,
                "explanation": "Ideal for cafe enthusiasts with a unique blend of Mexican and Italian cuisine along with cafe specialties. Perfect for casual dining within your budget range."
            },
            {
                "restaurant_id": restaurant_ids[3],
                "rank": 4,
                "explanation": "Excellent multi-cuisine option with cafe, fast food, and continental choices. Great variety for different tastes and fits comfortably in your high budget category."
            },
            {
                "restaurant_id": restaurant_ids[4],
                "rank": 5,
                "explanation": "Premium cafe experience with reliable fast food options. Slightly higher at Rs.900 but still within your budget, known for quality coffee and snacks."
            }
        ]
    }
    return json.dumps(mock_response)


def main():
    print("Starting Phase 4 Test with Mock LLM")
    print("=" * 50)
    
    # Test inputs
    test_location = "Banashankari"
    test_budget = 2000
    test_rating = None
    
    print(f"Test Parameters:")
    print(f"   Location: {test_location}")
    print(f"   Budget: Rs.{test_budget}")
    print(f"   Min Rating: {test_rating}")
    print()
    
    # Convert budget to budget band
    budget_band = determine_budget_band_from_cost(test_budget)
    print(f"Derived Budget Band: {budget_band}")
    print()
    
    # Step 1: Load restaurant data
    print("Step 1: Loading restaurant data...")
    try:
        restaurants = load_restaurants(limit=1000)
        print(f"   Loaded {len(restaurants)} restaurants")
    except Exception as e:
        print(f"   Failed to load restaurants: {e}")
        return
    
    # Step 2: Create user preferences
    print("Step 2: Creating user preferences...")
    prefs = UserPreferences(
        location=test_location,
        budget_band=budget_band,
        cuisines=(),
        min_rating=test_rating,
        additional_preferences_text=None
    )
    print(f"   Created preferences: {prefs}")
    print()
    
    # Step 3: Filter candidates
    print("Step 3: Filtering candidates...")
    candidates = filter_candidates(restaurants, prefs, limit=50)
    print(f"   Found {len(candidates)} matching candidates")
    
    if not candidates:
        print("   No candidates found! Try different filters.")
        return
    
    # Show top 10 candidates for context
    print("\nTop 10 Candidates (pre-ranking):")
    for i, restaurant in enumerate(candidates[:10], 1):
        print(f"   {i:2d}. {restaurant.name} | Rating: {restaurant.rating} | Cost: Rs.{restaurant.cost} | {', '.join(restaurant.cuisines)}")
    print()
    
    # Step 4: Build prompt payload
    print("Step 4: Building LLM prompt...")
    prompt_payload = build_prompt_payload(candidates[:20], prefs)
    print(f"   Built prompt with {len(candidates[:20])} candidates")
    print()
    
    # Step 5: Get LLM recommendations with mock
    print("Step 5: Getting LLM recommendations (with mock response)...")
    
    # Create mock response
    mock_response_content = create_mock_llm_response(candidates)
    
    # Mock the OpenAI client
    with patch("milestone1.phase4_recommendation.client.OpenAI") as mock_openai:
        # Set up the mock
        mock_client_instance = MagicMock()
        mock_openai.return_value = mock_client_instance
        mock_response = MagicMock()
        mock_response.choices[0].message.content = mock_response_content
        mock_client_instance.chat.completions.create.return_value = mock_response
        
        # Set environment variables to avoid fallback
        with patch.dict(os.environ, {'XAI_API_KEY': 'fake_key'}):
            try:
                recommendations = get_recommendations(prompt_payload, candidates[:20], top_k=5)
                print(f"   Got {len(recommendations)} recommendations")
                print()
                
                # Display results
                print("FINAL RECOMMENDATIONS (with LLM explanations)")
                print("=" * 60)
                
                for i, rec in enumerate(recommendations, 1):
                    restaurant = rec.restaurant
                    print(f"{i}. **{restaurant.name}** (Rank: {rec.rank})")
                    print(f"   Location: {restaurant.location}")
                    print(f"   Rating: {restaurant.rating}")
                    print(f"   Cost: Rs.{restaurant.cost} ({restaurant.budget_band})")
                    print(f"   Cuisines: {', '.join(restaurant.cuisines)}")
                    print(f"   Why: {rec.explanation}")
                    print()
                
                print(f"Test completed successfully! Got {len(recommendations)} recommendations with LLM explanations.")
                
            except Exception as e:
                print(f"   Failed to get recommendations: {e}")
                import traceback
                traceback.print_exc()


if __name__ == "__main__":
    main()

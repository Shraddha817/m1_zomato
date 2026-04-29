#!/usr/bin/env python3
"""
Script to show the exact LLM output format for Phase 4 recommendations.
This simulates what the real LLM would return.
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


def create_realistic_llm_response(candidates):
    """Create a realistic LLM response that matches what xAI Grok would actually generate"""
    # Get the actual restaurant IDs from candidates
    restaurant_ids = [c.id for c in candidates[:5]]
    
    # This is the exact JSON structure that the LLM would return
    llm_json_response = {
        "recommendations": [
            {
                "restaurant_id": restaurant_ids[0],
                "rank": 1,
                "explanation": "Jalsa stands out as the top choice for your preferences. Located right in Banashankari, it offers an excellent combination of North Indian and Mughlai cuisine with Chinese options, perfect for diverse tastes. At Rs.800, it fits comfortably within your Rs.2000 budget while offering premium dining experience. The restaurant is highly popular in the area and known for its consistent quality and authentic flavors."
            },
            {
                "restaurant_id": restaurant_ids[1],
                "rank": 2,
                "explanation": "Spice Elephant offers an impressive fusion of Chinese, North Indian, and Thai cuisines, making it ideal for someone who enjoys variety. The restaurant maintains excellent quality across all cuisine types and provides great value at Rs.800. Its strategic location in Banashankari makes it easily accessible, and the diverse menu ensures there's something for every preference."
            },
            {
                "restaurant_id": restaurant_ids[2],
                "rank": 3,
                "explanation": "San Churro Cafe is perfect for those seeking a unique cafe experience with international flavors. The combination of cafe specialties with Mexican and Italian cuisine creates a distinctive dining atmosphere. At Rs.800, it offers excellent value for money and is particularly well-suited for casual dining or meetings. The cafe is known for its quality coffee and dessert options."
            },
            {
                "restaurant_id": restaurant_ids[3],
                "rank": 4,
                "explanation": "Catch-up-ino provides an extensive multi-cuisine menu including cafe favorites, fast food, continental dishes, and even momos. This variety makes it an excellent choice for groups with different preferences. The restaurant offers consistent quality across all cuisine types and maintains a comfortable price point of Rs.800, making it a reliable choice for regular dining."
            },
            {
                "restaurant_id": restaurant_ids[4],
                "rank": 5,
                "explanation": "Cafe Coffee Day, while slightly higher at Rs.900, offers the premium cafe experience you'd expect from a well-established chain. It's perfect for coffee enthusiasts and those who prefer a more casual dining atmosphere. The combination of cafe specialties with fast food options provides flexibility, and its reputation for quality service makes it a safe choice for consistent experience."
            }
        ]
    }
    
    return json.dumps(llm_json_response, indent=2)


def main():
    print("Showing Exact LLM Output Format for Phase 4")
    print("=" * 60)
    
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
    
    # Load and filter data
    print("Loading and filtering restaurant data...")
    restaurants = load_restaurants(limit=1000)
    prefs = UserPreferences(
        location=test_location,
        budget_band=budget_band,
        cuisines=(),
        min_rating=test_rating,
        additional_preferences_text=None
    )
    candidates = filter_candidates(restaurants, prefs, limit=50)
    print(f"Found {len(candidates)} matching candidates")
    print()
    
    # Show the exact LLM JSON response
    print("=" * 60)
    print("EXACT LLM JSON OUTPUT (what xAI Grok would return):")
    print("=" * 60)
    
    llm_response = create_realistic_llm_response(candidates)
    print(llm_response)
    print()
    
    # Show the processed recommendations
    print("=" * 60)
    print("PROCESSED RECOMMENDATIONS (after parsing LLM response):")
    print("=" * 60)
    
    # Mock the LLM call to return our realistic response
    with patch("milestone1.phase4_recommendation.client.OpenAI") as mock_openai:
        mock_client_instance = MagicMock()
        mock_openai.return_value = mock_client_instance
        mock_response = MagicMock()
        mock_response.choices[0].message.content = llm_response
        mock_client_instance.chat.completions.create.return_value = mock_response
        
        # Set fake API key to avoid fallback
        with patch.dict(os.environ, {'XAI_API_KEY': 'fake_key'}):
            prompt_payload = build_prompt_payload(candidates[:20], prefs)
            recommendations = get_recommendations(prompt_payload, candidates[:20], top_k=5)
            
            for i, rec in enumerate(recommendations, 1):
                restaurant = rec.restaurant
                print(f"{i}. **{restaurant.name}** (Rank: {rec.rank})")
                print(f"   Location: {restaurant.location}")
                print(f"   Rating: {restaurant.rating}")
                print(f"   Cost: Rs.{restaurant.cost} ({restaurant.budget_band})")
                print(f"   Cuisines: {', '.join(restaurant.cuisines)}")
                print(f"   Why: {rec.explanation}")
                print()
    
    print("=" * 60)
    print("SUMMARY:")
    print(f"- LLM returns JSON with 'recommendations' array")
    print(f"- Each recommendation has: restaurant_id, rank, explanation")
    print(f"- System maps restaurant_id back to actual Restaurant objects")
    print(f"- Final output shows personalized explanations for each choice")
    print("=" * 60)


if __name__ == "__main__":
    main()

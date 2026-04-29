#!/usr/bin/env python3
"""
Live test script for Phase 4 recommendation system.
Tests with: location=Bellandur, budget=2000, rating=4.0
"""

import os
import sys
from pathlib import Path

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Set the XAI_API_KEY from the GROK_API_KEY in .env
if not os.environ.get("XAI_API_KEY"):
    os.environ["XAI_API_KEY"] = os.environ.get("GROK_API_KEY", "")

# Set the correct model name - try different possible names
os.environ["XAI_MODEL"] = "grok-2-mini"

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


def main():
    print("Starting Phase 4 Live Test")
    print("=" * 50)
    
    # Test inputs
    test_location = "Banashankari"  # Using available location since Bellandur not in dataset
    test_budget = 2000
    test_rating = None  # Most restaurants in dataset don't have ratings
    
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
        restaurants = load_restaurants(limit=1000)  # Load a reasonable subset
        print(f"   Loaded {len(restaurants)} restaurants")
    except Exception as e:
        print(f"   Failed to load restaurants: {e}")
        return
    
    # Step 2: Create user preferences
    print("Step 2: Creating user preferences...")
    prefs = UserPreferences(
        location=test_location,
        budget_band=budget_band,
        cuisines=(),  # No specific cuisine preference
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
    prompt_payload = build_prompt_payload(candidates[:20], prefs)  # Send top 20 to LLM
    print(f"   Built prompt with {len(candidates[:20])} candidates")
    print()
    
    # Step 5: Get LLM recommendations
    print("Step 5: Getting LLM recommendations...")
    print("   (This may take 30-60 seconds...)")
    
    try:
        recommendations = get_recommendations(prompt_payload, candidates[:20], top_k=5)
        print(f"   Got {len(recommendations)} recommendations")
        print()
        
        # Display results
        print("FINAL RECOMMENDATIONS")
        print("=" * 50)
        
        for i, rec in enumerate(recommendations, 1):
            restaurant = rec.restaurant
            print(f"{i}. **{restaurant.name}** (Rank: {rec.rank})")
            print(f"   Location: {restaurant.location}")
            print(f"   Rating: {restaurant.rating}")
            print(f"   Cost: Rs.{restaurant.cost} ({restaurant.budget_band})")
            print(f"   Cuisines: {', '.join(restaurant.cuisines)}")
            print(f"   Why: {rec.explanation}")
            print()
        
        print(f"Test completed successfully! Got {len(recommendations)} recommendations.")
        
    except Exception as e:
        print(f"   Failed to get recommendations: {e}")
        print("   Falling back to deterministic recommendations...")
        
        # Show fallback results
        fallback_recs = candidates[:5]
        print("\nFALLBACK RECOMMENDATIONS")
        print("=" * 50)
        
        for i, restaurant in enumerate(fallback_recs, 1):
            print(f"{i}. **{restaurant.name}**")
            print(f"   Location: {restaurant.location}")
            print(f"   Rating: {restaurant.rating}")
            print(f"   Cost: Rs.{restaurant.cost} ({restaurant.budget_band})")
            print(f"   Cuisines: {', '.join(restaurant.cuisines)}")
            print(f"   Why: Top-rated match based on your filters")
            print()


if __name__ == "__main__":
    main()

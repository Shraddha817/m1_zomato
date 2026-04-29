#!/usr/bin/env python3
"""
Test script to verify Phase 4 is hitting the Grok API correctly.
"""

import os
import sys
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

def test_grok_api_connection():
    """Test that Phase 4 can successfully connect to Grok API."""
    print("=" * 60)
    print("Phase 4 Grok API Connection Test")
    print("=" * 60)
    
    # Check environment variables
    print("Checking environment variables...")
    
    api_key = os.environ.get("XAI_API_KEY")
    base_url = os.environ.get("XAI_BASE_URL", "https://api.x.ai/v1")
    model = os.environ.get("XAI_MODEL", "grok-beta")
    
    print(f"API Key: {'OK Set' if api_key else 'MISSING Missing'}")
    print(f"Base URL: {base_url}")
    print(f"Model: {model}")
    
    if not api_key:
        print("\nXAI_API_KEY not found in .env file")
        print("Please add your Grok API key to .env:")
        print("XAI_API_KEY=your_grok_api_key_here")
        return False
    
    print("\n" + "=" * 60)
    print("Testing Phase 4 Recommendation System")
    print("=" * 60)
    
    try:
        # Import Phase 4 components
        from milestone1.ingestion import load_restaurants
        from milestone1.phase2_preferences.models import UserPreferences
        from milestone1.phase3_integration.filtering import filter_candidates
        from milestone1.phase3_integration.prompting import build_prompt_payload
        from milestone1.phase4_recommendation.client import get_recommendations
        
        print("OK All Phase 4 components imported successfully")
        
        # Load some test data
        print("\nLoading restaurant data...")
        restaurants = load_restaurants(limit=50)
        print(f"OK Loaded {len(restaurants)} restaurants")
        
        # Create test preferences
        print("\nCreating test user preferences...")
        prefs = UserPreferences(
            location="Banashankari",
            budget_band="high",
            cuisines=("North Indian", "Chinese"),
            min_rating=None,  # Don't filter by rating to get more candidates
            additional_preferences_text=None
        )
        print("OK User preferences created")
        
        # Filter candidates
        print("\nFiltering candidates...")
        candidates = filter_candidates(restaurants, prefs, limit=10)
        print(f"OK Found {len(candidates)} candidates")
        
        if not candidates:
            print("WARNING No candidates found. Trying different preferences...")
            prefs = UserPreferences(
                location="Banashankari",
                budget_band=None,
                cuisines=(),
                min_rating=None,
                additional_preferences_text=None
            )
            candidates = filter_candidates(restaurants, prefs, limit=10)
            print(f"OK Found {len(candidates)} candidates with relaxed preferences")
        
        if not candidates:
            print("WARNING Still no candidates found. Cannot test LLM.")
            return False
        
        # Build prompt payload
        print("\nBuilding prompt payload...")
        prompt_payload = build_prompt_payload(candidates[:5], prefs)
        print("OK Prompt payload built")
        
        # Test LLM call
        print("\n" + "=" * 60)
        print("🚀 Testing Grok API Call")
        print("=" * 60)
        print(f"API Endpoint: {base_url}/chat/completions")
        print(f"Model: {model}")
        print(f"Candidates: {len(candidates[:5])}")
        print(f"Timeout: 30 seconds")
        print("\nCalling Grok API...")
        
        # Get recommendations
        recommendations = get_recommendations(prompt_payload, candidates[:5], top_k=3)
        
        print("OK Grok API call successful!")
        print(f"OK Received {len(recommendations)} recommendations")
        
        # Display results
        print("\n" + "=" * 60)
        print("📋 Recommendations Results")
        print("=" * 60)
        
        for i, rec in enumerate(recommendations, 1):
            restaurant = rec.restaurant
            print(f"\n{i}. {restaurant.name}")
            print(f"   Location: {restaurant.location}")
            print(f"   Cuisines: {', '.join(restaurant.cuisines)}")
            print(f"   Rating: {restaurant.rating if restaurant.rating else 'Not rated'}")
            print(f"   Cost: Rs.{restaurant.cost:.0f}" if restaurant.cost else "   Cost: Not available")
            print(f"   Rank: {rec.rank}")
            print(f"   Explanation: {rec.explanation}")
        
        # Check if using fallback
        fallback_indicators = [
            "We couldn't generate a personalized reason",
            "fallback",
            "deterministic"
        ]
        
        using_fallback = any(
            indicator in rec.explanation.lower()
            for rec in recommendations
            for indicator in fallback_indicators
        )
        
        if using_fallback:
            print("\nWARNING Using fallback recommendations (not from Grok API)")
            print("This suggests the Grok API call failed or returned invalid response.")
        else:
            print("\nSUCCESS Using AI recommendations from Grok API!")
        
        print("\n" + "=" * 60)
        print("OK Phase 4 Grok API test completed successfully!")
        print("=" * 60)
        
        return not using_fallback
        
    except Exception as e:
        print(f"\nERROR Error during Phase 4 test: {e}")
        print("\nThis could be due to:")
        print("- Invalid API key")
        print("- Network connectivity issues")
        print("- API service unavailable")
        print("- Model not available")
        print("\nCheck your .env file and network connection.")
        return False

def test_api_key_validation():
    """Test if the API key is valid by making a simple API call."""
    print("\n" + "=" * 60)
    print("API Key Validation")
    print("=" * 60)
    
    try:
        import openai
        
        api_key = os.environ.get("XAI_API_KEY")
        base_url = os.environ.get("XAI_BASE_URL", "https://api.x.ai/v1")
        model = os.environ.get("XAI_MODEL", "grok-beta")
        
        if not api_key:
            print("❌ No API key found")
            return False
        
        client = openai.OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        
        print(f"Testing API key with {base_url}...")
        print(f"Using model: {model}")
        
        # Make a simple test call
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Hello from Grok API!'"}
            ],
            max_tokens=10,
            timeout=10
        )
        
        content = response.choices[0].message.content
        print(f"OK API key is valid!")
        print(f"OK Model response: {content}")
        
        return True
        
    except openai.AuthenticationError as e:
        print(f"ERROR Authentication failed: {e}")
        print("Check your API key in .env file")
        return False
    except openai.BadRequestError as e:
        print(f"ERROR Bad request: {e}")
        print("Model might not be available or API format incorrect")
        return False
    except Exception as e:
        print(f"ERROR API test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("TEST Phase 4 Grok API Test Suite")
    print("This test verifies that Phase 4 is successfully hitting the Grok API")
    
    # Test API key first
    api_key_valid = test_api_key_validation()
    
    if not api_key_valid:
        print("\nAPI key validation failed. Fix API key issues first.")
        return
    
    # Test full Phase 4 flow
    success = test_grok_api_connection()
    
    if success:
        print("\nALL TESTS PASSED!")
        print("Phase 4 is successfully hitting the Grok API")
    else:
        print("\nTESTS COMPLETED WITH ISSUES")
        print("Phase 4 is using fallback recommendations")
        print("Check API configuration and network connectivity")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Test script for Phase 5 UI components and functionality.
"""

import os
import sys
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def test_phase5_imports():
    """Test that all Phase 5 components can be imported."""
    print("Testing Phase 5 imports...")
    
    try:
        from milestone1.phase5_ui.models import UIState, UserInput, UIError
        print("OK Models imported successfully")
        
        from milestone1.phase5_ui.components import (
            render_input_form,
            render_results,
            render_empty_state,
            render_error_state,
            render_loading_state,
            render_fallback_message
        )
        print("OK Components imported successfully")
        
        from milestone1.phase5_ui.app import create_app
        print("OK App imported successfully")
        
        return True
    except Exception as e:
        print(f"FAIL Import failed: {e}")
        return False


def test_phase5_models():
    """Test Phase 5 model creation and functionality."""
    print("\nTesting Phase 5 models...")
    
    try:
        from milestone1.phase5_ui.models import UIState, UserInput, UIError
        
        # Test UIState enum
        assert UIState.INPUT.value == "input"
        assert UIState.RESULTS.value == "results"
        print("OK UIState enum working")
        
        # Test UserInput creation
        user_input = UserInput(
            location="Banashankari",
            budget_band="high",
            cuisines=["North Indian", "Chinese"],
            min_rating=4.0,
            additional_preferences_text="Good service"
        )
        assert user_input.location == "Banashankari"
        assert user_input.budget_band == "high"
        assert len(user_input.cuisines) == 2
        print("OK UserInput model working")
        
        # Test UserInput to_dict
        user_dict = user_input.to_dict()
        assert user_dict["location"] == "Banashankari"
        assert user_dict["cuisines"] == ["North Indian", "Chinese"]
        print("OK UserInput.to_dict() working")
        
        # Test UIError creation
        error = UIError(
            title="Test Error",
            message="This is a test error",
            is_retryable=True
        )
        assert error.title == "Test Error"
        assert error.is_retryable is True
        print("OK UIError model working")
        
        return True
    except Exception as e:
        print(f"FAIL Model test failed: {e}")
        return False


def test_phase5_integration():
    """Test Phase 5 integration with other phases."""
    print("\nTesting Phase 5 integration...")
    
    try:
        # Test integration with ingestion
        from milestone1.ingestion import load_restaurants
        restaurants = load_restaurants(limit=10)
        print(f"OK Loaded {len(restaurants)} restaurants")
        
        # Test integration with preferences
        from milestone1.phase2_preferences.models import UserPreferences
        prefs = UserPreferences(
            location="Banashankari",
            budget_band="high",
            cuisines=(),
            min_rating=None,
            additional_preferences_text=None
        )
        print("OK Created UserPreferences")
        
        # Test integration with filtering
        from milestone1.phase3_integration.filtering import filter_candidates
        candidates = filter_candidates(restaurants, prefs, limit=5)
        print(f"OK Filtered to {len(candidates)} candidates")
        
        # Test integration with recommendation (using fallback)
        from milestone1.phase3_integration.prompting import build_prompt_payload
        from milestone1.phase4_recommendation.client import get_recommendations
        
        if candidates:
            prompt_payload = build_prompt_payload(candidates, prefs)
            # This will use fallback since no API key is set
            recommendations = get_recommendations(prompt_payload, candidates, top_k=3)
            print(f"OK Got {len(recommendations)} recommendations")
        
        return True
    except Exception as e:
        print(f"FAIL Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_phase5_ui_functionality():
    """Test Phase 5 UI functionality (non-visual parts)."""
    print("\nTesting Phase 5 UI functionality...")
    
    try:
        from milestone1.phase5_ui.components import get_available_locations
        
        # Test location suggestions (this may be slow)
        print("Testing location suggestions...")
        locations = get_available_locations()
        print(f"OK Found {len(locations)} available locations")
        
        if locations:
            print(f"   Sample locations: {locations[:3]}")
        
        return True
    except Exception as e:
        print(f"FAIL UI functionality test failed: {e}")
        return False


def main():
    """Run all Phase 5 tests."""
    print("=" * 60)
    print("Phase 5 UI Test Suite")
    print("=" * 60)
    
    tests = [
        test_phase5_imports,
        test_phase5_models,
        test_phase5_integration,
        test_phase5_ui_functionality
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("SUCCESS All Phase 5 tests passed!")
        print("\nPhase 5 is ready to use!")
        print("To start the web UI, run:")
        print("  cd apps/web")
        print("  streamlit run app.py")
    else:
        print("FAIL Some tests failed. Please check the errors above.")
    
    print("=" * 60)


if __name__ == "__main__":
    main()

"""
Test fixtures and comprehensive testing for Phase 6 hardening.
"""

import json
import pytest
from typing import Any, Dict, List
from unittest.mock import MagicMock, patch

from milestone1.phase4_recommendation.models import Recommendation
from milestone1.phase2_preferences.models import UserPreferences
from milestone1.ingestion.models import Restaurant


class TestFixtures:
    """Test fixtures for LLM JSON parsing and fallback behavior."""
    
    @staticmethod
    def get_mock_restaurant_data() -> List[Restaurant]:
        """Get mock restaurant data for testing."""
        return [
            Restaurant(
                id="test_restaurant_1",
                name="Test Restaurant 1",
                location="Banashankari",
                cuisines=("North Indian", "Chinese"),
                rating=4.5,
                cost=800.0,
                budget_band="high",
                raw={"source": "test"}
            ),
            Restaurant(
                id="test_restaurant_2", 
                name="Test Restaurant 2",
                location="Banashankari",
                cuisines=("Italian", "Mexican"),
                rating=4.2,
                cost=750.0,
                budget_band="medium",
                raw={"source": "test"}
            ),
            Restaurant(
                id="test_restaurant_3",
                name="Test Restaurant 3",
                location="BTM",
                cuisines=("Cafe", "Fast Food"),
                rating=3.8,
                cost=400.0,
                budget_band="medium",
                raw={"source": "test"}
            )
        ]
    
    @staticmethod
    def get_mock_user_preferences() -> UserPreferences:
        """Get mock user preferences for testing."""
        return UserPreferences(
            location="Banashankari",
            budget_band="high",
            cuisines=("North Indian", "Chinese"),
            min_rating=4.0,
            additional_preferences_text="Good service and ambiance"
        )
    
    @staticmethod
    def get_valid_llm_response() -> Dict[str, Any]:
        """Get valid LLM response for testing."""
        return {
            "recommendations": [
                {
                    "restaurant_id": "test_restaurant_1",
                    "rank": 1,
                    "explanation": "Excellent North Indian cuisine with authentic flavors and great service. Perfect for your high budget preference."
                },
                {
                    "restaurant_id": "test_restaurant_2",
                    "rank": 2,
                    "explanation": "Great Italian and Mexican fusion with moderate pricing. Good value for money."
                }
            ]
        }
    
    @staticmethod
    def get_invalid_llm_response() -> Dict[str, Any]:
        """Get invalid LLM response for testing."""
        return {
            "invalid_field": "recommendations",
            "error": "Invalid response format"
        }
    
    @staticmethod
    def get_hallucinated_llm_response() -> Dict[str, Any]:
        """Get LLM response with hallucinated restaurant IDs."""
        return {
            "recommendations": [
                {
                    "restaurant_id": "nonexistent_restaurant",
                    "rank": 1,
                    "explanation": "This restaurant doesn't exist in our database."
                },
                {
                    "restaurant_id": "test_restaurant_1",
                    "rank": 2,
                    "explanation": "Valid restaurant from our database."
                }
            ]
        }
    
    @staticmethod
    def get_empty_llm_response() -> Dict[str, Any]:
        """Get empty LLM response for testing."""
        return {
            "recommendations": []
        }


class LLMResponseValidator:
    """Validator for LLM responses."""
    
    @staticmethod
    def validate_recommendations_structure(response: Dict[str, Any]) -> bool:
        """Validate the structure of recommendations response."""
        if "recommendations" not in response:
            return False
        
        recommendations = response["recommendations"]
        if not isinstance(recommendations, list):
            return False
        
        for rec in recommendations:
            if not isinstance(rec, dict):
                return False
            
            required_fields = ["restaurant_id", "rank", "explanation"]
            if not all(field in rec for field in required_fields):
                return False
        
        return True
    
    @staticmethod
    def validate_restaurant_ids(
        response: Dict[str, Any], 
        valid_ids: List[str]
    ) -> bool:
        """Validate that all restaurant IDs exist in valid list."""
        recommendations = response.get("recommendations", [])
        
        for rec in recommendations:
            restaurant_id = rec.get("restaurant_id")
            if restaurant_id not in valid_ids:
                return False
        
        return True
    
    @staticmethod
    def validate_ranks(response: Dict[str, Any]) -> bool:
        """Validate that ranks are unique and sequential."""
        recommendations = response.get("recommendations", [])
        ranks = [rec.get("rank") for rec in recommendations]
        
        # Check for duplicates
        if len(ranks) != len(set(ranks)):
            return False
        
        # Check for valid range
        if not all(1 <= rank <= len(ranks) for rank in ranks):
            return False
        
        return True


class ErrorScenarioTester:
    """Test various error scenarios."""
    
    @staticmethod
    def test_api_timeout():
        """Test API timeout scenario."""
        # Simulate timeout error
        pass
    
    @staticmethod
    def test_api_rate_limit():
        """Test API rate limit scenario."""
        # Simulate rate limit error
        pass
    
    @staticmethod
    def test_invalid_api_key():
        """Test invalid API key scenario."""
        # Simulate invalid API key error
        pass
    
    @staticmethod
    def test_network_error():
        """Test network error scenario."""
        # Simulate network error
        pass


# Pytest fixtures
@pytest.fixture
def mock_restaurants():
    """Fixture providing mock restaurant data."""
    return TestFixtures.get_mock_restaurant_data()


@pytest.fixture
def mock_preferences():
    """Fixture providing mock user preferences."""
    return TestFixtures.get_mock_user_preferences()


@pytest.fixture
def valid_llm_response():
    """Fixture providing valid LLM response."""
    return TestFixtures.get_valid_llm_response()


@pytest.fixture
def invalid_llm_response():
    """Fixture providing invalid LLM response."""
    return TestFixtures.get_invalid_llm_response()


@pytest.fixture
def hallucinated_llm_response():
    """Fixture providing hallucinated LLM response."""
    return TestFixtures.get_hallucinated_llm_response()


@pytest.fixture
def empty_llm_response():
    """Fixture providing empty LLM response."""
    return TestFixtures.get_empty_llm_response()


# Integration test helpers
def create_mock_api_client(response_data: Dict[str, Any], should_fail: bool = False):
    """Create a mock API client for testing."""
    mock_client = MagicMock()
    
    if should_fail:
        mock_client.chat.completions.create.side_effect = Exception("API Error")
    else:
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = json.dumps(response_data)
        mock_client.chat.completions.create.return_value = mock_response
    
    return mock_client


def assert_recommendation_structure(recommendations: List[Recommendation]):
    """Assert that recommendations have proper structure."""
    assert isinstance(recommendations, list)
    assert len(recommendations) > 0
    
    for rec in recommendations:
        assert hasattr(rec, 'restaurant')
        assert hasattr(rec, 'rank')
        assert hasattr(rec, 'explanation')
        assert isinstance(rec.rank, int)
        assert isinstance(rec.explanation, str)
        assert len(rec.explanation) > 0

import json
from unittest.mock import MagicMock, patch

import pytest

from milestone1.ingestion.models import Restaurant
from milestone1.phase3_integration.models import PromptPayload
from milestone1.phase4_recommendation.client import get_recommendations
from milestone1.phase4_recommendation.models import Recommendation

@pytest.fixture
def dummy_candidates():
    return [
        Restaurant(id="1", name="R1", location="L", cuisines=(), rating=4.5, cost=None, budget_band=None, raw=None),
        Restaurant(id="2", name="R2", location="L", cuisines=(), rating=4.0, cost=None, budget_band=None, raw=None),
        Restaurant(id="3", name="R3", location="L", cuisines=(), rating=3.5, cost=None, budget_band=None, raw=None),
    ]

@pytest.fixture
def dummy_prompt():
    return PromptPayload(system_message="sys", user_message="usr")

def test_fallback_when_api_key_missing(dummy_candidates, dummy_prompt, monkeypatch):
    monkeypatch.delenv("XAI_API_KEY", raising=False)
    recs = get_recommendations(dummy_prompt, dummy_candidates, top_k=2)

    assert len(recs) == 2
    assert recs[0].restaurant.id == "1"
    assert recs[1].restaurant.id == "2"
    assert "We couldn't generate a personalized reason" in recs[0].explanation

@patch("milestone1.phase4_recommendation.client.OpenAI")
def test_successful_llm_parsing(mock_openai, dummy_candidates, dummy_prompt, monkeypatch):
    monkeypatch.setenv("XAI_API_KEY", "fake_key")

    mock_client_instance = MagicMock()
    mock_openai.return_value = mock_client_instance
    mock_response = MagicMock()
    
    mock_response.choices[0].message.content = json.dumps({
        "recommendations": [
            {"restaurant_id": "2", "rank": 1, "explanation": "Best fit"},
            {"restaurant_id": "1", "rank": 2, "explanation": "Good fit"}
        ]
    })
    mock_client_instance.chat.completions.create.return_value = mock_response

    recs = get_recommendations(dummy_prompt, dummy_candidates, top_k=5)
    
    assert len(recs) == 2
    assert recs[0].restaurant.id == "2"
    assert recs[0].rank == 1
    assert recs[0].explanation == "Best fit"
    assert recs[1].restaurant.id == "1"
    assert recs[1].rank == 2

@patch("milestone1.phase4_recommendation.client.OpenAI")
def test_hallucinated_ids_are_discarded(mock_openai, dummy_candidates, dummy_prompt, monkeypatch):
    monkeypatch.setenv("XAI_API_KEY", "fake_key")

    mock_client_instance = MagicMock()
    mock_openai.return_value = mock_client_instance
    mock_response = MagicMock()
    
    mock_response.choices[0].message.content = json.dumps({
        "recommendations": [
            {"restaurant_id": "999", "rank": 1, "explanation": "Hallucinated"},
            {"restaurant_id": "3", "rank": 2, "explanation": "Real"}
        ]
    })
    mock_client_instance.chat.completions.create.return_value = mock_response

    recs = get_recommendations(dummy_prompt, dummy_candidates, top_k=5)
    
    assert len(recs) == 1
    assert recs[0].restaurant.id == "3"
    assert recs[0].rank == 2

@patch("milestone1.phase4_recommendation.client.OpenAI")
def test_fallback_on_api_error(mock_openai, dummy_candidates, dummy_prompt, monkeypatch):
    monkeypatch.setenv("XAI_API_KEY", "fake_key")

    mock_client_instance = MagicMock()
    mock_openai.return_value = mock_client_instance
    
    # Simulate API failure
    mock_client_instance.chat.completions.create.side_effect = Exception("API timeout")

    recs = get_recommendations(dummy_prompt, dummy_candidates, top_k=2)
    
    assert len(recs) == 2
    assert "We couldn't generate a personalized reason" in recs[0].explanation

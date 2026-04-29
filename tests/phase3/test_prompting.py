import json
from milestone1.ingestion.models import Restaurant
from milestone1.preferences.models import UserPreferences
from milestone1.phase3_integration.prompting import build_prompt_payload

def test_build_prompt_payload():
    prefs = UserPreferences(
        location="Delhi",
        budget_band="medium",
        cuisines=("Italian",),
        min_rating=4.0,
        additional_preferences_text="Must have good pasta"
    )

    candidates = [
        Restaurant(
            id="1",
            name="Pasta Place",
            location="Delhi",
            cuisines=("Italian",),
            rating=4.5,
            cost=500.0,
            budget_band="medium",
            raw=None
        )
    ]

    payload = build_prompt_payload(candidates, prefs)

    # Check system message properties
    assert "JSON Output Schema" in payload.system_message
    assert "recommendations" in payload.system_message

    # Check user message properties
    assert "Delhi" in payload.user_message
    assert "Must have good pasta" in payload.user_message
    assert "Pasta Place" in payload.user_message
    assert '"id": "1"' in payload.user_message

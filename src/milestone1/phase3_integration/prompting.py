import json
from milestone1.ingestion.models import Restaurant
from milestone1.preferences.models import UserPreferences
from milestone1.phase3_integration.models import PromptPayload

SYSTEM_PROMPT_TEMPLATE = """You are an expert AI restaurant recommender system inspired by Zomato.
You MUST follow these strict rules:
1. ONLY recommend restaurants that are provided in the candidate list. DO NOT hallucinate or invent any restaurants.
2. Rank the candidates based on how well they match the user's preferences, especially considering any 'additional_preferences_text'.
3. You must output your response in valid JSON format matching the schema below.

JSON Output Schema:
{
  "recommendations": [
    {
      "restaurant_id": "string (MUST perfectly match the ID from the candidate list)",
      "rank": "integer (1 for best match, 2 for second best, etc.)",
      "explanation": "string (A short, persuasive explanation of why this restaurant is a good fit based on the user's preferences)"
    }
  ]
}
"""

def build_prompt_payload(candidates: list[Restaurant], prefs: UserPreferences) -> PromptPayload:
    """
    Constructs the prompt payload containing system instructions and user message.
    """
    # Build preferences string
    prefs_dict = {
        "location": prefs.location,
        "budget_band": prefs.budget_band,
        "cuisines": prefs.cuisines,
        "min_rating": prefs.min_rating,
        "additional_preferences_text": prefs.additional_preferences_text
    }
    prefs_str = json.dumps({k: v for k, v in prefs_dict.items() if v is not None}, indent=2)

    # Build candidates table/JSON
    candidates_data = []
    for c in candidates:
        candidates_data.append({
            "id": c.id,
            "name": c.name,
            "cuisines": c.cuisines,
            "rating": c.rating,
            "budget_band": c.budget_band,
            "cost": c.cost
        })
    candidates_str = json.dumps(candidates_data, indent=2)

    user_message = f"""Here are the user's preferences:
{prefs_str}

Here is the candidate list of restaurants you can choose from:
{candidates_str}

Please rank the top candidates (up to 5) from the list above and provide your response in the requested JSON format.
"""

    return PromptPayload(
        system_message=SYSTEM_PROMPT_TEMPLATE,
        user_message=user_message
    )

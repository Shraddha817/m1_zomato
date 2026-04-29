import json
import logging
import os
from typing import Any

from openai import OpenAI

from milestone1.ingestion.models import Restaurant
from milestone1.phase3_integration.models import PromptPayload
from milestone1.phase4_recommendation.models import Recommendation

logger = logging.getLogger(__name__)

def _get_fallback_recommendations(candidates: list[Restaurant], top_k: int) -> list[Recommendation]:
    """Fallback logic: returns the top_k deterministic matches with a templated explanation."""
    logger.warning("Falling back to deterministic recommendations.")
    recs = []
    for idx, c in enumerate(candidates[:top_k], start=1):
        recs.append(
            Recommendation(
                restaurant=c,
                rank=idx,
                explanation="We couldn't generate a personalized reason right now, but this is a top-rated match based on your filters."
            )
        )
    return recs

def get_recommendations(prompt_payload: PromptPayload, candidates: list[Restaurant], top_k: int = 5) -> list[Recommendation]:
    """
    Calls the LLM (xAI Grok) with the prompt payload to rank and explain candidates.
    Falls back to deterministic results on failure.
    """
    if not candidates:
        return []

    api_key = os.environ.get("XAI_API_KEY")
    if not api_key:
        logger.error("XAI_API_KEY not found in environment. Using fallback.")
        return _get_fallback_recommendations(candidates, top_k)

    client = OpenAI(
        api_key=api_key,
        base_url=os.environ.get("XAI_BASE_URL", "https://api.x.ai/v1"),
    )

    model = os.environ.get("XAI_MODEL", "grok-beta")
    timeout = float(os.environ.get("XAI_TIMEOUT_SECONDS", "30.0"))
    max_tokens = int(os.environ.get("XAI_MAX_TOKENS", "600"))
    temperature = float(os.environ.get("XAI_TEMPERATURE", "0.3"))

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt_payload.system_message},
                {"role": "user", "content": prompt_payload.user_message}
            ],
            response_format={"type": "json_object"},
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout
        )

        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty response content from LLM")

        data: dict[str, Any] = json.loads(content)
        recommendations_data = data.get("recommendations", [])

        if not isinstance(recommendations_data, list):
            raise ValueError("JSON response missing 'recommendations' list")

        # Map IDs to actual Restaurant objects
        candidates_by_id = {c.id: c for c in candidates}
        final_recs = []

        for rec in recommendations_data:
            rec_id = rec.get("restaurant_id")
            if rec_id in candidates_by_id:
                final_recs.append(
                    Recommendation(
                        restaurant=candidates_by_id[rec_id],
                        rank=int(rec.get("rank", 999)),
                        explanation=str(rec.get("explanation", ""))
                    )
                )
            else:
                logger.warning(f"LLM hallucinated candidate ID: {rec_id}")

        if not final_recs:
            raise ValueError("No valid recommendations parsed from LLM")

        # Sort by rank
        final_recs.sort(key=lambda x: x.rank)
        return final_recs[:top_k]

    except Exception as e:
        logger.exception(f"LLM recommendation failed: {e}")
        return _get_fallback_recommendations(candidates, top_k)

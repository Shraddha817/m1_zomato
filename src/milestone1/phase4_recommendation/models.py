from __future__ import annotations

from dataclasses import dataclass

from milestone1.ingestion.models import Restaurant


@dataclass(frozen=True, slots=True)
class Recommendation:
    """
    A single recommended restaurant along with its LLM-generated rank and explanation.
    """
    restaurant: Restaurant
    rank: int
    explanation: str

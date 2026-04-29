from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Restaurant:
    """
    Canonical restaurant record used across later phases.

    Note: `id` must be stable across runs for grounding and parsing.
    """

    id: str
    name: str
    location: str
    cuisines: tuple[str, ...]
    rating: float | None
    cost: float | None
    budget_band: str | None  # "low" | "medium" | "high" | None
    raw: dict | None = None


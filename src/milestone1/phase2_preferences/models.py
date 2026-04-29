from __future__ import annotations

from dataclasses import dataclass


BudgetBand = str  # "low" | "medium" | "high"


@dataclass(frozen=True, slots=True)
class UserPreferences:
    location: str
    budget_band: BudgetBand | None
    cuisines: tuple[str, ...]
    min_rating: float | None
    additional_preferences_text: str | None


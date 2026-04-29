"""
Backward-compatible Phase 2 imports.

Canonical implementation now lives under `milestone1.phase2_preferences`.
"""

from milestone1.phase2_preferences import (  # noqa: F401
    ALLOWED_BUDGET_BANDS,
    ValidationError,
    UserPreferences,
    allowed_locations_from_restaurants,
    preferences_from_mapping,
)

__all__ = [
    "ALLOWED_BUDGET_BANDS",
    "ValidationError",
    "UserPreferences",
    "allowed_locations_from_restaurants",
    "preferences_from_mapping",
]


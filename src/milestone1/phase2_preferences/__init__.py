"""Phase 2: user preferences and validation."""

from .allowed_locations import allowed_locations_from_restaurants
from .models import UserPreferences
from .validation import ALLOWED_BUDGET_BANDS, ValidationError, preferences_from_mapping

__all__ = [
    "ALLOWED_BUDGET_BANDS",
    "ValidationError",
    "UserPreferences",
    "allowed_locations_from_restaurants",
    "preferences_from_mapping",
]


from __future__ import annotations

from milestone1.ingestion.models import Restaurant
from milestone1.preferences.models import UserPreferences

def filter_candidates(restaurants: list[Restaurant], prefs: UserPreferences, limit: int = 50) -> list[Restaurant]:
    """
    Filters a list of restaurants based on user preferences deterministically.
    """
    candidates = []

    for r in restaurants:
        # Filter by location (case-insensitive exact or substring match depending on dataset)
        # We assume strict exact match for location here but case-insensitive
        if not r.location or prefs.location.lower() != r.location.lower():
            continue

        # Filter by min_rating if provided
        if prefs.min_rating is not None:
            if r.rating is None or r.rating < prefs.min_rating:
                continue

        # Filter by budget_band if provided
        if prefs.budget_band is not None:
            if r.budget_band != prefs.budget_band:
                continue

        # Filter by cuisines overlap if provided
        if prefs.cuisines:
            # check if there's any intersection between requested cuisines and restaurant cuisines
            # case-insensitive check
            req_cuisines = {c.lower() for c in prefs.cuisines}
            rest_cuisines = {c.lower() for c in r.cuisines} if r.cuisines else set()
            if not req_cuisines.intersection(rest_cuisines):
                continue

        candidates.append(r)

    # Pre-rank candidates: Sort by rating descending (None ratings go to bottom)
    candidates.sort(key=lambda x: x.rating if x.rating is not None else -1.0, reverse=True)

    # Cap the result at `limit`
    return candidates[:limit]

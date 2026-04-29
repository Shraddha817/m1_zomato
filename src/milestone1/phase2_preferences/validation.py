from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Any, Iterable

from .models import BudgetBand, UserPreferences


_MULTI_SPACE_RE = re.compile(r"\s+")

ALLOWED_BUDGET_BANDS: tuple[str, ...] = ("low", "medium", "high")


@dataclass(frozen=True, slots=True)
class ValidationError:
    field: str
    message: str


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    s = str(value).strip()
    s = _MULTI_SPACE_RE.sub(" ", s)
    return s


def normalize_location(value: Any) -> str:
    return _normalize_text(value)


def normalize_budget_band(value: Any) -> BudgetBand | None:
    s = _normalize_text(value).lower()
    if not s:
        return None
    if s in ALLOWED_BUDGET_BANDS:
        return s
    return None


def normalize_cuisines(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()

    tokens: list[str] = []
    if isinstance(value, (list, tuple, set)):
        for item in value:
            t = _normalize_text(item)
            if t:
                tokens.append(t)
    else:
        s = _normalize_text(value)
        if not s:
            return ()
        parts = re.split(r"[,/]", s)
        for p in parts:
            t = _normalize_text(p)
            if t:
                tokens.append(t)

    seen: set[str] = set()
    out: list[str] = []
    for t in tokens:
        key = t.casefold()
        if key in seen:
            continue
        seen.add(key)
        out.append(t)

    return tuple(out)


def parse_min_rating(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        f = float(value)
    else:
        s = _normalize_text(value)
        if not s:
            return None
        s = s.replace(",", ".")
        try:
            f = float(s)
        except ValueError:
            return None

    if not math.isfinite(f) or f < 0.0 or f > 5.0:
        return None
    return f


def normalize_additional_text(value: Any, *, max_len: int = 500) -> str | None:
    s = _normalize_text(value)
    if not s:
        return None
    if len(s) > max_len:
        s = s[:max_len].rstrip()
    return s


def preferences_from_mapping(
    mapping: dict[str, Any],
    *,
    allowed_locations: Iterable[str] | None = None,
) -> tuple[UserPreferences | None, list[ValidationError]]:
    errors: list[ValidationError] = []

    location = normalize_location(mapping.get("location"))
    if not location:
        errors.append(ValidationError("location", "Location is required."))

    budget_raw = mapping.get("budget_band")
    budget_band = normalize_budget_band(budget_raw)
    if budget_raw is not None and _normalize_text(budget_raw):
        if budget_band is None:
            errors.append(
                ValidationError(
                    "budget_band",
                    f"Budget must be one of: {', '.join(ALLOWED_BUDGET_BANDS)}.",
                )
            )

    cuisines = normalize_cuisines(mapping.get("cuisines"))

    min_rating_raw = mapping.get("min_rating")
    min_rating = parse_min_rating(min_rating_raw)
    if min_rating_raw is not None and _normalize_text(min_rating_raw):
        if min_rating is None:
            errors.append(ValidationError("min_rating", "Minimum rating must be a number between 0 and 5."))

    additional = normalize_additional_text(mapping.get("additional_preferences_text"))

    if allowed_locations is not None and location:
        allowed_set = {str(x).casefold() for x in allowed_locations}
        if location.casefold() not in allowed_set:
            errors.append(ValidationError("location", "Location is not available in the dataset."))

    if errors:
        return None, errors

    return (
        UserPreferences(
            location=location,
            budget_band=budget_band,
            cuisines=cuisines,
            min_rating=min_rating,
            additional_preferences_text=additional,
        ),
        [],
    )


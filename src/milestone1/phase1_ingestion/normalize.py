from __future__ import annotations

import hashlib
import math
import re
from typing import Any, Iterable


_MULTI_SPACE_RE = re.compile(r"\s+")
_RATING_FLOAT_RE = re.compile(r"(?P<num>\d+(\.\d+)?)")


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    s = str(value).strip()
    s = _MULTI_SPACE_RE.sub(" ", s)
    return s


def normalize_location(value: Any) -> str:
    # Placeholder: later can add alias map (Bangalore ↔ Bengaluru, etc.)
    return normalize_text(value)


def normalize_cuisines(value: Any) -> tuple[str, ...]:
    """
    Normalize cuisines into a tuple of strings.

    Supports:
    - comma-separated string
    - slash-separated string
    - list/tuple of strings
    """
    if value is None:
        return ()

    tokens: list[str] = []
    if isinstance(value, (list, tuple, set)):
        for item in value:
            t = normalize_text(item)
            if t:
                tokens.append(t)
    else:
        s = normalize_text(value)
        if not s:
            return ()
        # Split on commas and slashes; keep it simple and predictable.
        parts = re.split(r"[,/]", s)
        for p in parts:
            t = normalize_text(p)
            if t:
                tokens.append(t)

    # Drop obvious placeholders
    filtered = []
    for t in tokens:
        lower = t.lower()
        if lower in {"na", "n/a", "not available", "none", "null"}:
            continue
        filtered.append(t)

    # Stable, de-duplicated, case-insensitive uniqueness while preserving display form.
    seen: set[str] = set()
    out: list[str] = []
    for t in filtered:
        key = t.casefold()
        if key in seen:
            continue
        seen.add(key)
        out.append(t)

    return tuple(out)


def parse_rating(value: Any) -> float | None:
    if value is None:
        return None

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        f = float(value)
        if math.isfinite(f) and 0.0 <= f <= 5.0:
            return f
        return None

    s = normalize_text(value)
    if not s:
        return None
    if s.upper() in {"NEW", "—", "-", "NA", "N/A"}:
        return None

    m = _RATING_FLOAT_RE.search(s)
    if not m:
        return None

    try:
        f = float(m.group("num"))
    except ValueError:
        return None

    if not math.isfinite(f) or f < 0.0 or f > 5.0:
        return None
    return f


def parse_cost(value: Any) -> float | None:
    if value is None:
        return None

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        f = float(value)
        if math.isfinite(f) and f >= 0:
            return f
        return None

    s = normalize_text(value)
    if not s:
        return None

    # Common patterns:
    # - "₹500 for two"
    # - "300-600"
    # We'll extract all integers and choose the first number as the canonical cost for v1.
    nums = re.findall(r"\d+", s)
    if not nums:
        return None
    try:
        f = float(nums[0])
    except ValueError:
        return None
    if not math.isfinite(f) or f < 0:
        return None
    return f


def derive_budget_band(
    cost: float | None,
    *,
    low_max: float = 300,
    medium_max: float = 700,
) -> str | None:
    if cost is None:
        return None
    if cost <= low_max:
        return "low"
    if cost <= medium_max:
        return "medium"
    return "high"


def stable_restaurant_id(*parts: str) -> str:
    """
    Deterministic ID derived from normalized text parts.

    Keeps IDs stable across dataset row order changes.
    """
    normalized_parts = [normalize_text(p).casefold() for p in parts if normalize_text(p)]
    payload = "||".join(normalized_parts).encode("utf-8", errors="ignore")
    digest = hashlib.sha256(payload).hexdigest()[:16]
    return digest


def pick_first_present(row: dict[str, Any], keys: Iterable[str]) -> Any:
    for k in keys:
        if k in row and row[k] not in (None, ""):
            return row[k]
    return None


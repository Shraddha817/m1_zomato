from __future__ import annotations

from collections.abc import Iterable

from milestone1.phase1_ingestion.models import Restaurant


def allowed_locations_from_restaurants(restaurants: Iterable[Restaurant]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for r in restaurants:
        loc = r.location.strip()
        if not loc:
            continue
        key = loc.casefold()
        if key in seen:
            continue
        seen.add(key)
        out.append(loc)

    out.sort(key=lambda s: s.casefold())
    return out


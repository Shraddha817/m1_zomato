from __future__ import annotations

from dataclasses import asdict
from typing import Any, Iterable

from .config import IngestionConfig, ingestion_config_from_env
from .hf_loader import load_hf_dataset
from .models import Restaurant
from .normalize import (
    derive_budget_band,
    normalize_cuisines,
    normalize_location,
    normalize_text,
    parse_cost,
    parse_rating,
    pick_first_present,
    stable_restaurant_id,
)


_NAME_KEYS: tuple[str, ...] = (
    "name",
    "restaurant_name",
    "Restaurant Name",
    "Restaurant",
    "res_name",
)

_LOCATION_KEYS: tuple[str, ...] = (
    "location",
    "city",
    "City",
    "locality",
    "Locality",
    "area",
    "Area",
)

_CUISINE_KEYS: tuple[str, ...] = (
    "cuisines",
    "Cuisines",
    "cuisine",
    "Cuisine",
)

_RATING_KEYS: tuple[str, ...] = (
    "rating",
    "Rating",
    "aggregate_rating",
    "Aggregate rating",
)

_COST_KEYS: tuple[str, ...] = (
    "cost",
    "Cost",
    "average_cost_for_two",
    "Average Cost for two",
    "approx_cost(for two people)",
    "Approx Cost(for two people)",
    "price",
    "Price",
)


def _row_to_restaurant(row: dict[str, Any]) -> Restaurant | None:
    name_raw = pick_first_present(row, _NAME_KEYS)
    location_raw = pick_first_present(row, _LOCATION_KEYS)

    name = normalize_text(name_raw)
    location = normalize_location(location_raw)

    if not name or not location:
        return None

    cuisines_raw = pick_first_present(row, _CUISINE_KEYS)
    cuisines = normalize_cuisines(cuisines_raw)

    rating_raw = pick_first_present(row, _RATING_KEYS)
    rating = parse_rating(rating_raw)

    cost_raw = pick_first_present(row, _COST_KEYS)
    cost = parse_cost(cost_raw)

    budget_band = derive_budget_band(cost)

    rid = stable_restaurant_id(name, location)

    raw = {
        "name": name_raw,
        "location": location_raw,
        "cuisines": cuisines_raw,
        "rating": rating_raw,
        "cost": cost_raw,
    }

    return Restaurant(
        id=rid,
        name=name,
        location=location,
        cuisines=cuisines,
        rating=rating,
        cost=cost,
        budget_band=budget_band,
        raw=raw,
    )


def iter_restaurants(
    *,
    cfg: IngestionConfig | None = None,
    limit: int | None = None,
) -> Iterable[Restaurant]:
    cfg = cfg or ingestion_config_from_env()
    loaded = load_hf_dataset(cfg)

    seen_ids: set[str] = set()
    yielded = 0
    for row in loaded.dataset:
        r = _row_to_restaurant(row)
        if r is None:
            continue
        if r.id in seen_ids:
            continue
        seen_ids.add(r.id)
        yield r
        yielded += 1
        if limit is not None and yielded >= limit:
            break


def load_restaurants(
    *,
    cfg: IngestionConfig | None = None,
    limit: int | None = None,
) -> list[Restaurant]:
    return list(iter_restaurants(cfg=cfg, limit=limit))


def restaurant_to_dict(r: Restaurant) -> dict[str, Any]:
    return asdict(r)


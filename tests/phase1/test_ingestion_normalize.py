from milestone1.ingestion.normalize import (
    derive_budget_band,
    normalize_cuisines,
    parse_cost,
    parse_rating,
    stable_restaurant_id,
)


def test_parse_rating_handles_common_strings() -> None:
    assert parse_rating("4.2/5") == 4.2
    assert parse_rating("NEW") is None
    assert parse_rating("—") is None
    assert parse_rating("") is None
    assert parse_rating(4.5) == 4.5
    assert parse_rating(6) is None


def test_parse_cost_extracts_digits() -> None:
    assert parse_cost("₹500 for two") == 500.0
    assert parse_cost("300-600") == 300.0
    assert parse_cost("") is None
    assert parse_cost(-1) is None


def test_normalize_cuisines_splits_and_dedupes() -> None:
    assert normalize_cuisines("North Indian, Chinese") == ("North Indian", "Chinese")
    assert normalize_cuisines(["Italian", "italian", ""]) == ("Italian",)


def test_budget_band_derivation() -> None:
    assert derive_budget_band(200) == "low"
    assert derive_budget_band(300) == "low"
    assert derive_budget_band(301) == "medium"
    assert derive_budget_band(700) == "medium"
    assert derive_budget_band(701) == "high"
    assert derive_budget_band(None) is None


def test_stable_id_is_deterministic() -> None:
    assert stable_restaurant_id("A", "B") == stable_restaurant_id("A", "B")
    assert stable_restaurant_id("A", "B") != stable_restaurant_id("A", "C")


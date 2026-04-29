from milestone1.preferences import ALLOWED_BUDGET_BANDS, preferences_from_mapping


def test_location_is_required() -> None:
    prefs, errors = preferences_from_mapping({})
    assert prefs is None
    assert any(e.field == "location" for e in errors)


def test_budget_band_validation() -> None:
    prefs, errors = preferences_from_mapping({"location": "Delhi", "budget_band": "cheap"})
    assert prefs is None
    assert any(e.field == "budget_band" for e in errors)

    prefs2, errors2 = preferences_from_mapping({"location": "Delhi", "budget_band": ALLOWED_BUDGET_BANDS[0]})
    assert errors2 == []
    assert prefs2 is not None


def test_min_rating_validation() -> None:
    prefs, errors = preferences_from_mapping({"location": "Delhi", "min_rating": "six"})
    assert prefs is None
    assert any(e.field == "min_rating" for e in errors)

    prefs2, errors2 = preferences_from_mapping({"location": "Delhi", "min_rating": "4.5"})
    assert errors2 == []
    assert prefs2 is not None
    assert prefs2.min_rating == 4.5


def test_cuisines_normalization() -> None:
    prefs, errors = preferences_from_mapping({"location": "Delhi", "cuisines": "Italian, italian / Chinese"})
    assert errors == []
    assert prefs is not None
    assert prefs.cuisines == ("Italian", "Chinese")


def test_allowed_locations_check() -> None:
    prefs, errors = preferences_from_mapping({"location": "Nowhere"}, allowed_locations=["Delhi", "Bangalore"])
    assert prefs is None
    assert any(e.field == "location" for e in errors)


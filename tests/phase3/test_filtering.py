from milestone1.ingestion.models import Restaurant
from milestone1.preferences.models import UserPreferences
from milestone1.phase3_integration.filtering import filter_candidates

def create_restaurant(id, name, loc, rating=None, budget=None, cuisines=()) -> Restaurant:
    return Restaurant(
        id=id,
        name=name,
        location=loc,
        cuisines=cuisines,
        rating=rating,
        cost=None,
        budget_band=budget,
    )

def test_filter_by_location():
    r1 = create_restaurant("1", "A", "Delhi")
    r2 = create_restaurant("2", "B", "Bangalore")
    prefs = UserPreferences(location="delhi", budget_band=None, cuisines=(), min_rating=None, additional_preferences_text=None)

    candidates = filter_candidates([r1, r2], prefs)
    assert len(candidates) == 1
    assert candidates[0].id == "1"

def test_filter_by_budget():
    r1 = create_restaurant("1", "A", "Delhi", budget="low")
    r2 = create_restaurant("2", "B", "Delhi", budget="medium")
    prefs = UserPreferences(location="Delhi", budget_band="low", cuisines=(), min_rating=None, additional_preferences_text=None)

    candidates = filter_candidates([r1, r2], prefs)
    assert len(candidates) == 1
    assert candidates[0].id == "1"

def test_filter_by_min_rating():
    r1 = create_restaurant("1", "A", "Delhi", rating=4.5)
    r2 = create_restaurant("2", "B", "Delhi", rating=3.5)
    r3 = create_restaurant("3", "C", "Delhi", rating=None)
    prefs = UserPreferences(location="Delhi", budget_band=None, cuisines=(), min_rating=4.0, additional_preferences_text=None)

    candidates = filter_candidates([r1, r2, r3], prefs)
    assert len(candidates) == 1
    assert candidates[0].id == "1"

def test_filter_by_cuisines():
    r1 = create_restaurant("1", "A", "Delhi", cuisines=("Italian", "Mexican"))
    r2 = create_restaurant("2", "B", "Delhi", cuisines=("Chinese",))
    prefs = UserPreferences(location="Delhi", budget_band=None, cuisines=("italian",), min_rating=None, additional_preferences_text=None)

    candidates = filter_candidates([r1, r2], prefs)
    assert len(candidates) == 1
    assert candidates[0].id == "1"

def test_sorting_by_rating():
    r1 = create_restaurant("1", "A", "Delhi", rating=3.0)
    r2 = create_restaurant("2", "B", "Delhi", rating=4.5)
    r3 = create_restaurant("3", "C", "Delhi", rating=None)
    prefs = UserPreferences(location="Delhi", budget_band=None, cuisines=(), min_rating=None, additional_preferences_text=None)

    candidates = filter_candidates([r1, r2, r3], prefs)
    assert len(candidates) == 3
    assert candidates[0].id == "2" # 4.5
    assert candidates[1].id == "1" # 3.0
    assert candidates[2].id == "3" # None

def test_capping_limit():
    restaurants = [create_restaurant(str(i), f"R{i}", "Delhi") for i in range(10)]
    prefs = UserPreferences(location="Delhi", budget_band=None, cuisines=(), min_rating=None, additional_preferences_text=None)

    candidates = filter_candidates(restaurants, prefs, limit=3)
    assert len(candidates) == 3

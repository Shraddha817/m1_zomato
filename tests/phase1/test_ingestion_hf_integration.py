import os

import pytest

from milestone1.ingestion import load_restaurants


@pytest.mark.integration
def test_loads_from_huggingface_when_enabled() -> None:
    if os.getenv("RUN_HF_INTEGRATION") != "1":
        pytest.skip("RUN_HF_INTEGRATION is not set to 1")

    restaurants = load_restaurants(limit=5)
    assert len(restaurants) > 0
    assert all(r.name and r.location for r in restaurants)


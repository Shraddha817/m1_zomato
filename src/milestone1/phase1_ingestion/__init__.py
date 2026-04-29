"""Phase 1: dataset ingestion and normalization."""

from .ingest import iter_restaurants, load_restaurants
from .models import Restaurant

__all__ = ["Restaurant", "iter_restaurants", "load_restaurants"]


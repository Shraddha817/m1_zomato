"""
Backward-compatible Phase 1 imports.

Canonical implementation now lives under `milestone1.phase1_ingestion`.
"""

from milestone1.phase1_ingestion import Restaurant, iter_restaurants, load_restaurants

__all__ = ["Restaurant", "iter_restaurants", "load_restaurants"]


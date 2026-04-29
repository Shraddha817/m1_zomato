from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class IngestionConfig:
    dataset_name: str
    dataset_revision: str | None
    cache_dir: Path | None


def ingestion_config_from_env() -> IngestionConfig:
    dataset_name = os.getenv(
        "HF_DATASET_NAME",
        "ManikaSaini/zomato-restaurant-recommendation",
    ).strip()

    dataset_revision = os.getenv("HF_DATASET_REVISION")
    if dataset_revision is not None:
        dataset_revision = dataset_revision.strip() or None

    cache_dir_raw = os.getenv("HF_DATASET_CACHE_DIR")
    cache_dir: Path | None = None
    if cache_dir_raw and cache_dir_raw.strip():
        cache_dir = Path(cache_dir_raw.strip())

    return IngestionConfig(
        dataset_name=dataset_name,
        dataset_revision=dataset_revision,
        cache_dir=cache_dir,
    )


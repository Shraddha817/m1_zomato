from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from datasets import Dataset, DatasetDict, IterableDataset, load_dataset

from .config import IngestionConfig


@dataclass(frozen=True)
class LoadedDataset:
    dataset_name: str
    split: str
    columns: tuple[str, ...]
    dataset: Dataset | IterableDataset


def _choose_split(ds: DatasetDict, preferred: Iterable[str] = ("train", "test", "validation")) -> str:
    for s in preferred:
        if s in ds:
            return s
    return next(iter(ds.keys()))


def load_hf_dataset(cfg: IngestionConfig) -> LoadedDataset:
    """
    Load dataset from Hugging Face.

    Returns a Dataset (or IterableDataset) plus metadata. Split selection:
    - Prefer "train", otherwise first available split.
    """
    ds_any: Any = load_dataset(
        cfg.dataset_name,
        revision=cfg.dataset_revision,
        cache_dir=str(cfg.cache_dir) if cfg.cache_dir else None,
    )

    if isinstance(ds_any, DatasetDict):
        split = _choose_split(ds_any)
        ds = ds_any[split]
    else:
        split = "train"
        ds = ds_any

    cols = tuple(getattr(ds, "column_names", []) or [])
    return LoadedDataset(dataset_name=cfg.dataset_name, split=split, columns=cols, dataset=ds)


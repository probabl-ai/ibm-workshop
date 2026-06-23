"""Data loading and X-marker wiring.

Owns: how raw data is materialized into ``(X, y)``, and how structural
metadata (groups, time ordering, ...) is attached at the X marker via
``split_kwargs``.

Workshop binding contract (see ``AGENTS.md``):

- ``data/public.csv`` — train / CV (``which="public"``)
- ``data/test/features.csv`` — test features only (``which="test"``)
- ``data/test/labels.csv`` — test labels (load for evaluation env-dicts only;
  never pass through ``load_table``)

Env-dict keys: ``data_dir``, ``which`` (``"public"`` | ``"test"``), ``y``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from ibm_workshop import PROJECT_ROOT

SAMPLE_ID_COL = "sample_id"
TARGET_COL = "target"
DATA_DIR = PROJECT_ROOT / "data"
PUBLIC_CSV = DATA_DIR / "public.csv"
TEST_FEATURES = DATA_DIR / "test" / "features.csv"
TEST_LABELS = DATA_DIR / "test" / "labels.csv"


def load_table(data_dir: str, which: str) -> pd.DataFrame:
    """Return a raw table for ``which`` in ``{"public", "test"}``.

    Parameters
    ----------
    data_dir
        Absolute path to the ``data/`` directory.
    which
        ``"public"`` loads ``public.csv``; ``"test"`` loads
        ``test/features.csv`` (no labels).
    """
    root = Path(data_dir)
    if which == "public":
        return pd.read_csv(root / "public.csv")
    if which == "test":
        return pd.read_csv(root / "test" / "features.csv")
    msg = f"which must be 'public' or 'test', got {which!r}"
    raise ValueError(msg)


def public_env(*, y: Any) -> dict[str, Any]:
    """Env-dict for fitting or public cross-validation."""
    return {"data_dir": str(DATA_DIR), "which": "public", "y": y}


def test_env(*, y: Any) -> dict[str, Any]:
    """Env-dict for test-set evaluation."""
    return {"data_dir": str(DATA_DIR), "which": "test", "y": y}


def load_test_targets() -> Any:
    """Return test labels aligned with ``test/features.csv`` row order."""
    features = pd.read_csv(TEST_FEATURES)
    labels = (
        pd.read_csv(TEST_LABELS)
        .set_index(SAMPLE_ID_COL)[TARGET_COL]
        .loc[features[SAMPLE_ID_COL]]
    )
    return labels.to_numpy()


def test_eval_env() -> dict[str, Any]:
    """Env-dict with features from ``load_table`` and aligned test labels."""
    return test_env(y=load_test_targets())

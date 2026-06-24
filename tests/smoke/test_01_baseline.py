"""Smoke test for experiments/01_baseline.py — structural predict-time check."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import roc_auc_score

from ibm_workshop import PROJECT_ROOT
from ibm_workshop.data import PUBLIC_CSV, TARGET_COL
from ibm_workshop.pipeline import build_learner

DATA_DIR = PROJECT_ROOT / "data"


def _train_predict_envs():
    frame = pd.read_csv(PUBLIC_CSV)
    rng = np.random.default_rng(0)
    indices = rng.permutation(len(frame))
    split_at = int(len(frame) * 0.8)
    train_frame = frame.iloc[indices[:split_at]]
    predict_frame = frame.iloc[indices[split_at:]]

    train_dir = DATA_DIR / "_smoke_train"
    predict_dir = DATA_DIR / "_smoke_predict"
    train_dir.mkdir(exist_ok=True)
    predict_dir.mkdir(exist_ok=True)

    train_path = train_dir / "public.csv"
    predict_path = predict_dir / "public.csv"
    train_frame.to_csv(train_path, index=False)
    predict_frame.to_csv(predict_path, index=False)

    train_y = train_frame[TARGET_COL].to_numpy()
    predict_y = predict_frame[TARGET_COL].to_numpy()

    return (
        {"data_dir": str(train_dir), "which": "public", "y": train_y},
        {"data_dir": str(predict_dir), "which": "public", "y": predict_y},
        len(predict_frame),
        predict_y,
    )


@pytest.fixture(scope="module")
def smoke_envs():
    """Build disjoint train/predict public slices for the smoke test."""
    train_env, predict_env, n_predict, predict_y = _train_predict_envs()
    yield train_env, predict_env, n_predict, predict_y
    for path in (
        DATA_DIR / "_smoke_train" / "public.csv",
        DATA_DIR / "_smoke_predict" / "public.csv",
    ):
        if path.exists():
            path.unlink()


def test_predict_row_count_matches_predict_grid(smoke_envs):
    """Hard assertion: every predict-grid row gets a prediction."""
    train_env, predict_env, n_predict_rows, _ = smoke_envs
    learner = build_learner()
    learner.fit(train_env)
    predictions = learner.predict(predict_env)
    assert len(predictions) == n_predict_rows


def test_smoke_roc_auc_is_finite(smoke_envs):
    """Soft check: scored predictions are usable (no CV baseline yet)."""
    train_env, predict_env, _, predict_y = smoke_envs
    learner = build_learner()
    learner.fit(train_env)
    proba = learner.predict_proba(predict_env)[:, 1]
    assert np.isfinite(proba).all()
    assert 0.0 <= roc_auc_score(predict_y, proba) <= 1.0

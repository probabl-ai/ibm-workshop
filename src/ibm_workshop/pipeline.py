"""Learner declaration for the random baseline model."""

from __future__ import annotations

from pathlib import Path

import skrub
from sklearn.dummy import DummyClassifier
from sklearn.pipeline import Pipeline

from ibm_workshop.data import SAMPLE_ID_COL, TARGET_COL, load_table
from ibm_workshop.features import make_scaler


def build_learner(data_dir_preview: str | Path | None = None):
    """Return the unfit SkrubLearner for the baseline experiment.

    Parameters
    ----------
    data_dir_preview
        Optional absolute path bound to ``data_dir`` for ``skb.preview()``.
    """
    data_dir = (
        skrub.var("data_dir", value=str(data_dir_preview))
        if data_dir_preview is not None
        else skrub.var("data_dir")
    )
    which = skrub.var("which")
    y = skrub.var("y").skb.mark_as_y()

    data = data_dir.skb.apply_func(load_table, which=which)
    X = (
        data.drop(columns=[SAMPLE_ID_COL, TARGET_COL], errors="ignore")
        .skb.mark_as_X()
    )

    estimator = Pipeline(
        steps=[
            ("preprocess", make_scaler()),
            ("model", DummyClassifier(strategy="uniform", random_state=0)),
        ]
    )
    predictions = X.skb.apply(estimator, y=y)
    return predictions.skb.make_learner()

"""Learner declaration.

Owns: the function that builds and returns the (unfit) learner —
typically a ``SkrubLearner`` produced from a skrub DataOps graph that
composes the steps in ``data.py`` and ``features.py`` with the chosen
estimator. Fitting, evaluation, and persistence happen elsewhere.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import skrub
from sklearn.preprocessing import StandardScaler

from ibm_workshop.data import SAMPLE_ID_COL, TARGET_COL, load_table


def build_learner(
    data_dir_preview: str | Path | None = None,
    *,
    estimator: Any,
) -> Any:
    """Return the unfit learner for the experiment scripts to consume.

    Parameters
    ----------
    data_dir_preview : str or Path or None, optional
        Preview value for the source-bound ``skrub.var("data_dir", ...)``
        root. Pass an absolute path (e.g. ``PROJECT_ROOT / "data"``)
        when iterating interactively so ``learner.skb.preview()`` works.
    estimator
        sklearn-compatible classifier attached at the tail of the graph.
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
    X = X.skb.apply(StandardScaler())
    predictions = X.skb.apply(estimator, y=y)
    return predictions.skb.make_learner()

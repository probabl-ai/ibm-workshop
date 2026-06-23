"""Learner declaration.

Owns: the function that builds and returns the (unfit) learner —
typically a ``SkrubLearner`` produced from a skrub DataOps graph that
composes the steps in ``data.py`` and ``features.py`` with the chosen
estimator. Fitting, evaluation, and persistence happen elsewhere.
"""

from __future__ import annotations

from pathlib import Path


def build_learner(data_dir_preview: str | Path | None = None):
    """Return the unfit learner for the experiment scripts to consume.

    Parameters
    ----------
    data_dir_preview : str or Path or None, optional
        Preview value for the source-bound ``skrub.var("data_dir", ...)``
        root. Pass an absolute path (e.g. ``PROJECT_ROOT / "data"``)
        when iterating interactively so ``learner.skb.preview()`` works.
    """
    raise NotImplementedError

"""Sealed private holdout submission to Skore Hub.

The only module that reads ``data/private/``. Participants fit their learner
on public data elsewhere, then call :func:`submit` with the fitted learner.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import pandas as pd
import skore
from sklearn.utils.validation import check_is_fitted
from skore import login

from ibm_workshop import PROJECT_ROOT

if TYPE_CHECKING:
    from skore import EstimatorReport

DATA_DIR = PROJECT_ROOT / "data"
PUBLIC_CSV = DATA_DIR / "public.csv"
PRIVATE_FEATURES = DATA_DIR / "private" / "features.csv"
PRIVATE_LABELS = DATA_DIR / "private" / "labels.csv"
SAMPLE_ID_COL = "sample_id"
TARGET_COL = "target"


def public_env(*, y: Any) -> dict[str, Any]:
    """Env-dict for fitting or public cross-validation.

    Parameters
    ----------
    y
        Aligned target vector for the public split (same row order as
        ``data/public.csv``).
    """
    return {"data_dir": str(DATA_DIR), "which": "public", "y": y}


def private_env() -> dict[str, str]:
    """Env-dict for private inference (features only, no labels)."""
    return {"data_dir": str(DATA_DIR), "which": "private"}


def _private_eval_data() -> dict[str, Any]:
    features = pd.read_csv(PRIVATE_FEATURES)
    labels = (
        pd.read_csv(PRIVATE_LABELS)
        .set_index(SAMPLE_ID_COL)[TARGET_COL]
        .loc[features[SAMPLE_ID_COL]]
    )
    return {**private_env(), "y": labels.to_numpy()}


@dataclass(frozen=True)
class SubmissionResult:
    """Outcome of a private holdout submission."""

    hub_key: str
    report: EstimatorReport


def submit(learner: Any, *, stem: str) -> SubmissionResult:
    """Evaluate a fitted learner on the private holdout and push to Skore Hub.

    Parameters
    ----------
    learner
        A fitted ``SkrubLearner`` (or sklearn-compatible estimator) that
        accepts the binding contract documented in ``AGENTS.md``.
    stem
        Experiment stem (e.g. ``"01_baseline"``). Hub key becomes
        ``{SKORE_USERNAME}/{stem}_private``.

    Returns
    -------
    SubmissionResult
        Hub key and the ``EstimatorReport`` that was persisted.
    """
    check_is_fitted(learner)

    username = os.environ.get("SKORE_USERNAME")
    if not username:
        msg = "SKORE_USERNAME must be set in the environment (.env)"
        raise RuntimeError(msg)
    workspace = os.environ.get("SKORE_HUB_WORKSPACE")
    if not workspace:
        msg = "SKORE_HUB_WORKSPACE must be set in the environment (.env)"
        raise RuntimeError(msg)

    report = skore.evaluate(learner, data=_private_eval_data(), splitter="prefit")

    login(mode="hub")
    project = skore.Project(workspace, mode="hub")
    hub_key = f"{username}/{stem}_private"
    project.put(hub_key, report)

    return SubmissionResult(hub_key=hub_key, report=report)

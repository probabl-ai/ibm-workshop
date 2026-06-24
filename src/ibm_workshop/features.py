"""Feature functions and transformers."""

from __future__ import annotations

from sklearn.preprocessing import StandardScaler


def make_scaler() -> StandardScaler:
    """Return a scaler for the numeric cytology feature columns."""
    return StandardScaler()

"""Inputs to ``skore.evaluate``."""

from __future__ import annotations

# Single 80/20 hold-out — no cross-validation.
splitter = 0.2


def configure_report(report):
    """Return the report (ROC-AUC is already a built-in classification metric)."""
    return report

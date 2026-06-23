"""Data loading and X-marker wiring.

Owns: how raw data is materialized into ``(X, y)``, and how structural
metadata (groups, time ordering, ...) is attached at the X marker via
``split_kwargs``.

Workshop binding contract (see ``AGENTS.md``):

- ``data/public.csv`` — train / CV (``which="public"``)
- ``data/private/features.csv`` — holdout features only (``which="private"``)
- Never read ``data/private/labels.csv`` here; ``submission.py`` supplies
  ``y`` for private eval.

Env-dict keys: ``data_dir``, ``which`` (``"public"`` | ``"private"``), ``y``.
"""

from __future__ import annotations

SAMPLE_ID_COL = "sample_id"
TARGET_COL = "target"


def load_table(data_dir: str, which: str):
    """Return a raw table for ``which`` in ``{"public", "private"}``.

    Parameters
    ----------
    data_dir
        Absolute path to the ``data/`` directory.
    which
        ``"public"`` loads ``public.csv``; ``"private"`` loads
        ``private/features.csv`` (no labels).
    """
    raise NotImplementedError

---
name: workshop-evaluate-test
description: >
  Test-set evaluation on Skore Hub: after each pipeline iteration, fit every
  catalog estimator on public data, evaluate on data/test/, and push
  EstimatorReport objects to Skore Hub. Use when the user asks to evaluate on
  the test set, push to Hub, or finalize an experiment iteration.
---

# Workshop Evaluate — Test Set on Skore Hub

Runs **after** each approved pipeline change. For **every** `(suffix, estimator)`
pair from `catalog_learners()`:

1. Build the learner with `build_learner(estimator=estimator)`.
2. Fit on full `data/public.csv`.
3. Score on `data/test/` via `EstimatorReport` (`fit=False`).
4. Push the report to Skore Hub.

## Stop conditions

- **Do not train or cross-validate on `data/test/`.** Use it only for the
  final held-out evaluation after fitting on public data.
- **Load test labels only for evaluation env-dicts** — via
  `test_eval_env()` or `load_test_targets()`. Pipelines must still load
  features through `load_table(..., which="test")`, never labels.
- **`SKORE_USERNAME`, `SKORE_HUB_API_KEY`, and `SKORE_HUB_WORKSPACE` must be
  set** in `.env` before pushing.
- **Fit is manual.** `EstimatorReport(..., fit=False)` does not call
  `learner.fit()`. Refit on full public in the experiment loop.

## Data bindings

| Path | Role |
|---|---|
| `data/public.csv` | Fit / CV (participant-owned) |
| `data/test/features.csv` | Test features (`which="test"`) |
| `data/test/labels.csv` | Test labels (evaluation env-dict only) |

Binding contract: see `AGENTS.md` § Binding contract. Use
`public_env(y=...)` for public fit and `test_eval_env()` for test eval.

## Procedure

### 1. Preconditions

```bash
uv sync --all-groups
set -a && source .env && set +a
test -n "$SKORE_USERNAME" || echo "Set SKORE_USERNAME in .env"
test -n "$SKORE_HUB_API_KEY" || echo "Set SKORE_HUB_API_KEY in .env"
uv run pytest tests/smoke/ -q   # if smoke tests exist for this experiment
```

### 2. Estimator sweep (experiment code)

```python
import os

import pandas as pd
import skore
from skore import EstimatorReport, login
from sklearn.utils.validation import check_is_fitted

from ibm_workshop.data import public_env, test_eval_env
from ibm_workshop.learners import catalog_learners
from ibm_workshop.pipeline import build_learner

public = pd.read_csv("data/public.csv")
train_env = public_env(y=public["target"].to_numpy())
test_env = test_eval_env()

login(mode="hub")
project = skore.Project(os.environ["SKORE_HUB_WORKSPACE"], mode="hub")
username = os.environ["SKORE_USERNAME"]
stem = "01_baseline"  # experiment stem

for suffix, estimator in catalog_learners():
    learner = build_learner(estimator=estimator)
    learner.fit(train_env)
    check_is_fitted(learner)

    report = EstimatorReport(
        learner,
        train_data=train_env,
        test_data=test_env,
        fit=False,
    )
    hub_key = f"{username}/{stem}_{suffix}"
    project.put(hub_key, report)
    print(hub_key)
```

Produces one **`EstimatorReport`** per estimator on Hub (`estimators/...`).

Confirm `skore.evaluate` / `EstimatorReport` signatures via `python-api` if needed.

## Where the call lives

Add the sweep as the final cell(s) of the approved experiment script after CV,
or run interactively. Do **not** hide test loading behind a removed
`submission` module — use `ibm_workshop.data` helpers directly.

## Agent must not

- Train or cross-validate on `data/test/`.
- Skip the catalog sweep after a pipeline change (unless the user explicitly
  asks to evaluate a single estimator).
- Push to Hub without `login(mode="hub")` and the `.env` credentials.

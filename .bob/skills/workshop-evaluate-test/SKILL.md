---
name: workshop-evaluate-test
description: >
  Test-set evaluation on Skore Hub: after each pipeline iteration, fit the
  learner on public data, evaluate on data/test/, and push an EstimatorReport
  to Skore Hub. Use when the user asks to evaluate on the test set, push to
  Hub, or finalize an experiment iteration.
---

# Workshop Evaluate — Test Set on Skore Hub

Runs **after** each approved pipeline change (iterations after baseline):

1. Build the learner with `build_learner()`.
2. Fit on full `data/public.csv`.
3. Score on `data/test/` via `EstimatorReport`.
4. Push the report to Skore Hub.

## Stop conditions

- **Do not train or cross-validate on `data/test/`.** Use it only for the
  final held-out evaluation after fitting on public data.
- **Load test labels only for evaluation env-dicts** — via
  `test_eval_env()` or `load_test_targets()`. Pipelines must still load
  features through `load_table(..., which="test")`, never labels.
- **`SKORE_USERNAME`, `SKORE_HUB_API_KEY`, and `SKORE_HUB_WORKSPACE` must be
  set** in `.env` before pushing.
- **Fit before `EstimatorReport`.** Call `learner.fit(train_env)` first; the
  report evaluates the already-fitted learner.

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

### 2. Test evaluation (experiment code)

```python
import os

import pandas as pd
import skore
from skore import EstimatorReport, login
from sklearn.utils.validation import check_is_fitted

from ibm_workshop.data import public_env, test_eval_env
from ibm_workshop.pipeline import build_learner

public = pd.read_csv("data/public.csv")
train_env = public_env(y=public["target"].to_numpy())
test_env = test_eval_env()

login(mode="hub")
hub_workspace, project_name = os.environ["SKORE_HUB_WORKSPACE"].split("/", 1)
project = skore.Project(
    name=project_name,
    mode="hub",
    workspace=hub_workspace,
)
username = os.environ["SKORE_USERNAME"]
stem = "02_my_experiment"  # experiment stem

learner = build_learner()
learner.fit(train_env)
check_is_fitted(learner)

report = EstimatorReport(
    learner,
    train_data=train_env,
    test_data=test_env,
)
hub_key = f"{username}/{stem}"
project.put(hub_key, report)
print(hub_key)
```

Produces one **`EstimatorReport`** on Hub (`estimators/...`).

Confirm `skore.evaluate` / `EstimatorReport` signatures via `python-api` if needed.

## Where the call lives

Add test evaluation as the final cell(s) of the approved experiment script
after CV, or run interactively. Use `ibm_workshop.data` helpers directly.

## Agent must not

- Train or cross-validate on `data/test/`.
- Push to Hub without `login(mode="hub")` and the `.env` credentials.

---
name: workshop-submit-private
description: >
  Final workshop submission: evaluate a fitted learner on the sealed private
  holdout via ibm_workshop.submission.submit, push EstimatorReport to Skore Hub.
  Use when the user asks to submit, finalize, evaluate on private, or push
  private eval to Hub after CV iteration is done.
---

# Workshop Submit — Private Evaluation on Skore Hub

Runs **after** public CV iteration is complete. The learner must already be
**fitted** (typically on full `public.csv`) before calling `submit()`.

## Stop conditions

- **Do not run during CV iteration.** Train and cross-validate on `public.csv`
  only until the user triggers submission.
- **`data/private/` is sealed.** Never read it via shell or pandas in experiment
  code. Only `ibm_workshop.submission` loads it at runtime.
- **`SKORE_USERNAME` must be set** in committed `.env` before `submit()`.
- **Fit is manual.** `submit()` does not call `learner.fit()`. Refit on full
  public in the experiment if needed, then submit.

## Data bindings

| Path | Agent ambient access | Role |
|---|---|---|
| `data/public.csv` | yes | Fit / CV (participant-owned) |
| `data/private/` | **no** (ignore files) | Loaded only inside `submission.py` |
| `data/split_meta.json` | yes | Split context — read, do not train on |

Binding contract: see `AGENTS.md` § Binding contract. Use
`submission.public_env(y=...)` for public fit and `submission.submit(learner,
stem=...)` for private eval.

## Procedure

### 1. Preconditions

```bash
uv sync --all-groups
set -a && source .env && set +a
test -n "$SKORE_USERNAME" || echo "Set SKORE_USERNAME in .env"
uv run pytest tests/smoke/ -q   # if smoke tests exist for this experiment
```

### 2. Fit on full public (experiment code — not in submit)

```python
import pandas as pd

from ibm_workshop.pipeline import build_learner
from ibm_workshop.submission import public_env

public = pd.read_csv("data/public.csv")
learner = build_learner()
learner.fit(public_env(y=public["target"].to_numpy()))
```

### 3. Private holdout → Skore Hub

```python
from ibm_workshop.submission import submit

result = submit(learner, stem="<experiment_stem>")  # e.g. 01_baseline
print(result.hub_key)  # {SKORE_USERNAME}/{stem}_private
```

Produces an **`EstimatorReport`** on Hub (`estimators/...`).

Confirm `skore.evaluate` / `EstimatorReport` signatures via `python-api` if needed.

## Where the call lives

Add a submission cell to the approved experiment script after the fit step, or
run interactively. Do **not** reimplement private loading in `experiments/` —
delegate to `submission.submit`.

## Agent must not

- Read `data/private/` outside `submission.py`.
- Train or cross-validate on private data.
- Expect `submit()` to fit the learner.
- Push to Hub without going through `submission.submit` (or duplicate its logic).

# IBM Breast Cancer Workshop — agent contract

Human-in-the-loop ML competition (~15–30 min). **Design an original pipeline**,
iterate on public data, evaluate on the held-out test set, and push each
`EstimatorReport` or `CrossValidationReport` to Skore Hub.
You should suggest 3 strategies for the user to consider, and then let the user choose the best one at each iteration.

**Iteration 1 is done** in this repo:
a uniform random classifier baseline (`01_baseline`, ROC-AUC on an 80/20 hold-out).

## Skills

When running any instructions, check the folder `.bob/skills/` and activate any skill that is relevant to the instructions.

## Before running anything, ensure this checklist is complete:


### 1. Python environment (uv)

Check that the uv python environement is correctly setup, else ask the user; you need to suggest the user to install `uv`, but you can recommend other environments as per the `python-env-manager` skill; if uv:
```bash
uv sync --all-groups
set -a && source .env && set +a
uv run python -c "import skore, skrub, ibm_workshop; print('imports OK')"
```
### 2. Skore Hub credentials

Check that `SKORE_HUB_API_KEY`, `SKORE_HUB_WORKSPACE`, and `SKORE_USERNAME` are
set in `.env`. If not, interrupt and ask the user to provide them.

## Skore Hub loggin -> BEFORE RUNNING ANY PYTHON SCRIPT

Always login to Skore Hub with the `SKORE_HUB_API_KEY` environment variable, no interactive login.
You do that by having the SKORE_HUB_API_KEY set in the shell environment (`set -a && source .env && set +a`) before calling any python script such that login() function can see the key.

## Submission guideline

When pushing an estimator or a CV to Skore Hub, push it to the workspace and
project specified in `SKORE_HUB_WORKSPACE`,
and the name of the push should be `{SKORE_USERNAME}/{experiment-name}`.
You must only push the Report on test set, not on the public data.

## Binding contract (skrub env-dict)

Pipelines must declare skrub vars `data_dir`, `which`, and `y`. Row loaders read
from `data/public.csv` or `data/test/features.csv` — never from
`data/test/labels.csv` (labels are supplied in the env-dict at evaluation time).

| Phase | Bindings |
|---|---|
| Public fit / CV | `{"data_dir": "<abs>/data", "which": "public", "y": <public targets>}` |
| Test eval | `{"data_dir": "<abs>/data", "which": "test", "y": <test targets>}` |

Helpers: `ibm_workshop.data.public_env(y=...)`, `test_env(y=...)`, `test_eval_env()`.
Use the skill `workshop-evaluate-test` for test-set evaluation and Hub push.

## Per-iteration test evaluation

After each pipeline change:

1. Fit on full `data/public.csv` via `public_env(y=...)`.
2. Build an `EstimatorReport` with `train_data=public_env(...)`,
   `test_data=test_eval_env()`.
3. Push to Skore Hub.

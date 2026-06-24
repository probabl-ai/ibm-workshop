# IBM Breast Cancer Workshop

Human-in-the-loop ML competition on Wisconsin-style cytology features:
maximize **ROC-AUC** on cross-validated `data/public.csv`, then fit on full
public data, evaluate on `data/test/`, and push reports to Skore Hub.

## Where this repo stands

**Iteration 1 is done.** A uniform random classifier baseline (`01_baseline`) is
implemented, evaluated (ROC-AUC on an 80/20 hold-out), and recorded in
[`journal/JOURNAL.md`](journal/JOURNAL.md). EDA lives under [`data/eda/eda.md`](data/eda/eda.md).

## Check the Skore Hub

Submissions land in workspace **`ibm-workshop/competition`** at
[https://skore.probabl.ai](https://skore.probabl.ai). Each report key is
`{SKORE_USERNAME}/{experiment_stem}` (set `SKORE_USERNAME` in `.env`).

Agent authentication uses `SKORE_HUB_API_KEY` from `.env` — no interactive login.

## Before you start — do this once

### 1. Set up Python (uv)

```bash
# install uv if needed: curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync --all-groups
set -a && source .env && set +a
uv run python -c "import skore, skrub, ibm_workshop; print('imports OK')"
```

### 2. Configure Skore Hub

Edit `.env` and set:

- `SKORE_USERNAME` — your username for the leaderboard

### 3. Sanity check

```bash
uv run pytest tests/smoke/test_01_baseline.py -q
```

# IBM Breast Cancer Workshop

Human-in-the-loop ML competition on Wisconsin-style cytology features:
maximize **ROC-AUC** on cross-validated `data/public.csv`, then fit every
catalog estimator on full public data, evaluate on `data/test/`, and push
reports to Skore Hub.

This repo is **self-contained**: workshop data and Bob agent skills ship in-tree
(`.bob/skills/`, `data/`). Open the folder in [Bob IDE](https://bob.probabl.ai)
to iterate with the agent.

## Where this repo stands

**Iteration 1** (`01_baseline`) is a uniform random classifier (`DummyClassifier`),
evaluated with an 80/20 hold-out on public data — same pattern as the
total-workshop baselines.
See [`journal/JOURNAL.md`](journal/JOURNAL.md) and
[`journal/01_baseline.md`](journal/01_baseline.md).

EDA: [`data/eda/eda.md`](data/eda/eda.md).

## Before you start — do this once

### 1. Agent skills (already in repo)

Skills live under `.bob/skills/`. Bob loads them automatically when you open
this project. No `npx skills add` step required.

### 2. Set up Python (uv)

```bash
# install uv if needed: curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync --all-groups
set -a && source .env && set +a
uv run python -c "import skore, skrub, ibm_workshop; print('imports OK')"
```

### 3. Data (already in repo)

| Path | Purpose |
|---|---|
| `data/public.csv` | Train + CV (450 labeled rows) |
| `data/test/features.csv` | Held-out test features |
| `data/test/labels.csv` | Held-out test labels (evaluation only) |

### 4. Configure Skore Hub

Edit `.env` and set:

- `SKORE_HUB_API_KEY` — Hub authentication
- `SKORE_HUB_WORKSPACE` — e.g. `ibm-workshop/competition`
- `SKORE_USERNAME` — prefixes every `project.put()` key

### 5. Sanity check

```bash
uv run pytest tests/smoke/test_01_baseline.py -q
```

### 6. Run the baseline experiment

```bash
set -a && source .env && set +a
uv run python experiments/01_baseline.py
```

Hub key: `{SKORE_USERNAME}/01_baseline`.

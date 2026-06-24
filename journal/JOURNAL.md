# JOURNAL

## Status

- **Project / dataset:** IBM breast cancer workshop — `data/public.csv` (450 labeled samples, 30 numeric features + `target`)
- **Goal:** maximize ROC-AUC on `data/public.csv`, then evaluate on `data/test/` and push to Skore Hub
- **Last experiment:** `01_baseline` — done (pipeline reset to dummy baseline)
- **Last result:** re-run after pipeline fix

- **Workspace decisions** (immutable unless the user pivots):
  - tabular library: pandas — recorded: 2026-06-24
  - env manager: uv — recorded: 2026-06-24
  - package name (`src/<pkg>/`): ibm_workshop — recorded: 2026-06-24
  - skore mode: hub — recorded: 2026-06-24
  - skore hub workspace: ibm-workshop/competition — recorded: 2026-06-24
  - CV splitter family: hold-out 0.2 — recorded: 2026-06-24

## Data understanding (EDA)

- **Status:** done — 2026-06-23
- **Summary:** 450×32 numeric tabular set (`data/public.csv`); no missing values; binary `target` imbalanced (136×0, 314×1); no datetime/group structure; strongest target links on radius/concavity features; tight collinearity among size-related columns. Drop `sample_id` from features.
- **Report:** [data/eda/eda.md](../data/eda/eda.md)

## History

| Stem | Intent (one line) | Status | Headline result | Design note |
|---|---|---|---|---|
| `01_baseline` | Uniform random classifier, ROC-AUC hold-out | done | re-run after fix | [design note](01_baseline.md) |

## Backlog

| # | Item | Source |
|---|---|---|
| | | |

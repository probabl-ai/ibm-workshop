# JOURNAL

## Status

- **Project / dataset:** IBM breast cancer workshop — `data/public.csv` (450 labeled samples, 30 numeric features + `target`)
- **Goal:** maximize ROC-AUC on cross-validated `data/public.csv`, then fit on full public data, evaluate every catalog estimator on `data/test/`, and push those evaluations to Skore Hub
- **Last experiment:** n/a — bootstrap
- **Last result:** n/a

## Data understanding (EDA)

- **Status:** done — 2026-06-23
- **Summary:** 450×32 numeric tabular set (`data/public.csv`); no missing values; binary `target` imbalanced (136×0, 314×1); no datetime/group structure; strongest target links on radius/concavity features; tight collinearity among size-related columns. Drop `sample_id` from features.
- **Report:** [data/eda/eda.md](../data/eda/eda.md)

## History

| Stem | Intent (one line) | Status | Headline result | Design note |
|---|---|---|---|---|
| | | | | |

## Backlog

| # | Item | Source |
|---|---|---|
| | | |

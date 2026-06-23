---
name: workshop-data
description: >
  IBM workshop data layout for the breast cancer challenge. Owns
  public/test split paths, EDA under data/eda/, and agent ignore rules
  (.cursorignore, .bobignore). TRIGGER when loading data, splitting,
  scoring, configuring agent access, or preparing test-set evaluations.
---

# Workshop Data

## Files

| Path | In git | Agent context | Purpose |
|---|---|---|---|
| `data/public.csv` | yes | yes | Train (labeled) |
| `data/test/features.csv` | yes | yes | Test features (no labels in table) |
| `data/test/labels.csv` | yes | yes | Test labels (evaluation only) |
| `data/eda/` | yes | yes | EDA deliverables (`eda.py`, `eda.md`, HTML) |
| `data/split_meta.json` | yes | **blocked** | Split provenance (ignore files) |

## Test evaluation

After each pipeline iteration, evaluate every catalog estimator on the test
set and push to Skore Hub — see `workshop-evaluate-test` skill.

---
name: workshop-data
description: >
  IBM workshop data layout for the breast cancer challenge. Owns
  public/private split paths, split_meta.json, EDA under data/eda/,
  agent ignore rules (.cursorignore, .bobignore), and the sealed
  data/private/ holdout (submission.py only). TRIGGER when loading
  data, splitting, scoring, configuring agent access, or preparing
  submissions.
---

# Workshop Data

## Files

| Path | In git | Agent context | Purpose |
|---|---|---|---|
| `data/public.csv` | yes | yes | Train (450 rows, labeled) |
| `data/split_meta.json` | yes | yes | Split stats (no row-level labels) |
| `data/eda/` | yes | yes | EDA deliverables (`eda.py`, `eda.md`, HTML) |

## Submission

Final private evaluation on Skore Hub: `ibm_workshop.submission.submit` via
`workshop-submit-private` skill.

---
name: workshop-data
description: >
  IBM workshop data layout for the breast cancer challenge. Owns
  public/private split paths, organizer-only ground truth, and agent
  ignore rules for IBM Bob (`.bobignore`) and Cursor (`.cursorignore`).
  TRIGGER when loading data, splitting, scoring, or configuring agent
  access to private labels.
---

# Workshop Data

## Files

| Path | In git | Agent context | Purpose |
|---|---|---|---|
| `data/public.csv` | yes | yes | Train (450 rows, labeled) |
| `data/private.csv` | yes | yes | Predict (119 rows, no `target`) |
| `data/split_meta.json` | yes | yes | Split stats only |
| `data/organizer/full.csv` | no | **blocked** | Full 569-row master |
| `data/organizer/private_labels.csv` | no | **blocked** | Private ground truth |

## Ignore rules

| IDE | Agent blocking | Version control | Behavior rules |
|---|---|---|---|
| **IBM Bob** | `.bobignore` | `.bob/` committed | `AGENTS.md`, `.bob/rules/workshop-data.md` |
| **Cursor** | `.cursorignore` | `.cursor/` gitignored | `AGENTS.md`, skill only (rules are local) |

- `.gitignore` ignores `data/organizer/` for both IDEs.
- Never put private labels in participant-facing paths.
- `.cursorignore` and `.bobignore` carry the same patterns.

## Split

- Stratified 450 / 119, `random_state=42`.
- Balance: ~37.3% malignant, ~62.7% benign (public matches full; private within 0.3 pp).

## Agent must not

- Read `data/organizer/` or circumvent ignore files via shell.
- Evaluate on the private set — only emit `predictions.csv`.

## Cursor setup note

`.cursor/` is gitignored (local IDE state). After clone, Cursor still loads
`.cursorignore` and `AGENTS.md`. To add local rules, create
`.cursor/rules/workshop-data.mdc` from `.agents/skills/workshop-data/references/cursor-rule.mdc`.

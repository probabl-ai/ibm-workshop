<!--
Exploratory data analysis summary for this workspace, written from
the data/eda.py run. Ground every claim in what the run actually
showed — do not invent facts. Keep "Modelling implications" as
candidate suggestions to weigh when designing the model, not final
decisions.
-->

# EDA — IBM breast cancer workshop (public training set)

_Generated from `data/eda.py` on 2026-06-23._

## Dataset at a glance

- **Tables:** `public` (`data/public.csv`)
- **Shape:** 450 rows × 32 columns (30 numeric cytology features, `sample_id`, `target`)
- **Target:** `target` — binary classification (0 / 1)
- **Rich reports:** [eda_public.html](eda_public.html)

## Per-column findings

- All 32 columns are numeric (`Int64` for `sample_id` and `target`, `Float64` for the 30 feature columns).
- **No missing values** — null proportion 0.0 on every column.
- `sample_id` is a row identifier (450 distinct values); it should not enter the model as a feature.
- Feature names follow the classic Wisconsin breast-cancer cytology schema (`mean radius`, `worst perimeter`, `concavity error`, …).

## Target

- **Class balance:** 136 samples with `target=0` (30.2%), 314 with `target=1` (69.8%) — mild-to-moderate imbalance.

## Structure

- **No datetime columns** detected.
- **No obvious group column** beyond `sample_id` (one row per sample).
- Standard IID tabular setup

## Associations

Strongest feature↔target associations (Cramér's V / Pearson):

| Feature | Association with `target` |
|---|---|
| `worst radius` | 0.74 |
| `mean concave points` | 0.70 |
| `mean concavity` | 0.65 |
| `worst concave points` | 0.61 |
| `worst compactness` | (moderate; see HTML report) |

Notable feature↔feature collinearity: `mean perimeter` ↔ `worst perimeter` (0.91), `worst perimeter` ↔ `worst area` (0.90), `mean area` ↔ `worst area` (0.86). Several size-related columns form a tight block. No implausibly perfect (≈1.0) feature↔target link; `sample_id` must still be excluded.

## Open questions

- Are any column names or value ranges known to carry domain-specific measurement semantics beyond what the data shows?

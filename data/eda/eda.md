<!--
Exploratory data analysis summary for this workspace, written from
the data/eda.py run. Ground every claim in what the run actually
showed — do not invent facts. Keep "Modelling implications" as
candidate suggestions to weigh when designing the model, not final
decisions.
-->

# EDA — IBM breast cancer workshop (public training set)

_Generated from `data/eda.py` on 2026-06-22._

## Dataset at a glance

- **Tables:** `public` (`data/public.csv`)
- **Shape:** 450 rows × 32 columns (30 numeric cytology features, `sample_id`, `target`)
- **Target:** `target` — binary classification (0 / 1)
- **Rich reports:** [eda_public.html](eda_public.html)

## Per-column findings

- All 32 columns are numeric (`Int64` for `sample_id` and `target`, `Float64` for the 30 feature columns).
- **No missing values** — null proportion 0.0 on every column.
- `sample_id` is a row identifier (450 distinct values implied by the table shape); it should not enter the model as a feature.
- Feature names follow the classic Wisconsin breast-cancer cytology schema (`mean radius`, `worst perimeter`, `concavity error`, …).

## Target

- **Class balance:** 168 samples with `target=0` (37.3%), 282 with `target=1` (62.7%).
- Mild imbalance — stratified cross-validation is preferable to plain `KFold`.
- Workshop metadata aligns with ~37% malignant / ~63% benign on the public split.

## Structure

- **No datetime columns** detected.
- **No obvious group column** beyond `sample_id` (one row per sample).
- Standard IID tabular setup — no temporal or grouped CV structure required unless future data adds it.

## Associations

Strongest feature↔target associations (Cramér's V / Pearson):

| Feature | Association with `target` |
|---|---|
| `worst perimeter` | 0.85 |
| `worst concave points` | 0.84 |
| `mean concave points` | 0.83 |
| `worst radius` | 0.83 |
| `worst area` | 0.83 |

Several “worst”-statistic columns dominate — consistent with malignant tumors showing larger, more irregular nuclei. No implausibly perfect (≈1.0) feature↔target link was observed; leakage risk from a single column looks low, but `sample_id` must still be excluded.

Notable feature↔feature collinearity: `mean radius` ↔ `mean perimeter` (0.84), `mean radius` ↔ `mean area` (0.80) — expect redundant signal; tree/linear models handle this differently.

## Modelling implications

- **Learner:** `skrub.tabular_pipeline` on the 30 numeric features (drop `sample_id`) is a sensible baseline for heterogeneous-but-all-numeric tabular data.
- **Metric:** ROC-AUC matches the stated goal and is robust to the 37/63 class split better than accuracy.
- **CV:** prefer **stratified** folding (`StratifiedKFold`) — decided concretely at the evaluation step (`G-CV-SPLITTER`).
- **Preprocessing:** no missing-value imputation needed; scaling may help linear models inside the default pipeline.
- **Private-set deliverable:** train on `public.csv`; sealed eval via `ibm_workshop.submission.submit` (reads `data/private/`, blocked from ambient context).

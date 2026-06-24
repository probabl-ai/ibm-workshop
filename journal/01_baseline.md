# 01_baseline

## Question / hypothesis

Does a uniform random classifier on `target` produce a ROC-AUC near chance on
an 80/20 hold-out?

## Motivation

- **Sourcing strategy:** my-pick
- **Source(s):**
  - Bootstrap after EDA — mirrors the total-workshop baseline pattern
    (`DummyClassifier(strategy="uniform")`).
- **Why this matters:** Establishes a deliberately weak reference point before
  richer models.

## Method

- **Files touched:** `src/ibm_workshop/{data,features,pipeline,evaluate}.py`,
  `experiments/01_baseline.py`
- **Change versus baseline (or previous experiment):** First experiment.
  `StandardScaler` + `DummyClassifier(strategy="uniform")` — ignores features,
  predicts 0/1 at random.
- **Cross-validation:** none — single 80/20 hold-out split.
- **Out of scope for this experiment:** feature engineering, hyperparameter
  tuning, test-set evaluation.

## Risks / things that could invalidate the result

- Random hold-out may yield high variance on ROC-AUC with only 450 rows.
- Mild class imbalance (30% / 70%) affects accuracy more than ROC-AUC for a
  uniform dummy.

## Status

- **State:** done
- **Approved by user on:** 2026-06-24
- **Headline result:** re-run after pipeline fix
- **Implication for next iteration:** Any real model should beat ROC-AUC ≈ 0.50.

# IBM Breast Cancer Workshop — agent contract

Human-in-the-loop ML competition (~15–30 min). **Design an original pipeline**,
iterate on public data, and **each iteration systematically evaluate every
estimator in `ibm_workshop.learners.catalog_learners()` on the test set**,
then push each `EstimatorReport` to Skore Hub.
You should suggest 3 strategies for the user to consider, and then let the user choose the best one at each iteration.

## Skills (mandatory)

Before acting, **systematically check** whether a skill in `.agents/skills/` applies to the
current task. When one does, read its `SKILL.md` and follow it — do not improvise equivalent
workflows from memory.

| Phase | Skills |
|---|---|
| Workspace setup | `organize-ml-workspace`, `python-env-manager` |
| Data understanding | `explore-ml-data`, `workshop-data` |
| Pipeline design | `build-ml-pipeline`, `evaluate-ml-pipeline` |
| Experiment loop | `iterate-ml-experiment`, `iterate-from-skore`, `iterate-from-user` |
| Quality | `smoke-test-ml-pipeline`, `audit-ml-pipeline`, `python-code-style` |
| Test eval + Hub | `workshop-evaluate-test` |

If several skills could apply, read each relevant `SKILL.md` frontmatter (description +
TRIGGER) and follow the most specific one first.

## Data

| Path | LLM context | Labels | Use |
|---|---|---|---|
| `data/public.csv` | yes | yes | Train + CV only |x
| `data/test/` | yes | yes (in `labels.csv`) | Held-out test set — evaluate only |
| `data/eda/` | yes | — | EDA deliverables (`eda.py`, `eda.md`, `eda_public.html`) |

Inside `data/test/`:

- `features.csv` — test features (no `target` column)
- `labels.csv` — test labels (`sample_id`, `target`)

### Binding contract (skrub env-dict)

Pipelines must declare skrub vars `data_dir`, `which`, and `y`. Row loaders
read from `data/public.csv` or `data/test/features.csv` — never from
`data/test/labels.csv` (labels are supplied in the env-dict at evaluation time).

| Phase | Bindings |
|---|---|
| Public fit / CV | `{"data_dir": "<abs>/data", "which": "public", "y": <public targets>}` |
| Test eval | `{"data_dir": "<abs>/data", "which": "test", "y": <test targets>}` |

Helpers: `ibm_workshop.data.public_env(y=...)`, `test_env(y=...)`, `test_eval_env()`.
Use the skill `workshop-evaluate-test` for test-set evaluation and Hub push.

## Per-iteration estimator sweep

After each pipeline change, **loop over every `(suffix, estimator)` pair** from
`catalog_learners()`:

1. Build the learner with `build_learner(estimator=estimator)`.
2. Fit on full `data/public.csv` via `public_env(y=...)`.
3. Build an `EstimatorReport` with `train_data=public_env(...)`,
   `test_data=test_eval_env()`, `fit=False`.
4. Push to Skore Hub (see `workshop-evaluate-test`).

Hub report keys: `{SKORE_USERNAME}/{experiment_stem}_{suffix}` (e.g.
`luigi/01_baseline_lr_l2`).

## Environment

This project uses **uv** as its sole Python environment manager. Never use `pip install`,
`poetry`, `conda`, or other managers directly — use `uv` for sync, run, add, and remove
(see the `python-env-manager` skill for the exact commands).

Bootstrap and load credentials:

```bash
uv sync --all-groups
set -a && source .env && set +a
```

Run scripts and tests through uv, e.g. `uv run pytest`, `uv run python experiments/…`.

### Skore Hub (committed `.env`)

| Variable | Required | Purpose |
|---|---|---|
| `SKORE_HUB_API_KEY` | yes | Hub authentication (`login(mode="hub")`) |
| `SKORE_HUB_WORKSPACE` | yes | e.g. `ibm-workshop/competition` |
| `SKORE_USERNAME` | **yes** | Prefixes every `project.put()` key |

If any of those variables are not set, the agent should interrupt and ask the user to set them.

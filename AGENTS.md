# IBM Breast Cancer Workshop — agent contract

Human-in-the-loop ML competition (~15–30 min). **Design an original pipeline**,
iterate on public data, and each time call **`ibm_workshop.submission.submit`** to test your 
pipeline on the sealed private holdout.
You should suggest 3 strategies for the user to consider, and then let the user choose the best one at each iteration.

## Data

| Path | LLM context | Labels | Use |
|---|---|---|---|
| `data/public.csv` | yes | yes | Train + CV only |
| `data/private/` | **blocked** | yes (in `labels.csv`) | Sealed holdout — only `submission.py` reads it |
| `data/eda/` | yes | — | EDA deliverables (`eda.py`, `eda.md`, `eda_public.html`) |

Inside `data/private/` (blocked from agent context):

- `features.csv` — holdout features (no `target` column)
- `labels.csv` — holdout labels (`sample_id`, `target`)

### Binding contract (skrub env-dict)

Pipelines must declare skrub vars `data_dir`, `which`, and `y`. Row loaders
read from `data/public.csv` or `data/private/features.csv` — never from
`data/private/labels.csv` (labels are supplied only by `submission.submit`).

| Phase | Bindings |
|---|---|
| Public fit / CV | `{"data_dir": "<abs>/data", "which": "public", "y": <public targets>}` |
| Private eval (`submit`) | built internally — same keys, `which="private"`, `y` from `labels.csv` |

Helpers: `ibm_workshop.submission.public_env(y=...)`, `private_env()`.
Use the skill `workshop-submit-private` to submit the private evaluation.

## Environment (committed `.env`)

| Variable | Required | Purpose |
|---|---|---|
| `SKORE_API_KEY` | yes | Hub authentication |
| `SKORE_HUB_WORKSPACE` | yes | e.g. `ibm-workshop/dev` |
| `SKORE_USERNAME` | **yes** | Prefixes every `project.put()` key |

If any of those variables are not set, the agent should interrupt and ask the user to set them.

To set the environment variables, the agent should run the following command:
```bash
uv sync --all-groups
set -a && source .env && set +a
```

Hub report keys: `{SKORE_USERNAME}/{experiment_stem}`
Only push private evaluations on the Hub.
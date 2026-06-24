# %% [markdown]
# # Experiment: baseline random classifier
#
# **Date:** 2026-06-24
# **Goal:** Uniform random classifier; ROC-AUC on hold-out.
# **Result:** filled in after the run.

# %%
import os

import pandas as pd
import skore
from skore import login

from ibm_workshop import PROJECT_ROOT
from ibm_workshop.data import public_env
from ibm_workshop.evaluate import configure_report, splitter
from ibm_workshop.pipeline import build_learner

# %%
DATA_DIR = PROJECT_ROOT / "data"

# %%
login(mode="hub")
hub_workspace, project_name = os.environ["SKORE_HUB_WORKSPACE"].split("/", 1)
project = skore.Project(
    name=project_name,
    mode="hub",
    workspace=hub_workspace,
)
username = os.environ["SKORE_USERNAME"]

# %%
public = pd.read_csv(DATA_DIR / "public.csv")
train_env = public_env(y=public["target"].to_numpy())

# %%
learner = build_learner(data_dir_preview=DATA_DIR)

# %%
report = configure_report(
    skore.evaluate(learner, data=train_env, splitter=splitter)
)
report

# %%
project.put(f"{username}/01_baseline", report)

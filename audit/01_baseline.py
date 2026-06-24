# %% [markdown]
# # Audit — 01_baseline: scaled logistic regression, ROC-AUC
#
# Read-only review of the stored CV report: checks and metrics.

# %%
import os

import skore
from skore import login

from ibm_workshop import PROJECT_ROOT

# %%
login(mode="hub")
hub_workspace, project_name = os.environ["SKORE_HUB_WORKSPACE"].split("/", 1)
project = skore.Project(
    name=project_name,
    mode="hub",
    workspace=hub_workspace,
)
project

# %%
summary = project.summarize().frame()
summary

# %%
username = os.environ["SKORE_USERNAME"]
summary_df = project.summarize().frame()
report_id = summary_df.loc[
    (summary_df["key"] == f"{username}/01_baseline")
    & (summary_df["report_type"] == "cross-validation"),
].index.get_level_values("id")[-1]
report = project.get(report_id)
type(report).__name__

# %%
report.checks.summarize().frame()

# %%
report.metrics.summarize().frame()

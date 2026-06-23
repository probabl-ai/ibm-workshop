"""Factory for 20 distinct sklearn classifiers used in batch submissions."""

from __future__ import annotations

from typing import Any

from sklearn.discriminant_analysis import (
    LinearDiscriminantAnalysis,
)
from sklearn.ensemble import (
    AdaBoostClassifier,
    BaggingClassifier,
    ExtraTreesClassifier,
    GradientBoostingClassifier,
    HistGradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.linear_model import (
    LogisticRegression,
    PassiveAggressiveClassifier,
    RidgeClassifier,
    SGDClassifier,
)
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.tree import DecisionTreeClassifier


def submission_learners() -> list[tuple[str, Any]]:
    """Return ``(stem_suffix, estimator)`` pairs — 20 distinct learners."""
    rs = 0
    return [
        ("lr_l2", LogisticRegression(max_iter=2000, random_state=rs)),
        (
            "lr_l1",
            LogisticRegression(
                penalty="l1", solver="saga", max_iter=2000, random_state=rs
            ),
        ),
        ("svc_rbf", SVC(kernel="rbf", probability=True, random_state=rs)),
        ("svc_linear", LinearSVC(random_state=rs)),
        ("rf_100", RandomForestClassifier(n_estimators=100, random_state=rs)),
        (
            "rf_300",
            RandomForestClassifier(n_estimators=300, max_depth=8, random_state=rs),
        ),
        ("extra_trees", ExtraTreesClassifier(n_estimators=200, random_state=rs)),
        ("grad_boost", GradientBoostingClassifier(random_state=rs)),
        ("hist_gb", HistGradientBoostingClassifier(random_state=rs)),
        ("ada_boost", AdaBoostClassifier(random_state=rs)),
        ("bagging", BaggingClassifier(random_state=rs)),
        ("knn_5", KNeighborsClassifier(n_neighbors=5)),
        ("knn_15", KNeighborsClassifier(n_neighbors=15)),
        ("gaussian_nb", GaussianNB()),
        ("ridge", RidgeClassifier(random_state=rs)),
        ("sgd_log", SGDClassifier(loss="log_loss", max_iter=2000, random_state=rs)),
        ("passive_agg", PassiveAggressiveClassifier(random_state=rs)),
        ("decision_tree", DecisionTreeClassifier(max_depth=6, random_state=rs)),
        (
            "mlp",
            MLPClassifier(
                hidden_layer_sizes=(64, 32), max_iter=500, random_state=rs
            ),
        ),
        ("lda", LinearDiscriminantAnalysis()),
    ]

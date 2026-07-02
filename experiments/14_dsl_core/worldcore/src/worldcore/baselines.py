from __future__ import annotations

import random
from collections import Counter

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from worldcore.metrics import task_feature_counts
from worldcore.types import Task


def labels(tasks: list[Task]) -> list[str]:
    return [str(task.answer) for task in tasks]


def majority_label(y: list[str]) -> str:
    return Counter(y).most_common(1)[0][0] if y else "unknown"


def majority_predictions(train_y: list[str], n: int) -> list[str]:
    return [majority_label(train_y)] * n


def random_predictions(train_y: list[str], n: int, seed: int) -> list[str]:
    rng = random.Random(seed)
    choices = sorted(set(train_y)) or ["unknown"]
    return [rng.choice(choices) for _ in range(n)]


def memorization_predictions(train_tasks: list[Task], test_tasks: list[Task]) -> list[str]:
    train_y = labels(train_tasks)
    default = majority_label(train_y)
    memory = {task.canonical_task_hash: str(task.answer) for task in train_tasks}
    return [memory.get(task.canonical_task_hash, default) for task in test_tasks]


def memorization_analysis(train_tasks: list[Task], test_tasks: list[Task]) -> dict[str, object]:
    from worldcore.metrics import answer_accuracy

    memory = {task.canonical_task_hash: str(task.answer) for task in train_tasks}
    default = majority_label(labels(train_tasks))
    seen_true: list[str] = []
    seen_pred: list[str] = []
    unseen_true: list[str] = []
    unseen_pred: list[str] = []
    for task in test_tasks:
        truth = str(task.answer)
        if task.canonical_task_hash in memory:
            seen_true.append(truth)
            seen_pred.append(memory[task.canonical_task_hash])
        else:
            unseen_true.append(truth)
            unseen_pred.append(default)
    return {
        "seen_hashes": len(seen_true),
        "unseen_hashes": len(unseen_true),
        "accuracy_on_seen": answer_accuracy(seen_true, seen_pred),
        "accuracy_on_unseen": answer_accuracy(unseen_true, unseen_pred),
        "majority_fallback": default,
    }


def fit_statistical_model(train_tasks: list[Task], seed: int = 0, kind: str = "logistic") -> Pipeline:
    features = [task_feature_counts(task) for task in train_tasks]
    y = labels(train_tasks)
    if len(set(y)) < 2:
        y = y + ["__dummy__"]
        features = features + [{"dummy": 1.0}]
    if kind == "forest":
        clf = RandomForestClassifier(n_estimators=80, random_state=seed, max_depth=8)
    else:
        clf = LogisticRegression(max_iter=500, random_state=seed)
    model = Pipeline([("vec", DictVectorizer()), ("clf", clf)])
    model.fit(features, np.array(y))
    return model


def predict_statistical_model(model: Pipeline, tasks: list[Task]) -> list[str]:
    features = [task_feature_counts(task) for task in tasks]
    return [str(value) for value in model.predict(features)]

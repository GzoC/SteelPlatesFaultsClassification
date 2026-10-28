import hashlib
import json
import platform
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from .schema import CLASSES, FEATURES, SCHEMA_VERSION, validate_features

# Exact original download bytes, protected from Git newline conversion.
DATA_SHA256 = "08994f5b0185a8e6cc22afe9910fd36834990fb1ca30852ed79012a832fbff55"


def read_data(path):
    if hashlib.sha256(Path(path).read_bytes()).hexdigest() != DATA_SHA256:
        raise ValueError("El archivo no coincide con la fuente UCI verificada")
    data = pd.read_csv(path, sep=r"\s+", header=None)
    if data.shape != (1941, 34):
        raise ValueError("Dimensiones UCI inesperadas")
    data.columns = FEATURES + CLASSES
    one_hot = data[CLASSES]
    if not one_hot.isin([0, 1]).all().all() or not one_hot.sum(axis=1).eq(1).all():
        raise ValueError("Cada observación debe tener un único tipo de defecto")
    return validate_features(data[FEATURES]), one_hot.idxmax(axis=1)


def review_mask(scores):
    ordered = np.sort(scores, axis=1)
    return (ordered[:, -1] < 0.6) | ((ordered[:, -1] - ordered[:, -2]) < 0.15)


def metrics(y, predictions, scores):
    needs_review = review_mask(scores)
    covered = ~needs_review
    return {
        "rows": len(y),
        "accuracy": float(accuracy_score(y, predictions)),
        "macro_f1": float(
            f1_score(y, predictions, labels=CLASSES, average="macro", zero_division=0)
        ),
        "per_class": classification_report(
            y, predictions, labels=CLASSES, output_dict=True, zero_division=0
        ),
        "confusion_matrix": confusion_matrix(y, predictions, labels=CLASSES).tolist(),
        "review": {
            "flagged": int(needs_review.sum()),
            "coverage": float(covered.mean()),
            "accuracy_on_unflagged": float(
                accuracy_score(np.asarray(y)[covered], predictions[covered])
            )
            if covered.any()
            else None,
        },
    }


def train(data_path, output):
    x, y = read_data(data_path)
    train_ids, rest = train_test_split(
        np.arange(len(x)), test_size=0.4, stratify=y, random_state=42
    )
    val_ids, test_ids = train_test_split(
        rest, test_size=0.5, stratify=y.iloc[rest], random_state=42
    )
    if x.duplicated().any():
        raise ValueError("Duplicados requieren partición por grupos antes de evaluar")
    candidates = {
        "majority": Pipeline([("model", DummyClassifier(strategy="most_frequent"))]),
        "logistic": Pipeline(
            [
                ("scale", StandardScaler()),
                (
                    "model",
                    LogisticRegression(class_weight="balanced", max_iter=3000, random_state=42),
                ),
            ]
        ),
        "forest": Pipeline(
            [
                (
                    "model",
                    RandomForestClassifier(
                        n_estimators=300,
                        min_samples_leaf=2,
                        class_weight="balanced_subsample",
                        random_state=42,
                        n_jobs=1,
                    ),
                )
            ]
        ),
    }
    validation = {}
    for name, pipeline in candidates.items():
        pipeline.fit(x.iloc[train_ids], y.iloc[train_ids])
        validation[name] = metrics(
            y.iloc[val_ids],
            pipeline.predict(x.iloc[val_ids]),
            pipeline.predict_proba(x.iloc[val_ids]),
        )
    # Selection finishes before any test prediction; never refit on validation/test.
    selected = max(candidates, key=lambda name: validation[name]["macro_f1"])
    model = candidates[selected]
    test = {
        name: metrics(
            y.iloc[test_ids],
            pipeline.predict(x.iloc[test_ids]),
            pipeline.predict_proba(x.iloc[test_ids]),
        )
        for name, pipeline in candidates.items()
    }
    importance = permutation_importance(
        model, x.iloc[val_ids], y.iloc[val_ids], scoring="f1_macro", n_repeats=3, random_state=42
    )
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output / "pipeline.joblib")
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "features": FEATURES,
        "classes": CLASSES,
        "dataset": {
            "name": "Steel Plates Faults / UCI",
            "doi": "10.24432/C5J88N",
            "sha256": DATA_SHA256,
            "rows": len(x),
            "healthy_class": False,
        },
        "environment": {"python": platform.python_version(), "sklearn": sklearn.__version__},
        "artifact_sha256": hashlib.sha256((output / "pipeline.joblib").read_bytes()).hexdigest(),
        "split": {
            name: {
                "rows": len(ids),
                "counts": y.iloc[ids].value_counts().to_dict(),
                "indices": ids.tolist(),
            }
            for name, ids in [("train", train_ids), ("validation", val_ids), ("test", test_ids)]
        },
        "selection": "Highest validation macro-F1 among fixed candidates, stratified 60/20/20 seed42; no temporal/asset claim",
        "selected": selected,
        "validation": validation,
        "test": test,
        "review_policy": "Fixed before evaluation: max score <0.60 or top-two margin <0.15. Uncalibrated scores; heuristic review flag, not guaranteed confidence.",
        "ranges": {
            name: {
                "min": float(x.iloc[train_ids][name].min()),
                "max": float(x.iloc[train_ids][name].max()),
            }
            for name in FEATURES
        },
        "validation_permutation_importance": sorted(
            [
                {"feature": name, "mean": float(mean), "std": float(std)}
                for name, mean, std in zip(
                    FEATURES, importance.importances_mean, importance.importances_std, strict=True
                )
            ],
            key=lambda item: -item["mean"],
        ),
        "examples": [
            {"row": int(i), "features": x.iloc[i].to_dict(), "observed": str(y.iloc[i])}
            for i in test_ids[:7]
        ],
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest

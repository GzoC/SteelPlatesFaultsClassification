import hashlib
import json
from pathlib import Path

import joblib
import numpy as np
import sklearn

from .schema import CLASSES, FEATURES, SCHEMA_VERSION, validate_features
from .training import review_mask


class Predictor:
    def __init__(self, directory):
        path = Path(directory)
        self.manifest = json.loads((path / "manifest.json").read_text(encoding="utf-8"))
        m = self.manifest
        if (
            m["schema_version"] != SCHEMA_VERSION
            or m["features"] != FEATURES
            or m["classes"] != CLASSES
        ):
            raise ValueError("Contrato del artefacto incompatible")
        if m["environment"]["sklearn"] != sklearn.__version__:
            raise ValueError("Reentrena con la versión instalada de scikit-learn")
        if (
            hashlib.sha256((path / "pipeline.joblib").read_bytes()).hexdigest()
            != m["artifact_sha256"]
        ):
            raise ValueError("El artefacto no coincide con su checksum")
        # Only trusted local training artifacts: a checksum is not authentication.
        self.pipeline = joblib.load(path / "pipeline.joblib")

    def predict(self, frame):
        frame = validate_features(frame)
        if len(frame) > 100:
            raise ValueError("Máximo 100 observaciones por consulta")
        scores = self.pipeline.predict_proba(frame)
        review = review_mask(scores)
        results = []
        for index, (row, probabilities) in enumerate(
            zip(frame.to_dict("records"), scores, strict=True)
        ):
            ordered = np.argsort(-probabilities)
            outside = [
                name
                for name, value in row.items()
                if not self.manifest["ranges"][name]["min"]
                <= value
                <= self.manifest["ranges"][name]["max"]
            ]
            results.append(
                {
                    "class": str(self.pipeline.classes_[ordered[0]]),
                    "score": float(probabilities[ordered[0]]),
                    "margin": float(probabilities[ordered[0]] - probabilities[ordered[1]]),
                    "review": bool(review[index] or outside),
                    "outside_training_range": outside,
                    "scores": {
                        str(name): float(p)
                        for name, p in zip(self.pipeline.classes_, probabilities, strict=True)
                    },
                }
            )
        return results

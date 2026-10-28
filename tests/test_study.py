import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from steel_faults.inference import Predictor
from steel_faults.schema import CLASSES, FEATURES, validate_features
from steel_faults.training import read_data, review_mask, train

DATA = Path(__file__).parents[1] / "data/raw/Faults.NNA"


@pytest.fixture(scope="session")
def trained(tmp_path_factory):
    path = tmp_path_factory.mktemp("model")
    report = train(DATA, path)
    return path, report


def test_dataset_schema_matches_source_labels():
    x, y = read_data(DATA)
    assert x.shape == (1941, 27)
    assert set(y) == set(CLASSES)
    assert not set(x.columns) & set(CLASSES)
    assert y.value_counts().to_dict()["Dirtiness"] == 55


def test_partitions_and_selection_are_explicit(trained):
    _, report = trained
    splits = [set(report["split"][name]["indices"]) for name in ["train", "validation", "test"]]
    assert not splits[0] & splits[1] and not splits[0] & splits[2] and not splits[1] & splits[2]
    assert set.union(*splits) == set(range(1941))
    assert report["selected"] == max(
        report["validation"], key=lambda n: report["validation"][n]["macro_f1"]
    )
    assert sum(map(sum, report["test"][report["selected"]]["confusion_matrix"])) == len(splits[2])


def test_reload_equivalence_and_column_order(trained):
    directory, report = trained
    predictor = Predictor(directory)
    frame = pd.DataFrame([report["examples"][0]["features"]])
    result = predictor.predict(frame)[0]
    direct = predictor.pipeline.predict_proba(frame.loc[:, FEATURES])[0]
    assert result["score"] == pytest.approx(direct.max())
    assert predictor.predict(frame.loc[:, FEATURES[::-1]]) == [result]
    assert sum(result["scores"].values()) == pytest.approx(1)


@pytest.mark.parametrize("bad", [np.nan, np.inf, "text", True])
def test_bad_values_rejected(bad):
    frame, _ = read_data(DATA)
    frame = frame.iloc[:1].copy()
    frame["Pixels_Areas"] = bad
    with pytest.raises(ValueError):
        validate_features(frame)


def test_extra_label_missing_column_and_geometry_rejected():
    frame, _ = read_data(DATA)
    for invalid in [
        frame.assign(Pastry=1),
        frame.drop(columns=[FEATURES[0]]),
        frame.assign(X_Minimum=frame.X_Maximum + 1),
        frame.assign(TypeOfSteel_A400=frame.TypeOfSteel_A300),
    ]:
        with pytest.raises(ValueError):
            validate_features(invalid)


def test_review_rule_and_out_of_range(trained):
    assert review_mask(np.array([[0.55, 0.45], [0.65, 0.35], [0.51, 0.49]])).tolist() == [
        True,
        False,
        True,
    ]
    directory, report = trained
    frame = pd.DataFrame([report["examples"][0]["features"]])
    frame["Pixels_Areas"] = report["ranges"]["Pixels_Areas"]["max"] + 1
    result = Predictor(directory).predict(frame)[0]
    assert result["review"] and "Pixels_Areas" in result["outside_training_range"]


def test_artifact_integrity_before_deserialization(trained, tmp_path, monkeypatch):
    directory, _ = trained
    (tmp_path / "manifest.json").write_bytes((directory / "manifest.json").read_bytes())
    (tmp_path / "pipeline.joblib").write_bytes(b"corrupt")

    def forbidden(*args):
        pytest.fail("A corrupt artifact must not reach joblib.load")

    monkeypatch.setattr("steel_faults.inference.joblib.load", forbidden)
    with pytest.raises(ValueError, match="checksum"):
        Predictor(tmp_path)


def test_version_mismatch_rejected(trained, tmp_path):
    directory, report = trained
    metadata = json.loads(json.dumps(report))
    metadata["environment"]["sklearn"] = "incompatible"
    (tmp_path / "manifest.json").write_text(json.dumps(metadata))
    with pytest.raises(ValueError, match="scikit-learn"):
        Predictor(tmp_path)

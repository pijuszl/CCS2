"""Smoke: metrics + McNemar + bootstrap on a tiny toy case."""
from pathlib import Path

import pandas as pd
import pytest

from src.evaluation.metrics import compute_metrics
from src.evaluation.significance import bootstrap_macro_f1, mcnemar_two_runs


def test_compute_metrics_perfect():
    classes = ["non", "open", "hidden"]
    yt = ["non", "open", "hidden", "non"]
    yp = list(yt)
    m = compute_metrics(yt, yp, classes)
    assert m["macro_f1"] == 1.0
    assert m["micro_f1"] == 1.0


def test_compute_metrics_random():
    classes = ["non", "open", "hidden"]
    yt = ["non", "open", "hidden"]
    yp = ["hidden", "non", "open"]
    m = compute_metrics(yt, yp, classes)
    assert m["macro_f1"] == 0.0


def test_bootstrap_and_mcnemar(tmp_path: Path):
    classes = ["non", "open", "hidden"]
    yt = ["non"] * 30 + ["open"] * 30 + ["hidden"] * 30
    yp_a = yt[:]                              # A: perfect
    yp_b = ["non"] * 90                       # B: always non
    run_a = tmp_path / "A"; run_a.mkdir()
    run_b = tmp_path / "B"; run_b.mkdir()
    pd.DataFrame({"id": [f"id{i}" for i in range(90)], "y_true": yt, "y_pred": yp_a}).to_parquet(run_a / "predictions.parquet")
    pd.DataFrame({"id": [f"id{i}" for i in range(90)], "y_true": yt, "y_pred": yp_b}).to_parquet(run_b / "predictions.parquet")

    bs = bootstrap_macro_f1(run_a, B=100, seed=0, classes=classes)
    assert bs["point_macro_f1"] == 1.0
    assert bs["ci95_lo"] <= bs["point_macro_f1"] <= bs["ci95_hi"]

    mc = mcnemar_two_runs(run_a, run_b)
    assert mc["table_2x2"]["a_right_b_wrong"] > 0
    assert 0.0 <= mc["pvalue"] <= 1.0

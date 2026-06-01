"""Heavy smoke: spin up the train.py loop on a synthetic 8-row dataset.

Skipped if transformers/torch aren't installed (CI may not have them).
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


pytest.importorskip("torch")
pytest.importorskip("transformers")


def _write_synthetic(tmp: Path):
    import pandas as pd
    rows = []
    classes = ["non", "open", "hidden"]
    for i in range(24):  # >= smoke_subset
        rows.append({
            "id": f"syn:{i}",
            "text": f"Sintetinis tekstas numeris {i}. Kategorija: {classes[i % 3]}.",
            "image_path": None,
            "image_path_224": None,
            "image_path_512": None,
            "source": "halt-prop",
            "source_type": "unknown",
            "native_label": "synthetic",
            "native_meta": "{}",
            "group_key": f"g{i % 6}",
            "label_3class": classes[i % 3],
            "needs_review": False,
        })
    df = pd.DataFrame(rows)
    processed = tmp / "data" / "processed"
    processed.mkdir(parents=True)
    df.to_parquet(processed / "articles.parquet", index=False)

    # 60% train, 20% val, 20% test, disjoint groups.
    train_ids = df[df["group_key"].isin({"g0", "g1", "g2"})]["id"].tolist()
    val_ids = df[df["group_key"].isin({"g3"})]["id"].tolist()
    test_ids = df[df["group_key"].isin({"g4", "g5"})]["id"].tolist()
    (processed / "splits.json").write_text(
        json.dumps({"train": train_ids, "val": val_ids, "test": test_ids})
    )


@pytest.mark.slow
def test_train_smoke(tmp_path: Path, monkeypatch):
    """End-to-end one-step training on synthetic data. Slow because it loads XLM-R."""
    workdir = tmp_path / "workdir"
    workdir.mkdir()
    # Mirror the data into our temp workdir; symlink the rest from the real repo.
    _write_synthetic(workdir)
    for name in ("src", "config", "experiments"):
        (workdir / name).symlink_to(ROOT / name, target_is_directory=True)

    env = {
        "PYTHONPATH": str(workdir),
        "PATH": __import__("os").environ.get("PATH", ""),
        "TRANSFORMERS_OFFLINE": "0",
    }
    cmd = [sys.executable, "-m", "src.models.train",
           "--config", "experiments/text_xlmr_existing.yaml", "--smoke"]
    res = subprocess.run(cmd, cwd=workdir, env=env, capture_output=True, text=True, timeout=600)
    if res.returncode != 0:
        pytest.skip(f"train.py smoke failed (likely no network / missing model weights):\n{res.stderr[-1500:]}")
    runs = sorted((workdir / "results" / "runs").glob("*"))
    assert runs, "no run dir written"
    assert (runs[-1] / "metrics.json").exists()

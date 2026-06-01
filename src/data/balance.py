"""Compute class weights and focal-loss alpha from the TRAIN split only.

No SMOTE on raw text/images (per CLAUDE.md).
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

from src.utils import ensure_dir, get_logger, read_yaml

log = get_logger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = PROJECT_ROOT / "config" / "config.yaml"


def class_weights(labels: list[str], classes: list[str]) -> dict[str, float]:
    counts = Counter(labels)
    n = sum(counts.get(c, 0) for c in classes)
    k = len(classes)
    weights = {}
    for c in classes:
        weights[c] = (n / (k * max(counts.get(c, 0), 1))) if n > 0 else 1.0
    return weights


def focal_alpha(labels: list[str], classes: list[str]) -> dict[str, float]:
    counts = Counter(labels)
    n = sum(counts.get(c, 0) for c in classes)
    if n == 0:
        return {c: 1.0 / len(classes) for c in classes}
    inv = {c: 1.0 / max(counts.get(c, 0), 1) for c in classes}
    s = sum(inv.values())
    return {c: inv[c] / s for c in classes}


def _binary_balance(interim_dir: Path) -> dict | None:
    """Compute class weights for the binary aux head from image_weak_labels.parquet."""
    wl_path = interim_dir / "image_weak_labels.parquet"
    if not wl_path.exists():
        return None
    wl = pd.read_parquet(wl_path)
    classes = ["non", "propaganda"]
    labels = wl["weak_label"].dropna().tolist()
    if not labels:
        return None
    cw = class_weights(labels, classes)
    fa = focal_alpha(labels, classes)
    return {
        "classes": classes,
        "counts": {c: int(Counter(labels).get(c, 0)) for c in classes},
        "class_weight": cw,
        "focal_alpha": fa,
        "imbalance_ratio": round(
            max(Counter(labels).values()) / max(min(Counter(labels).values()), 1), 2
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    args = parser.parse_args()
    cfg = read_yaml(args.config)
    processed_dir = PROJECT_ROOT / cfg["paths"]["processed_dir"]
    interim_dir = PROJECT_ROOT / cfg["paths"]["interim_dir"]

    articles_path = processed_dir / "articles.parquet"
    splits_path = processed_dir / "splits.json"
    if not articles_path.exists() or not splits_path.exists():
        raise SystemExit("articles.parquet and splits.json must exist (run preprocess + split first).")

    df = pd.read_parquet(articles_path)
    splits = json.loads(splits_path.read_text(encoding="utf-8"))
    train_ids = set(splits["train"])
    train_labels = df[df["id"].isin(train_ids)]["label_3class"].dropna().tolist()

    classes = cfg["classes"]
    cw = class_weights(train_labels, classes)
    fa = focal_alpha(train_labels, classes)

    out = {
        "classes": classes,
        "train_counts": {c: int(Counter(train_labels).get(c, 0)) for c in classes},
        "class_weight": cw,
        "focal_alpha": fa,
    }
    out_path = ensure_dir(processed_dir) / "balance.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("wrote %s\n%s", out_path, json.dumps(out, indent=2, ensure_ascii=False))

    # Binary aux balance (vision_aux_pretrain.yaml uses this).
    binary = _binary_balance(interim_dir)
    if binary is not None:
        out_path = processed_dir / "balance_binary.json"
        out_path.write_text(json.dumps(binary, ensure_ascii=False, indent=2), encoding="utf-8")
        log.info("wrote %s\n%s", out_path, json.dumps(binary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

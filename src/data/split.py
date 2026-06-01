"""Group-aware stratified split.

Inputs:
  data/processed/articles.parquet  (or data/interim/articles_3class.parquet as fallback)

Strategy:
  - Drop rows with label_3class is NaN.
  - Use StratifiedGroupKFold to allocate test (1 / round(1/test_size) folds),
    then split the remainder into train/val using a second StratifiedGroupKFold
    on the residual groups. Guarantees zero group overlap across splits.
  - Splits frozen at JSON: {"train": [ids], "val": [ids], "test": [ids]}.

Group key = combination of `source` and `group_key` column. For LITUND this prevents
same-topic-prefix leakage; for HALT-PROP each id is its own group (no leakage
problem since articles are independent); for scraped articles the source acts as
the group (conservative).
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold

from src.utils import ensure_dir, get_logger, read_yaml, set_seed

log = get_logger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = PROJECT_ROOT / "config" / "config.yaml"


def _make_groups(df: pd.DataFrame) -> np.ndarray:
    return (df["source"].astype(str) + "::" + df["group_key"].astype(str)).to_numpy()


def _stratified_group_split(df: pd.DataFrame, frac: float, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """Hold out `frac` of the data, group-aware, stratified by label_3class."""
    n_splits = max(2, int(round(1.0 / max(frac, 1e-6))))
    sgkf = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    y = df["label_3class"].to_numpy()
    g = _make_groups(df)
    train_idx, test_idx = next(sgkf.split(df, y=y, groups=g))
    return train_idx, test_idx


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--input", default=None,
                        help="Path to parquet with id, source, group_key, label_3class. "
                             "Defaults to data/processed/articles.parquet then data/interim/articles_3class.parquet.")
    args = parser.parse_args()

    cfg = read_yaml(args.config)
    set_seed(cfg.get("seed", 42))

    processed_dir = PROJECT_ROOT / cfg["paths"]["processed_dir"]
    interim_dir = PROJECT_ROOT / cfg["paths"]["interim_dir"]
    candidates = [args.input] if args.input else [
        processed_dir / "articles.parquet",
        interim_dir / "articles_3class.parquet",
    ]
    src = next((Path(p) for p in candidates if p and Path(p).exists()), None)
    if src is None:
        raise SystemExit("No input parquet found. Run load_existing + map_labels first.")
    log.info("using %s", src)
    df = pd.read_parquet(src)

    before = len(df)
    df = df[df["label_3class"].notna()].reset_index(drop=True)
    log.info("dropped %d rows with no label_3class (%d remain)", before - len(df), len(df))
    if len(df) == 0:
        raise SystemExit("No labelled rows after filtering.")

    test_size = float(cfg["split"]["test_size"])
    val_size = float(cfg["split"]["val_size"])
    seed = int(cfg["seed"])

    rest_idx, test_idx = _stratified_group_split(df, test_size, seed)
    rest = df.iloc[rest_idx].reset_index(drop=True)
    # Re-split the remainder into train/val.
    val_frac_of_rest = val_size / max(1.0 - test_size, 1e-6)
    train_idx, val_idx = _stratified_group_split(rest, val_frac_of_rest, seed + 1)
    train = rest.iloc[train_idx]
    val = rest.iloc[val_idx]
    test = df.iloc[test_idx]

    # Sanity: zero group overlap.
    g_train = set(_make_groups(train))
    g_val = set(_make_groups(val))
    g_test = set(_make_groups(test))
    assert not (g_train & g_val), "train/val groups overlap!"
    assert not (g_train & g_test), "train/test groups overlap!"
    assert not (g_val & g_test), "val/test groups overlap!"

    splits = {
        "train": train["id"].tolist(),
        "val": val["id"].tolist(),
        "test": test["id"].tolist(),
    }
    out_dir = ensure_dir(processed_dir)
    out_path = out_dir / "splits.json"
    out_path.write_text(json.dumps(splits, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("wrote %s", out_path)
    for name in ("train", "val", "test"):
        ids = splits[name]
        sub = df[df["id"].isin(ids)]
        dist = Counter(sub["label_3class"])
        log.info("  %5s: n=%d  dist=%s", name, len(ids), dict(dist))


if __name__ == "__main__":
    main()

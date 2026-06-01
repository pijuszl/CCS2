"""Statistical significance for the H1 / H2 claims.

  - McNemar's paired test between two classifiers on the same test set
  - Bootstrap CIs (B=1000) on macro-F1 for a single run
  - χ² feature-vs-class association on the feature table

CLI:
  python -m src.evaluation.significance mcnemar --a runA --b runB
  python -m src.evaluation.significance bootstrap --run results/runs/<id> [--B 1000]
  python -m src.evaluation.significance chi2 --feature-table data/processed/feature_table.parquet
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.utils import ensure_dir, get_logger

log = get_logger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]


# ----------------------------------------------------------------- McNemar


def mcnemar_two_runs(run_a: Path, run_b: Path) -> dict:
    from statsmodels.stats.contingency_tables import mcnemar
    a = pd.read_parquet(run_a / "predictions.parquet")
    b = pd.read_parquet(run_b / "predictions.parquet")
    merged = a.merge(b, on=["id"], suffixes=("_a", "_b"))
    if "y_true_a" in merged.columns:
        assert (merged["y_true_a"] == merged["y_true_b"]).all(), "y_true differs across runs"
        y_true = merged["y_true_a"]
    else:
        y_true = merged["y_true"]
    correct_a = (merged["y_pred_a"] == y_true).to_numpy()
    correct_b = (merged["y_pred_b"] == y_true).to_numpy()
    n10 = int(((correct_a) & (~correct_b)).sum())  # a right, b wrong
    n01 = int(((~correct_a) & (correct_b)).sum())  # a wrong, b right
    table = [[int((correct_a & correct_b).sum()), n10],
             [n01, int(((~correct_a) & (~correct_b)).sum())]]
    res = mcnemar(table, exact=(n10 + n01) < 25)
    return {
        "n_paired": int(len(merged)),
        "table_2x2": {"both_right": table[0][0], "a_right_b_wrong": n10,
                      "b_right_a_wrong": n01, "both_wrong": table[1][1]},
        "statistic": float(res.statistic),
        "pvalue": float(res.pvalue),
    }


# ----------------------------------------------------------------- bootstrap CI


def bootstrap_macro_f1(run_dir: Path, B: int = 1000, seed: int = 42, classes=None) -> dict:
    from sklearn.metrics import f1_score
    df = pd.read_parquet(run_dir / "predictions.parquet")
    y_true = df["y_true"].to_numpy()
    y_pred = df["y_pred"].to_numpy()
    rng = np.random.default_rng(seed)
    n = len(df)
    scores = np.empty(B, dtype=float)
    classes = classes or sorted(set(y_true) | set(y_pred))
    for b in range(B):
        idx = rng.integers(0, n, size=n)
        scores[b] = f1_score(y_true[idx], y_pred[idx], labels=classes,
                              average="macro", zero_division=0)
    point = float(f1_score(y_true, y_pred, labels=classes, average="macro", zero_division=0))
    lo, hi = float(np.percentile(scores, 2.5)), float(np.percentile(scores, 97.5))
    return {"point_macro_f1": point, "ci95_lo": lo, "ci95_hi": hi,
            "B": B, "n": int(n), "classes": classes}


# ----------------------------------------------------------------- chi-square on features


def chi2_features(feature_table: Path, label_col: str = "label_3class",
                  exclude_cols=("id", "source", "source_type")) -> dict:
    from scipy import stats
    df = pd.read_parquet(feature_table)
    df = df[df[label_col].notna()].reset_index(drop=True)
    results = {}
    classes = sorted(df[label_col].unique())
    for col in df.columns:
        if col in exclude_cols or col == label_col:
            continue
        if not pd.api.types.is_numeric_dtype(df[col]):
            continue
        # Bin continuous features into terciles; counts NaN as its own bucket.
        try:
            x = df[col].fillna(df[col].median())
            bins = pd.qcut(x, q=3, duplicates="drop")
        except Exception:
            continue
        ct = pd.crosstab(bins, df[label_col])
        if ct.shape[0] < 2 or ct.shape[1] < 2:
            continue
        chi2, p, dof, _ = stats.chi2_contingency(ct.values)
        results[col] = {"chi2": float(chi2), "pvalue": float(p), "dof": int(dof)}
    # Holm correction.
    pairs = sorted(results.items(), key=lambda kv: kv[1]["pvalue"])
    m = len(pairs)
    for rank, (col, r) in enumerate(pairs, 1):
        r["p_holm"] = min(1.0, r["pvalue"] * (m - rank + 1))
    return {"classes": classes, "features": results}


# ----------------------------------------------------------------- CLI


def main() -> None:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    p_m = sub.add_parser("mcnemar")
    p_m.add_argument("--a", required=True)
    p_m.add_argument("--b", required=True)
    p_m.add_argument("--out", default=None)

    p_b = sub.add_parser("bootstrap")
    p_b.add_argument("--run", required=True)
    p_b.add_argument("--B", type=int, default=1000)
    p_b.add_argument("--seed", type=int, default=42)
    p_b.add_argument("--out", default=None)

    p_c = sub.add_parser("chi2")
    p_c.add_argument("--feature-table", required=True)
    p_c.add_argument("--out", default=None)

    args = p.parse_args()

    def _abs(x: str) -> Path:
        return Path(x) if Path(x).is_absolute() else PROJECT_ROOT / x

    if args.cmd == "mcnemar":
        out = mcnemar_two_runs(_abs(args.a), _abs(args.b))
        log.info("%s", json.dumps(out, indent=2))
        if args.out:
            ensure_dir(Path(args.out).parent)
            Path(args.out).write_text(json.dumps(out, indent=2), encoding="utf-8")
    elif args.cmd == "bootstrap":
        out = bootstrap_macro_f1(_abs(args.run), B=args.B, seed=args.seed)
        log.info("%s", json.dumps(out, indent=2))
        if args.out:
            ensure_dir(Path(args.out).parent)
            Path(args.out).write_text(json.dumps(out, indent=2), encoding="utf-8")
    elif args.cmd == "chi2":
        out = chi2_features(_abs(args.feature_table))
        log.info("%s", json.dumps({"top": dict(sorted(out["features"].items(),
                                                       key=lambda kv: kv[1]["pvalue"])[:10])},
                                  indent=2))
        out_path = Path(args.out) if args.out else PROJECT_ROOT / "results" / "tables" / "chi2_features.json"
        ensure_dir(out_path.parent)
        out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
        log.info("wrote %s", out_path)


if __name__ == "__main__":
    main()

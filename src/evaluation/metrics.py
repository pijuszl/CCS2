"""Macro-F1 (headline), micro-F1, per-class P/R/F1, confusion matrix.

  python -m src.evaluation.metrics --run-dir results/runs/<id>

Reads predictions.parquet from the run dir, writes:
  - metrics.json (overwrites existing test metrics with full breakdown)
  - figures/confusion_matrix.png
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


def compute_metrics(y_true: list[str], y_pred: list[str], classes: list[str]) -> dict:
    from sklearn.metrics import (confusion_matrix, f1_score,
                                 precision_recall_fscore_support)
    macro_f1 = float(f1_score(y_true, y_pred, labels=classes, average="macro", zero_division=0))
    micro_f1 = float(f1_score(y_true, y_pred, labels=classes, average="micro", zero_division=0))
    P, R, F, S = precision_recall_fscore_support(y_true, y_pred, labels=classes, zero_division=0)
    per_class = {c: {"precision": float(P[i]), "recall": float(R[i]),
                     "f1": float(F[i]), "support": int(S[i])}
                 for i, c in enumerate(classes)}
    cm = confusion_matrix(y_true, y_pred, labels=classes).tolist()
    return {
        "macro_f1": macro_f1,
        "micro_f1": micro_f1,
        "per_class": per_class,
        "confusion_matrix": {"labels": classes, "matrix": cm},
        "n": len(y_true),
    }


def plot_confusion(cm: list[list[int]], labels: list[str], out_path: Path) -> None:
    import matplotlib.pyplot as plt
    arr = np.array(cm)
    fig, ax = plt.subplots(figsize=(4.5, 4.0))
    im = ax.imshow(arr, cmap="Blues")
    ax.set_xticks(range(len(labels))); ax.set_xticklabels(labels)
    ax.set_yticks(range(len(labels))); ax.set_yticklabels(labels)
    ax.set_xlabel("predicted"); ax.set_ylabel("true")
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            ax.text(j, i, str(arr[i, j]), ha="center", va="center",
                    color="white" if arr[i, j] > arr.max() / 2 else "black", fontsize=10)
    plt.colorbar(im)
    fig.tight_layout()
    ensure_dir(out_path.parent)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--run-dir", required=True)
    p.add_argument("--classes", nargs="+", default=["non", "open", "hidden"])
    args = p.parse_args()
    run_dir = Path(args.run_dir)
    if not run_dir.is_absolute():
        run_dir = PROJECT_ROOT / run_dir
    preds_path = run_dir / "predictions.parquet"
    if not preds_path.exists():
        raise SystemExit(f"missing {preds_path}")
    df = pd.read_parquet(preds_path)
    metrics = compute_metrics(df["y_true"].tolist(), df["y_pred"].tolist(), args.classes)
    log.info("metrics: %s", json.dumps({k: v for k, v in metrics.items() if k != "confusion_matrix"}, indent=2))
    (run_dir / "metrics_detail.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    plot_confusion(metrics["confusion_matrix"]["matrix"], args.classes,
                   run_dir / "figures" / "confusion_matrix.png")
    log.info("wrote %s and %s/figures/confusion_matrix.png", run_dir / "metrics_detail.json", run_dir)


if __name__ == "__main__":
    main()

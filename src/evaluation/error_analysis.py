"""Sample misclassifications and tag open↔hidden confusions for qualitative review.

  python -m src.evaluation.error_analysis --run results/runs/<id> --n 50
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.utils import ensure_dir, get_logger

log = get_logger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--run", required=True)
    p.add_argument("--n", type=int, default=50)
    p.add_argument("--articles", default=None,
                   help="parquet with id+text+source; defaults to data/processed/articles.parquet")
    args = p.parse_args()
    run_dir = Path(args.run) if Path(args.run).is_absolute() else PROJECT_ROOT / args.run
    preds = pd.read_parquet(run_dir / "predictions.parquet")
    articles_path = Path(args.articles) if args.articles else PROJECT_ROOT / "data" / "processed" / "articles.parquet"
    if articles_path.exists():
        arts = pd.read_parquet(articles_path)[["id", "text", "source"]]
        preds = preds.merge(arts, on="id", how="left")

    errors = preds[preds["y_true"] != preds["y_pred"]].copy()
    errors["pair"] = errors["y_true"] + "->" + errors["y_pred"]
    summary = errors["pair"].value_counts().to_dict()
    log.info("error pairs: %s", summary)

    sample = errors.sample(min(args.n, len(errors)), random_state=42)
    out_path = PROJECT_ROOT / "results" / "tables" / "errors_sample.csv"
    ensure_dir(out_path.parent)
    sample.to_csv(out_path, index=False)
    log.info("wrote %s (%d rows)", out_path, len(sample))


if __name__ == "__main__":
    main()

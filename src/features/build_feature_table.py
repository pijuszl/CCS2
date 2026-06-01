"""Join text + visual features into a single feature table for H2.

Output: data/processed/feature_table.parquet
        columns: id, label_3class, source, source_type, <textual features>, <visual features>
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.utils import ensure_dir, get_logger, read_yaml

log = get_logger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = PROJECT_ROOT / "config" / "config.yaml"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--config", default=str(DEFAULT_CONFIG))
    p.add_argument("--text-only", action="store_true",
                   help="Skip visual features (useful before scraping is done).")
    args = p.parse_args()
    cfg = read_yaml(args.config)
    processed = PROJECT_ROOT / cfg["paths"]["processed_dir"]

    articles = pd.read_parquet(processed / "articles.parquet")
    base = articles[["id", "source", "source_type", "label_3class"]].copy()

    # Build text features on the fly (cheap).
    from src.features.text_features import extract_text_features
    fcfg = read_yaml(PROJECT_ROOT / "config" / "features.yaml")
    text_rows = [extract_text_features(r, fcfg) for _, r in articles.iterrows()]
    text_feats = pd.DataFrame(text_rows)
    table = base.merge(text_feats, on="id", how="left")

    if not args.text_only:
        vis_path = processed / "visual_features.parquet"
        if vis_path.exists():
            vis_feats = pd.read_parquet(vis_path)
            table = table.merge(vis_feats, on="id", how="left")
        else:
            log.warning("visual_features.parquet not found; run src.features.visual_features first "
                        "(or pass --text-only).")

    out = processed / "feature_table.parquet"
    ensure_dir(out.parent)
    table.to_parquet(out, index=False)
    log.info("wrote %s (%d rows, %d cols)", out, len(table), table.shape[1])


if __name__ == "__main__":
    main()

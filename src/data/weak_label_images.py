"""Assign binary weak labels to scraped images by source_type.

  source_type == "propaganda" -> image label "propaganda"
  source_type == "neutral"    -> image label "non"

Also:
  - perceptual hash (phash) for dedup;
  - logo/aspect-ratio heuristic flag for downstream stripping;
  - emit data/interim/image_weak_labels.parquet.

Treat these labels as NOISY supervision (CLAUDE.md): a propaganda outlet can run
a neutral stock photo and vice-versa. Evaluation never uses weak labels.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.utils import ensure_dir, get_logger, read_jsonl, read_yaml

log = get_logger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = PROJECT_ROOT / "config" / "config.yaml"


def _phash(path: Path) -> str | None:
    try:
        from PIL import Image
        import imagehash
        with Image.open(path) as im:
            return str(imagehash.phash(im))
    except Exception as e:
        log.warning("phash failed (%s): %s", path, e)
        return None


def _likely_logo(path: Path) -> bool:
    """Heuristic: tiny images or extreme aspect ratios are probably site logos / nav icons."""
    try:
        from PIL import Image
        with Image.open(path) as im:
            w, h = im.size
            if w < 100 or h < 100:
                return True
            ar = w / max(h, 1)
            if ar > 5 or ar < 0.2:
                return True
        return False
    except Exception:
        return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    args = parser.parse_args()

    cfg = read_yaml(args.config)
    raw_dir = PROJECT_ROOT / cfg["paths"]["raw_dir"]
    interim_dir = ensure_dir(PROJECT_ROOT / cfg["paths"]["interim_dir"])
    scraped_path = raw_dir / "scraped.jsonl"

    if not scraped_path.exists():
        log.warning("no %s yet (scraper hasn't been run); writing empty parquet", scraped_path)
        pd.DataFrame(columns=["id", "image_path", "source", "source_type",
                               "weak_label", "phash", "likely_logo"]).to_parquet(
            interim_dir / "image_weak_labels.parquet", index=False
        )
        return

    rows = []

    def _emit(r: dict, default_source: str | None = None) -> None:
        img_rel = r.get("image_path")
        if not img_rel:
            return
        img_path = PROJECT_ROOT / img_rel
        if not img_path.exists():
            return
        weak = "propaganda" if r.get("source_type") == "propaganda" else "non"
        rows.append({
            "id": r["id"],
            "image_path": img_rel,
            "source": r.get("source") or default_source,
            "source_type": r.get("source_type"),
            "weak_label": weak,
            "phash": _phash(img_path),
            "likely_logo": _likely_logo(img_path),
        })

    for r in read_jsonl(scraped_path):
        _emit(r)

    # Also include LITUND article images scraped from their native URLs. LITUND's
    # LRT subset gives us real `non` images (finally both classes for the aux head).
    litund_path = raw_dir / "litund_images.jsonl"
    if litund_path.exists():
        n_before = len(rows)
        for r in read_jsonl(litund_path):
            _emit(r, default_source="litund")
        log.info("added %d LITUND images to weak-label parquet", len(rows) - n_before)

    df = pd.DataFrame(rows)
    # Dedup by phash; keep first.
    if not df.empty:
        before = len(df)
        df = df.drop_duplicates(subset=["phash"], keep="first")
        log.info("phash dedup: %d -> %d", before, len(df))
    out = interim_dir / "image_weak_labels.parquet"
    df.to_parquet(out, index=False)
    log.info("wrote %s (%d rows; %d flagged as likely_logo)",
             out, len(df), int(df.get("likely_logo", pd.Series([], dtype=bool)).sum()))


if __name__ == "__main__":
    main()

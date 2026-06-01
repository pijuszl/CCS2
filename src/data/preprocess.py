"""Unify, clean, and resize.

Inputs:
  data/interim/articles_3class.parquet              (from map_labels.py)
  data/raw/scraped.jsonl + data/interim/image_weak_labels.parquet (optional)

Outputs:
  data/processed/articles.parquet                   (one row per item)
  data/processed/images/{224,512}/<basename>        (resized copies, when image_path is present)

Preserves Lithuanian diacritics. Strips obvious whitespace artefacts only.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd

from src.utils import ensure_dir, get_logger, read_jsonl, read_yaml

log = get_logger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = PROJECT_ROOT / "config" / "config.yaml"


_WS = re.compile(r"[ \t]+")
_NL = re.compile(r"\n{3,}")


def _clean(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.replace("\r", "")
    text = _WS.sub(" ", text)
    text = _NL.sub("\n\n", text)
    return text.strip()


def _resize_one(src: Path, dst: Path, size: int) -> bool:
    try:
        from PIL import Image
        with Image.open(src) as im:
            im = im.convert("RGB")
            im.thumbnail((size, size), Image.LANCZOS)
            ensure_dir(dst.parent)
            im.save(dst, quality=90)
        return True
    except Exception as e:
        log.warning("resize failed (%s): %s", src, e)
        return False


def _load_scraped_as_df(raw_dir: Path) -> pd.DataFrame:
    path = raw_dir / "scraped.jsonl"
    if not path.exists():
        return pd.DataFrame()
    rows = list(read_jsonl(path))
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    # Bring into the common schema; label is unknown until the agent labels it.
    df_out = pd.DataFrame({
        "id": df["id"],
        "text": (df.get("title", "").fillna("") + "\n\n" + df.get("text", "").fillna("")).str.strip(),
        "image_path": df.get("image_path"),
        "source": df.get("source"),
        "source_type": df.get("source_type"),
        "native_label": None,
        "native_meta": [{"url": u} for u in df.get("url", [""] * len(df))],
        # Per-article group key: each scraped article is its own event so we
        # don't want all rubaltic_lt articles in the same split.
        "group_key": df["id"].astype(str),
        "label_3class": None,
        "needs_review": True,
    })
    return df_out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--include-scraped", action="store_true",
                        help="Also include scraped items (label=None until annotated).")
    parser.add_argument("--no-resize", action="store_true")
    args = parser.parse_args()

    cfg = read_yaml(args.config)
    interim_dir = PROJECT_ROOT / cfg["paths"]["interim_dir"]
    raw_dir = PROJECT_ROOT / cfg["paths"]["raw_dir"]
    processed_dir = ensure_dir(PROJECT_ROOT / cfg["paths"]["processed_dir"])

    src_path = interim_dir / "articles_3class.parquet"
    if not src_path.exists():
        raise SystemExit(f"missing {src_path}; run map_labels first")
    df = pd.read_parquet(src_path)

    if args.include_scraped:
        scraped = _load_scraped_as_df(raw_dir)
        if not scraped.empty:
            # Optionally bring in LLM labels if they exist.
            llm_path = PROJECT_ROOT / cfg["paths"]["annotations_dir"] / "llm_labels.jsonl"
            if llm_path.exists():
                llm = pd.DataFrame(list(read_jsonl(llm_path)))
                if not llm.empty:
                    llm = llm[["id", "label", "confidence"]].rename(
                        columns={"label": "label_3class"}
                    )
                    scraped = scraped.drop(columns=["label_3class"]).merge(llm, on="id", how="left")
                    scraped["needs_review"] = scraped["label_3class"].isna()
            df = pd.concat([df, scraped], ignore_index=True)

    df["text"] = df["text"].astype(str).map(_clean)
    # Drop empty texts.
    before = len(df)
    df = df[df["text"].str.len() > 0].reset_index(drop=True)
    log.info("dropped %d empty-text rows", before - len(df))

    # Attach LITUND article images scraped from their native URLs. Labels for
    # these come straight from the LITUND mapping (LRT -> non, Unreliable -> hidden),
    # so no LLM labelling is involved.
    litund_imgs_path = raw_dir / "litund_images.jsonl"
    if litund_imgs_path.exists():
        litund_imgs = list(read_jsonl(litund_imgs_path))
        if litund_imgs:
            img_map = {r["id"]: r["image_path"] for r in litund_imgs if r.get("image_path")}
            mask = df["id"].isin(img_map)
            df.loc[mask, "image_path"] = df.loc[mask, "id"].map(img_map)
            log.info("attached %d LITUND images to articles parquet", int(mask.sum()))

    # Normalise native_meta to JSON strings (some loaders emit dicts, others strings).
    import json as _json
    def _to_jstr(v):
        if isinstance(v, str):
            return v
        if v is None:
            return "{}"
        try:
            return _json.dumps(v, ensure_ascii=False, default=str)
        except Exception:
            return "{}"
    df["native_meta"] = df["native_meta"].map(_to_jstr)

    # Resize images present on disk (only scraped items have any).
    if not args.no_resize:
        size_small = int(cfg["image"]["size"])
        size_large = int(cfg["image"]["size_large"])
        small_dir = ensure_dir(processed_dir / "images" / str(size_small))
        large_dir = ensure_dir(processed_dir / "images" / str(size_large))
        resized_small: list[str | None] = []
        resized_large: list[str | None] = []
        for img in df["image_path"]:
            if not img:
                resized_small.append(None)
                resized_large.append(None)
                continue
            src = PROJECT_ROOT / img
            if not src.exists():
                resized_small.append(None)
                resized_large.append(None)
                continue
            base = Path(img).name
            d_s = small_dir / base
            d_l = large_dir / base
            ok_s = _resize_one(src, d_s, size_small) if not d_s.exists() else True
            ok_l = _resize_one(src, d_l, size_large) if not d_l.exists() else True
            resized_small.append(str(d_s.relative_to(PROJECT_ROOT)).replace("\\", "/") if ok_s else None)
            resized_large.append(str(d_l.relative_to(PROJECT_ROOT)).replace("\\", "/") if ok_l else None)
        df["image_path_224"] = resized_small
        df["image_path_512"] = resized_large

    out_path = processed_dir / "articles.parquet"
    df.to_parquet(out_path, index=False)
    log.info("wrote %s (%d rows)", out_path, len(df))


if __name__ == "__main__":
    main()

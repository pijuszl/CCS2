"""Map native corpus labels into the unified {non, open, hidden} taxonomy.

Strategy (documented in CLAUDE.md §"Label mapping" and config/halt_prop_technique_mapping.yaml):

  HALT-PROP
    is_propaganda == "no"                        -> non
    is_propaganda == "yes" with any OVERT tag    -> open
    is_propaganda == "yes" with only SUBTLE tags -> hidden
    is_propaganda == "yes" with unknown/no tags  -> hidden (conservative)
    is_propaganda in {Unclear, nonDeterminable, propagandaCitation}
                                                 -> dropped from 3-class gold (kept with NaN)

  DIGIRES
    Label 0 (reliable)   -> non
    Label 1 (unreliable) -> hidden  (covert by topic; documented as method choice)

  LITUND
    LRT subset           -> non
    Unreliable subset    -> hidden  (techniques unknown; needs_review=True flag)
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pandas as pd

from src.utils import ensure_dir, get_logger, read_yaml

log = get_logger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = PROJECT_ROOT / "config" / "config.yaml"
DEFAULT_MAPPING = PROJECT_ROOT / "config" / "halt_prop_technique_mapping.yaml"


def _norm_tech(tag: str) -> str:
    return re.sub(r"[\s_-]", "", tag).lower()


def _extract_halt_prop_techniques(meta_json: str) -> list[str]:
    """The HALT-PROP techniques column is a JSON-ish array of objects with technique
    abbreviations. We try the lenient parse and fall back to a regex extraction.
    """
    if not meta_json or meta_json == "{}":
        return []
    try:
        meta = json.loads(meta_json) if isinstance(meta_json, str) else (meta_json or {})
    except Exception:
        return []
    techs_field = meta.get("techniques")
    if not techs_field or (isinstance(techs_field, float) and pd.isna(techs_field)):
        return []
    if isinstance(techs_field, list):
        items = techs_field
    elif isinstance(techs_field, str):
        try:
            items = json.loads(techs_field)
        except Exception:
            # Last-ditch: pull bare abbreviations.
            items = re.findall(r"[A-Za-z_]+", techs_field)
            return [t for t in items if t]
    else:
        return []

    out = []
    for it in items:
        if isinstance(it, dict):
            for key in ("technique", "label", "abbr", "abbreviation", "type"):
                if key in it and it[key]:
                    out.append(str(it[key]))
                    break
        elif isinstance(it, str):
            out.append(it)
    return out


def _map_halt_prop(row: pd.Series, mapping: dict) -> tuple[str | None, bool]:
    is_prop = (row.get("native_label") or "").strip()
    ambiguous = set(mapping.get("ambiguous_is_propaganda_values", []))
    if is_prop in ambiguous:
        return None, False  # drop
    if is_prop.lower() == "no":
        return "non", False

    techs = _extract_halt_prop_techniques(row.get("native_meta", ""))
    overt = {_norm_tech(t) for t in mapping.get("overt", [])}
    subtle = {_norm_tech(t) for t in mapping.get("subtle", [])}

    norm_techs = {_norm_tech(t) for t in techs}
    has_overt = bool(norm_techs & overt)
    has_subtle = bool(norm_techs & subtle)

    if has_overt:
        return "open", False
    if has_subtle:
        return "hidden", False
    # is_propaganda=yes but no recognised techniques (common for the 1,870 articles
    # outside the Annotations.csv subset).
    return "hidden", True  # needs_review flag


def _map_digires(row: pd.Series) -> tuple[str, bool]:
    nl = (row.get("native_label") or "").strip().lower()
    if nl == "reliable":
        return "non", False
    return "hidden", False


def _map_litund(row: pd.Series) -> tuple[str, bool]:
    nl = (row.get("native_label") or "").strip().lower()
    if nl == "lrt":
        return "non", False
    return "hidden", True


def map_corpus(df: pd.DataFrame, source: str, mapping: dict) -> pd.DataFrame:
    df = df.copy()
    labels: list[str | None] = []
    needs_review: list[bool] = []
    for _, row in df.iterrows():
        if source == "halt-prop":
            lab, nr = _map_halt_prop(row, mapping)
        elif source == "digires":
            lab, nr = _map_digires(row)
        elif source == "litund":
            lab, nr = _map_litund(row)
        else:
            lab, nr = None, True
        labels.append(lab)
        needs_review.append(nr)
    df["label_3class"] = labels
    df["needs_review"] = needs_review
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description="Map native labels to {non, open, hidden}.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--mapping", default=str(DEFAULT_MAPPING))
    args = parser.parse_args()

    cfg = read_yaml(args.config)
    mapping = read_yaml(args.mapping) or {}
    interim_dir = PROJECT_ROOT / cfg["paths"]["interim_dir"]
    ensure_dir(interim_dir)

    parts = []
    for source in ("halt-prop", "digires", "litund"):
        path = interim_dir / f"{source}.parquet"
        if not path.exists():
            log.warning("missing %s, skipping (run load_existing first)", path)
            continue
        df = pd.read_parquet(path)
        log.info("mapping %s (%d rows) ...", source, len(df))
        df = map_corpus(df, source, mapping)
        parts.append(df)

    if not parts:
        raise SystemExit("No interim parquet files found; run `python -m src.data.load_existing --all` first.")

    unified = pd.concat(parts, ignore_index=True)
    n_total = len(unified)
    n_kept = unified["label_3class"].notna().sum()
    dist = unified["label_3class"].value_counts(dropna=False).to_dict()
    log.info("Unified: %d rows; kept-with-3class=%d; dist=%s", n_total, n_kept, dist)

    out_path = interim_dir / "articles_3class.parquet"
    unified.to_parquet(out_path, index=False)
    log.info("  -> %s", out_path)


if __name__ == "__main__":
    main()

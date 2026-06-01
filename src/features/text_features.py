"""High-level textual features for the interpretable model used in H2.

Cheap, dependency-light implementations. Each function returns a single feature
value or count, all wrapped by `extract_text_features` into a flat dict.

Lexica are tiny stubs that can be replaced by larger LT resources later.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

import pandas as pd

from src.utils import ensure_dir, get_logger, read_yaml

log = get_logger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = PROJECT_ROOT / "config" / "config.yaml"
DEFAULT_FEATURES = PROJECT_ROOT / "config" / "features.yaml"


# Tiny LT emotive/loaded lexicon stub. Expand with a real resource.
LT_EMOTIVE = {
    "melas", "melagis", "meluoja", "klastotė", "marionetė", "išdavikas",
    "agresyvus", "kruvinas", "šokas", "siaubas", "tragedija", "skandalas",
    "atskleidžia", "tiesa", "sąmokslas", "diktatas", "diktatorius", "okupantas",
    "fašistinis", "naciai", "barbariškas", "žvėriškas", "smerkia", "gėda",
    "išdavystė", "išdavikiškas", "klastingai",
}

# Tiny LT modal/uncertainty stub.
LT_MODALS = {
    "gali", "galbūt", "galimai", "tikriausiai", "panašu", "atrodo", "manoma",
    "tariamai", "neva", "esą", "galbūt", "abejotina", "neaišku", "tariama",
    "abejojama", "spėjama",
}

_WORD = re.compile(r"\b[\wŽžĄąČčĘęĖėĮįŠšŲųŪūŸÿ]+\b", flags=re.UNICODE)


def _tokens(text: str) -> list[str]:
    return [m.group(0).lower() for m in _WORD.finditer(text or "")]


def lexicon_match_rate(text: str, lex: Iterable[str]) -> float:
    toks = _tokens(text)
    if not toks:
        return 0.0
    lex = set(lex)
    hits = sum(1 for t in toks if t in lex)
    return hits / len(toks)


def regex_ner_count(text: str, targets: Iterable[str]) -> int:
    if not text:
        return 0
    n = 0
    for t in targets:
        n += len(re.findall(re.escape(t), text, flags=re.IGNORECASE))
    return n


def pronoun_ratio(text: str, in_group: Iterable[str], out_group: Iterable[str]) -> float:
    toks = _tokens(text)
    if not toks:
        return 0.0
    ig = sum(1 for t in toks if t in set(in_group))
    og = sum(1 for t in toks if t in set(out_group))
    total = ig + og
    if total == 0:
        return 0.0
    return (ig - og) / total  # +1 = all in-group, -1 = all out-group


def quote_source_balance(text: str) -> float:
    """Counts straight quotes + Lithuanian guillemets; returns 0 if none.
    Positive = many quotes (likely cited reporting); negative = none.
    Cheap proxy for source balance; real implementation would parse attributions.
    """
    if not text:
        return 0.0
    n_open = text.count("„") + text.count("«") + text.count("\"")
    return min(n_open / 5.0, 1.0)  # cap at 1.0


def headline_markers(headline: str, markers: Iterable[str]) -> float:
    if not headline:
        return 0.0
    h = headline.upper()
    hits = sum(1 for m in markers if m.upper() in h)
    return min(hits / len(list(markers) or [1]), 1.0)


def extract_text_features(row: pd.Series, features_cfg: dict) -> dict:
    text = str(row.get("text", "") or "")
    # First non-empty line as the headline proxy.
    first_line = text.split("\n", 1)[0]
    out: dict[str, float | int] = {"id": row["id"]}
    for feat in features_cfg.get("textual", []):
        name = feat["name"]
        method = feat.get("method")
        if method == "lexicon_match_rate":
            lex_id = feat.get("lexicon")
            lex = LT_EMOTIVE if lex_id == "lt_emotive_v1" else LT_MODALS if lex_id == "lt_modal_v1" else set()
            out[name] = lexicon_match_rate(text, lex)
        elif method == "regex_ner":
            out[name] = regex_ner_count(text, feat.get("targets", []))
        elif method == "pronoun_ratio":
            out[name] = pronoun_ratio(text, feat.get("in_group", []), feat.get("out_group", []))
        elif method == "quote_source_balance":
            out[name] = quote_source_balance(text)
        elif method == "headline_markers":
            out[name] = headline_markers(first_line, feat.get("markers", []))
        else:
            out[name] = 0.0
    return out


def main() -> None:
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--config", default=str(DEFAULT_CONFIG))
    p.add_argument("--features-yaml", default=str(DEFAULT_FEATURES))
    p.add_argument("--input", default=None)
    p.add_argument("--out", default=None)
    args = p.parse_args()

    cfg = read_yaml(args.config)
    fcfg = read_yaml(args.features_yaml)
    in_path = Path(args.input) if args.input else PROJECT_ROOT / cfg["paths"]["processed_dir"] / "articles.parquet"
    out_path = Path(args.out) if args.out else PROJECT_ROOT / cfg["paths"]["processed_dir"] / "text_features.parquet"
    df = pd.read_parquet(in_path)
    rows = [extract_text_features(r, fcfg) for _, r in df.iterrows()]
    feat_df = pd.DataFrame(rows)
    ensure_dir(out_path.parent)
    feat_df.to_parquet(out_path, index=False)
    log.info("wrote %s (%d rows)", out_path, len(feat_df))


if __name__ == "__main__":
    main()

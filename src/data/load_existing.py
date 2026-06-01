"""Load HALT-PROP, DIGIRES, LITUND into a common schema.

Common schema (one row per item):
    id            str   — globally unique
    text          str   — heading + "\n\n" + body when available
    image_path    str | None  — always None for existing corpora (text-only)
    source        str   — "halt-prop" | "digires" | "litund"
    source_type   str   — "propaganda" | "neutral" | "unknown"  (best-effort, native)
    native_label  str   — corpus-specific label preserved verbatim
    native_meta   dict  — extra fields (narratives, techniques, topic, url, ...)
    group_key     str   — for group-aware splits; corpus-specific

Outputs one parquet per corpus to data/interim/.
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

# ----------------------------------------------------------------------- HALT-PROP


def load_halt_prop(datasets_dir: Path) -> pd.DataFrame:
    """HALT-PROP: two semicolon CSVs. PrimaryFilter covers all 2,870 articles;
    Annotations is a 1,000-article subset with technique + narrative tags.
    We merge so that subset rows carry their techniques/narratives.
    """
    root = datasets_dir / "HALT-PROP"
    primary_path = root / "PrimaryFilter.csv"
    annot_path = root / "Annotations.csv"

    primary = pd.read_csv(primary_path, sep=";", dtype=str, encoding="utf-8")
    annot = pd.read_csv(annot_path, sep=";", dtype=str, encoding="utf-8")
    log.info("HALT-PROP: %d primary, %d annotated", len(primary), len(annot))

    # Align column names defensively. CSVs sometimes carry an unnamed first
    # column with the row index — promote it to a real `index` column.
    def _normalise(df_: pd.DataFrame) -> pd.DataFrame:
        df_ = df_.copy()
        df_.columns = [c.strip() for c in df_.columns]
        if "index" not in df_.columns:
            for c in df_.columns:
                if c.lower().startswith("unnamed"):
                    df_ = df_.rename(columns={c: "index"})
                    break
            else:
                df_ = df_.reset_index(drop=False).rename(columns={"index": "index"})
        return df_

    primary = _normalise(primary)
    annot = _normalise(annot)

    # Keep annot's narratives/techniques; left-join on index
    merge_cols = [c for c in ("narratives", "custom_narratives", "techniques") if c in annot.columns]
    annot_subset = annot[["index"] + merge_cols].copy() if merge_cols else annot[["index"]].copy()
    df = primary.merge(annot_subset, on="index", how="left")

    out = pd.DataFrame()
    out["id"] = "halt-prop:" + df["index"].astype(str)
    heading = df.get("heading", pd.Series([""] * len(df))).fillna("")
    content = df.get("content", pd.Series([""] * len(df))).fillna("")
    out["text"] = (heading.astype(str).str.strip() + "\n\n" + content.astype(str).str.strip()).str.strip()
    out["image_path"] = None
    out["source"] = "halt-prop"
    out["source_type"] = "unknown"
    out["native_label"] = df.get("is_propaganda", pd.Series([""] * len(df))).fillna("")
    # native_meta: pack narratives/techniques + anything else as JSON-able dict.
    meta_cols = [c for c in df.columns if c not in {"index", "heading", "content", "is_propaganda"}]
    out["native_meta"] = df[meta_cols].apply(
        lambda r: {k: (None if pd.isna(v) else v) for k, v in r.to_dict().items()}, axis=1
    )
    out["group_key"] = "halt-prop:" + df["index"].astype(str)
    return out


# ----------------------------------------------------------------------- DIGIRES


def load_digires(datasets_dir: Path) -> pd.DataFrame:
    root = datasets_dir / "DIGIRES"
    path = root / "DIGIRES_COVID19_LT.tsv"
    df = pd.read_csv(path, sep="\t", dtype=str, encoding="utf-8")
    df.columns = [c.strip() for c in df.columns]
    log.info("DIGIRES: %d rows", len(df))

    out = pd.DataFrame()
    out["id"] = "digires:" + pd.Series(range(len(df))).astype(str)
    title = df.get("Title", pd.Series([""] * len(df))).fillna("")
    body = df.get("Text", pd.Series([""] * len(df))).fillna("")
    out["text"] = (title.astype(str).str.strip() + "\n\n" + body.astype(str).str.strip()).str.strip()
    out["image_path"] = None
    out["source"] = "digires"
    label = df.get("Label", pd.Series(["0"] * len(df))).fillna("0").astype(str)
    out["native_label"] = label.map(lambda x: "reliable" if x.strip() == "0" else "unreliable")
    out["source_type"] = out["native_label"].map(
        {"reliable": "neutral", "unreliable": "propaganda"}
    ).fillna("unknown")
    out["native_meta"] = [{"topic": "covid-19"} for _ in range(len(df))]
    # No event grouping available in DIGIRES; use per-item id for groups (degenerate).
    out["group_key"] = out["id"]
    return out


# ----------------------------------------------------------------------- LITUND


_LITUND_FAILAS_RE = re.compile(r"^([A-Z]{2,3})_([A-Z]{3,6})_(\d+)")


def _read_litund_metadata(path: Path) -> pd.DataFrame:
    """LITUND metadata is tab-separated with a Lithuanian column header."""
    try:
        df = pd.read_csv(path, sep="\t", dtype=str, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(path, sep="\t", dtype=str, encoding="latin-1")
    df.columns = [c.strip() for c in df.columns]
    # Find the Failas column under any spelling variant.
    failas_col = next((c for c in df.columns if c.lower().startswith("failas")), None)
    if failas_col is None:
        # Fallback: assume first column is the filename.
        failas_col = df.columns[0]
    df = df.rename(columns={failas_col: "Failas"})
    return df


def load_litund(datasets_dir: Path) -> pd.DataFrame:
    root = datasets_dir / "LITUND"
    rows = []

    for subset_name, dir_name, meta_name, src_type in [
        ("unreliable", "Unreliable", "unreliable_corpus-metadata.txt", "propaganda"),
        ("lrt", "LRT", "LRT_corpus-metadata.txt", "neutral"),
    ]:
        text_dir = root / dir_name
        meta_path = root / meta_name
        if not text_dir.exists():
            log.warning("LITUND: missing %s, skipping", text_dir)
            continue
        meta = _read_litund_metadata(meta_path) if meta_path.exists() else pd.DataFrame()
        meta_by_failas = {r["Failas"]: r.to_dict() for _, r in meta.iterrows()} if not meta.empty else {}

        for txt_path in sorted(text_dir.glob("*.txt")):
            failas = txt_path.stem
            try:
                text = txt_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                text = txt_path.read_text(encoding="latin-1")
            m = meta_by_failas.get(failas, {})
            # Group key: shared prefix (e.g. UN_POL) groups same topic; keeps events together.
            mm = _LITUND_FAILAS_RE.match(failas)
            group = f"{subset_name}:{mm.group(1)}_{mm.group(2)}" if mm else f"{subset_name}:{failas}"
            rows.append({
                "id": f"litund:{subset_name}:{failas}",
                "text": text.strip(),
                "image_path": None,
                "source": "litund",
                "source_type": src_type,
                "native_label": subset_name,  # "unreliable" or "lrt"
                "native_meta": {k: (None if pd.isna(v) else v) for k, v in m.items() if k != "Failas"},
                "group_key": group,
            })

    log.info("LITUND: %d rows", len(rows))
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------- driver


LOADERS = {
    "halt-prop": load_halt_prop,
    "digires": load_digires,
    "litund": load_litund,
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Load existing corpora into common schema.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--corpus", choices=list(LOADERS.keys()) + ["all"], default="all")
    parser.add_argument("--all", action="store_true", help="alias for --corpus all")
    args = parser.parse_args()

    cfg = read_yaml(args.config)
    datasets_dir = PROJECT_ROOT / cfg["paths"]["datasets_dir"]
    interim_dir = ensure_dir(PROJECT_ROOT / cfg["paths"]["interim_dir"])

    targets = list(LOADERS.keys()) if (args.corpus == "all" or args.all) else [args.corpus]
    for name in targets:
        log.info("Loading %s ...", name)
        df = LOADERS[name](datasets_dir)
        # native_meta must be JSON-serialisable for parquet; coerce to str.
        df = df.copy()
        df["native_meta"] = df["native_meta"].apply(lambda d: json.dumps(d, ensure_ascii=False, default=str))
        out_path = interim_dir / f"{name}.parquet"
        df.to_parquet(out_path, index=False)
        log.info("  -> %s  (%d rows)", out_path, len(df))


if __name__ == "__main__":
    main()

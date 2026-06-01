"""Batch-and-validate annotation harness.

The 3-class labeller is **Claude Code in the loop**, not an API client. This
module:

  - slices the scraped JSONL into manageable batches
  - writes each batch as a markdown file containing system prompt + few-shot +
    articles, and an empty matching `.output.jsonl` skeleton
  - in self-consistency mode, writes N copies per batch so the harness can
    majority-vote afterwards
  - merges all per-batch output JSONLs into data/annotations/llm_labels.jsonl
  - aggregates N self-consistency runs into a single label with majority vote

CLI:

  python -m src.annotation.agent make-batches --input data/raw/scraped.jsonl \
        --batch-size 20 --out data/annotations/batches/

  python -m src.annotation.agent merge-batches --batches data/annotations/batches/

  python -m src.annotation.agent aggregate --batches data/annotations/batches/ \
        --n 3   # self-consistency vote across 3 runs
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

from src.utils import (append_jsonl, ensure_dir, get_logger, read_jsonl,
                       read_yaml, write_jsonl)

log = get_logger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = PROJECT_ROOT / "config" / "config.yaml"
PROMPTS_DIR = Path(__file__).parent / "prompts"


# ----------------------------------------------------------------- make-batches


def _load_prompts() -> tuple[str, str]:
    sys_p = (PROMPTS_DIR / "system_classifier_v1.md").read_text(encoding="utf-8")
    fs = (PROMPTS_DIR / "fewshot_examples_v1.md").read_text(encoding="utf-8")
    return sys_p, fs


def _batch_input_markdown(system_prompt: str, fewshot: str, items: list[dict], run_idx: int) -> str:
    parts = [
        "# Annotation batch input",
        "",
        f"Run index (for self-consistency): {run_idx}",
        "",
        "## System prompt",
        "",
        system_prompt,
        "",
        "## Few-shot exemplars",
        "",
        fewshot,
        "",
        "## Articles to label",
        "",
        "Output one JSON object per article into the matching `.output.jsonl` file,",
        "in the same order as below. Do NOT output anything else.",
        "",
    ]
    for i, it in enumerate(items, 1):
        parts.append(f"### Article {i} — id: `{it['id']}`")
        parts.append("")
        title = it.get("title") or ""
        parts.append(f"**Title:** {title}")
        parts.append("")
        parts.append(f"**Source:** {it.get('source','?')} ({it.get('source_type','?')})")
        parts.append("")
        parts.append("**Text:**")
        parts.append("")
        parts.append("```")
        parts.append(it.get("text", "").strip())
        parts.append("```")
        parts.append("")
    return "\n".join(parts)


def make_batches(
    input_jsonl: Path,
    out_dir: Path,
    batch_size: int,
    self_consistency_n: int = 1,
    source_filter: str | None = None,
) -> int:
    ensure_dir(out_dir)
    items = list(read_jsonl(input_jsonl))
    if source_filter:
        before = len(items)
        items = [it for it in items if it.get("source") == source_filter]
        log.info("source filter %r: %d -> %d items", source_filter, before, len(items))
    system_prompt, fewshot = _load_prompts()
    n_batches = 0
    for start in range(0, len(items), batch_size):
        chunk = items[start:start + batch_size]
        idx = start // batch_size
        for run in range(self_consistency_n):
            tag = f"batch_{idx:04d}" + (f".run{run+1}" if self_consistency_n > 1 else "")
            md = _batch_input_markdown(system_prompt, fewshot, chunk, run + 1)
            (out_dir / f"{tag}.input.md").write_text(md, encoding="utf-8")
            # Empty output skeleton with a per-line comment explaining the schema.
            out_path = out_dir / f"{tag}.output.jsonl"
            if not out_path.exists():
                out_path.write_text(
                    "",
                    encoding="utf-8",
                )
            n_batches += 1
    log.info("wrote %d batch files (%d articles, batch_size=%d, sc_n=%d) to %s",
             n_batches, len(items), batch_size, self_consistency_n, out_dir)
    log.info("Next: open each batch_*.input.md in Claude Code and fill the matching batch_*.output.jsonl.")
    return n_batches


# ----------------------------------------------------------------- merge-batches


def _iter_batch_outputs(batches_dir: Path) -> Iterable[tuple[str, dict]]:
    for p in sorted(batches_dir.glob("batch_*.output.jsonl")):
        for row in read_jsonl(p):
            yield p.name, row


def merge_batches(batches_dir: Path, out_path: Path) -> int:
    rows = []
    seen = set()
    for batch_name, row in _iter_batch_outputs(batches_dir):
        if "id" not in row or "label" not in row:
            log.warning("%s: row missing id/label, skipping: %s", batch_name, row)
            continue
        if row["id"] in seen:
            continue
        seen.add(row["id"])
        rows.append(row)
    n = write_jsonl(out_path, rows)
    log.info("merged %d rows -> %s", n, out_path)
    return n


# ----------------------------------------------------------------- aggregate (self-consistency)


def aggregate_self_consistency(batches_dir: Path, n: int, out_path: Path,
                                conf_threshold: float = 0.6) -> int:
    """Majority-vote across N parallel runs."""
    by_id: dict[str, list[dict]] = defaultdict(list)
    for _, row in _iter_batch_outputs(batches_dir):
        if "id" in row and "label" in row:
            by_id[row["id"]].append(row)

    rows = []
    for aid, votes in by_id.items():
        labs = [v["label"] for v in votes]
        winner, n_winner = Counter(labs).most_common(1)[0]
        agreement = n_winner / max(len(labs), 1)
        avg_conf = sum(float(v.get("confidence", 0.0)) for v in votes if v.get("label") == winner) / max(n_winner, 1)
        # Combined confidence: average winner-conf * agreement.
        comb_conf = avg_conf * agreement
        rationale = next((v.get("rationale", "") for v in votes if v.get("label") == winner), "")
        features = next((v.get("features", {}) for v in votes if v.get("label") == winner), {})
        rows.append({
            "id": aid,
            "label": winner,
            "confidence": round(comb_conf, 3),
            "self_consistency_agreement": round(agreement, 3),
            "n_votes": len(labs),
            "rationale": rationale,
            "features": features,
            "abstain": comb_conf < conf_threshold,
        })
    nw = write_jsonl(out_path, rows)
    log.info("aggregated %d items (%d abstain by conf<%.2f)",
             nw, sum(1 for r in rows if r["abstain"]), conf_threshold)
    return nw


# ----------------------------------------------------------------- CLI


def main() -> None:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    pm = sub.add_parser("make-batches")
    pm.add_argument("--input", required=True, help="scraped.jsonl (or any JSONL with id+text+title)")
    pm.add_argument("--out", default="data/annotations/batches/")
    pm.add_argument("--batch-size", type=int, default=20)
    pm.add_argument("--self-consistency-n", type=int, default=1)
    pm.add_argument("--source", default=None,
                    help="If set, only batch articles whose `source` field matches (e.g. rubaltic_lt)")
    pm.add_argument("--config", default=str(DEFAULT_CONFIG))

    pmm = sub.add_parser("merge-batches")
    pmm.add_argument("--batches", default="data/annotations/batches/")
    pmm.add_argument("--out", default="data/annotations/llm_labels.jsonl")

    pa = sub.add_parser("aggregate")
    pa.add_argument("--batches", default="data/annotations/batches/")
    pa.add_argument("--n", type=int, default=3)
    pa.add_argument("--out", default="data/annotations/llm_labels.jsonl")
    pa.add_argument("--conf-threshold", type=float, default=0.6)

    args = p.parse_args()

    if args.cmd == "make-batches":
        cfg = read_yaml(args.config)
        sc_n = args.self_consistency_n or cfg.get("annotation", {}).get("self_consistency_n", 1)
        make_batches(
            Path(args.input),
            Path(args.out) if Path(args.out).is_absolute() else PROJECT_ROOT / args.out,
            args.batch_size,
            sc_n,
            source_filter=args.source,
        )
    elif args.cmd == "merge-batches":
        batches = Path(args.batches) if Path(args.batches).is_absolute() else PROJECT_ROOT / args.batches
        out = Path(args.out) if Path(args.out).is_absolute() else PROJECT_ROOT / args.out
        merge_batches(batches, out)
    elif args.cmd == "aggregate":
        batches = Path(args.batches) if Path(args.batches).is_absolute() else PROJECT_ROOT / args.batches
        out = Path(args.out) if Path(args.out).is_absolute() else PROJECT_ROOT / args.out
        aggregate_self_consistency(batches, args.n, out, args.conf_threshold)


if __name__ == "__main__":
    main()

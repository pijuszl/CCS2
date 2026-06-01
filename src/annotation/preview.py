"""Compact previewer for label-in-the-loop work.

Reads a batch's source records from scraped.jsonl and prints, for each id in the
target batch, a one-screen preview:
    [N] id
      Title
      First ~200 chars of body
      Total length / has scare quotes / loaded-lexicon hits

This is purely a UX helper for the human-in-the-loop annotator (Claude or human).
The authoritative input is still batch_NNNN.input.md — use this to speed-skim
and only open the full md when uncertain.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from src.utils import read_jsonl

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Cheap surface markers — same intent as features.yaml lexica
LOADED = {
    "režimas", "marionetė", "marionetės", "marionietė", "marionietėmis",
    "rusofob", "kretinizm", "pakalik", "modžahed", "konvulsij", "psichoz",
    "smilkin", "okupant", "fašist", "naci", "šūvis sau", "tragiško",
    "nevykėli", "kvailyst", "bukum", "iškrypėli", "landsbergist",
}
DOUBT = {"būk tai", "neva", "tariam", "ar tai tikra", "atrodo", "panašu"}


def _surface(text: str) -> dict:
    lower = (text or "").lower()
    loaded_hits = sum(1 for w in LOADED if w in lower)
    doubt_hits = sum(1 for w in DOUBT if w in lower)
    scare = lower.count("„") + lower.count("«")
    return {"loaded": loaded_hits, "doubt": doubt_hits, "scare_quotes": scare,
            "len": len(text or "")}


def main() -> None:
    import sys
    p = argparse.ArgumentParser()
    p.add_argument("--scraped", default="data/raw/scraped.jsonl")
    p.add_argument("--batches-dir", default="data/annotations/batches")
    p.add_argument("--batch", required=True, type=int, help="batch index (0-based)")
    p.add_argument("--batch-size", type=int, default=20)
    p.add_argument("--source", default="rubaltic_lt")
    p.add_argument("--first-chars", type=int, default=240)
    p.add_argument("--out", default=None, help="Write to file (UTF-8). Defaults to stdout.")
    args = p.parse_args()

    scraped = list(read_jsonl(PROJECT_ROOT / args.scraped))
    pool = [r for r in scraped if r.get("source") == args.source]
    start = args.batch * args.batch_size
    chunk = pool[start:start + args.batch_size]
    if not chunk:
        raise SystemExit(f"empty batch {args.batch} for source {args.source}")

    lines = [f"# Batch {args.batch:04d}  ({args.source}, {len(chunk)} items)", ""]
    for i, r in enumerate(chunk, 1):
        title = (r.get("title") or "").strip()
        text = (r.get("text") or "").strip()
        body = text[: args.first_chars].replace("\n", " ")
        s = _surface(text)
        lines.append(f"## [{i:2d}] {r['id']}")
        lines.append(f"     Title: {title}")
        lines.append(f"     Body : {body}{'…' if len(text) > args.first_chars else ''}")
        lines.append(f"     Stats: loaded={s['loaded']}  doubt={s['doubt']}  scare={s['scare_quotes']}  len={s['len']}")
        lines.append("")
    out = "\n".join(lines)
    if args.out:
        Path(args.out).write_text(out, encoding="utf-8")
    else:
        sys.stdout.buffer.write(out.encode("utf-8"))
        sys.stdout.buffer.write(b"\n")


if __name__ == "__main__":
    main()

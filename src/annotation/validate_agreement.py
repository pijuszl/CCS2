"""Cohen's κ and per-class confusion vs human gold.

Inputs:
  --llm    data/annotations/llm_labels.jsonl
  --gold   data/annotations/human_gold.jsonl

Each file is JSONL of {id, label, ...}.

Prints κ, per-class P/R/F1, confusion matrix; writes JSON report.
Gates at κ ≥ threshold (default 0.6 per CLAUDE.md).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.utils import ensure_dir, get_logger, read_jsonl

log = get_logger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _index(rows: list[dict]) -> dict[str, str]:
    return {r["id"]: r["label"] for r in rows if "id" in r and "label" in r}


def cohen_kappa(y_a: list[str], y_b: list[str], labels: list[str]) -> float:
    from sklearn.metrics import cohen_kappa_score
    return float(cohen_kappa_score(y_a, y_b, labels=labels))


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--llm", required=True)
    p.add_argument("--gold", required=True)
    p.add_argument("--threshold", type=float, default=0.6)
    p.add_argument("--report", default=None)
    p.add_argument("--classes", nargs="+", default=["non", "open", "hidden"])
    args = p.parse_args()

    llm = _index(list(read_jsonl(args.llm)))
    gold = _index(list(read_jsonl(args.gold)))
    common = sorted(set(llm) & set(gold))
    if not common:
        raise SystemExit("No overlapping ids between llm and gold files.")

    y_llm = [llm[i] for i in common]
    y_gold = [gold[i] for i in common]

    kappa = cohen_kappa(y_gold, y_llm, args.classes)

    from sklearn.metrics import (classification_report, confusion_matrix,
                                 precision_recall_fscore_support)
    cm = confusion_matrix(y_gold, y_llm, labels=args.classes).tolist()
    P, R, F, _ = precision_recall_fscore_support(y_gold, y_llm, labels=args.classes, zero_division=0)
    per_class = {c: {"precision": float(P[i]), "recall": float(R[i]), "f1": float(F[i])}
                 for i, c in enumerate(args.classes)}

    report = {
        "n_compared": len(common),
        "kappa": round(kappa, 4),
        "gate_threshold": args.threshold,
        "gate_passed": kappa >= args.threshold,
        "per_class": per_class,
        "confusion_matrix": {"labels": args.classes, "matrix": cm},
        "classification_report": classification_report(
            y_gold, y_llm, labels=args.classes, zero_division=0, digits=3
        ),
    }
    log.info("\n%s", report["classification_report"])
    log.info("Cohen's κ = %.4f (threshold %.2f) -> %s",
             kappa, args.threshold, "OK" if report["gate_passed"] else "REVIEW")

    out_path = Path(args.report) if args.report else PROJECT_ROOT / "results" / "tables" / "agreement.json"
    ensure_dir(out_path.parent)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("wrote %s", out_path)


if __name__ == "__main__":
    main()

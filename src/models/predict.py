"""Load a saved checkpoint and predict on an arbitrary parquet of items.

Inputs:
  --checkpoint   results/runs/<id>/best_model.pt
  --input        parquet with id + text + image_path_224 (optional)
  --out          parquet to write {id, y_pred, p_<class>...}
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
import torch
from torch.utils.data import DataLoader

from src.models.train import ArticleDataset, _build_image_preprocess, _build_model, _device
from src.utils import get_logger

log = get_logger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--checkpoint", required=True)
    p.add_argument("--input", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()

    sd = torch.load(args.checkpoint, map_location="cpu")
    cfg = sd["config"]
    exp = sd["exp"]
    classes = cfg["classes"]
    device = _device(cfg.get("device", "auto"))

    model_kind, model = _build_model(cfg, exp)
    model.load_state_dict(sd["state_dict"], strict=False)
    model = model.to(device).eval()

    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(cfg["text"]["model_name"])
    pre = _build_image_preprocess(model_kind, model)

    df = pd.read_parquet(args.input)
    # Stub label column so ArticleDataset doesn't choke; we don't use it.
    if "label_3class" not in df.columns:
        df["label_3class"] = classes[0]
    ds = ArticleDataset(df, tok, int(cfg["text"]["max_len"]), pre, classes,
                       require_image=(model_kind in ("multimodal", "vision_only")))
    loader = DataLoader(ds, batch_size=int(cfg["train"]["batch_size"]), shuffle=False)
    rows = []
    with torch.no_grad():
        for batch in loader:
            ids = batch["id"]
            if model_kind == "text":
                logits = model(batch["input_ids"].to(device), batch["attention_mask"].to(device))
            elif model_kind == "multimodal":
                logits = model(
                    batch["input_ids"].to(device),
                    batch["attention_mask"].to(device),
                    batch["image"].to(device),
                    batch["image_mask"].to(device) if "image_mask" in batch else None,
                )
            elif model_kind == "vision_only":
                logits = model(batch["image"].to(device))
            else:
                raise NotImplementedError(model_kind)
            probs = torch.softmax(logits, dim=-1).cpu().tolist()
            preds = logits.argmax(dim=-1).cpu().tolist()
            for i, aid in enumerate(ids):
                row = {"id": aid, "y_pred": classes[preds[i]]}
                for j, c in enumerate(classes):
                    row[f"p_{c}"] = probs[i][j]
                rows.append(row)
    out = pd.DataFrame(rows)
    out.to_parquet(args.out, index=False)
    log.info("wrote %s (%d rows)", args.out, len(out))


if __name__ == "__main__":
    main()

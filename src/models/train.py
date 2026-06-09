"""Single training entry point — reads an experiment YAML and runs the full loop.

  python -m src.models.train --config experiments/text_xlmr_existing.yaml [--smoke]

Experiment YAML overrides the global config piecewise. Keys recognised:

  base_config: config/config.yaml   (overrideable, default global)
  model_kind:  "text" | "multimodal" | "joint_jinaclip" | "vision_only"
  dataset:
    require_label: true
    image_required: false   # for H1 comparison, keep image-bearing subset
    use_scraped: false      # include data/processed/scraped items
  train: { ...overrides... }
  vision: { ...overrides... }
  text: { ...overrides... }
  tag: "text_xlmr_existing"

Logs everything to results/runs/<ts>_<tag>/ : config.yaml, metrics.json, predictions.parquet,
best_model.pt, train.log.
"""
from __future__ import annotations

import argparse
import json
import os
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset

from src.utils import (ensure_dir, get_logger, git_hash, new_run_dir, read_yaml,
                       set_seed, write_yaml)

log = get_logger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = PROJECT_ROOT / "config" / "config.yaml"


# ----------------------------------------------------------------- losses


class FocalLoss(nn.Module):
    def __init__(self, alpha: torch.Tensor | None, gamma: float = 2.0):
        super().__init__()
        self.register_buffer("alpha", alpha if alpha is not None else None, persistent=False)
        self.gamma = gamma

    def forward(self, logits, targets):
        logp = torch.log_softmax(logits, dim=-1)
        p = logp.exp()
        ce = -logp.gather(1, targets.unsqueeze(1)).squeeze(1)
        pt = p.gather(1, targets.unsqueeze(1)).squeeze(1)
        focal = (1.0 - pt) ** self.gamma * ce
        if self.alpha is not None:
            a = self.alpha.gather(0, targets)
            focal = a * focal
        return focal.mean()


# ----------------------------------------------------------------- dataset


class ArticleDataset(Dataset):
    def __init__(self, df: pd.DataFrame, tokenizer, max_len: int,
                 image_preprocess, classes: list[str], require_image: bool):
        self.df = df.reset_index(drop=True)
        self.tok = tokenizer
        self.max_len = max_len
        self.image_preprocess = image_preprocess
        self.class_to_idx = {c: i for i, c in enumerate(classes)}
        self.require_image = require_image

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        r = self.df.iloc[idx]
        enc = self.tok(
            r["text"], truncation=True, max_length=self.max_len,
            padding="max_length", return_tensors="pt"
        )
        label = self.class_to_idx[r["label_3class"]]
        img_path = r.get("image_path_224") or r.get("image_path")
        has_image = bool(img_path) and (PROJECT_ROOT / img_path).exists() if isinstance(img_path, str) else False
        if self.image_preprocess is not None:
            if has_image:
                from PIL import Image
                full = PROJECT_ROOT / img_path
                try:
                    im = Image.open(full).convert("RGB")
                    image = self.image_preprocess(im)
                    image_mask = 1
                except Exception:
                    image = torch.zeros(3, 224, 224)
                    image_mask = 0
                    has_image = False
            else:
                image = torch.zeros(3, 224, 224)
                image_mask = 0
            return {
                "input_ids": enc["input_ids"].squeeze(0),
                "attention_mask": enc["attention_mask"].squeeze(0),
                "image": image,
                "image_mask": image_mask,
                "label": label,
                "id": r["id"],
            }
        return {
            "input_ids": enc["input_ids"].squeeze(0),
            "attention_mask": enc["attention_mask"].squeeze(0),
            "label": label,
            "id": r["id"],
        }


# ----------------------------------------------------------------- helpers


def _device(cfg_device: str) -> torch.device:
    if cfg_device == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return torch.device(cfg_device)


def _merge_cfg(base: dict, override: dict) -> dict:
    out = json.loads(json.dumps(base))
    for k, v in (override or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _merge_cfg(out[k], v)
        else:
            out[k] = v
    return out


def _load_weak_image_data(cfg: dict, smoke: bool) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, list[str]]:
    """Load the weak-label image set for vision aux pretraining.

    Splits are made on-the-fly (no group leakage matters here — these images
    have no article-level grouping that the main task uses). Stratified
    80/10/10 split by `weak_label`.
    """
    from sklearn.model_selection import train_test_split

    interim = PROJECT_ROOT / cfg["paths"]["interim_dir"]
    processed = PROJECT_ROOT / cfg["paths"]["processed_dir"]
    wl_path = interim / "image_weak_labels.parquet"
    if not wl_path.exists():
        raise SystemExit(f"missing {wl_path}; run src.data.weak_label_images first.")
    wl = pd.read_parquet(wl_path)
    # Resolve to the resized 224 path (if it exists) so the vision encoder uses
    # pre-resized files. We re-derive from articles.parquet if present.
    articles_path = processed / "articles.parquet"
    if articles_path.exists():
        arts = pd.read_parquet(articles_path)[["id", "image_path_224", "image_path_512"]]
        wl = wl.merge(arts, on="id", how="left")
        # Fall back to raw image_path when resized not yet built (litund newly-added items).
        wl["image_path_224"] = wl["image_path_224"].fillna(wl["image_path"])
    else:
        wl["image_path_224"] = wl["image_path"]
    # Drop logo-flagged images (they hurt aux representation learning).
    if "likely_logo" in wl.columns:
        wl = wl[~wl["likely_logo"].fillna(False)].reset_index(drop=True)
    # The main 3-class task uses `label_3class`; ArticleDataset reads that
    # column. Shoehorn weak_label in under the same name so we can reuse it.
    wl = wl.rename(columns={"weak_label": "label_3class"})
    wl["text"] = ""  # vision-only path doesn't tokenise text
    wl["id"] = wl["id"].astype(str)
    classes = ["non", "propaganda"]
    wl = wl[wl["label_3class"].isin(classes)].reset_index(drop=True)
    train, rest = train_test_split(wl, test_size=0.2, stratify=wl["label_3class"],
                                    random_state=int(cfg.get("seed", 42)))
    val, test = train_test_split(rest, test_size=0.5, stratify=rest["label_3class"],
                                 random_state=int(cfg.get("seed", 42)) + 1)
    train = train.reset_index(drop=True); val = val.reset_index(drop=True); test = test.reset_index(drop=True)
    if smoke:
        k = int(cfg["train"].get("smoke_subset", 64))
        train = train.head(k); val = val.head(max(k // 4, 4)); test = test.head(max(k // 4, 4))
    log.info("weak data sizes: train=%d val=%d test=%d  (classes=%s)",
             len(train), len(val), len(test), classes)
    return train, val, test, classes


def _load_data(cfg: dict, exp: dict, smoke: bool) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, list[str]]:
    dataset_cfg = exp.get("dataset", {}) or {}
    if dataset_cfg.get("weak_label_source") == "image_weak_labels":
        return _load_weak_image_data(cfg, smoke)

    processed = PROJECT_ROOT / cfg["paths"]["processed_dir"]
    articles = pd.read_parquet(processed / "articles.parquet")
    splits_path = processed / "splits.json"
    if not splits_path.exists():
        raise SystemExit("splits.json missing; run src.data.split first.")
    splits = json.loads(splits_path.read_text(encoding="utf-8"))

    classes = cfg["classes"]
    articles = articles[articles["label_3class"].isin(classes)].reset_index(drop=True)
    if dataset_cfg.get("image_required"):
        has_img = articles.apply(
            lambda r: bool(r.get("image_path_224"))
            and (PROJECT_ROOT / r["image_path_224"]).exists(),
            axis=1,
        )
        articles = articles[has_img].reset_index(drop=True)

    if not dataset_cfg.get("use_scraped", False):
        articles = articles[articles["source"].isin({"halt-prop", "digires", "litund"})].reset_index(drop=True)

    def take(ids):
        return articles[articles["id"].isin(set(ids))].reset_index(drop=True)

    train = take(splits["train"])
    val = take(splits["val"])
    test = take(splits["test"])

    if smoke:
        k = int(cfg["train"].get("smoke_subset", 64))
        train = train.head(k)
        val = val.head(max(k // 4, 4))
        test = test.head(max(k // 4, 4))

    log.info("data sizes: train=%d val=%d test=%d", len(train), len(val), len(test))
    return train, val, test, classes


def _build_model(cfg: dict, exp: dict):
    kind = exp.get("model_kind", "text")
    if kind == "text":
        from .text_baseline import TextBaseline, TextBaselineCfg
        tcfg = TextBaselineCfg(
            model_name=cfg["text"]["model_name"],
            num_classes=len(cfg["classes"]),
            freeze_until_layer=int(exp.get("text", {}).get("freeze_until_layer", 0)),
        )
        return ("text", TextBaseline(tcfg))
    if kind == "multimodal":
        from .multimodal import MultimodalCfg, MultimodalLateFusion
        from .text_baseline import TextBaselineCfg
        from .vision_encoder import VisionEncoderCfg
        mcfg = MultimodalCfg(
            text=TextBaselineCfg(
                model_name=cfg["text"]["model_name"],
                num_classes=len(cfg["classes"]),
                freeze_until_layer=int(exp.get("text", {}).get("freeze_until_layer", 0)),
            ),
            vision=VisionEncoderCfg(
                backbone=cfg["vision"]["backbone"],
                pretrained=cfg["vision"]["pretrained"],
                freeze_until_layer=int(cfg["vision"].get("freeze_until_layer", 0)),
                aux_binary=False,
            ),
            hidden_dim=int(cfg["fusion"]["hidden_dim"]),
            num_classes=len(cfg["classes"]),
            dropout=float(cfg["fusion"]["dropout"]),
            modality_dropout=float(cfg["train"].get("modality_dropout", 0.0)),
        )
        return ("multimodal", MultimodalLateFusion(mcfg))
    if kind == "vision_only":
        # Vision encoder + linear head; reuses VisionEncoder.
        from .vision_encoder import VisionEncoder, VisionEncoderCfg
        vcfg = VisionEncoderCfg(
            backbone=cfg["vision"]["backbone"],
            pretrained=cfg["vision"]["pretrained"],
            freeze_until_layer=int(cfg["vision"].get("freeze_until_layer", 0)),
            aux_binary=False,
        )
        enc = VisionEncoder(vcfg)
        head = nn.Linear(enc.out_dim, len(cfg["classes"]))

        class VisionOnly(nn.Module):
            def __init__(self, enc, head):
                super().__init__()
                self.enc = enc
                self.head = head

            def forward(self, images):
                return self.head(self.enc.encode(images))

        return ("vision_only", VisionOnly(enc, head))
    if kind == "joint_jinaclip":
        from .joint_jinaclip import JinaClipCfg, JinaClipMLP
        return ("joint", JinaClipMLP(JinaClipCfg(
            model_name=cfg.get("joint", {}).get("model_name", "jinaai/jina-clip-v2"),
            num_classes=len(cfg["classes"]),
        )))
    raise ValueError(f"unknown model_kind: {kind}")


def _build_image_preprocess(model_kind: str, model):
    if model_kind in ("multimodal", "vision_only"):
        return model.vision.preprocess if model_kind == "multimodal" or hasattr(model, "vision") else model.enc.preprocess  # type: ignore[attr-defined]
    return None


def _evaluate(model, model_kind: str, loader, device, classes) -> dict[str, Any]:
    from src.evaluation.metrics import compute_metrics
    model.eval()
    preds, gts, ids = [], [], []
    with torch.no_grad():
        for batch in loader:
            ids.extend(batch["id"])
            labels = batch["label"].to(device)
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
            p = logits.argmax(dim=-1).cpu().tolist()
            preds.extend(p)
            gts.extend(labels.cpu().tolist())
    label_names = [classes[i] for i in gts]
    pred_names = [classes[i] for i in preds]
    metrics = compute_metrics(label_names, pred_names, classes)
    return {"metrics": metrics, "preds": pred_names, "gts": label_names, "ids": ids}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True, help="experiments/<name>.yaml")
    p.add_argument("--base-config", default=str(DEFAULT_CONFIG))
    p.add_argument("--smoke", action="store_true")
    args = p.parse_args()

    base_cfg = read_yaml(args.base_config)
    exp = read_yaml(args.config) or {}
    cfg = _merge_cfg(base_cfg, exp)

    set_seed(cfg.get("seed", 42))
    device = _device(cfg.get("device", "auto"))
    tag = exp.get("tag") or Path(args.config).stem
    run_dir = new_run_dir(PROJECT_ROOT / cfg["paths"]["runs_dir"], tag=tag)
    log.info("device=%s run_dir=%s", device, run_dir)
    (run_dir / "git.txt").write_text(git_hash(), encoding="utf-8")

    # Load data first so the binary-aux path can override the class list.
    train_df, val_df, test_df, classes = _load_data(cfg, exp, args.smoke)
    cfg["classes"] = classes
    write_yaml(run_dir / "config.yaml", cfg)

    model_kind, model = _build_model(cfg, exp)
    model = model.to(device)

    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(cfg["text"]["model_name"])
    image_preprocess = _build_image_preprocess(model_kind, model)

    def make_loader(df, shuffle):
        ds = ArticleDataset(df, tokenizer, int(cfg["text"]["max_len"]),
                            image_preprocess, classes,
                            require_image=(model_kind in ("multimodal", "vision_only")))
        return DataLoader(ds, batch_size=int(cfg["train"]["batch_size"]),
                          shuffle=shuffle, num_workers=0)

    train_loader = make_loader(train_df, True)
    val_loader = make_loader(val_df, False)
    test_loader = make_loader(test_df, False)

    # Loss + optim. Pick the balance file matching the task: binary aux uses
    # balance_binary.json (computed from the weak-label parquet); main 3-class
    # uses balance.json (computed from the labelled train split).
    processed_dir = PROJECT_ROOT / cfg["paths"]["processed_dir"]
    is_binary_aux = (model_kind == "vision_only" and set(classes) == {"non", "propaganda"})
    balance_path = processed_dir / ("balance_binary.json" if is_binary_aux else "balance.json")
    class_weight = None
    balance_strategy = (cfg.get("balance") or {}).get("strategy", "auto")
    if balance_strategy != "none" and balance_path.exists():
        b = json.loads(balance_path.read_text(encoding="utf-8"))
        class_weight = torch.tensor([b["class_weight"][c] for c in classes], dtype=torch.float, device=device)
        log.info("loaded class weights from %s: %s",
                 balance_path.name, dict(zip(classes, [float(w) for w in class_weight])))
    if cfg["train"].get("loss", "ce") == "focal":
        loss_fn = FocalLoss(alpha=class_weight, gamma=float(cfg["train"].get("focal_gamma", 2.0)))
    else:
        loss_fn = nn.CrossEntropyLoss(weight=class_weight)

    params = [p for p in model.parameters() if p.requires_grad]
    optim = torch.optim.AdamW(params, lr=float(cfg["train"]["lr"]),
                              weight_decay=float(cfg["train"]["weight_decay"]))
    use_amp = bool(cfg["train"].get("mixed_precision", False)) and device.type == "cuda"
    scaler = torch.cuda.amp.GradScaler(enabled=use_amp)
    grad_accum = int(cfg["train"].get("grad_accum", 1))
    n_epochs = int(cfg["train"].get("smoke_epochs" if args.smoke else "epochs", 1))
    patience = int(cfg["train"]["early_stop_patience"])
    metric_key = cfg["train"]["early_stop_metric"]

    best_metric = -1.0
    best_path = run_dir / "best_model.pt"
    bad_epochs = 0
    history = []
    log_file = open(run_dir / "train.log", "w", encoding="utf-8")

    def fwd(batch):
        if model_kind == "text":
            return model(batch["input_ids"].to(device), batch["attention_mask"].to(device))
        if model_kind == "multimodal":
            return model(
                batch["input_ids"].to(device),
                batch["attention_mask"].to(device),
                batch["image"].to(device),
                batch["image_mask"].to(device) if "image_mask" in batch else None,
            )
        if model_kind == "vision_only":
            return model(batch["image"].to(device))
        raise NotImplementedError(model_kind)

    t0 = time.time()
    for epoch in range(n_epochs):
        model.train()
        optim.zero_grad(set_to_none=True)
        epoch_loss = 0.0
        n_steps = 0
        for step, batch in enumerate(train_loader):
            with torch.cuda.amp.autocast(enabled=use_amp):
                logits = fwd(batch)
                loss = loss_fn(logits, batch["label"].to(device)) / grad_accum
            scaler.scale(loss).backward()
            if (step + 1) % grad_accum == 0:
                scaler.step(optim)
                scaler.update()
                optim.zero_grad(set_to_none=True)
            epoch_loss += float(loss.item()) * grad_accum
            n_steps += 1
        val_out = _evaluate(model, model_kind, val_loader, device, classes)
        val_metric = float(val_out["metrics"][metric_key])
        log.info("epoch %d: train_loss=%.4f val_%s=%.4f", epoch + 1,
                 epoch_loss / max(n_steps, 1), metric_key, val_metric)
        log_file.write(json.dumps({"epoch": epoch + 1,
                                    "train_loss": epoch_loss / max(n_steps, 1),
                                    "val": val_out["metrics"]}) + "\n")
        history.append({"epoch": epoch + 1, "val": val_out["metrics"]})
        if val_metric > best_metric:
            best_metric = val_metric
            torch.save({"state_dict": model.state_dict(),
                        "config": cfg, "exp": exp,
                        "model_kind": model_kind}, best_path)
            bad_epochs = 0
        else:
            bad_epochs += 1
            if bad_epochs >= patience:
                log.info("early stop at epoch %d", epoch + 1)
                break

    # Load best and evaluate on test.
    if best_path.exists():
        sd = torch.load(best_path, map_location=device)
        model.load_state_dict(sd["state_dict"])
    test_out = _evaluate(model, model_kind, test_loader, device, classes)
    log.info("TEST: %s", test_out["metrics"])
    (run_dir / "metrics.json").write_text(
        json.dumps({"history": history, "test": test_out["metrics"],
                    "best_val": best_metric,
                    "elapsed_s": round(time.time() - t0, 2)},
                   indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    pd.DataFrame({"id": test_out["ids"], "y_true": test_out["gts"],
                  "y_pred": test_out["preds"]}).to_parquet(
        run_dir / "predictions.parquet", index=False
    )
    log_file.close()
    log.info("DONE: %s", run_dir)


if __name__ == "__main__":
    main()

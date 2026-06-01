"""Zero-shot CLIP-based visual features for the H2 interpretable model.

For each item with an image we score the CLIP cosine similarity of the image
against each prompt in `config/features.yaml`. Returns one column per feature:

  presence features  -> log-prob of (positive prompt) vs (negative prompt)
                        scaled to [0, 1] via softmax.
  scalar valence     -> softmax(pos) - softmax(neg) in [-1, 1].

The CLIP backbone is loaded lazily via open_clip; if open_clip is unavailable,
features are written as NaN and a warning is logged. We never block the
text-only pipeline on this.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.utils import ensure_dir, get_logger, read_yaml

log = get_logger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = PROJECT_ROOT / "config" / "config.yaml"
DEFAULT_FEATURES = PROJECT_ROOT / "config" / "features.yaml"


class _CLIPScorer:
    def __init__(self, backbone_spec: str, pretrained: str, device: str):
        import open_clip
        import torch
        self.torch = torch
        # spec like "open_clip:ViT-B-32"
        name = backbone_spec.split(":", 1)[1] if ":" in backbone_spec else backbone_spec
        self.model, _, self.preprocess = open_clip.create_model_and_transforms(name, pretrained=pretrained)
        self.tokenizer = open_clip.get_tokenizer(name)
        self.device = device
        self.model = self.model.to(device).eval()

    def encode_image(self, img):
        with self.torch.no_grad():
            t = self.preprocess(img).unsqueeze(0).to(self.device)
            v = self.model.encode_image(t)
            v = v / v.norm(dim=-1, keepdim=True)
            return v

    def encode_text(self, texts: list[str]):
        with self.torch.no_grad():
            tok = self.tokenizer(texts).to(self.device)
            v = self.model.encode_text(tok)
            v = v / v.norm(dim=-1, keepdim=True)
            return v

    def softmax_pair(self, img, pos_prompts: list[str], neg_prompts: list[str]) -> tuple[float, float]:
        v_img = self.encode_image(img)
        v_pos = self.encode_text(pos_prompts).mean(dim=0, keepdim=True)
        v_neg = self.encode_text(neg_prompts).mean(dim=0, keepdim=True)
        logits = (v_img @ self.torch.cat([v_pos, v_neg]).T).squeeze(0)
        probs = logits.softmax(dim=-1)
        return float(probs[0].item()), float(probs[1].item())


def _make_scorer(cfg: dict):
    try:
        import torch
        device = cfg.get("device", "auto")
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else "cpu"
        spec = cfg["vision"]["backbone"]
        pretrained = cfg["vision"]["pretrained"]
        return _CLIPScorer(spec, pretrained, device)
    except Exception as e:
        log.warning("CLIP unavailable (%s); visual features will be NaN.", e)
        return None


def extract_visual(df: pd.DataFrame, fcfg: dict, scorer: _CLIPScorer | None) -> pd.DataFrame:
    if scorer is None:
        cols = {"id": df["id"]}
        for feat in fcfg.get("visual", []):
            cols[feat["name"]] = [float("nan")] * len(df)
        return pd.DataFrame(cols)

    from PIL import Image
    rows = []
    for _, r in df.iterrows():
        out: dict[str, float] = {"id": r["id"]}
        img_path = r.get("image_path_224") or r.get("image_path")
        if not img_path:
            for feat in fcfg.get("visual", []):
                out[feat["name"]] = float("nan")
            rows.append(out)
            continue
        full = (PROJECT_ROOT / img_path) if not Path(img_path).is_absolute() else Path(img_path)
        if not full.exists():
            for feat in fcfg.get("visual", []):
                out[feat["name"]] = float("nan")
            rows.append(out)
            continue
        try:
            img = Image.open(full).convert("RGB")
        except Exception:
            for feat in fcfg.get("visual", []):
                out[feat["name"]] = float("nan")
            rows.append(out)
            continue
        for feat in fcfg.get("visual", []):
            name = feat["name"]
            t = feat.get("type", "presence")
            if t == "presence":
                pos = feat["clip_prompts"][:1]
                neg = feat["clip_prompts"][1:2] or ["a generic photograph"]
                p_pos, _ = scorer.softmax_pair(img, pos, neg)
                out[name] = p_pos
            elif t == "scalar":
                p_pos, p_neg = scorer.softmax_pair(img, feat["clip_prompts_pos"], feat["clip_prompts_neg"])
                out[name] = p_pos - p_neg
        rows.append(out)
    return pd.DataFrame(rows)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--config", default=str(DEFAULT_CONFIG))
    p.add_argument("--features-yaml", default=str(DEFAULT_FEATURES))
    p.add_argument("--input", default=None)
    p.add_argument("--out", default=None)
    args = p.parse_args()
    cfg = read_yaml(args.config)
    fcfg = read_yaml(args.features_yaml)
    in_path = Path(args.input) if args.input else PROJECT_ROOT / cfg["paths"]["processed_dir"] / "articles.parquet"
    out_path = Path(args.out) if args.out else PROJECT_ROOT / cfg["paths"]["processed_dir"] / "visual_features.parquet"
    df = pd.read_parquet(in_path)
    scorer = _make_scorer(cfg)
    feat_df = extract_visual(df, fcfg, scorer)
    ensure_dir(out_path.parent)
    feat_df.to_parquet(out_path, index=False)
    log.info("wrote %s (%d rows)", out_path, len(feat_df))


if __name__ == "__main__":
    main()

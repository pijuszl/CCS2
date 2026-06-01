"""Vision encoder wrapper supporting open_clip or torchvision backbones.

backbone_spec:
  "open_clip:ViT-B-32"   (uses open_clip, image-tower only)
  "open_clip:ViT-B-16"
  "torchvision:resnet50"

Auxiliary binary head is exposed for multi-task pre-fine-tune on weak image labels.
"""
from __future__ import annotations

from dataclasses import dataclass

import torch
import torch.nn as nn


@dataclass
class VisionEncoderCfg:
    backbone: str = "open_clip:ViT-B-32"
    pretrained: str = "openai"
    freeze_until_layer: int = 0
    aux_binary: bool = False


class VisionEncoder(nn.Module):
    def __init__(self, cfg: VisionEncoderCfg):
        super().__init__()
        self.cfg = cfg
        self.kind, model_name = cfg.backbone.split(":", 1)
        if self.kind == "open_clip":
            import open_clip
            self.model, _, self.preprocess = open_clip.create_model_and_transforms(
                model_name, pretrained=cfg.pretrained
            )
            self.out_dim = self.model.visual.output_dim
            self._encode = lambda x: self.model.encode_image(x)
        elif self.kind == "torchvision":
            from torchvision import models, transforms
            if model_name == "resnet50":
                m = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
                m.fc = nn.Identity()
                self.out_dim = 2048
                self.model = m
            elif model_name == "vit_b_16":
                m = models.vit_b_16(weights=models.ViT_B_16_Weights.DEFAULT)
                self.out_dim = m.heads.head.in_features
                m.heads = nn.Identity()
                self.model = m
            else:
                raise ValueError(f"unknown torchvision model: {model_name}")
            self.preprocess = transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ])
            self._encode = lambda x: self.model(x)
        else:
            raise ValueError(f"unknown backbone kind: {self.kind}")

        self.aux_head = nn.Linear(self.out_dim, 2) if cfg.aux_binary else None
        self._maybe_freeze()

    def _maybe_freeze(self):
        if self.cfg.freeze_until_layer <= 0:
            return
        # Generic: freeze the first N children of `model`.
        n = 0
        for child in self.model.children():
            for p in child.parameters():
                p.requires_grad = False
            n += 1
            if n >= self.cfg.freeze_until_layer:
                break

    def encode(self, images: torch.Tensor) -> torch.Tensor:
        emb = self._encode(images)
        # Normalise for stable fusion.
        return emb / emb.norm(dim=-1, keepdim=True).clamp_min(1e-9)

    def forward_aux(self, images: torch.Tensor) -> torch.Tensor:
        assert self.aux_head is not None, "aux head not enabled"
        return self.aux_head(self.encode(images))

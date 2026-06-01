"""Multimodal late-fusion model: XLM-R text + CLIP/ViT vision + late-fusion head.

Supports modality dropout: with probability p during training, the image branch
is zeroed (encourages robustness when images are missing at inference).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import torch
import torch.nn as nn

from .fusion import LateFusionHead
from .text_baseline import TextBaseline, TextBaselineCfg
from .vision_encoder import VisionEncoder, VisionEncoderCfg


@dataclass
class MultimodalCfg:
    text: TextBaselineCfg = field(default_factory=TextBaselineCfg)
    vision: VisionEncoderCfg = field(default_factory=VisionEncoderCfg)
    hidden_dim: int = 512
    num_classes: int = 3
    dropout: float = 0.1
    modality_dropout: float = 0.0


class MultimodalLateFusion(nn.Module):
    def __init__(self, cfg: MultimodalCfg):
        super().__init__()
        self.cfg = cfg
        self.text = TextBaseline(cfg.text)
        self.vision = VisionEncoder(cfg.vision)
        text_dim = self.text.classifier.in_features
        image_dim = self.vision.out_dim
        self.head = LateFusionHead(text_dim, image_dim, cfg.hidden_dim, cfg.num_classes, cfg.dropout)

    def forward(self, input_ids, attention_mask, images, image_mask=None) -> torch.Tensor:
        text_emb = self.text.text_embedding(input_ids, attention_mask)
        image_emb = self.vision.encode(images)
        # Modality dropout: drop image with prob p during training, OR drop per-sample
        # if image_mask explicitly marks missing.
        if image_mask is not None:
            image_emb = image_emb * image_mask.unsqueeze(-1).float()
        if self.training and self.cfg.modality_dropout > 0:
            drop_mask = (torch.rand(image_emb.size(0), device=image_emb.device)
                         > self.cfg.modality_dropout).float().unsqueeze(-1)
            image_emb = image_emb * drop_mask
        return self.head(text_emb, image_emb)

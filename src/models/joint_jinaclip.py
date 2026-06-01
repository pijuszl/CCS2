"""Joint alt model: jinaai/jina-clip-v2 -> MLP head.

jina-clip-v2 is multilingual (incl. Lithuanian), 512² images, long text. Both
modalities share an embedding space; we concat the two embeddings and run a
small MLP.

Loaded lazily; transformers handles the weights.
"""
from __future__ import annotations

from dataclasses import dataclass

import torch
import torch.nn as nn


@dataclass
class JinaClipCfg:
    model_name: str = "jinaai/jina-clip-v2"
    num_classes: int = 3
    hidden_dim: int = 512
    dropout: float = 0.1


class JinaClipMLP(nn.Module):
    def __init__(self, cfg: JinaClipCfg):
        super().__init__()
        from transformers import AutoModel
        self.cfg = cfg
        self.backbone = AutoModel.from_pretrained(cfg.model_name, trust_remote_code=True)
        # jina-clip-v2 exposes encode_text + encode_image. The embedding dim is
        # available as self.backbone.config.projection_dim or .text_config.embed_dim.
        # We detect dynamically at first forward via a dummy.
        self._emb_dim: int | None = None
        self.head: nn.Module | None = None
        self.cfg_hidden = cfg.hidden_dim
        self.cfg_dropout = cfg.dropout
        self.num_classes = cfg.num_classes

    def _build_head(self, dim: int) -> nn.Module:
        return nn.Sequential(
            nn.LayerNorm(2 * dim),
            nn.Linear(2 * dim, self.cfg_hidden),
            nn.GELU(),
            nn.Dropout(self.cfg_dropout),
            nn.Linear(self.cfg_hidden, self.num_classes),
        )

    def forward(self, texts: list[str], images) -> torch.Tensor:
        t_emb = self.backbone.encode_text(texts)
        i_emb = self.backbone.encode_image(images)
        if isinstance(t_emb, (list, tuple)):
            t_emb = torch.stack(list(t_emb))
        if isinstance(i_emb, (list, tuple)):
            i_emb = torch.stack(list(i_emb))
        if self._emb_dim is None:
            self._emb_dim = t_emb.shape[-1]
            self.head = self._build_head(self._emb_dim).to(t_emb.device)
        return self.head(torch.cat([t_emb, i_emb], dim=-1))

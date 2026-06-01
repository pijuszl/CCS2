"""XLM-R text baseline. 3-class head."""
from __future__ import annotations

from dataclasses import dataclass

import torch
import torch.nn as nn


@dataclass
class TextBaselineCfg:
    model_name: str = "xlm-roberta-base"
    num_classes: int = 3
    freeze_until_layer: int = 0
    dropout: float = 0.1


class TextBaseline(nn.Module):
    """Returns logits over `num_classes`."""

    def __init__(self, cfg: TextBaselineCfg):
        super().__init__()
        from transformers import AutoConfig, AutoModel
        self.cfg = cfg
        hf_cfg = AutoConfig.from_pretrained(cfg.model_name)
        self.backbone = AutoModel.from_pretrained(cfg.model_name)
        self.dropout = nn.Dropout(cfg.dropout)
        self.classifier = nn.Linear(hf_cfg.hidden_size, cfg.num_classes)
        self._maybe_freeze()

    def _maybe_freeze(self):
        if self.cfg.freeze_until_layer <= 0:
            return
        for name, p in self.backbone.named_parameters():
            if "embeddings" in name:
                p.requires_grad = False
            else:
                # Layer index extraction.
                if ".layer." in name:
                    try:
                        idx = int(name.split(".layer.")[1].split(".")[0])
                        if idx < self.cfg.freeze_until_layer:
                            p.requires_grad = False
                    except ValueError:
                        pass

    def text_embedding(self, input_ids, attention_mask) -> torch.Tensor:
        out = self.backbone(input_ids=input_ids, attention_mask=attention_mask)
        # XLM-R: pooler is None; use CLS token (first position).
        hidden = out.last_hidden_state
        cls = hidden[:, 0]
        return cls

    def forward(self, input_ids, attention_mask) -> torch.Tensor:
        emb = self.text_embedding(input_ids, attention_mask)
        return self.classifier(self.dropout(emb))

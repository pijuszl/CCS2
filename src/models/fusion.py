"""Late-fusion head: LayerNorm(concat) -> Linear -> GELU -> Dropout -> Linear."""
from __future__ import annotations

import torch
import torch.nn as nn


class LateFusionHead(nn.Module):
    def __init__(self, text_dim: int, image_dim: int, hidden_dim: int = 512,
                 num_classes: int = 3, dropout: float = 0.1):
        super().__init__()
        self.norm = nn.LayerNorm(text_dim + image_dim)
        self.fc1 = nn.Linear(text_dim + image_dim, hidden_dim)
        self.act = nn.GELU()
        self.drop = nn.Dropout(dropout)
        self.fc2 = nn.Linear(hidden_dim, num_classes)

    def forward(self, text_emb: torch.Tensor, image_emb: torch.Tensor) -> torch.Tensor:
        x = torch.cat([text_emb, image_emb], dim=-1)
        x = self.norm(x)
        x = self.fc1(x)
        x = self.act(x)
        x = self.drop(x)
        return self.fc2(x)

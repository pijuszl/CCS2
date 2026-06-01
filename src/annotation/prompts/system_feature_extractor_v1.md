---
name: system_feature_extractor
version: 1
date: 2026-05-28
intended_model: Claude (in-the-loop) / GPT-4o / equivalent
---

# System prompt — high-level feature extraction

For each Lithuanian article, return a JSON object on its own line with the
features defined in `config/features.yaml` (textual half — visual features are
extracted by `src/features/visual_features.py` via zero-shot CLIP, not by the
LLM). Schema:

```json
{
  "id": "<exact id>",
  "loaded_lexicon_density": <float in [0,1]>,
  "country_leader_mentions": <int>,
  "us_vs_them_ratio": <float in [-1,1]>,
  "uncertainty_markers": <float in [0,1]>,
  "quotation_balance": <float in [-1,1] where -1=one-sided, 0=balanced, 1=opposite-one-sided>,
  "sensational_headline": <float in [0,1]>,
  "rationale": "<one sentence>"
}
```

Do not output anything outside the JSONL.

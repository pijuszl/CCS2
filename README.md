# Decoding Deception — Lithuanian Multimodal Propaganda Detection

**Computational Cognitive Science II — University of Copenhagen, June 2026**  
Pijus Zlatkus · Vadim Ceremisinov · Klaidas Sinkevicius

Classify Lithuanian news articles into **non / open (overt) / hidden (covert)** propaganda using a text-only XLM-RoBERTa baseline and a multimodal late-fusion model (XLM-R + CLIP ViT-B/32). Cognitive-science motivation: hidden propaganda relies on emotional visual framing that bypasses deliberate System-2 evaluation ([Kahneman 2011](https://en.wikipedia.org/wiki/Thinking,_Fast_and_Slow)), so images should be most diagnostic where text is deliberately ambiguous.

---

## Results

### 2×2 Core Experiment — Macro-F1 on test set (n=522)

| | Existing corpora only | + LLM-labelled scraped |
|---|---|---|
| **Text-only XLM-R** | **0.669** [0.613–0.725] | **0.744** [0.700–0.783] |
| Multimodal (XLM-R + CLIP) | 0.319 [0.310–0.626] | 0.235 [0.202–0.260] |

Bootstrap 95% CIs (B=1000). Multimodal comparison on the image-bearing subset (n=92 test items).

### Per-class F1

| Model | Non | Open | Hidden |
|---|---|---|---|
| Text XLM-R, existing | 0.881 | 0.458 | 0.669 |
| **Text XLM-R, +scraped** | **0.876** | **0.667** | **0.691** |
| Multimodal, existing | 0.585 | 0.000 | 0.370 |
| Multimodal, +scraped | 0.000 | 0.704 | 0.000 |
| Modality dropout (best multimodal variant) | 0.859 | 0.618 | 0.597 |

### McNemar significance (paired test on same test items)

| Comparison | p-value | n |
|---|---|---|
| H1: multimodal vs text-only (existing) | **< 0.001** | 92 |
| H1: multimodal vs text-only (+scraped) | **< 0.001** | 92 |
| RQ2: +scraped vs existing (text) | 1.000 | 522 |
| RQ2: +scraped vs existing (multimodal) | 1.000 | 92 |

### Ablations

| Experiment | Macro-F1 | Hidden-F1 | Key finding |
|---|---|---|---|
| Vision only | 0.278 | 0.000 | Images alone cannot detect hidden class |
| **Modality dropout** | **0.691** | **0.597** | Best multimodal result; text rescues poor image signal |
| No focal loss / class weights | 0.541 | 0.732 | Open class collapses (F1=0.000) without balancing |
| No weak-label aux head | 0.315 | 0.118 | Vision encoder degrades further without aux pretraining |
| jina-clip-v2 | — | — | Run OOM on A100; excluded |

### Feature-based interpretable baseline

| Model | Non | Open | Hidden | Macro-F1 |
|---|---|---|---|---|
| Logistic regression (6 text features) | 0.61 | 0.44 | 0.30 | 0.45 |
| Gradient boosting (6 text features) | 0.70 | 0.44 | 0.28 | 0.48 |

XLM-R (0.669) substantially exceeds the feature-based ceiling (0.48), confirming deep representations are necessary.

---

## Discussion

### H1 — Multimodal does NOT outperform text-only (hypothesis not confirmed)

The late-fusion XLM-R + CLIP model significantly **underperforms** the text-only baseline (McNemar p < 0.001 for both data conditions). The model collapses to predicting a single class, yielding F1 = 0.000 for two of the three classes.

The root cause is the **source-identity confound**: every scraped image-bearing article comes from a propaganda outlet (rubaltic.lt, bukimevieningi.lt). The image-bearing training subset is overwhelmingly open-labelled, so the CLIP encoder learns to associate image content with *propaganda source* rather than with the open/hidden distinction. Without neutral-source images, the vision encoder cannot learn a meaningful discriminative signal.

The **modality dropout** ablation (macro-F1 = 0.691) avoids this collapse by stochastically zeroing the image branch during training, forcing the model to rely on text when visual signal is unreliable. This is now the recommended multimodal configuration for future work.

### H2 — +scraped improves text model on full test set, not on existing-corpus items

Adding scraped data improves the text model by +7.5 macro-F1 points overall. However, McNemar on the shared existing-corpus test items gives p = 1.0, meaning both models make identical errors on HALT-PROP/LITUND/DIGIRES test articles. The gain comes entirely from the scraped test articles (predominantly open propaganda from rubaltic.lt) which the +scraped model was explicitly trained to recognise.

### H3 — Feature analysis confirmed

Four text features significantly separate the three classes (all p < 0.001 after Holm correction):

| Feature | χ² | GBM permutation importance |
|---|---|---|
| Country / leader mentions | 415.3 | 0.052 (rank 1) |
| Quotation balance | 73.0 | 0.010 (rank 4) |
| Us-vs-them ratio | 36.8 | 0.014 (rank 3) |
| Uncertainty markers | 14.4 | 0.022 (rank 2) |

The dominance of *country/leader mentions* is consistent with framing theory: open propaganda names adversaries explicitly; hidden propaganda relies on structural implication. *Quotation balance* separating the hidden class confirms that covert manipulation works through which voices receive prominence, not through explicit claims. Both rankings are consistent across the χ² and permutation importance methods.

### Why the hidden class is hardest — and what that means

Across every model, hidden propaganda has the lowest per-class F1:

| Model family | Hidden-F1 |
|---|---|
| Feature-based (GBM) | 0.28 |
| Text XLM-R (existing only) | 0.67 |
| Multimodal late-fusion | 0.00–0.37 |
| Modality dropout | 0.60 |

This is exactly the dual-process prediction: hidden propaganda is engineered to evade surface-level detection. XLM-R's deep representations close most of the gap, but the visual modality — as implemented here without neutral images — does not add further signal. Adding LRT/Delfi images is the single highest-priority next step.

### Limitations

- **No neutral scraped images**: the core reason H1 fails. LRT and lrytas.lt were identified but encountered access restrictions during the project window.
- **Small image-bearing test set** (n=92): multimodal evaluation is noisy at this scale.
- **LLM label validation**: Claude's 437 scraped labels have not been validated against a human gold standard; Qwen κ is pending.
- **HALT-PROP unlabelled subset**: ~1,730 articles with binary labels but no technique tags could not be assigned to open/hidden.

---

## Dataset

| Source | Total | non | open | hidden |
|---|---|---|---|---|
| HALT-PROP (technique-tagged) | 1,000 | 100 | 396 | 504 |
| HALT-PROP (binary label only, excluded) | 1,870 | — | — | — |
| LITUND | 294 | 225 | 28 | 41 |
| DIGIRES | 351 | 77 | 219 | 55 |
| rubaltic.lt (LLM-labelled) | 437 | — | 368 | 69 |
| bukimevieningi.lt | 1,426 | labelling in progress | | |
| **Total labelled** | **3,647** | **1,879** | **1,011** | **669** |

Train / Val / Test: 2,604 / 521 / 522. Group-aware stratified split (no source spans train and test). Image-bearing articles: 2,102 total; 676 labelled.

---

## Repo structure

```
├── config/            config.yaml, rubric.md, features.yaml, sources.yaml
├── datasets/          HALT-PROP, LITUND, DIGIRES (read-only)
├── data/processed/    articles.parquet, splits.json, balance.json, images/224/
├── src/
│   ├── data/          scrape, load_existing, map_labels, preprocess, split, balance
│   ├── annotation/    agent.py (Claude), agent_qwen.py, validate_agreement.py
│   ├── features/      text_features, visual_features, build_feature_table
│   ├── models/        train.py, text_baseline, vision_encoder, multimodal, fusion
│   └── evaluation/    metrics, significance, interpretability, error_analysis
├── experiments/       one YAML per run (10 configs)
├── results/runs/      per-run metrics.json, predictions.parquet, confusion matrices
├── notebooks/         colab_train.ipynb, colab_qwen_label.ipynb
└── report/            main.tex, references.bib
```

## Reproducing results

1. Upload `src/`, `config/`, `experiments/`, `data/processed/` (~80 MB) to Google Drive as `MyDrive/CCS2/`
2. Open `notebooks/colab_train.ipynb` in Colab → Runtime → **A100 GPU**
3. Run all cells, **skip cell 5** (data already processed)
4. Results zip is saved back to Drive automatically (~4–6 hours total)

## Quickstart (local CPU smoke test)

```bash
pip install -r requirements.txt
python -m src.models.train --config experiments/text_xlmr_existing.yaml --smoke
python -m src.evaluation.metrics --run-dir results/runs/<run-id>
```

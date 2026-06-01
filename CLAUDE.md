# CLAUDE.md

Project context for coding agents. **Decoding Deception: A Multimodal Approach to Propaganda Detection in Lithuanian News Media.** Course: Computational Cognitive Science II (multimodality in communication/cognition), UCPH. Project type: multimodal corpus study — annotation + statistics + deep learning.

## Goal

Classify Lithuanian news articles into **non-propaganda / open (overt) propaganda / hidden (covert) propaganda**. Test (1) whether a text+image model beats a text-only baseline, especially on the hard *hidden* class, (2) whether adding an LLM-labelled scraped set helps, and (3) which high-level human-defined features separate the classes. Cog-sci hook: hidden propaganda relies on emotional *visual framing* that bypasses deliberate (System-2) scrutiny, so the visual modality should expose manipulation that ambiguous text hides (dual-process theory; framing/agenda-setting).

## Research questions & hypotheses

- **RQ1:** Does multimodal (text+image) beat text-only at 3-class classification, especially on *hidden*?
- **RQ2:** Does adding the LLM-labelled scraped set improve performance?
- **RQ3:** Which high-level features most distinguish non/open/hidden?
- **H1:** Multimodal > text-only on macro-F1, largest gain on *hidden*.
- **H2:** A small set of interpretable features reliably separates open from hidden ("cognitive triggers").

Anchor novelty against existing **text-only** Lithuanian dual-input propaganda work (EPJ Data Science 2026): our contribution is the visual modality + the open/hidden taxonomy + agentic labelling.

## Data

**Existing corpora (in `datasets/`, available, text-only — no images):**
- **HALT-PROP** (DOI 10.1038/s41597-025-06367-w): 2,870 articles binary propaganda-presence + 1,000-article subset with technique/narrative tags.
- **LITUND**: fact-checker-sourced unreliable news.
- **DIGIRES**: COVID-19 disinfo corpus + ML dataset (CLARIN-LT), topic-narrow.

**Label mapping to {non, open, hidden}:** the corpora don't use this taxonomy, so map via HALT-PROP technique tags — overt techniques (name-calling, loaded language, slogans, explicit appeals) → **open**; subtle techniques (selective framing, whataboutism, appeal to authority, vagueness, implicit narrative) → **hidden**; none → **non**. Keep `native_label` for traceability; document the mapping as a method choice and validity threat.

**Scraped data (in `data/`, text + images):** config-driven scrape from provided seed URLs/sublinks. Each source tagged `source_type: propaganda|neutral` (e.g. Sputnik LT = propaganda; LRT, lrytas, Delfi = neutral). Per post, save text + main image (if present) + metadata; respect robots.txt, rate-limit, cache HTML. Existing corpora supply only text; **all multimodality comes from scraping.**

**Weak labeling for images (source prior):** scraped images inherit a **binary** label from source_type (propaganda-site image → `propaganda`, neutral-site image → `non`). Source can't distinguish open vs hidden, so image weak labels stay binary; the article-level task remains 3-class. Treat weak labels as **noisy supervision**: a propaganda outlet may run a neutral stock photo and vice-versa. Mitigations baked in: dedup images; strip/avoid outlet logos & watermarks so the vision encoder learns content, not branding (shortcut-learning risk); down-weight or use a noise-robust loss on the weak head; and **evaluate only on the human-verified gold set, never on weak labels**. Note that source is a confound across scraped text+image — the existing corpora and the gold subset guard against the model simply exploiting source.

## Annotation

- **Scraped text → 3-class** via an LLM agent: summarise framing + extract claims → classify against the rubric with few-shot exemplars → self-consistency (sample N, majority vote) → `{label, confidence, rationale, features}` → abstain below threshold (route to human).
- **Human gold:** stratified ≥150–200 items, ≥2 annotators. Report agent-vs-human **Cohen's κ**, per-class P/R, confusion matrix. Use agent labels only if κ ≥ ~0.6; otherwise discuss. Prompts versioned in `annotation/prompts/`; log model/version/temperature/date.
- **Rubric** with 3–5 worked examples per class in `config/rubric.md`, written before labelling; governs both the agent and humans.

## Architecture

- **Text baseline:** fine-tune `xlm-roberta-base` (→ `large` if compute allows), max_len 256–512 (truncate or sliding-window pooling).
- **Vision encoder:** CLIP ViT-B/32 image tower or `vit-base-patch16-224` or ResNet-50; freeze early layers, fine-tune top. (Vanilla OpenAI CLIP's text tower is English/77-token, so CLIP is used for vision only.)
- **Multimodal (primary):** late fusion — concat [text_emb ‖ image_emb] → LayerNorm → Linear → GELU → Dropout → Linear(3-class softmax).
- **Weak-label use:** auxiliary binary image head (multi-task) trained on the weak image labels to shape the vision encoder; the main 3-class head is article-level. Optionally pre-fine-tune the vision encoder on the binary weak set first.
- **Joint alt (comparison):** `jinaai/jina-clip-v2` (multilingual ~89 langs incl. Lithuanian, 512² images, long text) text+image embeddings → MLP head.
- Mixed precision, gradient accumulation, early stop on val macro-F1, save best checkpoint.

## High-level features (H2)

Define in `config/features.yaml`.
- **Visual:** national symbol, military presence, known public figure, crowd/protest, map/territory, religious symbol, agriculture/rural, emotional facial expression, image emotional valence (−/0/+).
- **Textual:** loaded/emotive lexicon density, named entities (country/leader), us-vs-them framing, modal/uncertainty markers, quotation balance, sensational-headline markers.
Extract via LLM structured (JSON) output for both modalities; zero-shot CLIP / object detection for visual; LT lexica/NER for textual. `features/build_feature_table.py` → one row per item.

## Experimental design

2×2: dataset {existing-only, existing+LLM-augmented} × modality {text-only XLM-R, multimodal late-fusion}. Keep the modality comparison (H1) on the **same image-bearing subset** (report N). Limited ablations only: vision-only sanity baseline, jina-clip-v2 joint model, modality-dropout robustness, with/without balancing, with/without weak-label auxiliary head. One config per run in `experiments/`.

## Splits, balancing, evaluation

- **Splits:** group-aware (no same outlet/event/template across splits), stratified by class, split **before** balancing, freeze test.
- **Balancing (train only):** class weights / focal loss (preferred). No SMOTE on raw text/images.
- **Metrics:** macro-F1 (headline; handles imbalance) + micro-F1, per-class precision/recall, confusion matrices. Not raw accuracy.
- **Significance:** **McNemar's test** for two classifiers on the same test set; **bootstrap CIs** on macro-F1. For >2 conditions use an omnibus test + corrected post-hoc (no pile of independent t-tests).
- **H2 / cognition:** **χ²** for feature–class association; **SHAP** on a feature-based interpretable model (logistic regression / gradient-boosted trees fitted on the high-level feature table). Deep-model attributions (Captum text, Grad-CAM image) are supplementary.
- **Error analysis:** sample misclassifications, tag open↔hidden confusions and Lithuanian cultural/historical nuance. Report negative results honestly.

## Repo structure

```
propaganda-lt/
├── CLAUDE.md  README.md  requirements.txt
├── config/        config.yaml  rubric.md  features.yaml  sources.yaml   # seed URLs/sublinks + source_type
├── datasets/      # existing corpora (HALT-PROP, LITUND, DIGIRES) + DATA_LICENSES.md
├── data/          raw/ interim/ processed/ annotations/   # scraped data we collect; llm_labels.jsonl, human_gold.jsonl
├── src/
│   ├── data/        scrape.py  load_existing.py  map_labels.py  weak_label_images.py  preprocess.py  split.py  balance.py
│   ├── annotation/  agent.py  prompts/  validate_agreement.py
│   ├── features/    text_features.py  visual_features.py  build_feature_table.py
│   ├── models/      text_baseline.py  vision_encoder.py  fusion.py  multimodal.py  train.py  predict.py
│   ├── evaluation/  metrics.py  significance.py  interpretability.py  error_analysis.py
│   └── utils/       seed.py  io.py  logging.py
├── experiments/   # one yaml per run
├── results/       figures/ tables/ logs/ checkpoints/
└── report/        # LuaLaTeX on Overleaf: main.tex  sections/  figures/  references.bib (biblatex style=apa, biber)
```
`datasets/` = third-party (read-mostly); `data/` = everything we collect/produce. Never commit raw scraped data or API keys (`.env` + `.gitignore`).

## Build order

1. `config/sources.yaml` (seed URLs/sublinks + source_type) and `config/rubric.md`.
2. `load_existing.py` → common schema `{id, text, image_path?, source, source_type, native_label}`; `map_labels.py`.
3. `scrape.py` → text+image+metadata to `data/raw/`; `weak_label_images.py` (binary image labels by source_type).
4. `agent.py` (3-class scraped text) → `validate_agreement.py` (κ vs gold).
5. `preprocess.py` (keep LT diacritics; image resize 512²/224²; dedup; strip logos) → `split.py` → `balance.py`.
6. `build_feature_table.py`.
7. `train.py` for the 4 runs + ablations.
8. `metrics.py` / `significance.py` / `interpretability.py` / `error_analysis.py`; export figures/tables.

## Environment & compute

Python 3.10+, PyTorch, HF `transformers`/`datasets`, `scikit-learn`, `shap`, `lime`, `captum`, CLIP/jina deps, an LLM API client. Pin versions. Log seeds + git hash + config per run. Train on Hendrix/Colab Pro (not locally); configurable batch size / grad-accum; checkpoint to `results/checkpoints/`.

## Ethics

Respect robots.txt/ToS, rate-limit, cache. GDPR: news images show identifiable people — store minimally, academic purpose, no redistribution beyond license. Frame outputs as article-level classification under a documented rubric; acknowledge source-prior bias (weak labels and scraping both leak source) and make no deployment/censorship claims. One short report paragraph on this.

## Report

LuaLaTeX on Overleaf; APA via `biblatex` (`style=apa`, `biber`). 3-student group → 8–10 standard pages, where a standard page = 2,400 keystrokes incl. spaces (cover/ToC/bibliography/abstract/appendices excluded). Mark per-section authorship; joint part ≤50%. Structure: Abstract; Introduction (problem, gap, RQ+hypotheses, paper structure); Related work (multimodal ML — Liang et al. 2023; propaganda detection; multilingual transformers; open/hidden distinction); Data (corpora, mapping, scraping, weak labels, agent κ); Method & tools; Results & evaluation (2×2 table, per-class F1, H1 with McNemar/bootstrap, H2 with χ²/SHAP); Discussion (interpret features via cog-sci, assess vs RQ/hypotheses, limitations); Conclusion/future work; References. Figures: 2×2 macro-F1 bars, per-class confusion matrices, SHAP summary, example Grad-CAM.

## References seed (`report/references.bib`) — verify APA 7, cite only what you use

Liang, Zadeh & Morency (2023) multimodal ML survey (DOI 10.1145/3656580); HALT-PROP (10.1038/s41597-025-06367-w); Lithuanian dual-input (10.1140/epjds/s13688-026-00648-z); jina-clip-v2 (arXiv 2412.08802); Conneau et al. 2020 (XLM-R); Radford et al. 2021 (CLIP); Dosovitskiy et al. 2021 (ViT); Lin et al. 2017 (focal loss); Lundberg & Lee 2017 (SHAP); Ribeiro et al. 2016 (LIME); Entman 1993 (framing); Kahneman 2011 (dual-process); Perneger & Hudelson 2004 (research-question criteria). Add: LITUND and DIGIRES/CLARIN-LT dataset citations; any LT NER/lexicon resources.
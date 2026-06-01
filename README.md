# Decoding Deception — Lithuanian Multimodal Propaganda Detection

Course project for **Computational Cognitive Science II (UCPH)**. Classify Lithuanian news articles into
`non / open / hidden` propaganda using a text-only baseline (XLM-R) and a multimodal late-fusion model
(XLM-R + CLIP). See `CLAUDE.md` for the full project spec.

## Quickstart (local CPU smoke test)

```bash
python -m venv .venv
. .venv/Scripts/activate          # Windows PowerShell: . .venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 1. Load the three existing corpora into a common schema
python -m src.data.load_existing --all

# 2. Map native labels to {non, open, hidden}
python -m src.data.map_labels

# 3. Group-aware stratified split (writes data/processed/splits.json)
python -m src.data.split

# 4. Build text-only feature table (visual features need scraped images)
python -m src.features.build_feature_table --text-only

# 5. Smoke-train the text baseline (1 epoch, tiny subset)
python -m src.models.train --config experiments/text_xlmr_existing.yaml --smoke

# 6. Evaluate
python -m src.evaluation.metrics --run-dir results/runs/<run-id>
```

## Tests

```bash
pytest -q
```

## Scraping

1. Fill in seed URLs in `config/sources.yaml` (template provided; replace the TODO).
2. `python -m src.data.scrape --limit 10 --dry-run` to sanity-check.
3. `python -m src.data.scrape` for the real run. Output: `data/raw/scraped.jsonl` + `data/raw/images/`.
4. `python -m src.data.weak_label_images` adds binary image labels from `source_type`.

## LLM labelling (Claude Code in the loop)

The agentic 3-class labeller is **not** an API caller. It batches articles for a human (or
Claude Code) to label deterministically:

```bash
python -m src.annotation.agent make-batches \
    --input data/raw/scraped.jsonl \
    --batch-size 20 \
    --out data/annotations/batches/
```

Then open each `batch_NNNN.input.md` in Claude Code, follow the in-file instructions, and fill the
matching `batch_NNNN.output.jsonl`. Finally:

```bash
python -m src.annotation.agent merge-batches --batches data/annotations/batches/
python -m src.annotation.validate_agreement \
    --llm data/annotations/llm_labels.jsonl \
    --gold data/annotations/human_gold.jsonl
```

The validator prints Cohen's κ; gate at κ ≥ 0.6 per CLAUDE.md.

## Cross-validating Claude's labels with Qwen3-Next-80B

Two-LLM agreement (Cohen's κ) checks that the labels don't depend on which LLM
read them. `src/annotation/agent_qwen.py` runs `Qwen/Qwen3-Next-80B-A3B-Thinking`
over the same 437 rubaltic articles with the same rubric and few-shot exemplars.
The output `data/annotations/llm_labels_qwen.jsonl` matches Claude's schema, so
the comparison is one command:

```bash
python -m src.annotation.validate_agreement \
    --llm  data/annotations/llm_labels.jsonl \
    --gold data/annotations/llm_labels_qwen.jsonl \
    --report results/tables/agreement_claude_vs_qwen.json
```

The 80B-A3B MoE needs ~40GB VRAM at int4. Use `notebooks/colab_qwen_label.ipynb`
on a Colab A100 — ~2–5 hours for the full 437 articles. The notebook supports
`--resume` so a disconnected session can be restarted.

If κ ≥ 0.7, labels are robust to which LLM produced them (good methodology note).
If κ is low, the disagreement set in
`results/tables/disagreements_claude_vs_qwen.csv` is the stratified sample your
human gold subset should focus on.

## Vision aux pretraining (binary weak labels)

`experiments/vision_aux_pretrain.yaml` fine-tunes the vision encoder on the
binary `{non, propaganda}` weak labels in `data/interim/image_weak_labels.parquet`.
After the LITUND image scrape, the parquet has 1983 unique images split
145 / 1838 (`non` / `propaganda`) — a 12.7× imbalance, so `balance.py` writes
`balance_binary.json` with class weights and `train.py` automatically uses
focal loss with the binary alpha on this experiment.

```
python -m src.data.balance                          # writes balance_binary.json
python -m src.models.train --config experiments/vision_aux_pretrain.yaml
```

The resulting checkpoint can be loaded into `experiments/multimodal_*.yaml`
runs via a `pretrained_vision:` key (supported in `vision_encoder.py`).

## Colab (GPU training)

Open `notebooks/colab_train.ipynb`. The notebook mounts Drive, clones this repo, installs deps,
then calls `src/models/train.py` with one of the YAML configs under `experiments/`. All training
logic lives in `train.py` — the notebook is a thin shell.

## Repo layout

See `CLAUDE.md` § "Repo structure". The key idea: `datasets/` is read-only third-party corpora;
`data/` is everything we collect or derive. Never commit raw scraped data or images.

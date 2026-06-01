"""Label scraped articles with Qwen3-Next-80B-A3B-Thinking for cross-validation.

Supports two backends:

1. transformers:
   - fp16
   - bf16
   - int8
   - int4 via BitsAndBytes

2. gguf:
   - llama.cpp / llama-cpp-python GGUF files, e.g. UD-Q4_K_XL

Examples:

Transformers int4:
    python -m src.annotation.agent_qwen \
        --input data/raw/scraped.jsonl \
        --source rubaltic_lt \
        --backend transformers \
        --quantization int4 \
        --resume

GGUF UD-Q4_K_XL:
    python -m src.annotation.agent_qwen \
        --input data/raw/scraped.jsonl \
        --source rubaltic_lt \
        --backend gguf \
        --gguf-path models/Qwen3-Next-80B-A3B-Thinking-UD-Q4_K_XL.gguf \
        --limit 5 \
        --out data/annotations/llm_labels_qwen_smoke.jsonl
"""
from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path
from typing import Any

from src.utils import append_jsonl, ensure_dir, get_logger, read_jsonl

log = get_logger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROMPTS_DIR = Path(__file__).parent / "prompts"

DEFAULT_MODEL = "Qwen/Qwen3-Next-80B-A3B-Thinking"


def _resolve_path(path_str: str | None) -> Path | None:
    if path_str is None:
        return None
    p = Path(path_str)
    return p if p.is_absolute() else PROJECT_ROOT / p


def _load_prompts() -> tuple[str, str]:
    sys_p = (PROMPTS_DIR / "system_classifier_v1.md").read_text(encoding="utf-8")
    fs = (PROMPTS_DIR / "fewshot_examples_v1.md").read_text(encoding="utf-8")
    return sys_p, fs


def _build_messages(system_prompt: str, fewshot: str, article: dict) -> list[dict[str, str]]:
    """Same prompt content as the Claude-in-the-loop batches; one article per call."""
    user = (
        "You will classify a single Lithuanian news article into one of "
        "`non`, `open`, `hidden` (per the rubric below). "
        "Output EXACTLY one JSON object with the schema specified, and nothing else.\n\n"
        "## System prompt\n\n" + system_prompt.strip() + "\n\n"
        "## Few-shot exemplars\n\n" + fewshot.strip() + "\n\n"
        "## Article to label\n\n"
        f"id: {article['id']}\n"
        f"Title: {article.get('title', '').strip()}\n"
        f"Source: {article.get('source', '?')} ({article.get('source_type', '?')})\n\n"
        "Text:\n```\n" + article.get("text", "").strip() + "\n```\n\n"
        "Now produce ONE JSON object on a single line. The `id` field must be "
        f"exactly: {article['id']}"
    )

    return [{"role": "user", "content": user}]


def _parse_output(raw: str) -> dict | None:
    """Strip <think>...</think> if present, then extract the first balanced JSON object."""
    if "</think>" in raw:
        raw = raw.split("</think>")[-1]

    depth = 0
    start = None

    for i, c in enumerate(raw):
        if c == "{":
            if depth == 0:
                start = i
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0 and start is not None:
                candidate = raw[start:i + 1]
                try:
                    return json.loads(candidate)
                except json.JSONDecodeError:
                    start = None

    return None


def _messages_to_plain_prompt(messages: list[dict[str, str]]) -> str:
    """Fallback prompt format for GGUF models if chat template is unavailable."""
    parts: list[str] = []

    for m in messages:
        role = m.get("role", "user")
        content = m.get("content", "")
        parts.append(f"<|im_start|>{role}\n{content}<|im_end|>")

    parts.append("<|im_start|>assistant\n")
    return "\n".join(parts)


def _generate_transformers(
    model: Any,
    tok: Any,
    messages: list[dict[str, str]],
    max_new_tokens: int,
    temperature: float,
) -> str:
    import torch

    prompt_str = tok.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    inputs = tok(prompt_str, return_tensors="pt").to(model.device)

    with torch.no_grad():
        out_ids = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=temperature > 0,
            temperature=temperature if temperature > 0 else None,
            top_p=0.95,
            pad_token_id=tok.eos_token_id,
        )

    new_tokens = out_ids[0][inputs["input_ids"].shape[1]:]
    return tok.decode(new_tokens, skip_special_tokens=True)


def _generate_gguf(
    llm: Any,
    messages: list[dict[str, str]],
    max_new_tokens: int,
    temperature: float,
) -> str:
    """Generate using llama-cpp-python.

    First tries chat completion. If the GGUF metadata/chat template is incompatible,
    falls back to a Qwen-style plain prompt.
    """
    try:
        response = llm.create_chat_completion(
            messages=messages,
            max_tokens=max_new_tokens,
            temperature=temperature,
            top_p=0.95,
            stop=["<|im_end|>", "</s>"],
        )

        return response["choices"][0]["message"]["content"]

    except Exception as e:
        log.warning("GGUF chat completion failed, falling back to plain prompt: %s", e)

        prompt = _messages_to_plain_prompt(messages)

        response = llm(
            prompt,
            max_tokens=max_new_tokens,
            temperature=temperature,
            top_p=0.95,
            stop=["<|im_end|>", "</s>"],
            echo=False,
        )

        return response["choices"][0]["text"]


def _generate(
    backend: str,
    model: Any,
    tok: Any,
    messages: list[dict[str, str]],
    max_new_tokens: int,
    temperature: float,
) -> str:
    if backend == "gguf":
        return _generate_gguf(model, messages, max_new_tokens, temperature)

    return _generate_transformers(model, tok, messages, max_new_tokens, temperature)


def _load_transformers_model(args: argparse.Namespace) -> tuple[Any, Any]:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True)

    load_kwargs: dict[str, Any] = {
        "device_map": "auto",
        "trust_remote_code": True,
    }

    if args.quantization in ("int4", "int8"):
        from transformers import BitsAndBytesConfig

        if args.quantization == "int4":
            load_kwargs["quantization_config"] = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.bfloat16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
            )
        else:
            load_kwargs["quantization_config"] = BitsAndBytesConfig(
                load_in_8bit=True,
            )

    elif args.quantization == "bf16":
        load_kwargs["torch_dtype"] = torch.bfloat16

    elif args.quantization == "fp16":
        load_kwargs["torch_dtype"] = torch.float16

    else:
        raise ValueError(f"Unsupported transformers quantization: {args.quantization}")

    model = AutoModelForCausalLM.from_pretrained(args.model, **load_kwargs)
    model.eval()

    return model, tok


def _load_gguf_model(args: argparse.Namespace) -> tuple[Any, None]:
    if not args.gguf_path:
        raise ValueError("--gguf-path is required when --backend gguf")

    gguf_path = _resolve_path(args.gguf_path)

    if gguf_path is None or not gguf_path.exists():
        raise FileNotFoundError(f"GGUF file not found: {gguf_path}")

    from llama_cpp import Llama

    llm = Llama(
        model_path=str(gguf_path),
        n_ctx=args.n_ctx,
        n_gpu_layers=args.n_gpu_layers,
        n_batch=args.n_batch,
        verbose=args.llama_verbose,
    )

    return llm, None


def main() -> None:
    p = argparse.ArgumentParser()

    p.add_argument(
        "--input",
        default="data/raw/scraped.jsonl",
        help="JSONL with id/title/text/source",
    )
    p.add_argument(
        "--out",
        default="data/annotations/llm_labels_qwen.jsonl",
    )
    p.add_argument(
        "--source",
        default="rubaltic_lt",
        help="Filter input to this source. '' for all.",
    )

    p.add_argument(
        "--backend",
        choices=["transformers", "gguf"],
        default="transformers",
        help="Use transformers or llama.cpp GGUF backend.",
    )

    p.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help="Hugging Face model id for transformers backend.",
    )

    p.add_argument(
        "--gguf-path",
        default=None,
        help="Path to .gguf file, e.g. models/Qwen3-Next-80B-A3B-Thinking-UD-Q4_K_XL.gguf",
    )

    p.add_argument(
        "--max-new-tokens",
        type=int,
        default=4096,
    )
    p.add_argument(
        "--temperature",
        type=float,
        default=0.6,
    )

    p.add_argument(
        "--quantization",
        choices=["fp16", "bf16", "int8", "int4"],
        default="int4",
        help="Only used by transformers backend. GGUF quantization is selected by --gguf-path.",
    )

    p.add_argument(
        "--resume",
        action="store_true",
        help="Skip ids already present in --out so a crashed run can continue.",
    )

    p.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Cap number of articles labelled; useful for smoke tests.",
    )

    # llama.cpp / GGUF settings
    p.add_argument(
        "--n-ctx",
        type=int,
        default=8192,
        help="Context window for GGUF backend.",
    )
    p.add_argument(
        "--n-gpu-layers",
        type=int,
        default=-1,
        help="GGUF backend GPU offload. -1 means try to offload all layers.",
    )
    p.add_argument(
        "--n-batch",
        type=int,
        default=512,
        help="GGUF backend batch size.",
    )
    p.add_argument(
        "--llama-verbose",
        action="store_true",
        help="Show llama.cpp backend logs.",
    )

    args = p.parse_args()

    log.info(
        "loading backend=%s model=%s gguf_path=%s quantization=%s",
        args.backend,
        args.model,
        args.gguf_path,
        args.quantization,
    )

    if args.backend == "gguf":
        model, tok = _load_gguf_model(args)
    else:
        model, tok = _load_transformers_model(args)

    in_path = _resolve_path(args.input)
    out_path = _resolve_path(args.out)

    if in_path is None or not in_path.exists():
        raise FileNotFoundError(f"Input file not found: {in_path}")

    if out_path is None:
        raise ValueError("--out cannot be empty")

    ensure_dir(out_path.parent)

    articles = list(read_jsonl(in_path))

    if args.source:
        articles = [a for a in articles if a.get("source") == args.source]

    log.info("loaded %d articles after source filter=%r", len(articles), args.source)

    if args.resume and out_path.exists():
        done: set[str] = set()

        for r in read_jsonl(out_path):
            if "id" in r:
                done.add(r["id"])

        articles = [a for a in articles if a["id"] not in done]

        log.info("resume: %d already done, %d remaining", len(done), len(articles))

    elif out_path.exists():
        out_path.write_text("", encoding="utf-8")

    if args.limit:
        articles = articles[: args.limit]

    system_prompt, fewshot = _load_prompts()

    t0 = time.time()
    n_ok = 0
    n_bad = 0

    failed_path = out_path.with_name(out_path.stem + "_failed.jsonl")

    for i, article in enumerate(articles, 1):
        try:
            messages = _build_messages(system_prompt, fewshot, article)

            raw = _generate(
                backend=args.backend,
                model=model,
                tok=tok,
                messages=messages,
                max_new_tokens=args.max_new_tokens,
                temperature=args.temperature,
            )

            parsed = _parse_output(raw)

            if parsed and parsed.get("label") in {"non", "open", "hidden"}:
                parsed["id"] = article["id"]
                parsed.setdefault(
                    "provenance",
                    str(args.gguf_path) if args.backend == "gguf" else args.model,
                )
                parsed.setdefault("backend", args.backend)

                append_jsonl(out_path, parsed)
                n_ok += 1

            else:
                append_jsonl(
                    failed_path,
                    {
                        "id": article["id"],
                        "backend": args.backend,
                        "raw": raw[:4000],
                    },
                )
                n_bad += 1
                log.warning("[%d/%d] parse failed for %s", i, len(articles), article["id"])

        except Exception as e:
            n_bad += 1
            append_jsonl(
                failed_path,
                {
                    "id": article.get("id", "?"),
                    "backend": args.backend,
                    "error": str(e),
                },
            )
            log.warning(
                "[%d/%d] generation failed for %s: %s",
                i,
                len(articles),
                article.get("id", "?"),
                e,
            )

        elapsed = time.time() - t0
        rate = i / max(elapsed, 1e-6) * 60
        eta_min = (len(articles) - i) / max(rate, 1e-6)

        log.info(
            "[%d/%d] ok=%d bad=%d %.2f/min ETA=%.1fmin",
            i,
            len(articles),
            n_ok,
            n_bad,
            rate,
            eta_min,
        )

    log.info("DONE. ok=%d bad=%d wrote %s", n_ok, n_bad, out_path)


if __name__ == "__main__":
    main()
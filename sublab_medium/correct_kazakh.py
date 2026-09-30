"""Sublab Medium - one Kazakh-correction task, six models."""

import json
import os
import re
import sys
import time
from pathlib import Path

# Жобаның түбірлік қалтасын қосу
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sublab_easy.registration_bot import (RATES_PER_MTOK,  # noqa: E402
                                           ask_once, estimate_cost)

DATA = Path(__file__).resolve().parent.parent / "data" / "kazakh_errors.json"

# OpenRouter-де нақты жұмыс істейтін тегін модельдер тізімі
MODELS = [
    ("openrouter", "google/gemma-4-26b-a4b-it:free"),
    ("openrouter", "qwen/qwen3.8-27b"),
    ("openrouter", "deepseek/deepseek-v4-flash-0731"),
    ("openai", "gpt-5.6-luna"),
    ("openai", "gpt-5.6-terra"),
    ("openai", "gpt-5.6-sol"),
]

def load_sentences() -> list[dict]:
    """The eight corrupted sentences and their published originals."""
    return json.loads(DATA.read_text(encoding="utf-8"))["sentences"]


def build_prompt(corrupted: str) -> str:
    """Ask for a corrected sentence AND a list of the changes made."""
    return (
        "Fix the errors in this Kazakh text (wrong letters, joined words, Cyrillic/Latin script mix-ups).\n"
        f"Corrupted text: {corrupted}\n\n"
        "Output ONLY a valid raw JSON object with no preamble or markdown fences. "
        "Strict JSON schema:\n"
        '{"corrected": "<corrected sentence>", "changes": ["<change 1>", "<change 2>"]}'
    )


def parse_response(text: str) -> dict:
    """Pull {"corrected": str, "changes": list} out of the model's reply."""
    cleaned = text.strip()

    # Clean markdown code blocks
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    cleaned = cleaned.strip()

    # DeepSeek-R1 / Reasoning модельдерінің <think> ... </think> тегтерін жою
    cleaned = re.sub(r"<think>.*?</think>", "", cleaned, flags=re.DOTALL).strip()

    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        json_str = match.group(0)
        try:
            parsed = json.loads(json_str)
            if isinstance(parsed, dict) and "corrected" in parsed:
                changes = parsed.get("changes", [])
                if not isinstance(changes, list):
                    changes = [str(changes)]
                return {
                    "corrected": str(parsed["corrected"]).strip(),
                    "changes": [str(c) for c in changes],
                }
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Could not extract valid JSON from response: {text!r}")


def correct_with(model: str, corrupted: str, via: str) -> dict:
    """Send one sentence to one model."""
    prompt = build_prompt(corrupted)
    
    # API лимитінен аспау үшін 1 секунд кідіріс
    time.sleep(1.0)
    
    resp = ask_once(prompt, model=model, via=via)
    parsed = parse_response(resp["text"])
    
    return {
        "corrected": parsed["corrected"],
        "changes": parsed["changes"],
        "input_tokens": resp.get("input_tokens", 0),
        "output_tokens": resp.get("output_tokens", 0),
        "model": model,
    }


def score_correction(returned: str, expected: str) -> dict:
    """Compare a model's output against the published original."""
    ret_str = returned.strip()
    exp_str = expected.strip()
    
    exact = ret_str == exp_str
    
    min_len = min(len(ret_str), len(exp_str))
    char_mismatches = sum(1 for i in range(min_len) if ret_str[i] != exp_str[i])
    length_diff = abs(len(ret_str) - len(exp_str))
    
    return {"exact": exact, "char_diff": char_mismatches + length_diff}


def run_all() -> list[dict]:
    """Every model against every sentence."""
    rows = []
    for via, model in MODELS:
        print(f"Running model: {model} ...")
        for s in load_sentences():
            try:
                r = correct_with(model, s["corrupted"], via)
            except Exception as exc:
                rows.append({"model": model, "id": s["id"],
                             "errors": s["errors"], "failed": repr(exc)})
                continue
            rate_in, rate_out = RATES_PER_MTOK.get(model, (0.0, 0.0))
            rows.append({
                "model": model,
                "id": s["id"],
                "errors": s["errors"],
                "corrected": r["corrected"],
                "changes": r["changes"],
                **score_correction(r["corrected"], s["correct"]),
                "cost": estimate_cost(r["input_tokens"], r["output_tokens"],
                                     rate_in, rate_out),
                "input_tokens": r["input_tokens"],
                "output_tokens": r["output_tokens"],
            })
    return rows


def summarise(rows: list[dict]) -> None:
    """Per-model totals, to paste into SUBMISSION.md."""
    print(f"\n{'model':55}{'exact':>7}{'failed':>8}{'tokens':>9}{'cost $':>10}")
    print("-" * 89)
    for _, model in MODELS:
        mine = [r for r in rows if r["model"] == model]
        exact = sum(1 for r in mine if r.get("exact"))
        failed = sum(1 for r in mine if r.get("failed"))
        toks = sum(r.get("input_tokens", 0) + r.get("output_tokens", 0) for r in mine)
        cost = sum(r.get("cost", 0.0) for r in mine)
        print(f"{model:55}{exact:>7}{failed:>8}{toks:>9}{cost:>10.5f}")


if __name__ == "__main__":
    out = run_all()
    summarise(out)
    dest = Path(__file__).resolve().parent.parent / "outputs"
    dest.mkdir(exist_ok=True)
    (dest / "corrections.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwrote outputs/corrections.json ({len(out)} rows)")
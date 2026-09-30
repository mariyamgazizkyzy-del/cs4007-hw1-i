"""Sublab Harder - why Kazakh costs more, and what a homoglyph does to a word."""

import json
import unicodedata
from pathlib import Path

import tiktoken

DATA = Path(__file__).resolve().parent.parent / "data"
PARALLEL = DATA / "parallel.json"
KAZAKH_ERRORS = DATA / "kazakh_errors.json"

ENCODINGS = ["cl100k_base", "o200k_base"]
LANGS = ["kk", "ru", "en"]


def load_triplets() -> list[dict]:
    """Six meanings, each written in Kazakh, Russian and English."""
    return json.loads(PARALLEL.read_text(encoding="utf-8"))["triplets"]


def load_sentences() -> list[dict]:
    """The corrupted Kazakh sentences from Sublab Medium."""
    return json.loads(KAZAKH_ERRORS.read_text(encoding="utf-8"))["sentences"]


# --------------------------------------------------------------------------
# The tokenizer itself
# --------------------------------------------------------------------------

def encode(text: str, encoding_name: str = "o200k_base") -> list[int]:
    """Token ids for `text` under the named encoding."""
    enc = tiktoken.get_encoding(encoding_name)
    return enc.encode(text)


def pieces(ids: list[int], encoding_name: str = "o200k_base") -> list[str]:
    """The text of each token, one string per id."""
    enc = tiktoken.get_encoding(encoding_name)
    res = []
    for token_id in ids:
        raw_bytes = enc.decode_single_token_bytes(token_id)
        res.append(raw_bytes.decode("utf-8", errors="replace"))
    return res


# --------------------------------------------------------------------------
# Pure measurements
# --------------------------------------------------------------------------

def tokens_per_char(text: str, ids: list[int]) -> float:
    """How many tokens each character of `text` cost."""
    if not text:
        return 0.0
    return len(ids) / len(text)


def first_divergence(a: list[int], b: list[int]) -> int | None:
    """Index of the first position where two token streams differ."""
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return i
    if len(a) != len(b):
        return min(len(a), len(b))
    return None


def foreign_chars(text: str) -> list[tuple[int, str, str]]:
    """Every character that is a letter but not a Cyrillic one."""
    res = []
    for i, ch in enumerate(text):
        if ch.isalpha():
            name = unicodedata.name(ch, "")
            if "CYRILLIC" not in name:
                res.append((i, ch, name))
    return res


# --------------------------------------------------------------------------
# A. The price of a language
# --------------------------------------------------------------------------

def language_table(encoding_name: str) -> dict[str, dict]:
    """Total tokens, total characters and tokens-per-character, per language."""
    triplets = load_triplets()
    stats = {lang: {"tokens": 0, "chars": 0, "tok_per_char": 0.0} for lang in LANGS}
    
    for item in triplets:
        for lang in LANGS:
            text = item[lang]
            toks = encode(text, encoding_name)
            stats[lang]["tokens"] += len(toks)
            stats[lang]["chars"] += len(text)

    for lang in LANGS:
        c = stats[lang]["chars"]
        t = stats[lang]["tokens"]
        stats[lang]["tok_per_char"] = t / c if c > 0 else 0.0

    return stats


def cost_per_thousand(tok_per_char: float, chars: int,
                      rate_in: float = 5.00) -> float:
    """What 1,000 sentences of this length would cost as input tokens."""
    tokens_per_sentence = tok_per_char * chars
    total_tokens = tokens_per_sentence * 1000
    return (total_tokens / 1_000_000) * rate_in


# --------------------------------------------------------------------------
# B. What the homoglyph did
# --------------------------------------------------------------------------

def homoglyph_report(corrupted: str, correct: str,
                     encoding_name: str = "o200k_base") -> dict:
    """Side-by-side forensics on one corrupted sentence."""
    cor_ids = encode(correct, encoding_name)
    bad_ids = encode(corrupted, encoding_name)
    
    foreign = foreign_chars(corrupted)
    diverge = first_divergence(cor_ids, bad_ids)
    
    p_cor = pieces(cor_ids, encoding_name)
    p_bad = pieces(bad_ids, encoding_name)
    
    return {
        "foreign": foreign,
        "tokens_correct": len(cor_ids),
        "tokens_corrupted": len(bad_ids),
        "delta": len(bad_ids) - len(cor_ids),
        "diverge_at": diverge,
        "pieces_correct": p_cor,
        "pieces_corrupted": p_bad,
    }


def show_homoglyphs(encoding_name: str = "o200k_base") -> None:
    """Print the report for every latin_homoglyph row in the dataset."""
    rows = [r for r in load_sentences() if "latin_homoglyph" in r["errors"]]
    if not rows:
        print("  no latin_homoglyph rows in the dataset")
        return
    for row in rows:
        rep = homoglyph_report(row["corrupted"], row["correct"], encoding_name)
        print("\n  [%s]  %+d tokens (%d -> %d), diverging at index %s"
              % (row["id"], rep["delta"], rep["tokens_correct"],
                 rep["tokens_corrupted"], rep["diverge_at"]))
        for idx, ch, name in rep["foreign"]:
            print("    char %d is %r - %s" % (idx, ch, name))
        d = rep["diverge_at"] or 0
        print("    correct  : %s" % rep["pieces_correct"][max(0, d - 1):d + 5])
        print("    corrupted: %s" % rep["pieces_corrupted"][max(0, d - 1):d + 5])


if __name__ == "__main__":
    print("=== A. the same six meanings, three languages, two tokenizers ===")
    for enc_name in ENCODINGS:
        table = language_table(enc_name)
        print("\n  %s" % enc_name)
        print("    %-4s %8s %8s %12s" % ("lang", "tokens", "chars", "tok/char"))
        for lang in LANGS:
            row = table[lang]
            print("    %-4s %8d %8d %12.3f"
                  % (lang, row["tokens"], row["chars"], row["tok_per_char"]))
        base = table["en"]["tok_per_char"]
        for lang in LANGS:
            print("    %s costs %.2fx English"
                  % (lang, table[lang]["tok_per_char"] / base))

    print("\n=== B. what a Latin homoglyph does to the token stream ===")
    show_homoglyphs("o200k_base")

    print("\n=== C. did the newer tokenizer narrow the gap? ===")
    old, new = (language_table(e) for e in ENCODINGS)
    for lang in LANGS:
        print("  %s: %.3f -> %.3f tok/char"
              % (lang, old[lang]["tok_per_char"], new[lang]["tok_per_char"]))
    print("\n  Now answer question 2 in SUBMISSION.md, with these numbers in hand.")
    
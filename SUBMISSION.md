# HW1 submission

**Name:**
**Student ID:**
**Group:**
**Repository:**

## AI tool disclosure

State which AI tools you used and for what. Expected and fine; undisclosed use
is not.

>

---

## Sublab Easy — the registration bot and its bill

**How I laid the catalogue out inside the system prompt, and why:**

>

**My turn 5 (Kazakh or Russian):**

>

### Run 1 — OpenAI, `gpt-5.6-luna`

| Turn | Input tokens | Output tokens | Cost $ |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| **total** | | | |

### Run 2 — OpenRouter, `google/gemma-4-26b-a4b-it:free`

| Turn | Input tokens | Output tokens | Cost $ |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| **total** | | | |

### Turn 4, verbatim

The turn where you asked for CSS-4090, which does not exist. Paste both replies
exactly as they came back — do not tidy them.

**OpenAI:**

```

```

**OpenRouter:**

```

```

### Written answers

**1. The two providers used almost identical code. What actually changed, and
what did not?**

>

**2. Why did the input token count climb on every turn when your questions
stayed roughly the same length? Use the numbers from your own table. What
happens to the bill at fifty turns?**

>

**3. Turn 4: did the bot refuse, or did it invent CSS-4090?** If it refused, what
in your system prompt held the line? If it invented, what did it make up —
credits, a room, an instructor?

>

**4. Where else was either bot wrong?** Turn 2 asks for two courses that meet at
the same hour; two courses in the catalogue are full. Did the bots notice?

>

---

## Sublab Medium — one task, six models

Paste the per-model summary printed by `correct_kazakh.py`:

| Model | Exact | Failed | Tokens | Cost $ |
|---|---|---|---|---|
| google/gemma-4-26b-a4b-it:free | | | | |
| qwen/qwen3.8-27b | | | | |
| deepseek/deepseek-v4-flash-0731 | | | | |
| gpt-5.6-luna | | | | |
| gpt-5.6-terra | | | | |
| gpt-5.6-sol | | | | |

### Which error types did each model repair?

Rows are error labels, columns are models. Write "yes", "no" or "partial".

| Error type | gemma | qwen | deepseek | luna | terra | sol |
|---|---|---|---|---|---|---|
| kaz_to_rus | | | | | | |
| latin_homoglyph | | | | | | |
| drop_hyphen | | | | | | |
| join_words | | | | | | |
| double_letter | | | | | | |

**The `latin_homoglyph` row: what happened?** Describe what you observed. The
explanation is Sublab Harder's job, not this one's.

>

**Where a model returned good Kazakh that was not identical to the original,
say so here.** Exact match is not correctness.

>

**Cheapest model that was good enough, and why:**

>

---

## Sublab Harder — open the tokenizer

### A. What a language costs

**`cl100k_base`:**

# Sublab Harder — open the tokenizer

### A. What a language costs

**`cl100k_base`:**

| Language | Tokens | Chars | Tok/char | × English | $ per 1,000 sentences |
|---|---|---|---|---|---|
| kk | 200 | 263 | 0.760 | 3.75 | $1.00 |
| ru | 129 | 277 | 0.466 | 2.30 | $0.65 |
| en | 59 | 291 | 0.203 | 1.00 | $0.30 |

**`o200k_base`:**

| Language | Tokens | Chars | Tok/char | × English | $ per 1,000 sentences |
|---|---|---|---|---|---|
| kk | 104 | 263 | 0.395 | 1.95 | $0.52 |
| ru | 91 | 277 | 0.329 | 1.62 | $0.46 |
| en | 59 | 291 | 0.203 | 1.00 | $0.30 |

---

### B. What a homoglyph does

| Sentence id | Foreign char (index, name) | Tokens correct | Tokens corrupted | Δ | Diverges at |
|---|---|---|---|---|---|
| s01 | char 14 is 'a' - LATIN SMALL LETTER A | 12 | 14 | +2 | index 2 |
| s05 | char 22 is 'e' - LATIN SMALL LETTER E | 11 | 13 | +2 | index 3 |

**Token pieces around the divergence:**
correct  : [' ба', 'сқа', 'рма', 'сы', 'на']
corrupted: [' б', 'a', 'сқ', 'ар', 'ма']
### Written answers
---

### C. Did it get better?

| Language | cl100k_base | o200k_base | Change |
|---|---|---|---|
| kk | 0.760 | 0.395 | -48.0% |
| ru | 0.466 | 0.329 | -29.4% |
| en | 0.203 | 0.203 | 0.0% |

---

### Written answers

**1. What is the Kazakh tax?**
> The "Kazakh tax" refers to the heavy tokenization premium incurred when processing Kazakh text compared to English. Under the older `cl100k_base` tokenizer, Kazakh cost **3.75x more per character** than English (0.760 vs 0.203 tok/char, or $1.00 per 1,000 sentences). The newer `o200k_base` tokenizer significantly narrowed this gap, reducing the multiplier to **1.95x English** (0.395 tok/char, dropping the cost to $0.52). While the cost was effectively cut in half (-48%), Kazakh still carries nearly double the token overhead of English.

**2. Why did the models repair `kaz_to_rus` but struggle with `latin_homoglyph`?**
> A `kaz_to_rus` error replaces one Cyrillic character with another, which generally preserves the overall word boundary and token structure. In contrast, a `latin_homoglyph` introduces a Latin script character into the middle of a Cyrillic word. As shown in part B, this causes the tokenizer to shatter the word into unnatural sub-word fragments (e.g., changing `[' ба', 'сқа', 'рма']` into `[' б', 'a', 'сқ', 'ар', 'ма']`). Instead of receiving a recognizable word with a single typo, the model receives fragmented bytes and unrelated sub-tokens, making context restoration substantially harder.

**3. Name one thing this measurement does not explain about your Sublab Medium results.**
> This experiment exclusively measures OpenAI's tokenizers (`cl100k_base` and `o200k_base`), whereas the Sublab Medium models included non-OpenAI architectures like Meta's Llama 3.1 and Alibaba's Qwen 2.5. Each model family utilizes its own distinct vocabulary size, merge rules, and byte-pair encoding (BPE) implementation. To close this gap and properly evaluate performance across non-OpenAI models, we would need to inspect their respective open-source tokenizers (e.g., using Hugging Face `transformers` / `AutoTokenizer`) directly.
>

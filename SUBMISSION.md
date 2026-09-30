# HW1 submission

**Name:** Gazizkyzy Mariyam
**Student ID:** S23067455
**Group:** CSS4007-9
**Repository:** https://github.com/mariyamgazizkyzy-del

## AI tool disclosure

State which AI tools you used and for what. Expected and fine; undisclosed use
is not.

>I used OpenAI ChatGPT as a coding and analysis assistant. I used it to help understand the assignment requirements, debug Python and PowerShell errors, explain tokenization and API usage, and prepare the written analysis in SUBMISSION.md. The actual numerical results and model outputs reported below were obtained from my own program runs.

---

## Sublab Easy — the registration bot and its bill

**How I laid the catalogue out inside the system prompt, and why:**

> I stored the course catalogue in the system prompt with course codes, course names, prerequisites, available seats, schedules, and credit values. I also included the student's completed courses, the maximum credit limit, and rules for checking prerequisites, schedule conflicts, seat availability, and invalid course codes. This structure allows the bot to make registration decisions consistently using the same information on every turn.

**My turn 5 (Kazakh or Russian):**

> Мен үшінші курс студентімін. Мен әлі де қандай курстарға жазыла аламын?

### Run 1 — OpenAI, `gpt-5.6-luna`

| Turn      | Input tokens | Output tokens | Cost $ |
| --------- | -----------: | ------------: | -----: |
| 1         |            — |             — |      — |
| 2         |            — |             — |      — |
| 3         |            — |             — |      — |
| 4         |            — |             — |      — |
| 5         |            — |             — |      — |
| **Total** |            — |             — |      — |

> The OpenAI run was not successfully completed because the API returned an insufficient-quota error.

### Run 2 — OpenRouter, `google/gemma-3-27b-it`

| Turn      | Input tokens | Output tokens |       Cost $ |
| --------- | -----------: | ------------: | -----------: |
| 1         |          790 |           368 |     0.000122 |
| 2         |         1184 |           165 |     0.000121 |
| 3         |         1373 |           253 |     0.000150 |
| 4         |         1648 |            47 |     0.000139 |
| 5         |         1727 |           390 |     0.000201 |
| **Total** |     **6722** |      **1223** | **0.000733** |

### Turn 4, verbatim

**OpenAI:**

```text
No successful OpenAI output was available because the API returned an insufficient-quota error.
```

**OpenRouter:**

```text
CSS-4090 Quantum Machine Learning does not exist in the course catalogue. Please provide a valid course code.
```

### Written answers

**1. What changed between the OpenAI and OpenRouter runs?**

The main difference was the API provider and model endpoint. The OpenRouter run used `google/gemma-3-27b-it`, while the OpenAI run could not be completed because of an insufficient-quota error. The registration logic and catalogue rules remained the same.

**2. Why did input tokens grow from Turn 1 to Turn 5? What would 50 turns do to the bill?**

The bot sends the conversation history together with the new user message on each turn. Therefore, as the conversation becomes longer, the number of input tokens also increases. For example, the input grew from 790 tokens in Turn 1 to 1727 tokens in Turn 5. With 50 turns, the total number of processed input tokens would be much larger, so the total API cost would also increase.

**3. Why did the bot refuse Turn 4 instead of inventing a course?**

The system prompt contains a fixed course catalogue and rules for invalid course codes. `CSS-4090` was not in the catalogue, so the bot correctly refused the request instead of inventing a course.

**4. What other error or interesting behaviour did you notice?**

In Turn 1, the response included the student's already completed courses under the “Eligible Courses” section, although it also correctly explained that those courses could not be registered again. In Turn 2, the bot correctly detected a schedule conflict between `CSS-4007` and `CSS-4102`, because both were scheduled on Tuesday from 09:00 to 10:50. In Turn 3, it correctly calculated the credit totals.

---
## Sublab Medium — one task, six models

| Model                           | Exact | Failed | Tokens |  Cost $ |
| ------------------------------- | ----: | -----: | -----: | ------: |
| google/gemma-4-26b-a4b-it:free  |     0 |      8 |      0 | 0.00000 |
| qwen/qwen3.8-27b                |     0 |      8 |      0 | 0.00000 |
| deepseek/deepseek-v4-flash-0731 |     7 |      0 |  21938 | 0.00595 |
| gpt-5.6-luna                    |     0 |      8 |      0 | 0.00000 |
| gpt-5.6-terra                   |     0 |      8 |      0 | 0.00000 |
| gpt-5.6-sol                     |     0 |      8 |      0 | 0.00000 |

### Which error types did each model repair?

The available summary shows that only `deepseek/deepseek-v4-flash-0731` successfully completed model calls for all eight sentences. It produced 7 exact corrections out of 8. The other five models failed on all eight requests, so their correction results cannot be evaluated from the failed calls.

| Error type      | gemma     | qwen      | deepseek                               | luna      | terra     | sol       |
| --------------- | --------- | --------- | -------------------------------------- | --------- | --------- | --------- |
| kaz_to_rus      | no result | no result | **yes/partial — see 7/8 exact result** | no result | no result | no result |
| latin_homoglyph | no result | no result | **yes/partial — see 7/8 exact result** | no result | no result | no result |
| drop_hyphen     | no result | no result | **yes/partial — see 7/8 exact result** | no result | no result | no result |
| join_words      | no result | no result | **yes/partial — see 7/8 exact result** | no result | no result | no result |
| double_letter   | no result | no result | **yes/partial — see 7/8 exact result** | no result | no result | no result |

> Note: the per-error-type `yes/no/partial` classification should only be filled from the individual rows in `outputs/corrections.json`. The terminal summary alone does not identify which specific sentence was the one non-exact correction, so I do not infer those five labels from the total of 7/8.

**The `latin_homoglyph` row: what happened?**

> The Medium experiment showed that Latin homoglyph correction can be handled by a model when the model call succeeds, but the summary alone does not isolate the exact result for the homoglyph examples. The Harder tokenizer experiment provides direct evidence that homoglyphs change the token stream and can increase token fragmentation.

**Where a model returned good Kazakh that was not identical to the original, say so here.**

> The DeepSeek model produced 7 exact matches out of 8 cases. Therefore, one of its eight corrections was not an exact string match. However, exact match is a strict string-level metric: a non-exact answer can still be linguistically acceptable. The specific non-exact correction should be checked in `outputs/corrections.json`.

**Cheapest model that was good enough, and why:**

> Among the models that successfully completed the task, `deepseek/deepseek-v4-flash-0731` was the only model with successful results in this run. It produced 7 exact corrections out of 8 and cost $0.00595 for the eight-sentence experiment. The other models returned API/model-call failures, so their quality cannot be compared from this run.

---

## Sublab Harder — open the tokenizer

### A. What a language costs

**`cl100k_base`:**

| Language | Tokens | Chars | Tok/char | × English |
| -------- | -----: | ----: | -------: | --------: |
| kk       |    200 |   263 |    0.760 |      3.75 |
| ru       |    129 |   277 |    0.466 |      2.30 |
| en       |     59 |   291 |    0.203 |      1.00 |

**`o200k_base`:**

| Language | Tokens | Chars | Tok/char | × English |
| -------- | -----: | ----: | -------: | --------: |
| kk       |     84 |   263 |    0.319 |      1.58 |
| ru       |     74 |   277 |    0.267 |      1.32 |
| en       |     59 |   291 |    0.203 |      1.00 |

### B. What a homoglyph does

| Sentence id | Foreign char (index, name)                                                                                      | Tokens correct | Tokens corrupted |  Δ | Diverges at |
| ----------- | --------------------------------------------------------------------------------------------------------------- | -------------: | ---------------: | -: | ----------: |
| KZ-03       | char 0 `'A'` — LATIN CAPITAL LETTER A; char 2 `'a'` — LATIN SMALL LETTER A; char 5 `'t'` — LATIN SMALL LETTER T |             16 |               20 | +4 |     index 0 |
| KZ-08       | char 1 `'o'` — LATIN SMALL LETTER O; char 3 `'a'` — LATIN SMALL LETTER A; char 9 `'T'` — LATIN CAPITAL LETTER T |             21 |               24 | +3 |     index 1 |

**Token pieces around the divergence:**

```text
KZ-03

correct  : ['А', 'лая', 'қ', 'тарға', ' ақша']
corrupted: ['A', 'л', 'a', 'я', 'қ']
```

```text
KZ-08

correct  : ['Д', 'он', 'аль', 'д', ' Т', 'рамп']
corrupted: ['Д', 'o', 'н', 'a', 'л', 'ль']
```

### C. Did it get better?

| Language | cl100k_base | o200k_base | Change |
| -------- | ----------: | ---------: | -----: |
| kk       |       0.760 |      0.319 | -58.0% |
| ru       |       0.466 |      0.267 | -42.7% |
| en       |       0.203 |      0.203 |   0.0% |

### Written answers

**1. What is the Kazakh tax?**

> With `cl100k_base`, Kazakh uses 0.760 tokens per character, compared with 0.203 for English. This means that Kazakh uses about 3.75 times as many tokens per character as English in this experiment. With `o200k_base`, Kazakh decreases to 0.319 tokens per character, giving a ratio of 1.58× English. Therefore, the newer tokenizer narrows the gap substantially. Russian also improves, from 2.30× English to 1.32×, while English remains at 1.00× in both tokenizers.

**2. Why did the models repair `kaz_to_rus` but struggle with `latin_homoglyph`?**

> A Latin homoglyph looks visually similar to a Cyrillic character, but it is a different Unicode character. This can produce a very different token stream. In KZ-03, the correct sentence contains 16 tokens, while the corrupted sentence contains 20 tokens, an increase of 4 tokens. The streams diverge at index 0. In KZ-08, the number increases from 21 to 24 tokens, and the streams diverge at index 1. For example, the correct KZ-03 pieces include `['А', 'лая', 'қ', 'тарға', ' ақша']`, while the corrupted version contains smaller fragments such as `['A', 'л', 'a', 'я', 'қ']`. This shows why a visually small character substitution can have a larger effect on tokenization.

**3. Name one thing this measurement does not explain about your Sublab Medium results.**

> The Harder experiment only measures `cl100k_base` and `o200k_base`. It does not directly measure the internal tokenizer of every model used in Sublab Medium. Therefore, the tokenizer experiment can demonstrate that Cyrillic and Latin homoglyphs affect tokenization, but it cannot by itself explain every difference between the six Medium models. The Medium results also depend on API availability, model behavior and the actual correction ability of each model.


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

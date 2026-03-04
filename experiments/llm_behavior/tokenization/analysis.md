---
title: "EXP-06 Analysis — Tokenization Domain Ratios"
tags: [analysis, tokenization, bpe, cost-model, context-window, llm-behavior, japanese, arabic, json]
aliases: [exp-06-analysis, tokenization-analysis]
---

# EXP-06 Analysis — Tokenization: Domain-Specific Token Ratios

**Run date:** 2026-03-04
**Status:** ✅ Complete

---

## What the data shows

### Finding 1 — The English-centric assumption holds, but only for English

Common English prose tokenises at **1.25 tokens/word** and technical AI-domain English at **1.34** — both
within the conventional "1,000 words ≈ 750–800 tokens" estimate. The BPE vocabulary is dense with common
English words: "the", "language", "model", "attention" each occupy a single vocabulary slot. The technical
English penalty (+7%) is driven almost entirely by compound terms that split at morpheme boundaries:
`aut|ore|gressive` (3 tokens), `architecture` (1 token, common enough), `conditional` (1 token).

Medical/legal text lands at **1.70** — a 36% premium over prose. The boundary preview makes the mechanism
visible: `hyp|ox|emia` → 3 tokens, `t|ach|yc|ard|ia` → 5 tokens, `radi|ograph` → 2 tokens. Clinical
terminology is rare in web-scale text, so BPE never merged these substrings into single high-frequency
tokens. Every Latin/Greek medical root is effectively unknown to the tokenizer.

### Finding 2 — Code and structured data have a 2–4× cost premium, explained by structure

Python code at **2.10** and JSON at **4.15** reveal two distinct mechanisms:

**Python code (2.10×):** Identifiers split at camelCase and underscore boundaries — `count_tokens` →
`count|_tokens` (2 tokens), `build_safe_prompt` → `build|_safe|_prompt` (3 tokens). String literals
fragment at quote characters: `"|g|pt|-|4|o|-mini|"` is 9 tokens for 10 characters. Indentation
(`   ` = 3 spaces) produces separate tokens. The net result: ~130 "words" of Python code uses the same
270 tokens as ~215 words of English prose.

**JSON at 4.15× is the single most important production finding.** Every structural character tokenises
separately: `{`, `"`, `:`, `,` are each 1 token. A key-value pair `"id": "EXP-06"` takes 8 tokens
(`"|id|":|` `"|EXP|-|06|"`). A 52-word JSON blob used 216 tokens — the word-count measure is nearly
useless here because most "words" in JSON are structural characters that `.split()` simply doesn't count.
The practical rule: **every field in a JSON object costs approximately 4–6 tokens for its scaffolding
alone**, before any value content.

### Finding 3 — The Japanese ratio (37.00) is a measurement artifact — and that reveals something deeper

The Japanese sample returned **7 "words" for 259 tokens**, giving a 37.00 ratio. This is not a valid
comparison: Japanese text does not use spaces between words, so Python's `.split()` returned only 7
space-separated chunks (whitespace around punctuation and newlines) for what is actually ~80+ semantic
word units.

The correct metric for space-free scripts is **tokens per character**:
- Japanese: 259 tokens / ~230 characters ≈ **1.13 tokens/character**
- Arabic: 291 tokens / ~280 characters ≈ **1.04 tokens/character**

But comparing *character* counts across scripts is also misleading — a Japanese kanji conveys ~5–6× more
semantic content than a Latin letter. The real engineering takeaway is:

> **For Japanese and Chinese, the only reliable unit is tokens.** Never estimate from word count or
> character count. A "100-word" Japanese paragraph in English is ~130 tokens; the *equivalent semantic
> content* in Japanese is 200–300 tokens — and the tokeniser confirms this by assigning individual tokens
> to each kanji.

The Arabic result (**4.77 ratio, 61 actual space-separated words**) is not an artifact — Arabic does use
spaces between words. Each Arabic letter fragments because the `cl100k_base` vocabulary has minimal Arabic
subword coverage. The boundary preview shows single-character tokens throughout:
`ال|ذ|ك|اء|` = 4 tokens for the 4-letter word "الذكاء" (intelligence). A production Arabic chatbot
running on GPT-4o-mini would use **~4× more tokens** than the equivalent English system — and cost 4×
more per call for identical information.

### Finding 4 — Emoji is cheaper than expected

Emoji-heavy text at **1.76** is lower than predicted (2.0–6.0 per emoji). The boundary preview explains
why: the surrounding English text is cheap (1.25×), and the experiment's sample had roughly 1 emoji per
8 words. The emoji themselves do fragment into multiple tokens (`🚀` = 3 tokens: `|🚀|`), but they are
diluted by the English context. A text that is *predominantly* emoji with no English surrounding text
would show a much higher ratio.

---

## Hypothesis Verdict

- [x] **Confirmed** — spread is **29.55×** between common English (1.25) and Japanese (37.00 by word count).
  Even discounting the Japanese word-count artifact and using Arabic as the cleanest non-Latin comparison,
  the spread is **3.81×** — still well above the predicted 2× threshold.

The hypothesis correctly identified the mechanism (BPE vocabulary coverage bias) and the direction
(English cheapest, non-Latin and structured data most expensive). The magnitude for Japanese was
underestimated because the word-count metric breakdown was not anticipated.

---

## Comparison to Prior Experiments

| Finding here | Finding in prior EXP | Relationship |
|---|---|---|
| Python code ratio: 2.10 tokens/word | EXP-03: code generation required 800+ tokens for a class-level task | **Confirms with mechanism:** a 400-word class implementation × 2.10 = ~840 tokens — exactly what EXP-03 measured empirically |
| English prose ratio: 1.25 tokens/word | EXP-03: RAG factual answer used 51 tokens at ~40 words | **Confirms:** 40 words × 1.25 ≈ 50 tokens — the token count is now predictable from word count |
| JSON at 4.15 tokens/word | EXP-03: code domain used highest token budget | **Extends:** JSON-heavy prompts (API schemas, structured context) are even more expensive than Python — the max_tokens ceiling risk is higher for JSON payloads |
| Arabic/Japanese cost at 4–37× | EXP-01: max_tokens=400 caused mid-sentence truncation in English | **Extends:** For Arabic at 4.77×, the same max_tokens=400 budget covers only ~84 Arabic "words" — a single paragraph. Truncation risk is 4× higher in Arabic systems |

---

## Production Implications

### Cost model correction factors for `cl100k_base`

Replace the default "750 tokens per 1,000 words" estimate with domain-specific values:

| Domain | Tokens per 1,000 words | vs English rule | Practical example |
|--------|:----------------------:|:---------------:|-------------------|
| Common English prose | **1,250** | baseline | 1,000-word news article → 1,250 tokens |
| Technical English (AI/ML) | **1,340** | 1.07× | Same article with jargon → 1,340 tokens |
| Medical / legal | **1,700** | 1.36× | Clinical note, 500 words → 850 tokens |
| Emoji-heavy social | **1,760** | 1.41× | Twitter thread, 500 words → 880 tokens |
| Python source code | **2,100** | 1.68× | 500-line module (~400 words) → ~840 tokens |
| JSON / structured data | **4,150** | 3.32× | 1,000-char JSON object → ~830 tokens |
| Arabic | **4,770** | 3.81× | 200-word Arabic paragraph → ~954 tokens |
| Japanese | *Use tokens/char* | *N/A* | 100-char Japanese sentence → ~115 tokens |

### Context window budget guard (production pattern)

The conventional wisdom "my prompt is 500 words, I have plenty of room" is **only safe for English
prose.** For a GPT-4o-mini deployment with a 128K context:

| Content type | Words that fit in 128K tokens |
|-------------|:-----------------------------:|
| English prose | ~102,000 words |
| Python code | ~60,900 words |
| JSON payloads | ~30,800 words |
| Arabic text | ~26,800 words |

A RAG system that retrieves JSON-formatted documents and serves Arabic-speaking users can exhaust context
at **~4× the speed** of a plain English system. The retrieval chunk budget must be calculated in tokens,
not words or characters.

### The "JSON context injection" trap

Many production RAG and agent systems inject retrieved context as JSON:

```json
{"source": "doc_1", "content": "...", "score": 0.91, "metadata": {...}}
```

At a 4.15× ratio, every 100 characters of JSON wrapping costs ~40 extra tokens of overhead.
A 20-document retrieval result formatted as a JSON array adds **600–800 tokens of structural overhead**
before any document content. Prefer plain text or minimal markdown formatting for retrieved context
injection — not JSON.

---

## Key Insights

1. **JSON is 3.32× more expensive than English prose per word:**
   A JSON payload that "looks like" 52 words uses 216 tokens — equivalent to 173 words of English prose.
   Every API system that injects JSON-formatted context, tool results, or structured data into prompts is
   paying a silent 3–4× token premium on those segments.
   *(Evidence: json_structured ratio = 4.15 vs common_english = 1.25)*

2. **Arabic systems need a 4× cost and context buffer:**
   Arabic text at 4.77 tokens/word means a production Arabic-language AI system using `cl100k_base`
   costs approximately **4× more per equivalent semantic unit** than its English counterpart — and
   exhausts the context window 4× faster. This is a structural argument for domain-specific multilingual
   models with Arabic-heavy vocabularies for Arabic-language products.
   *(Evidence: arabic ratio = 4.77, boundary preview shows single-character token fragmentation)*

3. **The word-count abstraction collapses for space-free scripts:**
   Japanese text returns only 7 "words" from `.split()` for 259 tokens — a 37× ratio that is a
   measurement artifact, not a meaningful engineering number. For Japanese, Chinese, and Thai, the only
   reliable token estimation is `tiktoken.encode()` directly. Never use word count or character count
   for these languages in production token budgeting.
   *(Evidence: japanese ratio = 37.00 vs arabic = 4.77 for comparable semantic density)*

---

## Next Research Question

**Question:** Does the `o200k_base` vocabulary (200,019 tokens, used by GPT-4o newer versions and o1)
reduce token-per-word ratios for Arabic and code domains — and by how much?

**Why it matters:** `o200k_base` has 2× the vocabulary size of `cl100k_base`. A larger vocabulary means
more Arabic subword sequences and code identifiers can earn dedicated vocabulary entries instead of being
decomposed. If the Arabic ratio drops from 4.77 to, say, 2.5, that is a 47% cost reduction for Arabic
workloads — a real selection criterion when choosing between models.

**Suggested next experiment:** EXP-06b — compare `cl100k_base` vs `o200k_base` token counts on identical
domain texts using `tiktoken.get_encoding("o200k_base")`. Focus on Arabic, Japanese, Python code, and
JSON as the highest-ratio domains from this experiment.

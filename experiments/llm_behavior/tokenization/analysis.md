---
title: "EXP-06 Analysis — Tokenization Domain Ratios"
tags: [analysis, tokenization, bpe, cost-model, context-window, llm-behavior]
aliases: [exp-06-analysis, tokenization-analysis]
---

# EXP-06 Analysis — Tokenization: Domain-Specific Token Ratios

> **Status:** ⬜ Not yet written
>
> Complete this section after running `code.py` and reviewing `results.md`.
> Cite specific numbers from the results table.

---

## Instructions

After running the experiment, fill in each section below.

### What the data shows

*(2–3 paragraphs interpreting the ratio table. Questions to answer:)*
- *Which domain had the highest ratio? Was it what the hypothesis predicted?*
- *Was the English prose baseline stable at 1.0–1.3?*
- *How did non-Latin scripts (Japanese, Arabic) compare to the prediction?*
- *Was code more or less expensive than JSON?*
- *Did the "emoji-heavy" text show byte-fallback tokenization?*

### Hypothesis verdict

- [ ] **Confirmed** — spread ≥ 2× between cheapest and most expensive domain
- [ ] **Partially confirmed** — some domains matched predictions, others did not
- [ ] **Refuted** — spread < 2×

### Mechanism explanation

*(Explain WHY the ratios differ — connect back to BPE algorithm:)*

**Why English prose is cheapest:**
> BPE is trained on web-scale English text. Common English words like "the", "is",
> "a", "language" appear millions of times in the training corpus and earn their own
> single-token vocabulary entry. Word-level tokens are possible when the word appears
> frequently enough to exceed the BPE merge threshold.

**Why code and JSON are more expensive than prose:**
> Code identifiers (`build_safe_prompt`, `max_context`), operators (`->`, `**`),
> and formatting characters (`{`, `"`, `:`) are low-frequency in the training corpus
> relative to their length. Each becomes 2–4 tokens rather than 1.

**Why non-Latin scripts are expensive:**
> The cl100k_base vocabulary was trained predominantly on English text. Japanese and
> Arabic characters have limited vocabulary entries — the tokenizer falls back to
> encoding individual Unicode codepoints or byte sequences, multiplying token count.

**Why emoji is the most expensive per character:**
> A single emoji like 🚀 is encoded as a 4-byte UTF-8 sequence. If absent from the
> BPE vocabulary, each byte becomes a separate token — up to 6 tokens per emoji.

### Production implications

*(Fill after seeing actual numbers. Template:)*

**Cost model correction factor:**

| If your content is… | Apply this multiplier to "1,000 words = 750 tokens" estimate |
|---------------------|:------------------------------------------------------------:|
| English prose | 1.0× (estimate is valid) |
| Technical English | *(fill from results)* |
| Python / code | *(fill from results)* |
| JSON payloads | *(fill from results)* |
| Japanese / Chinese | *(fill from results)* |
| Arabic | *(fill from results)* |
| Medical / legal | *(fill from results)* |
| Emoji-heavy | *(fill from results)* |

**Context window budget rule:**

If a production system handles non-English text or code, the "words fit in context"
estimate must be divided by the domain multiplier. Example:
- A 10,000-word Japanese document at ratio *(fill)* uses *(calculate)* tokens
- GPT-4o-mini context: 128,000 tokens → room for *(calculate)* such documents simultaneously

### Comparison to prior experiments

| Finding here | Finding in prior EXP | Relationship |
|---|---|---|
| Code token ratio | EXP-03: code generation required 800+ tokens at 600 max_tokens budget | *Explains the mechanism: code is inherently more token-dense than English* |
| English prose ratio | EXP-03: RAG factual answer used ~51 tokens regardless of budget | *Confirms: short English answers have low token counts; ratio explains why 51 tokens ≈ ~40 words* |
| *(add after run)* | *(link to prior EXP)* | *(confirms / contradicts / extends)* |

---

## Key Insight

*(Fill after run. Template:)*

1. **Domain drives cost:** The *(most expensive domain)* domain uses *(X.X)× more tokens
   per word than common English prose — a *(N)% cost premium* for identical character count.
   *(Evidence: ratio = X.X vs baseline = Y.Y)*

2. **The "750 tokens per 1,000 words" rule only applies to English:**
   For *(non-English domain)*, the correct estimate is *(N)* tokens per 1,000 words.
   Using the English estimate underestimates cost by *(N)%* and risks silent context overflow.
   *(Evidence: ratio = X.X)*

3. **Token boundaries ≠ word boundaries in code:**
   Python identifiers and structural tokens split into *(N)* tokens on average — meaning
   a 500-line function consumes *(N)* tokens, not the 500-word English estimate of ~650.
   *(Evidence: code ratio = X.X)*

---

## Next Research Question

> Does using a newer, larger vocabulary tokenizer (e.g. `o200k_base` with 200,019 tokens)
> meaningfully reduce the token-per-word ratio for non-English text or code — and by how much?
> At what vocabulary size do diminishing returns appear?

**Practical impact:** If `o200k_base` reduces code token counts by 15–20%, deployments
on GPT-4o (which uses this tokenizer) would be noticeably cheaper for code-heavy workloads
than GPT-3.5-era models — a real architectural selection criterion.

---

*Write this section after reviewing `results.md`. Do not fill placeholders with invented numbers.*

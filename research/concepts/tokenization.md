---
title: "Concept — Tokenization"
tags: [research, concepts, tokenization, bpe, tiktoken, llm-behavior, tokens, context-window, cost]
aliases: [tokenization, bpe-tokenization, subword-tokenization, tiktoken]
---

# Concept: Tokenization

> What is the actual unit of input and output that an LLM processes — and why does it matter that it is not a word?

**Added:** 2026-03-04
**Related experiments:** [EXP-01 — Temperature](../../experiments/llm_behavior/temperature/experiment.md) · [EXP-03 — Token Limit](../../experiments/llm_behavior/token_limit/experiment.md)
**Concept chapter:** Chapter 1 — LLM Behavior

---

## Definition

**Tokenization** is the process of splitting raw text into a sequence of integer IDs (tokens)
using a vocabulary-based subword algorithm — most commonly Byte-Pair Encoding (BPE) — before
passing it to a transformer model.

A token is neither a word nor a character. It is a variable-length subword unit drawn from
a fixed vocabulary (e.g. 100,277 entries for `cl100k_base`, the GPT-4 tokenizer). Common
words are a single token; rare words are split into 2–4 tokens; individual Unicode bytes
are the fallback for characters outside the vocabulary.

```
"tokenization"  → ["token", "ization"]         → [3239, 2065]       (2 tokens)
"unhappiness"   → ["un", "happiness"]           → [359, 34171]       (2 tokens)
"ChatGPT"       → ["Chat", "G", "PT"]           → [14149, 38, 2898]  (3 tokens)
"日本語"          → ["日", "本", "語"]              → [37955, 26705, 30567] (3 tokens)
```

---

## Why It Matters

Every measurable quantity in an LLM system is counted in tokens, not words:

| Production decision | Why tokenization is the wrong abstraction to skip |
|--------------------|--------------------------------------------------|
| **API cost** | OpenAI charges per input + output token. Estimating in words undercharges by ~25% for English, ~300% for Japanese. |
| **Context window** | `gpt-4o-mini` has a 128K token context. A 100-page PDF is ~50,000 tokens — it may not fit even though it is "only 100 pages". |
| **`max_tokens` budget** | Setting `max_tokens=400` cuts at a token boundary, which can fall mid-word: `"compre` → `"comprehensively"` truncated. EXP-03 observed this. |
| **Truncation detection** | `finish_reason="length"` fires when the token limit is hit — not when a sentence ends. Counting words misses this signal. |
| **Prompt engineering** | System prompts consume tokens from the same budget as the response. A 500-word system prompt is ~650 tokens — before the user says anything. |

**Practical rule:** Always call `tiktoken.encode(text)` before sending any prompt to a model.
Never estimate token count from word count.

---

## How It Works

### 1. Byte-Pair Encoding (BPE)

BPE is a bottom-up compression algorithm trained on a text corpus:

1. Start with a vocabulary of individual bytes (256 entries)
2. Count the most frequent adjacent byte pair in the corpus
3. Merge that pair into a new vocabulary entry
4. Repeat until the target vocabulary size is reached (e.g. 100,277 for `cl100k_base`)

The result is a vocabulary where common words and subwords are single tokens, and rare
sequences decompose into shorter units that were seen more frequently during training.

```python
# Simplified BPE step:
# "low lower lowest" → most frequent pair: "lo" → merge into one token
# "low lower lowest" → ["l","o","w"] → ["lo","w"] → "low" eventually
```

### 2. tiktoken — OpenAI's tokenizer

```python
import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o-mini")  # cl100k_base vocabulary

tokens = enc.encode("Hello, world!")          # → [9906, 11, 1917, 0]
text   = enc.decode([9906, 11, 1917, 0])      # → "Hello, world!"
count  = len(enc.encode(text))                # token count

# Count tokens in a full chat message:
def count_message_tokens(messages: list[dict], model: str = "gpt-4o-mini") -> int:
    enc = tiktoken.encoding_for_model(model)
    tokens = 0
    for msg in messages:
        tokens += 4  # every message uses 4 overhead tokens
        for value in msg.values():
            tokens += len(enc.encode(str(value)))
    return tokens + 2  # reply priming
```

### 3. Vocabulary differences across models

| Tokenizer | Vocabulary size | Used by |
|-----------|:--------------:|---------|
| `cl100k_base` | 100,277 | GPT-4, GPT-4o, GPT-4o-mini, text-embedding-3 |
| `o200k_base` | 200,019 | GPT-4o (newer versions), o1, o3 |
| `p50k_base` | 50,257 | GPT-3, Codex |
| `r50k_base` | 50,257 | GPT-3 davinci |

The vocabulary difference matters: a token ID for "the" in `cl100k_base` is not the same
integer as in `p50k_base`. Never hardcode token IDs — always encode from text.

### 4. Token-per-word ratios by domain

From the `cl100k_base` vocabulary:

| Input domain | Tokens / word (approx.) | Why |
|-------------|:-----------------------:|-----|
| Common English prose | 1.0 – 1.3 | Most words are in the vocabulary |
| Technical English (papers) | 1.3 – 1.7 | Domain jargon splits into subwords |
| Python source code | 1.5 – 2.0 | Identifiers, operators, indentation |
| JSON / structured data | 1.8 – 2.5 | Brackets, quotes, colons each tokenise |
| Japanese / Chinese | 1.5 – 3.0 | Multi-byte characters; vocabulary overlap |
| Arabic / Hindi | 2.0 – 5.0 | Low vocabulary coverage for these scripts |
| Emoji | 2 – 6 per emoji | Multi-byte Unicode encoded as byte fallbacks |

---

## Practical Observations

**From EXP-03 — Token Limit (max_tokens experiment):**

- The RAG factual answer used exactly **51 tokens** regardless of budget (150, 300, or 600) — because the model's natural stopping point was 51 tokens.
- Code generation for a class-level task required **800+ tokens** to complete — every method signature, docstring, and implementation line is 5–15 tokens.
- `finish_reason="length"` appeared at exactly `max_tokens` — confirmed the model counts its own output tokens in real time, stopping the moment the budget is exhausted.

**From EXP-01 — Temperature:**

- Setting `max_tokens=400` with a 300-token response budget meant the model sometimes produced outputs that were cut mid-sentence — a token boundary can fall inside a multi-token word like `"comprehensively"` → `"comprehensively"[:-3]`.

**Key production observation:** A 1,000-character prompt in English is approximately 250 tokens. The same 1,000-character prompt in Arabic or Japanese can be 500–700 tokens — nearly doubling cost and halving available response budget.

---

## Limitations

| Limitation | Description |
|-----------|-------------|
| **Non-uniform word cost** | Different words have different token counts even in the same language. "AI" = 2 tokens, "the" = 1 token. Budgeting by word count is always wrong. |
| **Vocabulary mismatch for specialised domains** | Medical, legal, and scientific terminology splits into 3–6 tokens per term. General-purpose tokenizers are inefficient for specialised corpora. |
| **Token boundary artifacts** | `max_tokens` cuts at a token boundary, not a word or sentence boundary. Downstream parsers that expect complete sentences will receive fragments. |
| **Model version changes vocabulary** | A model update can ship a new tokenizer vocabulary (e.g. `cl100k_base` → `o200k_base`). Hardcoded token counts become stale. EXP-05 showed `system_fingerprint` changes mid-session. |
| **Cross-tokenizer incompatibility** | Claude (Anthropic) uses a different tokenizer from GPT-4. A prompt that uses 1,000 tokens in GPT-4 may use 1,100 tokens in Claude. Cost estimates and context budgets are model-specific. |

---

## Related Experiments

| Experiment | Relationship |
|-----------|-------------|
| [EXP-01 — Temperature & Output Entropy](../../experiments/llm_behavior/temperature/experiment.md) | `max_tokens=400` caused mid-token truncation in long outputs — tokenization explains the boundary |
| [EXP-03 — Token Limits & Truncation](../../experiments/llm_behavior/token_limit/experiment.md) | **Primary evidence** — 51-token RAG stop, 800+ token code requirement, `finish_reason="length"` |
| [EXP-05 — Seed Determinism](../../experiments/llm_behavior/seed_determinism/experiment.md) | `system_fingerprint` changes can indicate a new tokenizer vocabulary — token counts for identical text may shift |
| [EXP-06 — Tokenization Domain Ratios](../../experiments/llm_behavior/tokenization/experiment.md) | **Primary measurement** — cl100k_base ratios across 8 domains: English 1.25, JSON 4.15, Arabic 4.77, Python 2.10; word-count abstraction collapses for space-free scripts |

---

## Key Insight

> Always call `tiktoken.encode()` — never estimate token count from word count.
> A 1,000-word English document is ~1,300 tokens.
> The same 1,000-word document in Japanese can be 2,500 tokens.
> Every production system that handles non-English text must account for this or
> it will silently exceed context limits and miscalculate costs.

**Production token budget guard:**

```python
import tiktoken

MAX_CONTEXT = 128_000   # gpt-4o-mini
RESPONSE_BUDGET = 2_000

def build_prompt(system: str, history: list[dict], user: str) -> list[dict]:
    enc = tiktoken.encoding_for_model("gpt-4o-mini")
    messages = [{"role": "system", "content": system}] + history + [{"role": "user", "content": user}]

    prompt_tokens = sum(len(enc.encode(m["content"])) + 4 for m in messages) + 2
    available = MAX_CONTEXT - RESPONSE_BUDGET - prompt_tokens

    if available < 0:
        raise ValueError(f"Prompt exceeds context window by {-available} tokens")

    return messages
```

---

## Open Questions

- **[RQ proposed]** How does per-token cost compare across GPT-4o, GPT-4o-mini, Claude 3.5 Sonnet, and Gemini 1.5 Flash when controlling for identical input text? At what output length does the cheapest model flip?

- **[RQ proposed]** Does the `o200k_base` vocabulary (GPT-4o newer versions) produce meaningfully fewer tokens for specialised domains (medical, legal, code) compared to `cl100k_base` — reducing cost and context pressure for domain-specific applications?

- **Experiment proposed:** `experiments/llm_behavior/tokenization/` — measure token-per-word ratios across 8 input domains, verify the ratios above empirically, visualise token boundaries with colour-coded output.

---

## References

- [OpenAI Tokenizer (interactive)](https://platform.openai.com/tokenizer) — visualise token splits in real time
- [OpenAI Cookbook — How to count tokens with tiktoken](https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken) — authoritative tiktoken usage guide
- [HuggingFace NLP Course — Chapter 2: Tokenizers](https://huggingface.co/learn/nlp-course/chapter2/4) — BPE, WordPiece, Unigram algorithms
- [tiktoken GitHub](https://github.com/openai/tiktoken) — source and vocabulary files
- [`research/concepts/llm_behavior.md`](llm_behavior.md) — parent concept: token budget as a control surface
- [EXP-03 analysis.md](../../experiments/llm_behavior/token_limit/analysis.md) — empirical token count data

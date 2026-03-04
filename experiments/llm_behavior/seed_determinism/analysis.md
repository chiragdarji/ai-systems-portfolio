---
title: "EXP-05 — Seed Determinism Analysis"
tags: [analysis, llm-behavior, seed, determinism, temperature, reproducibility]
aliases: [exp-05-analysis]
---

# EXP-05 — Seed + T=0 Determinism — Analysis

*Run date: 2026-03-04 | Model: gpt-4o-mini | T=0.0 | seed=42 | 10 calls × 3 prompts × 2 conditions*

---

## Hypothesis Verdict

**Hypothesis was REFUTED.**

> ~~`seed=42` combined with `T=0` reduces but does not eliminate output variation.~~

The measured delta between `T=0+seed` and `T=0 (no seed)` was **+0.0%** across all three
prompt types. Seed made zero measurable difference in identity rate.

| Condition | Analytical | Creative | Code | Average |
|-----------|:----------:|:--------:|:----:|:-------:|
| T=0 + seed=42 | 0.0% | 0.0% | **100.0%** | 33.3% |
| T=0 (no seed) | 0.0% | 0.0% | **100.0%** | 33.3% |
| **Δ (seed advantage)** | **+0.0%** | **+0.0%** | **+0.0%** | **+0.0%** |

**The 100% code identity was achieved in both conditions — seed was not the cause.**

---

## The Surprising `system_fingerprint` Finding

During the `code / no_seed` condition, call 6 received a **different** `system_fingerprint`:

```
calls 1-5, 7-10:  fp=fp_373a14eb6f
call 6:           fp=fp_583fd98828   ← different backend model version
```

Despite serving from a different model version, the output was **still identical**.
This tells us:

> For maximally constrained, short, canonical outputs (a Fibonacci function), even a
> **backend model change does not affect the output** — the task is so over-determined
> that there is only one reasonable answer.

---

## Why Seed Made No Difference

The `seed` parameter seeds the **random number generator** used for sampling from the
token probability distribution. At `T=0`, the sampling distribution has already collapsed
to a delta function (argmax token). There is no random sampling to seed.

```python
# T=0 token selection (pseudocode):
logits = model.forward(context)
next_token = argmax(logits / 0.0)   # temperature → 0 → argmax

# seed has no effect here because there is no random sampling
# seed only matters when temperature > 0 and you're sampling from a distribution
```

The residual non-determinism at `T=0` (which caused the 0% identity on analytical/creative)
comes from **floating-point non-associativity** in distributed GPU matrix multiplication —
not from random sampling. `seed` cannot fix this.

---

## Why Code Was 100% Identical (Both Conditions)

The code prompt asked for "a Python function that returns the nth Fibonacci number using memoisation."

This task has exactly one canonical solution in the Python ecosystem:

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
```

Every well-trained model converges on this same output because:
1. **Token count is small (~60 tokens)** — fewer generation steps means less accumulated FP error
2. **The task is maximally over-constrained** — "Fibonacci + memoisation + Python" has one correct answer
3. **The model has seen this pattern millions of times** — the argmax logit is extremely confident

This is **task-driven determinism**, not seed-driven determinism.

---

## What Drives Determinism — A Framework

| Factor | Effect on Determinism | Example |
|--------|----------------------|---------|
| `temperature=0` | Necessary but not sufficient — eliminates sampling noise | All conditions in this experiment |
| `seed=N` | **No measurable effect at T=0** | Δ=+0.0% across all prompts |
| Task over-constraint | **Strong effect** — one canonical answer → 100% identical | Fibonacci with memoisation |
| Output length | **Inverse effect** — longer output → more FP accumulation → more drift | Analytical: 300 tokens → 10 unique outputs |
| Backend model version | **Potentially breaks determinism** — but not always | `fp_583fd98828` still produced same code output |

---

## When Does T=0 Actually Give You Determinism?

Based on this experiment and EXP-01:

| Task Type | T=0 Identity Rate | Why |
|-----------|:-----------------:|-----|
| Short canonical code (Fibonacci, sort, etc.) | ~100% | Maximally over-constrained, short output |
| Multi-sentence explanation (300 tokens) | ~0% | Long output, high FP accumulation |
| Creative writing (3 sentences) | ~0% | Multiple valid first tokens, high FP noise |
| Single-word classification | Likely ~100% | Over-constrained, argmax gap is huge |
| JSON with fixed schema + short values | Likely ~100% | Highly constrained format + short |

**Rule of thumb:** `T=0` gives you determinism when the task has exactly one reasonable answer
and that answer is short (< ~100 tokens). For everything else, determinism must come from
your application architecture.

---

## Production Architecture Implications

### ❌ Do NOT rely on T=0 + seed for reproducibility

```python
# WRONG — assumes T=0+seed gives identical outputs
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[...],
    temperature=0,
    seed=42,
)
# DO NOT cache assumptions about output being identical to previous call
```

### ✅ Correct architecture: explicit response caching

```python
import hashlib, json

def cached_llm_call(system: str, user: str, **kwargs) -> str:
    """Cache LLM responses by input hash — guaranteed determinism."""
    cache_key = hashlib.sha256(
        json.dumps({"system": system, "user": user, **kwargs}, sort_keys=True).encode()
    ).hexdigest()

    if cache_key in RESPONSE_CACHE:
        return RESPONSE_CACHE[cache_key]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        temperature=0,
        **kwargs,
    )
    content = response.choices[0].message.content
    RESPONSE_CACHE[cache_key] = content
    return content
```

### ✅ Always monitor system_fingerprint

```python
EXPECTED_FINGERPRINT = "fp_373a14eb6f"  # pinned at deployment

if response.system_fingerprint != EXPECTED_FINGERPRINT:
    logger.warning(
        f"Model version changed: {EXPECTED_FINGERPRINT} → {response.system_fingerprint}. "
        "Invalidate response cache and re-run regression tests."
    )
```

---

## Cross-Experiment Links

| Experiment | Relationship |
|-----------|-------------|
| [EXP-01 — Temperature](../temperature/experiment.md) | Baseline: 0% determinism at T=0 established the question |
| [RQ-08 — Agent Tool-Call Reliability](../../../research/questions/open_questions.md#rq-08) | Key downstream question: does this non-determinism break agents? |
| [RQ-09 — Structured Output Truncation](../../../research/questions/open_questions.md#rq-09) | Related: does task structure (code/JSON) improve output validity under truncation? |

---

## Key Insight (One-Sentence)

> `seed` has no effect at `T=0` because there is nothing to seed — the remaining
> non-determinism is floating-point arithmetic noise, not random sampling, and the only
> reliable path to reproducible LLM outputs is **explicit application-layer response caching**.

---

## References

- [OpenAI API Reference — seed parameter](https://platform.openai.com/docs/api-reference/chat/create#chat-create-seed)
- [OpenAI Reproducibility Guide](https://platform.openai.com/docs/guides/text-generation/reproducible-outputs)
- Dao, T. et al. (2022). *"FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness"* — context on GPU FP non-associativity
- Mirhoseini et al. (2021). *"A graph placement methodology for fast chip design"* — GPU scheduling non-determinism

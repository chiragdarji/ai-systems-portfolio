---
title: "Concept — Seed Determinism"
tags: [research, concepts, seed-determinism, reproducibility, temperature, llm-behavior, openai]
aliases: [seed-determinism, temperature-seed, api-reproducibility]
---

# Concept: Seed Determinism

> Does fixing the random seed in an LLM API call guarantee identical outputs across repeated calls?

**Added:** 2026-03-04
**Related experiments:** [EXP-01 — Temperature](../../experiments/llm_behavior/temperature/experiment.md) · [EXP-05 — Seed + T=0 Determinism](../../experiments/llm_behavior/seed_determinism/experiment.md)
**Concept chapter:** Chapter 1 — LLM Behavior

---

## Definition

**Seed determinism** is the property of an LLM API call producing byte-exact identical output
across repeated calls when the same `seed` parameter and `temperature=0` are supplied.

OpenAI's `seed` parameter documentation states:
> *"If specified, our system will make a best effort to sample deterministically...
> Determinism is not guaranteed, and you should refer to the `system_fingerprint`
> response parameter to monitor changes in the backend."*

The phrase "best effort / high probability" — not "guaranteed" — is the key qualifier.

---

## Why It Matters

Production systems that depend on reproducible LLM outputs include:

| Use case | Why reproducibility matters |
|----------|---------------------------|
| Regression testing | Must detect when model output changes between deployments |
| Audit trails | Legal/compliance contexts require identical replay of decisions |
| Cached responses | Cost optimisation by returning stored outputs for identical inputs |
| Agent testing | Verifying that an agent always selects the same tool for the same query |

If the reproducibility guarantee is probabilistic rather than absolute, any of these systems
must implement their own determinism layer — they cannot rely on the API alone.

**EXP-05 established that `seed` is not a reliable reproducibility mechanism.** Any production
architecture that depends on it is built on a false assumption.

---

## How It Works

### What `seed` actually does

The `seed` parameter seeds the **pseudo-random number generator (PRNG)** used during
token sampling. At temperature > 0, sampling draws from a probability distribution —
fixing the PRNG means the draw is reproducible.

```
logits → softmax(logits / T) → probability distribution → sample(seed=42) → token
```

At `T > 0`, fixing the seed makes the sample deterministic (for the same distribution).

### Why `seed` has no effect at `T = 0`

At `T = 0`, the probability distribution collapses to a delta function — all probability
mass sits on the argmax token. There is **no sampling step** — therefore nothing to seed.

```
logits → softmax(logits / 0) → [0, 0, ..., 1.0, ..., 0] → argmax → token
                                                 ↑
                                   deterministic by construction
                                   seed has no effect here
```

### What causes the remaining non-determinism at `T = 0`

Residual variation at `T = 0` comes from **floating-point non-associativity** in GPU computation:

1. Large matrix multiplications (`Q @ K.T`, FFN projections) involve thousands of
   floating-point additions
2. GPU thread scheduling varies between calls — the order of additions changes
3. `(a + b) + c ≠ a + (b + c)` in IEEE 754 floating-point arithmetic
4. Different addition order → slightly different intermediate values → occasionally
   different argmax on a near-tie logit pair

This is a hardware-level effect. No API parameter can fix it.

### `system_fingerprint` — the backend version signal

Every OpenAI API response includes `system_fingerprint` to identify the backend model version:

```python
response.system_fingerprint  # e.g. "fp_373a14eb6f"
```

When OpenAI updates model weights, quantisation, or serving infrastructure, the fingerprint
changes. **A seed that produced output X under `fp_373a14eb6f` may produce output Y under
`fp_583fd98828`** — even with identical inputs and `seed=42`.

EXP-05 observed a fingerprint change mid-run (`fp_583fd98828` on one call out of 30)
while the code output remained identical — showing fingerprint changes don't always change
output for maximally over-constrained tasks.

---

## Practical Observations

From **EXP-05** (60 API calls, 3 prompts × 2 conditions × 10 runs, 2026-03-04):

| Condition | Analytical (300 tok) | Creative (3 sentences) | Code (Fibonacci) |
|-----------|:-------------------:|:---------------------:|:----------------:|
| T=0 + seed=42 | 0.0% identical | 0.0% identical | **100% identical** |
| T=0, no seed | 0.0% identical | 0.0% identical | **100% identical** |
| **Δ (seed advantage)** | **+0.0%** | **+0.0%** | **+0.0%** |

**Finding:** Seed had zero measurable effect across all prompt types.

**The code result is not evidence that seed works.** Code was deterministic in both conditions
because the Fibonacci+memoisation task is maximally over-constrained — one canonical answer,
~60 tokens, model has seen it millions of times.

**Task-driven determinism, not seed-driven determinism:**

| Task type | T=0 identity rate | Reason |
|-----------|:-----------------:|--------|
| Canonical short code (~60 tok) | ~100% | Over-constrained, huge argmax gap |
| Multi-sentence explanation (300 tok) | ~0% | Long output, FP accumulation |
| Creative writing (3 sentences) | ~0% | Multiple valid first tokens |
| Single-word classification | Expected ~100% | Over-constrained |

---

## Limitations

- **Seed does not fix FP non-associativity** — the root cause of non-determinism at T=0
- **Seed is model-version scoped** — a fingerprint change invalidates any seed-based
  reproducibility guarantee, even if seed was previously working
- **Task over-constraint is not controllable by the caller** — you cannot engineer a prompt
  to be "deterministic" for arbitrary tasks; it depends on the model's internal confidence
- **These findings are model/version specific** — behaviour may differ for `gpt-4o`,
  Claude, or Gemini; the mechanism (FP noise) is universal but the threshold varies

---

## Related Experiments

| Experiment | Relationship |
|-----------|-------------|
| [EXP-01 — Temperature & Output Entropy](../../experiments/llm_behavior/temperature/experiment.md) | Established T=0 baseline: 0% determinism, raised RQ-01 |
| [EXP-05 — Seed + T=0 Determinism](../../experiments/llm_behavior/seed_determinism/experiment.md) | **Primary experiment** — 60 calls, measured Δ=+0.0% |

---

## Key Insight

> `seed` seeds the sampler, not the GPU arithmetic — at `T=0` there is no sampling,
> so seed has nothing to fix. The only reliable path to reproducible LLM outputs is
> **application-layer response caching**: hash `(system, user, params)` → store the output.

**Production pattern:**

```python
import hashlib, json

def deterministic_llm(system: str, user: str, **kwargs) -> str:
    key = hashlib.sha256(
        json.dumps({"system": system, "user": user, **kwargs}, sort_keys=True).encode()
    ).hexdigest()
    if key in CACHE:
        return CACHE[key]
    result = call_api(system, user, **kwargs)
    CACHE[key] = result
    return result
```

---

## Open Questions

- **[RQ-08](../../research/questions/open_questions.md#rq-08)** Does this non-determinism
  extend to agent tool-call selection — where inconsistency is a correctness failure, not
  a style variation?

- *(proposed)* At what output length does T=0 cross from deterministic to non-deterministic?
  Is there a token-count threshold below which FP noise never changes the argmax?

- *(proposed)* Does using `temperature=0` + `seed` on the Anthropic or Gemini API show
  the same zero-effect pattern — or do different serving architectures produce different results?

---

## References

- [OpenAI API Reference — `seed` parameter](https://platform.openai.com/docs/api-reference/chat/create#chat-create-seed)
- [OpenAI Reproducibility Guide](https://platform.openai.com/docs/guides/text-generation/reproducible-outputs)
- [`research/concepts/llm_behavior.md`](llm_behavior.md) — parent concept: sampling & control
- [EXP-05 analysis.md](../../experiments/llm_behavior/seed_determinism/analysis.md) — full experimental write-up

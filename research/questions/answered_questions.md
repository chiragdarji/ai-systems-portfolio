---
title: "Answered Research Questions"
tags: [research, questions, answered, llm-behavior, experiments]
aliases: [answered-questions, resolved-questions]
---

# Answered Research Questions

Research questions that have been resolved through experiments in this repository.

> For open questions → [`open_questions.md`](open_questions.md)
> To add a new question → copy [`question_template.md`](question_template.md)

---

## Answered Questions Table

| ID | Question | Answered By | Answer Summary | Date |
|----|----------|-------------|----------------|------|
| [AQ-01](#aq-01--does-temperature-control-output-entropy) | Does `temperature` meaningfully control the entropy and variability of LLM output across different domains? | [EXP-01](../../experiments/llm_behavior/temperature/experiment.md) | Yes — measurably and consistently across all four domains. T=1.5 produces substantially more varied output than T=0. Domain determines the acceptable range. | Mar 2026 |
| [AQ-02](#aq-02--does-system-prompt-alone-determine-behaviour) | Does changing only the system prompt — holding all other variables constant — produce measurably different outputs in tone, length, and quality? | [EXP-02](../../experiments/llm_behavior/system_prompt/experiment.md) | Yes — the RESEARCHER persona produced significantly longer, denser responses than BASELINE; CARELESS produced shorter, lower-precision outputs. System prompt is the primary behaviour lever. | Mar 2026 |
| [AQ-03](#aq-03--is-max_tokens-a-ceiling-or-a-target) | Is `max_tokens` a ceiling that the model always fills, or a target it stops at naturally when done? | [EXP-03](../../experiments/llm_behavior/token_limit/experiment.md) | Ceiling. RAG answers completed at 51 tokens with budgets of 150, 300, or 600 — the model stopped itself. Code generation hit the ceiling at all tested budgets. | Mar 2026 |
| [AQ-04](#aq-04--is-the-attention-weight-matrix-always-n×n) | Is the attention weight matrix necessarily n×n in shape — and does this structure make memory complexity O(n²)? | [EXP-04](../../experiments/llm_behavior/attention/experiment.md) | Yes on both. `Q @ K.T = [n, d_k] × [d_k, n] = [n, n]` is unavoidable with full attention. Live sweep confirmed O(n²): 4× memory per 2× tokens, ~15× compute. | Mar 2026 |

---

## Detailed Entries

---

### AQ-01 — Does Temperature Control Output Entropy?

**Original question:** Does `temperature` meaningfully control the entropy and variability of LLM output, and does the effect hold consistently across different task domains?

**Answered by:** [EXP-01 — Temperature](../../experiments/llm_behavior/temperature/experiment.md)

**Answer:** **Yes — confirmed across all four domains.**

Temperature controls the probability distribution over next-token predictions via the softmax scaling formula `P(token_i) = exp(z_i/T) / Σ exp(z_j/T)`. Higher T flattens the distribution; lower T peaks it. This effect is:
- **Consistent across domains**: measurable in general explanation, financial, legal, and code outputs
- **Practically significant**: T=1.5 outputs differ substantially from T=0 outputs in vocabulary, structure, and examples used
- **Domain-dependent in risk**: financial and legal outputs at T≥0.7 introduced imprecision not acceptable in production; code at T≥1.0 introduced stylistic variation but largely remained correct

**Unexpected finding:** `T=0` via the OpenAI API is **not** byte-exact deterministic. Distributed GPU floating-point non-associativity produces output variation even at zero temperature. This opened [RQ-01](open_questions.md#rq-01--temperature-seed-determinism).

**Impact on practice:**
- Financial / legal / code: `T=0–0.3`
- Standard chat: `T=0.5–0.7`
- Creative generation: `T=0.7–1.2`
- Always pair `T=0` with `seed=` for maximum reproducibility

**Updated concept note:** [`research/concepts/llm_behavior.md`](../concepts/llm_behavior.md)

---

### AQ-02 — Does System Prompt Alone Determine Behaviour?

**Original question:** Can changing only the system prompt — holding temperature and user prompts identical — produce measurably different outputs in tone, length, precision, and code quality?

**Answered by:** [EXP-02 — System Prompt Control](../../experiments/llm_behavior/system_prompt/experiment.md)

**Answer:** **Yes — confirmed. System prompt is the primary behaviour lever.**

Three personas (BASELINE, CARELESS, RESEARCHER) produced measurably different outputs across all four user prompts, with temperature fixed at 0.7:
- **RESEARCHER** produced the longest, most technically dense responses — consistently higher word count and domain vocabulary
- **CARELESS** produced shorter, less precise responses — validated that the model follows degraded instructions faithfully
- **BASELINE** served as a reliable neutral reference

**Key finding:** The model follows even deliberately degraded system prompts (`"You are a careless AI"`). This means the system prompt is simultaneously a behaviour contract and a security boundary — any adversary who can modify the system prompt has full control over model behaviour.

**Impact on practice:**
- System prompts must be version-controlled and tested like code
- Multi-tenant systems must isolate system prompts per tenant
- Security audits must include system prompt integrity verification

**Downstream question opened:** [RQ-02 — Prompt Injection Resistance](open_questions.md#rq-02--prompt-injection-resistance)

**Updated concept note:** [`research/concepts/llm_behavior.md`](../concepts/llm_behavior.md)

---

### AQ-03 — Is `max_tokens` a Ceiling or a Target?

**Original question:** Does the model always fill the full `max_tokens` budget, or does it stop naturally when the response is complete — making `max_tokens` a ceiling rather than a target?

**Answered by:** [EXP-03 — Token Limit](../../experiments/llm_behavior/token_limit/experiment.md)

**Answer:** **Ceiling — confirmed.**

The clearest evidence: RAG factual answers used exactly 51 tokens regardless of whether the budget was 150, 300, or 600. The model stopped itself (`finish_reason = "stop"`) — it did not fill the extra budget. Code generation, by contrast, hit the ceiling at every tested budget because the task genuinely requires more tokens than were allocated.

**Stopping behaviour:**
- `finish_reason = "stop"`: model decided it was done — response is complete
- `finish_reason = "length"`: budget exhausted — response is truncated

**Domain-specific findings:**
- Summarisation: completes at ~85–100 tokens regardless of budget
- RAG factual Q&A: completes at ~51 tokens regardless of budget
- Explanation: never completes within 600 tokens for multi-part questions
- Code generation: never completes within 600 tokens for class-level tasks

**Impact on practice:**
- Never set `max_tokens` globally — calibrate per endpoint type
- RAG endpoints: 150–200 tokens sufficient
- Code endpoints: 800–1500 tokens required
- Always log `finish_reason` — treat `"length"` as a production alert

**Downstream question opened:** [RQ-03 — Token Budget Across Model Sizes](open_questions.md#rq-03--token-budget-across-model-sizes)

**Updated concept note:** [`research/concepts/llm_behavior.md`](../concepts/llm_behavior.md)

---

### AQ-04 — Is the Attention Weight Matrix Always n×n?

**Original question:** Is the attention weight matrix necessarily n×n in shape for n input tokens, and does this structure make memory complexity unavoidably O(n²)?

**Answered by:** [EXP-04 — Self-Attention Mechanics](../../experiments/llm_behavior/attention/experiment.md)

**Answer:** **Yes on both — confirmed with mathematical proof and live measurement.**

**Mathematical answer:** `Q @ K.T = [n, d_k] × [d_k, n] = [n, n]`. Entry `[i, j]` stores one score: *"how much should token i attend to token j?"* With n tokens and n candidate tokens to attend to, there are exactly n² questions — the matrix cannot be smaller.

**Empirical answer (live sweep):**

| n_tokens | Memory | Time |
|---|---|---|
| 512 | 1 MB | 4 ms |
| 1,024 | 4 MB | 11 ms |
| 2,048 | 16 MB | 59 ms |

Doubling n → 4× memory, ~5× compute — consistent with O(n²) prediction.

**Implication for n=10,000:** ~381 MB per head per layer. For a 32-layer, 8-head model: ~97 GB for attention matrices alone — physically impossible on consumer hardware without FlashAttention.

**Impact on understanding:**
- Context window limits are a **hardware problem**, not a **model capability problem**
- RAG is an architectural workaround: keep n small by retrieving only relevant chunks
- FlashAttention solves the I/O cost but not the FLOPs cost

**Downstream question opened:** [RQ-04 — FlashAttention Tiled Computation](open_questions.md#rq-04--flashattention-tiled-computation)

**Updated concept note:** [`research/concepts/transformers.md`](../concepts/transformers.md)

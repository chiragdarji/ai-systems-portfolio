---
title: "Experiment 03 — Token Limit"
tags: [experiment, token-limit, max-tokens, llm-behavior, cost]
aliases: [token-limit-experiment, exp-03]
---

# Experiment 03 — Token Limit

**Phase:** LLM Behavior & Prompt Control
**Status:** Complete

---

## Hypothesis

`max_tokens` sets a hard ceiling on output length. Responses that exceed the budget are truncated mid-generation (`finish_reason = "length"`). The budget required for a complete response is domain-dependent: RAG answers need far fewer tokens than code generation.

## Variables

| Variable | Values |
|---|---|
| max_tokens | 50, 150, 300, 600 |
| Domains | explanation, summarisation, code, rag_chunk |
| Temperature | 0.3 (fixed) |
| Model | gpt-4o-mini |

## Method

Run identical prompts at 4 different token budgets. Record `finish_reason`, tokens used vs budget, utilisation percentage, and estimated cost. Detect truncation via `finish_reason == "length"` and heuristic sentence-ending checks.

## Key Questions

- At what budget does each domain produce a complete response?
- How does truncation manifest in structured outputs (code, JSON)?
- What is the cost difference between budgets at scale?
- How does `max_tokens` interact with RAG chunking and chat memory?

## Run

```bash
python experiments/llm_behavior/token_limit/code.py
```

## Outputs

| File | Contents |
|---|---|
| `results.md` | Per-domain, per-budget outputs with finish_reason and cost |
| `analysis.md` | Truncation mechanics, cost model, memory strategy, RAG alignment |

## Key Finding

`max_tokens` is a **ceiling, not a target** — the model stops at its natural end if the budget allows. RAG factual answers needed only 51 tokens regardless of whether the budget was 150, 300, or 600. Code generation never completed even at 600 tokens for a class-level task — requiring 800+.

---

## Links

**Concepts:**
- [`LLM Behavior`](../../../research/concepts/llm_behavior.md) — token budget as a control surface; cost and context window implications

**Research Questions raised:**
- [RQ-03](../../../research/questions/open_questions.md#rq-03--token-budget-across-model-sizes) — Does gpt-4o produce more concise answers than gpt-4o-mini at the same `max_tokens` budget?
- [RQ-09](../../../research/questions/open_questions.md#rq-09--structured-output-truncation-failure) — Does `finish_reason="length"` produce silently invalid JSON/code at a higher rate than prose truncation?

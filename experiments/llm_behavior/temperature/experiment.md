---
title: "Experiment 01 — Temperature"
tags: [experiment, temperature, llm-behavior, entropy, determinism]
aliases: [temperature-experiment, exp-01]
---

# Experiment 01 — Temperature

**Phase:** LLM Behavior & Prompt Control
**Status:** Complete

---

## Hypothesis

The `temperature` parameter controls the entropy of the model's token-sampling distribution. Higher values produce more varied, creative outputs; lower values produce more deterministic, conservative outputs.

## Variables

| Variable | Values |
|---|---|
| Temperature | 0.0, 0.3, 0.7, 1.0, 1.5 |
| Domains | general, financial, legal, code |
| Runs per config | 2 (determinism check) |
| Model | gpt-4o-mini |

## Method

Run identical prompts across all temperature values for each domain. Record outputs, token counts, and latency. Check whether T=0 produces identical outputs across runs.

## Key Questions

- What changes between temperature 0 and 1?
- Which setting is deterministic? Which is creative?
- Where is randomness dangerous (financial, legal, code)?
- Does T=0 via the OpenAI API guarantee byte-exact reproducibility?

## Run

```bash
python experiments/llm_behavior/temperature/code.py
```

## Outputs

| File | Contents |
|---|---|
| `results.md` | Raw outputs, per-call token/latency stats, determinism checks |
| `analysis.md` | Scientific breakdown, risk table, decision framework |

## Key Finding

`T=0` was **not** deterministic in live testing against `gpt-4o-mini` — all 20 determinism checks returned `DIFFERS`. Distributed GPU floating-point non-associativity causes sub-token-level variation even at zero temperature. Use `seed=<int>` alongside `T=0` for maximum reproducibility.

---

## Links

**Concepts:**
- [`LLM Behavior`](../../../research/concepts/llm_behavior.md) — sampling, temperature mechanics, control surfaces
- [`Seed Determinism`](../../../research/concepts/seed_determinism.md) — T=0 non-determinism root cause and production patterns

**Research Questions raised:**
- [RQ-01](../../../research/questions/open_questions.md#rq-01--temperature-seed-determinism) — Does `seed` combined with `T=0` guarantee byte-exact identical outputs?

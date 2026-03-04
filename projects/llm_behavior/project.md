---
title: "Project — LLM Behavior Explorer"
tags: [project, llm-behavior, tokenization, seed-determinism, temperature, system-prompts, portfolio]
aliases: [llm_behavior, llm-behavior-project, llm-parameter-explorer]
---

# Project: LLM Behavior Explorer

**Name:** `llm_behavior`
**Started:** 2026-03-04
**Status:** 🚧 In Progress
**Concepts demonstrated:**
[LLM Behavior](../../research/concepts/llm_behavior.md) ·
[Seed Determinism](../../research/concepts/seed_determinism.md) ·
[Tokenization](../../research/concepts/tokenization.md)

**Related experiments:**
[EXP-01](../../experiments/llm_behavior/temperature/experiment.md) ·
[EXP-02](../../experiments/llm_behavior/system_prompt/experiment.md) ·
[EXP-03](../../experiments/llm_behavior/token_limit/experiment.md) ·
[EXP-05](../../experiments/llm_behavior/seed_determinism/experiment.md) ·
[EXP-06](../../experiments/llm_behavior/tokenization/experiment.md)

---

## Problem

In production LLM systems, the five most fundamental parameters — `temperature`,
`system_prompt`, `max_tokens`, `seed`, and the tokenizer vocabulary — are typically
set by intuition, copied from tutorials, or ignored entirely. Engineers learn their
actual behaviour only when something breaks in production: a financial report generated
with `T=1.0`, a RAG response silently truncated mid-sentence, an Arabic chatbot
burning 4× its token budget, or a reproducibility claim failing because `seed` does
nothing at `T=0`.

The experiments in this lab (EXP-01 through EXP-06) have now established the ground
truth for each of these parameters — with empirical data and precise numbers. This
project translates that research into a runnable, observable, production-pattern toolkit:
a single Python package that a developer can import, run, and use to audit any LLM
workload before it reaches users.

---

## Goal

A working version of this project must be able to do the following:

1. - [ ] **Token budget pre-flight:** Given any prompt (system + user), compute exact token counts using `tiktoken`, check against a user-supplied context limit, and raise a structured error before any API call is made if the budget would be exceeded
2. - [ ] **Domain cost estimator:** Given a text string and a model name, return the domain-adjusted cost estimate in tokens and USD — using the domain ratios measured in EXP-06
3. - [ ] **Temperature sweep:** Run N identical prompts across a configurable temperature range and return a structured report: output text, token count, finish reason, and a determinism flag (outputs identical to T=0 run?)
4. - [ ] **System prompt auditor:** Given a prompt and two system prompts (A and B), run both and return a structured diff: word count, tone metrics, and whether the model obeyed or violated each persona constraint
5. - [ ] **Non-determinism detector:** Run M identical calls at T=0 and report: identity rate, unique output count, and verdict (task-driven determinism vs non-determinism)
6. - [ ] **Markdown report writer:** All five tools above write a structured `results/` markdown report on every run — following the same format as the research experiments

---

## Related Concepts

| Concept | What this project tests | File |
|---------|:-----------------------:|------|
| LLM Behavior | Temperature, system prompt, max_tokens, finish_reason — the five control surfaces | [research/concepts/llm_behavior.md](../../research/concepts/llm_behavior.md) |
| Seed Determinism | T=0 non-determinism mechanism; why seed has zero effect; when task-driven determinism appears | [research/concepts/seed_determinism.md](../../research/concepts/seed_determinism.md) |
| Tokenization | BPE domain ratios; tiktoken pre-flight; why word-count estimates are wrong for code/JSON/Arabic | [research/concepts/tokenization.md](../../research/concepts/tokenization.md) |

---

## Related Experiments

| Experiment | Finding used in this project |
|-----------|:----------------------------:|
| [EXP-01 — Temperature](../../experiments/llm_behavior/temperature/experiment.md) | T=0 is not deterministic across distributed GPU calls — entropy scales with temperature |
| [EXP-02 — System Prompt Control](../../experiments/llm_behavior/system_prompt/experiment.md) | System prompt is architecture, not config — simultaneously a behaviour contract and security boundary |
| [EXP-03 — Token Limits](../../experiments/llm_behavior/token_limit/experiment.md) | `max_tokens` is a ceiling, not a target; domain determines natural stopping point (~51 tokens for RAG) |
| [EXP-05 — Seed Determinism](../../experiments/llm_behavior/seed_determinism/experiment.md) | `seed` has zero measurable effect at T=0; use application-layer response caching for reproducibility |
| [EXP-06 — Tokenization Ratios](../../experiments/llm_behavior/tokenization/experiment.md) | JSON = 3.32× token premium; Arabic = 3.81×; Python = 1.68×; word-count abstraction invalid for Japanese |

---

## System Overview

The LLM Behavior Explorer is a Python toolkit with five independent modules, each
corresponding to one of the lab's completed experiments. Each module exposes a single
entry-point function that accepts structured inputs and returns a dataclass result —
making it composable, testable, and importable by other projects (e.g. the future
`rag_assistant` project can import the `TokenBudgetGuard` directly).

The toolkit has no framework dependencies: it uses only `openai`, `tiktoken`, and
`python-dotenv`. All modules write markdown reports to `results/` on every run,
following the same 4-section format (hypothesis, data, verdict, next question) used
in the research experiments.

**Modules:**

| Module | Entry point | Calls API? | Experiment source |
|--------|:-----------:|:----------:|:-----------------:|
| `token_budget.py` | `TokenBudgetGuard` | No | EXP-06 |
| `temperature_sweep.py` | `run_temperature_sweep()` | Yes | EXP-01 |
| `system_prompt_audit.py` | `audit_system_prompts()` | Yes | EXP-02 |
| `token_cost.py` | `estimate_domain_cost()` | No | EXP-03, EXP-06 |
| `determinism_probe.py` | `probe_determinism()` | Yes | EXP-05 |

---

## Implementation Status

| Component | Status | Notes |
|-----------|:------:|-------|
| `implementation/token_budget.py` | ⬜ Not started | No API key needed — pure tiktoken |
| `implementation/temperature_sweep.py` | ⬜ Not started | Requires `OPENAI_API_KEY` |
| `implementation/system_prompt_audit.py` | ⬜ Not started | Requires `OPENAI_API_KEY` |
| `implementation/token_cost.py` | ⬜ Not started | No API key needed — uses EXP-06 ratios |
| `implementation/determinism_probe.py` | ⬜ Not started | Requires `OPENAI_API_KEY` |
| `implementation/main.py` | ⬜ Not started | CLI entry point; orchestrates all modules |
| `evaluation/` | ⬜ Not started | Run-all script + comparison to experiment baselines |
| `README.md` | ✅ Done | Quick start and usage |

---

## Engineering Decisions

> **Decision:** Separate API-calling modules from pure-compute modules.
> **Why:** EXP-06 showed that tokenization analysis needs no API — it runs entirely locally
> with tiktoken. Keeping these separate allows CI/CD to run cost-free token analysis checks
> without an API key.
> **Trade-off:** Two separate import paths, but zero surprise API costs in automated pipelines.

> **Decision:** Each module returns a typed dataclass, not a raw dict.
> **Why:** EXP-01 through EXP-06 all collected data in free-form dicts, making cross-experiment
> comparison tedious. The project enforces typed results to make downstream evaluation trivial.
> **Trade-off:** Slightly more boilerplate per module, but eliminates key-name bugs.

> **Decision:** Results written to `results/` as markdown, not JSON.
> **Why:** Follows the research lab's 4-file contract. Markdown is human-readable in the IDE,
> git-diffable, and directly linkable from experiment.md files.
> **Trade-off:** Not machine-parseable without a markdown parser; acceptable for a research toolkit.

---

## Open Questions

- Should the `TokenBudgetGuard` support Claude (Anthropic) tokenizers? EXP-06 used `cl100k_base`
  — Anthropic uses a different vocabulary. A multi-model token counter would require a different
  library (`anthropic-tokenizer` or byte-fallback counting).
- How much does the domain cost correction (from EXP-06) matter in practice for English-only
  RAG pipelines? A future evaluation could measure the gap between estimated and actual token usage
  on a real document corpus.

---

*Architecture → [`architecture.md`](architecture.md)*
*How to run → [`README.md`](README.md)*

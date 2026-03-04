---
title: "AI Research Index"
tags: [index, concepts, learning-path, research, tracking]
aliases: [research-index, concept-index, learning-tracker]
---

# AI Research Index

Central tracker for concept progress, experiment budgets, and research question limits.
Enforces the **3-experiment / 2-RQ per concept** governance rule defined in `.cursor/rules/ai_lab_rules.mdc §9`.

> **Rule:** A concept chapter closes when 3 experiments complete OR when explicitly closed with `@close_concept`.
> New experiments on a closed concept require opening a new sub-concept.

---

## Concept Status Overview

| # | Concept | Status | Experiments | Open RQs | Summary | Next |
|---|---------|:------:|:-----------:|:--------:|---------|------|
| 1 | [LLM Behavior — Sampling & Control](#1-llm-behavior--sampling--control) | ✅ Complete | 4 / 3 ⚠ | 0 / 2 | [→ summary](research/concepts/llm_behavior_summary.md) | Concept 2 |
| 2 | [Transformer Architecture](#2-transformer-architecture) | 📖 Active | 1 / 3 | 1 / 2 | — | Concept 3 |
| 3 | [Embeddings](#3-embeddings) | 📋 Planned | 0 / 3 | 1 / 2 | — | Concept 4 |
| 4 | [RAG — Retrieval-Augmented Generation](#4-rag--retrieval-augmented-generation) | 📋 Planned | 0 / 3 | 1 / 2 | — | Concept 5 |
| 5 | [Agents & Tool Use](#5-agents--tool-use) | 📋 Planned | 0 / 3 | 1 / 2 | — | Concept 6 |
| 6 | [Evaluation & Reliability](#6-evaluation--reliability) | 📋 Planned | 0 / 3 | 0 / 2 | — | Concept 7 |
| 7 | [Production AI Systems](#7-production-ai-systems) | 📋 Planned | 0 / 3 | 0 / 2 | — | — |

**Status legend:** `📖 Active` · `✅ Complete` · `📦 Closed` · `📋 Planned`

---

## Governance Counters

> Cursor reads these counters before creating any new experiment or research question.
> If experiments = 3 → STOP. Close concept first. If open RQs = 2 → defer new questions.

| Concept | Exp Slots Used | Exp Slots Free | RQ Slots Used | RQ Slots Free | Can Add Exp? | Can Add RQ? |
|---------|:--------------:|:--------------:|:-------------:|:-------------:|:------------:|:-----------:|
| LLM Behavior | 4 | 0 ⚠ | 0 | 2 | ❌ Closed | ✅ Yes |
| Transformer Arch | 1 | 2 | 1 | 1 | ✅ Yes | ✅ Yes |
| Embeddings | 0 | 3 | 1 | 1 | ✅ Yes | ✅ Yes |
| RAG | 0 | 3 | 1 | 1 | ✅ Yes | ✅ Yes |
| Agents | 0 | 3 | 1 | 1 | ✅ Yes | ✅ Yes |
| Evaluation | 0 | 3 | 0 | 2 | ✅ Yes | ✅ Yes |
| Production Systems | 0 | 3 | 0 | 2 | ✅ Yes | ✅ Yes |

> ⚠ LLM Behavior exceeded 3 experiments before this governance rule was introduced. Grandfathered.
> EXP-04 and EXP-05 logically belong to Transformer Architecture; they are cross-linked.

---

## Detailed Concept Entries

---

### 1. LLM Behavior — Sampling & Control

**Concept note:** [`research/concepts/llm_behavior.md`](research/concepts/llm_behavior.md)
**Concept summary:** [`research/concepts/llm_behavior_summary.md`](research/concepts/llm_behavior_summary.md) *(to generate)*
**Status:** ✅ Complete (chapter closed — exceeded 3 experiments before governance rule; grandfathered)

**Core question:** How do temperature, system prompt, and token budget control what an LLM outputs — and what are the limits of that control?

#### Experiments (4 / 3 — grandfathered)

| Slot | Experiment | Status | Key Finding |
|------|-----------|:------:|------------|
| 1 | [EXP-01 — Temperature](experiments/llm_behavior/temperature/experiment.md) | ✅ Complete | T=0 is not deterministic; T controls entropy but domain determines acceptable range |
| 2 | [EXP-02 — System Prompt](experiments/llm_behavior/system_prompt/experiment.md) | ✅ Complete | System prompt is a security boundary, not just a hint |
| 3 | [EXP-03 — Token Limit](experiments/llm_behavior/token_limit/experiment.md) | ✅ Complete | `max_tokens` is a ceiling; RAG answers self-truncate at ~51 tokens regardless of budget |
| 4 | [EXP-05 — Seed Determinism](experiments/llm_behavior/seed_determinism/experiment.md) | ✅ Complete | `seed` has zero effect at T=0; only task over-constraint creates determinism |

#### Open Research Questions (0 / 2)

*All RQs from this concept have been answered or deferred.*

| Slot | RQ | Status |
|------|----|:------:|
| 1 | [AQ-01](research/questions/answered_questions.md) — Temperature controls entropy | 🟢 Answered |
| 2 | [AQ-05](research/questions/answered_questions.md) — Seed determinism | 🟢 Answered |

#### Concept Closure Checklist

- [x] All experiments at `✅ Complete`
- [x] All RQs answered or deferred
- [ ] `llm_behavior_summary.md` generated ← **TODO: run `@close_concept llm_behavior`**
- [ ] `AI_RESEARCH_INDEX.md` updated with summary link
- [ ] Next concept activated (Transformer Architecture → already active)

---

### 2. Transformer Architecture

**Concept note:** [`research/concepts/transformers.md`](research/concepts/transformers.md)
**Concept summary:** *(not yet generated — concept in progress)*
**Status:** 📖 Active

**Core question:** How do transformers compute attention, and why does the n×n attention matrix make long contexts computationally prohibitive — and how do modern architectures solve this?

#### Experiments (1 / 3)

| Slot | Experiment | Status | Key Finding |
|------|-----------|:------:|------------|
| 1 | [EXP-04 — Self-Attention Mechanics](experiments/llm_behavior/attention/experiment.md) | ✅ Complete | O(n²) confirmed live: n=2048 → 16 MB / 59 ms. At n=10K → 381 MB per head per layer |
| 2 | EXP-04b — FlashAttention NumPy Simulation *(planned, from RQ-04)* | 📋 Planned | — |
| 3 | *(reserved)* | — | — |

#### Open Research Questions (1 / 2)

| Slot | RQ | Priority | Status |
|------|----|:--------:|:------:|
| 1 | [RQ-04 — FlashAttention Tiled Computation](research/questions/open_questions.md#rq-04) | ⬆ High | 🔴 Open |
| 2 | [RQ-11 — Attention Head Specialisation on Real Text](research/questions/open_questions.md#rq-11) | ⬆ High | 🔴 Open |

#### Concept Closure Checklist

- [ ] 2nd experiment complete (EXP-04b)
- [ ] All RQs answered or deferred
- [ ] `transformers_summary.md` generated
- [ ] Next concept (Embeddings) activated

---

### 3. Embeddings

**Concept note:** [`research/concepts/embeddings.md`](research/concepts/embeddings.md)
**Concept summary:** *(not yet generated)*
**Status:** 📋 Planned

**Core question:** How do embedding models map tokens and sentences into a geometric space — and how does cosine similarity enable semantic search and RAG retrieval?

#### Experiments (0 / 3)

| Slot | Experiment | Status | Key Finding |
|------|-----------|:------:|------------|
| 1 | EXP-06 — Sentence Embeddings & Cosine Similarity *(planned)* | 📋 Planned | — |
| 2 | EXP-06b — Domain Degradation Test *(planned, from RQ-05)* | 📋 Planned | — |
| 3 | *(reserved)* | — | — |

#### Open Research Questions (1 / 2)

| Slot | RQ | Priority | Status |
|------|----|:--------:|:------:|
| 1 | [RQ-05 — Embedding Domain Degradation](research/questions/open_questions.md#rq-05) | ➡ Medium | 🔴 Open |
| 2 | *(open)* | — | — |

---

### 4. RAG — Retrieval-Augmented Generation

**Concept note:** [`research/concepts/rag.md`](research/concepts/rag.md)
**Concept summary:** *(not yet generated)*
**Status:** 📋 Planned

**Core question:** How do chunk size, retrieval strategy, and context window budget interact to determine RAG answer quality — and what are the design decisions that generalise across domains?

#### Experiments (0 / 3)

| Slot | Experiment | Status | Key Finding |
|------|-----------|:------:|------------|
| 1 | EXP-07 — Naive RAG Pipeline *(planned)* | 📋 Planned | — |
| 2 | EXP-08 — Chunk Size Optimisation *(planned, from RQ-07)* | 📋 Planned | — |
| 3 | *(reserved)* | — | — |

#### Open Research Questions (1 / 2)

| Slot | RQ | Priority | Status |
|------|----|:--------:|:------:|
| 1 | [RQ-07 — RAG Chunk Size Optimum](research/questions/open_questions.md#rq-07) | ⬆ High | 🔴 Open |
| 2 | *(open)* | — | — |

---

### 5. Agents & Tool Use

**Concept note:** [`research/concepts/agents.md`](research/concepts/agents.md)
**Concept summary:** *(not yet generated)*
**Status:** 📋 Planned

**Core question:** How does the ReAct loop enable agents to use tools reliably — and how does temperature, prompt design, and tool schema quality affect correctness in production?

#### Experiments (0 / 3)

| Slot | Experiment | Status | Key Finding |
|------|-----------|:------:|------------|
| 1 | EXP-10 — Single-Tool Agent *(planned)* | 📋 Planned | — |
| 2 | EXP-11 — Multi-Tool Agent *(planned)* | 📋 Planned | — |
| 3 | EXP-12 — Agent Temperature & Reliability *(planned, from RQ-08)* | 📋 Planned | — |

#### Open Research Questions (1 / 2)

| Slot | RQ | Priority | Status |
|------|----|:--------:|:------:|
| 1 | [RQ-08 — Agent Temperature Reliability](research/questions/open_questions.md#rq-08) | 🔥 Critical | 🔴 Open |
| 2 | *(open)* | — | — |

---

### 6. Evaluation & Reliability

**Concept note:** *(not yet written — create when this concept becomes Active)*
**Concept summary:** *(not yet generated)*
**Status:** 📋 Planned

**Core question:** How do you measure whether an LLM system is working correctly — and what failure signals are meaningful enough to trigger automated alerts in production?

#### Experiments (0 / 3)

| Slot | Experiment | Status | Key Finding |
|------|-----------|:------:|------------|
| 1 | EXP-13 — LLM-as-Judge Evaluation *(planned)* | 📋 Planned | — |
| 2 | EXP-14 — Structured Output Validation *(planned, from RQ-09)* | 📋 Planned | — |
| 3 | *(reserved)* | — | — |

#### Open Research Questions (0 / 2)

*Populate when concept becomes Active.*

---

### 7. Production AI Systems

**Concept note:** *(not yet written — create when this concept becomes Active)*
**Concept summary:** *(not yet generated)*
**Status:** 📋 Planned

**Core question:** How do you move from a working prototype to a production LLM system — covering latency, cost, observability, failure handling, and safe deployment?

#### Experiments (0 / 3)

*Populate when concept becomes Active.*

#### Open Research Questions (0 / 2)

*Populate when concept becomes Active.*

---

## Concept Transition Log

| Date | Event | Concept | Action |
|------|-------|---------|--------|
| 2026-03-04 | Governance rule introduced | All | `AI_RESEARCH_INDEX.md` created; existing experiments grandfathered |
| 2026-03-04 | EXP-05 complete | LLM Behavior | RQ-01 answered → AQ-05; concept flagged for summary generation |
| 2026-03-04 | Concept 2 activated | Transformer Architecture | EXP-04 cross-linked; RQ-04, RQ-11 registered as active RQs |

---

## How to Use This File

### Before creating a new experiment
1. Identify the concept the experiment belongs to (column "Concept" above)
2. Check "Exp Slots Free" in the Governance Counters table
3. If slots free = 0 → run `@close_concept <name>` first, then start the next concept
4. If slots free > 0 → proceed with `@create_experiment`

### Before adding a research question
1. Check "RQ Slots Free" for the concept in the Governance Counters table
2. If slots free = 0 → set the new RQ to `⏸ Deferred` in `open_questions.md`
3. RQ slots reopen when the concept is closed (deferred RQs can flow into the next related concept)

### To close a concept
1. Verify all experiments for the concept are `✅ Complete`
2. Run `@close_concept <concept_name>` — Cursor will:
   - Generate `research/concepts/<concept_name>_summary.md`
   - Update this file's status and summary link
   - Activate the next concept in the learning path
   - Move excess RQs to `⏸ Deferred`

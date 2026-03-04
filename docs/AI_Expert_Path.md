---
title: "AI Systems Expert Learning Path"
tags: [roadmap, learning-path, ai-systems, curriculum]
aliases: [learning-path, roadmap, expert-path]
---

# AI Systems Expert Learning Path

A structured 7-concept curriculum for developing expert-level AI systems engineering skills.
Each concept is a **chapter**: up to 3 experiments, up to 2 open research questions, closed with a synthesis summary.

Progress is tracked in [`AI_RESEARCH_INDEX.md`](../AI_RESEARCH_INDEX.md).

---

## Learning Path Overview

```
Concept 1          Concept 2          Concept 3          Concept 4
LLM Behavior   →   Transformer    →   Embeddings     →   RAG
(sampling,         Architecture       (vectors,          (retrieval,
 control,          (attention,         cosine sim,        chunking,
 token budget)     O(n²), Flash)       domain gaps)       generation)

      ↓
Concept 5          Concept 6          Concept 7
Agents         →   Evaluation     →   Production Systems
(ReAct,            (LLM-as-judge,     (latency, cost,
 tool use,          reliability,       observability,
 memory)            structured         safe deployment)
                    output)
```

**Rule:** Each concept must be `✅ Complete` before moving to the next.
Cursor enforces this via `AI_RESEARCH_INDEX.md`.

---

## Concept 1 — LLM Behavior: Sampling & Control

**Status:** ✅ Complete (grandfathered — 4 experiments before governance rule)
**Concept note:** [`research/concepts/llm_behavior.md`](../research/concepts/llm_behavior.md)

### What this chapter answers

> How do temperature, system prompt, and token budget control what an LLM outputs — and what are the limits of that control?

### Core skills developed

- Reading and interpreting `temperature`, `max_tokens`, `seed`, `finish_reason`, `system_fingerprint`
- Understanding softmax and logit-to-probability mechanics
- Designing deterministic LLM calls for production (response caching pattern)
- Identifying when a system prompt is a security boundary vs a style hint

### Experiments

| ID | Topic | Key Finding |
|----|-------|------------|
| EXP-01 | Temperature & Output Entropy | T=0 is not deterministic; entropy scales predictably with temperature |
| EXP-02 | System Prompt as Behaviour Control | System prompt is absolute in cooperative settings; test adversarial conditions |
| EXP-03 | Token Limits, Truncation & Cost | `max_tokens` is a ceiling; domain determines natural stopping point |
| EXP-05 | Seed + T=0 Determinism | `seed` has zero effect at T=0; use application-layer response caching |

### Graduation Criteria

- [x] Understand why T=0 is not byte-exact deterministic
- [x] Know when to use `system_fingerprint` monitoring in production
- [x] Can set appropriate `max_tokens` for different task types without trial and error
- [x] Understand that `seed` is not a reproducibility solution

---

## Concept 2 — Transformer Architecture

**Status:** 📖 Active
**Concept note:** [`research/concepts/transformers.md`](../research/concepts/transformers.md)

### What this chapter answers

> How does scaled dot-product attention work mechanically — why is its memory O(n²) — and how do FlashAttention, sparse attention, and SSMs solve the long-context problem?

### Core skills developed

- Implementing scaled dot-product attention from scratch (NumPy)
- Proving the O(n²) memory complexity of full attention empirically
- Understanding how FlashAttention achieves the same output with O(n) memory I/O
- Interpreting what individual attention heads specialise in over real text

### Experiments

| ID | Topic | Status |
|----|-------|:------:|
| EXP-04 | Self-Attention Mechanics (NumPy) | ✅ Complete |
| EXP-04b | FlashAttention Tiled Computation (NumPy) ← [RQ-04](../research/questions/open_questions.md#rq-04) | 📋 Planned |
| *(slot 3)* | *(reserved — possibly RQ-11: attention head specialisation)* | — |

### Graduation Criteria

- [ ] Can implement multi-head attention without a framework
- [ ] Can explain why FlashAttention tile-based computation avoids materialising the full n×n matrix
- [ ] Knows the memory footprint formula: `n² × d_model × 4 bytes` at inference
- [ ] Understands why SSMs (Mamba, etc.) are architecturally different from attention, not just faster

---

## Concept 3 — Embeddings

**Status:** 📋 Planned (activate after Concept 2 closes)
**Concept note:** [`research/concepts/embeddings.md`](../research/concepts/embeddings.md)

### What this chapter answers

> How do embedding models project tokens and sentences into a geometric space — and where does this geometric representation break down for domain-specific text?

### Core skills developed

- Computing and comparing sentence embeddings using OpenAI `text-embedding-3-small`
- Measuring semantic similarity with cosine distance vs Euclidean distance
- Identifying when general-purpose embeddings degrade for specialised domains
- Understanding the embedding pipeline in a RAG system (encode → index → retrieve)

### Experiments

| ID | Topic | Status |
|----|-------|:------:|
| EXP-06 | Sentence Embeddings & Cosine Similarity | 📋 Planned |
| EXP-06b | Domain Degradation Test ← [RQ-05](../research/questions/open_questions.md#rq-05) | 📋 Planned |
| *(slot 3)* | *(reserved)* | — |

### Graduation Criteria

- [ ] Can embed and cluster sentences by semantic theme
- [ ] Understands the difference between cosine similarity (angle) and L2 distance (magnitude)
- [ ] Knows when to use fine-tuned embeddings vs general-purpose models
- [ ] Can explain why MTEB benchmarks correlate with RAG retrieval quality

---

## Concept 4 — RAG: Retrieval-Augmented Generation

**Status:** 📋 Planned (activate after Concept 3 closes)
**Concept note:** [`research/concepts/rag.md`](../research/concepts/rag.md)

### What this chapter answers

> How do chunk size, retrieval strategy, and context window budget interact to determine RAG answer quality — and what is the minimal production-grade RAG architecture?

### Core skills developed

- Building a naive RAG pipeline (embed → FAISS index → retrieve → generate)
- Measuring the effect of chunk size on retrieval precision and recall
- Implementing hybrid retrieval (dense + sparse)
- Debugging RAG failures: bad retrieval vs bad generation

### Experiments

| ID | Topic | Status |
|----|-------|:------:|
| EXP-07 | Naive RAG Pipeline | 📋 Planned |
| EXP-08 | Chunk Size Optimisation ← [RQ-07](../research/questions/open_questions.md#rq-07) | 📋 Planned |
| *(slot 3)* | *(reserved — possibly hybrid retrieval)* | — |

### Graduation Criteria

- [ ] Can build a working RAG system from scratch (no LangChain abstraction)
- [ ] Knows the retrieval precision/recall tradeoffs at 128, 256, 512, 1024 token chunk sizes
- [ ] Can diagnose: "is this a retrieval failure or a generation failure?"
- [ ] Understands when fine-tuning beats RAG and vice versa

---

## Concept 5 — Agents & Tool Use

**Status:** 📋 Planned (activate after Concept 4 closes)
**Concept note:** [`research/concepts/agents.md`](../research/concepts/agents.md)

### What this chapter answers

> How does the ReAct loop enable reliable multi-step reasoning with tools — and how do temperature, tool schema design, and memory type affect agent correctness in production?

### Core skills developed

- Implementing the ReAct loop (Reason → Act → Observe → Reason)
- Designing tool schemas that minimise argument hallucination
- Measuring temperature's effect on tool-call consistency
- Understanding agent memory types and their failure modes

### Experiments

| ID | Topic | Status |
|----|-------|:------:|
| EXP-10 | Single-Tool Agent (Calculator + Search) | 📋 Planned |
| EXP-11 | Multi-Tool Agent with Memory | 📋 Planned |
| EXP-12 | Agent Temperature & Reliability ← [RQ-08](../research/questions/open_questions.md#rq-08) | 📋 Planned |

### Graduation Criteria

- [ ] Can implement a ReAct agent without LangChain
- [ ] Knows the tool schema properties that reduce hallucinated arguments
- [ ] Can explain the risk of infinite loops and how to bound agent execution
- [ ] Understands why T=0 does not guarantee reliable tool selection (from EXP-05 → EXP-12 link)

---

## Concept 6 — Evaluation & Reliability

**Status:** 📋 Planned (activate after Concept 5 closes)

### What this chapter answers

> How do you measure whether an LLM system is working correctly at scale — and what evaluation signals are reliable enough to trigger automated production alerts?

### Core skills developed

- LLM-as-judge evaluation pattern (pros, failure modes, cost)
- Structured output validation (parser-level vs semantic)
- Building automated regression test suites for LLM outputs
- Knowing when human evaluation is unavoidable

### Experiments

| ID | Topic | Status |
|----|-------|:------:|
| EXP-13 | LLM-as-Judge Evaluation | 📋 Planned |
| EXP-14 | Structured Output Validation ← [RQ-09](../research/questions/open_questions.md#rq-09) | 📋 Planned |
| *(slot 3)* | *(reserved)* | — |

### Graduation Criteria

- [ ] Can implement LLM-as-judge scoring with known failure modes accounted for
- [ ] Knows which `finish_reason` signals require automatic retry vs escalation
- [ ] Can build a regression test suite that runs on every model version change
- [ ] Understands the distinction between format validity, semantic validity, and factual accuracy

---

## Concept 7 — Production AI Systems

**Status:** 📋 Planned (activate after Concept 6 closes)

### What this chapter answers

> How do you move from a working AI prototype to a production system — managing latency, cost, observability, safe deployment, and graceful degradation?

### Core skills developed

- Latency profiling an LLM API call pipeline end-to-end
- Response caching, streaming, and fallback architectures
- Cost modelling (tokens × price × request rate)
- LLM observability: traces, spans, token counters, error rates
- Blue/green deployment for model version changes

### Experiments

| ID | Topic | Status |
|----|-------|:------:|
| EXP-15 | Production Pipeline Profiling | 📋 Planned |
| *(slot 2)* | *(TBD — determined when concept becomes Active)* | — |
| *(slot 3)* | *(reserved)* | — |

### Graduation Criteria

- [ ] Can profile and optimise an LLM API call pipeline to <2s P95 latency
- [ ] Knows the cost per 1,000 requests at different model + context sizes
- [ ] Has implemented a `system_fingerprint` change alert
- [ ] Can explain a safe model upgrade strategy (parallel eval → shadow traffic → gradual rollout)

---

## Progress Tracker

| Concept | Status | Experiments Done | Key Insight |
|---------|:------:|:----------------:|------------|
| 1 — LLM Behavior | ✅ Complete | 4/3 (grandfathered) | T=0 + seed ≠ determinism; use response caching |
| 2 — Transformer Architecture | 📖 Active | 1/3 | O(n²) attention confirmed at n=2048: 16 MB / 59 ms |
| 3 — Embeddings | 📋 Planned | 0/3 | — |
| 4 — RAG | 📋 Planned | 0/3 | — |
| 5 — Agents | 📋 Planned | 0/3 | — |
| 6 — Evaluation | 📋 Planned | 0/3 | — |
| 7 — Production Systems | 📋 Planned | 0/3 | — |

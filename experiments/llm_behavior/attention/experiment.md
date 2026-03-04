---
title: "Experiment 04 — Self-Attention Mechanics"
tags: [experiment, attention, transformer, llm-internals, numpy]
aliases: [attention-experiment, exp-04]
---

# Experiment 04 — Self-Attention Mechanics

**Phase:** Transformer & Representation Learning
**Status:** Complete

---

## Hypothesis

Self-attention requires every token to compare itself against every other token, producing an n×n score matrix. This fundamental structure makes memory complexity O(n²) in sequence length — the root cause of context window limits in all transformer models.

## Variables

| Variable | Values |
|---|---|
| Token counts (complexity sweep) | 8, 64, 256, 512, 1024, 2048 |
| Embedding dimension (d_model) | 4 (demo), 64 (sweep) |
| Attention heads | 1 (single), 2 (multi-head) |
| Libraries | NumPy only — no ML framework |

## Method

Implement scaled dot-product attention and 2-head multi-head attention from scratch using only NumPy. Measure the actual shape of the attention weight matrix at each step. Run a complexity sweep measuring wall-clock time and memory footprint across token sequence lengths from 8 to 2048.

## Key Questions

- Why is the attention weight matrix always n×n?
- What are the memory and compute consequences at 10,000 tokens?
- Why is full attention memory O(n²) and not O(n)?
- How does multi-head attention work without increasing memory beyond O(n²)?
- What architectural alternatives (FlashAttention, SSMs) address the quadratic bottleneck?

## Run

```bash
python experiments/llm_behavior/attention/code.py
```

No API key required — pure NumPy computation.

## Outputs

| File | Contents |
|---|---|
| `results.md` | Attention weight matrices, row-sum verification, complexity sweep table |
| `analysis.md` | Step-by-step derivation, O(n²) proof, FlashAttention/SSM comparison, RAG connections |

## Key Finding

Live sweep confirmed O(n²) scaling: n=512 → 1 MB / 4 ms; n=2048 → 16 MB / 59 ms (4× memory, ~15× compute per 2× token increase). At n=10,000: ~381 MB per head per layer for the attention matrix alone — making 32-layer, 8-head models impractical without FlashAttention at this scale.

---

## Links

**Concepts:**
- [`Transformer Architecture`](../../../research/concepts/transformers.md) — scaled dot-product attention, O(n²) memory complexity, FlashAttention

**Research Questions raised:**
- [RQ-04](../../../research/questions/open_questions.md#rq-04--flashattention-tiled-computation) — How does FlashAttention achieve identical output with O(n) memory I/O through tiled computation?
- [RQ-11](../../../research/questions/open_questions.md#rq-11--attention-head-specialisation-on-real-text) — Do attention heads on real semantic sentences show interpretable specialisation patterns?

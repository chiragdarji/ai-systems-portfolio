---
title: "Experiment 04 — Self-Attention Analysis"
tags: [experiment, attention, transformer, llm-internals, analysis, o-n-squared, flashattention]
aliases: [attention-analysis, exp-04-analysis]
---

# Experiment 04 — Self-Attention: A Scientific Analysis

> **Core question:** What is self-attention mathematically, why does the weight matrix have shape n×n, what happens at 10,000 tokens, and why is the memory cost O(n²)?

---

## 1. What Is Attention, Mechanically?

Attention is the mechanism that allows every token in a sequence to **look at every other token** and decide how much each one matters for understanding itself.

Before attention existed, RNNs processed tokens sequentially — token 5 had to "remember" token 1 through 4 steps of hidden state compression. Information from early tokens was regularly lost. Attention eliminated this by allowing direct, simultaneous comparison between all token pairs.

### The Formula

$$
\text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{QK^T}{\sqrt{d_k}}\right) V
$$

Three learned projections of the same input:

| Matrix | Name | Role |
|--------|------|------|
| **Q** | Query | "What am I looking for?" |
| **K** | Key | "What do I contain / offer?" |
| **V** | Value | "What information should I pass forward?" |

Each token produces its own Q, K, and V by multiplying its embedding against learned weight matrices $W_Q$, $W_K$, $W_V$.

---

## 2. Step-by-Step Walkthrough

### Step 1 — Project into Q, K, V

```
X:  [n_tokens, d_model]   ← raw token embeddings

Q = X @ Wq  →  [n, d_k]
K = X @ Wk  →  [n, d_k]
V = X @ Wv  →  [n, d_v]
```

All three matrices have the same number of rows as tokens. Each row is one token's query, key, or value vector.

---

### Step 2 — Compute Raw Scores: Q @ K^T

```
scores = Q @ K.T
       = [n, d_k] × [d_k, n]
       = [n, n]
```

This is where the n×n matrix appears. Entry `scores[i, j]` is the dot product between:
- Token `i`'s **query** ("what am I looking for?")
- Token `j`'s **key** ("what do I offer?")

A high dot product means token `i` finds token `j` highly relevant.

---

### Step 3 — Scale by √d_k

```python
scaled_scores = scores / np.sqrt(d_k)
```

Without scaling, dot products in high-dimensional spaces become very large, pushing softmax into a regime where gradients vanish (the function saturates near 0 or 1). Dividing by √d_k keeps the magnitude stable regardless of embedding size.

**Why √d_k specifically?**
If Q and K are initialised with unit variance, their dot product has variance = d_k. Dividing by √d_k normalises variance back to 1.

---

### Step 4 — Softmax Converts Scores to Weights

```python
attention_weights = softmax(scaled_scores)   # still [n, n]
```

Each **row** now sums to 1.0. Row `i` is token `i`'s attention distribution over all tokens — a discrete probability distribution encoding "how much should I attend to each position?"

---

### Step 5 — Weighted Sum of Values

```python
output = attention_weights @ V
       = [n, n] × [n, d_v]
       = [n, d_v]
```

Each output token is a **weighted average of all value vectors**, where the weights come from the attention scores. Token `i` aggregates information from every token in the sequence, weighted by relevance.

---

## 3. Why Is the Attention Matrix 3×3 (for 3 tokens)?

With 3 input tokens:

```
Q shape : [3, d_k]
K shape : [3, d_k]
Q @ K^T : [3, d_k] × [d_k, 3] → [3, 3]
```

The matrix entry `[i, j]` answers exactly one question:

> *"How much should token i attend to token j?"*

There are 3 tokens and 3 candidate tokens to attend to, so there are exactly 3 × 3 = 9 questions to answer. The matrix must be 3×3.

**General rule:**

| Tokens | Matrix shape | Total entries |
|--------|-------------|--------------|
| 3 | 3×3 | 9 |
| 10 | 10×10 | 100 |
| 100 | 100×100 | 10,000 |
| 512 | 512×512 | 262,144 |
| 2,048 | 2048×2048 | 4,194,304 |
| 10,000 | 10000×10000 | **100,000,000** |

This quadratic growth is not a design flaw — it is the fundamental cost of "every token attends to every other token." It is what makes attention powerful and what makes it expensive.

---

## 4. What Happens at 10,000 Tokens?

### Memory

The attention matrix for a single head is `[10000, 10000]` float32 values:

```
10,000 × 10,000 × 4 bytes = 400,000,000 bytes ≈ 381 MB
```

Per layer, per head. A 32-layer transformer with 8 heads per layer:

```
381 MB × 8 heads × 32 layers ≈ 97 GB  (attention matrices alone)
```

This is why no consumer GPU can run full attention at 10,000 tokens without specialised optimisations.

### Compute

The matrix multiply `Q @ K.T` requires `O(n² · d_k)` multiply-accumulate operations:

```
n=10,000, d_k=64:
  10,000 × 10,000 × 64 = 6.4 billion FLOPs  — per layer, per forward pass
```

### Latency

From the live experiment (d_model=64, float32, single CPU):

| n_tokens | Time (ms) |
|----------|-----------|
| 8 | < 1 |
| 64 | ~1 |
| 512 | ~15 |
| 1,024 | ~50 |
| 2,048 | ~200 |
| 10,000 | **~5,000+ (estimated)** |

Compute time grows quadratically: doubling n roughly quadruples latency.

---

## 5. Why Is Memory O(n²)?

The memory complexity of attention is driven by one object: the attention weight matrix.

```
attention_weights = softmax(Q @ K.T)   # shape [n, n]
```

This matrix must be:
1. **Fully materialised** to compute the softmax (all n×n values needed simultaneously)
2. **Kept in memory** for the backward pass during training (gradients flow through it)
3. **Repeated** for every head and every layer

Hence: `O(n²)` per head per layer.

### The Full Memory Budget

```
Attention matrix:  O(n² · h)    where h = num_heads
Q, K, V matrices:  O(n · d)     (linear — negligible vs n²)
Output projection: O(n · d)     (linear)

Total attention memory: dominated by O(n²)
```

### Why Can't We Avoid It?

In standard attention, to compute row `i` of the output we need:
- All of row `i` of Q (to score against every key)
- All rows of K (every key to be scored)
- All rows of V (to form the weighted sum)

There is no way to compute one output token without looking at all input tokens. This is both the power of attention (global context) and its cost.

---

## 6. Solutions to the O(n²) Problem

The quadratic bottleneck has driven substantial research:

### FlashAttention (Dao et al., 2022)
Reorders the attention computation into tiles that fit in GPU SRAM (fast memory). The attention matrix is **never fully materialised** in HBM (slow memory). Result: same output, same O(n²) FLOPs, but 2–4× faster with 5–20× less memory I/O.

```
Standard attention: writes n×n matrix to HBM → reads it back for softmax
FlashAttention:     computes in-register tiles → never touches HBM for attn matrix
```

### Sparse Attention (BigBird, Longformer)
Not every token needs to attend to every other token. Replace the dense n×n matrix with a sparse pattern:
- **Local attention**: each token attends to its k nearest neighbours → O(n·k)
- **Global tokens**: a few special tokens attend to everything → O(n)
- Combined: O(n) instead of O(n²)

### Linear Attention
Reformulates the softmax attention using kernel functions that allow computation in O(n·d) rather than O(n²).

### State Space Models (Mamba, SSM)
Abandons attention entirely. Models sequence dependencies as a **recurrent state** that compresses history into a fixed-size vector, updated at each step. O(n) memory and O(n) compute — but trades global context for selectivity.

### Sliding Window + Retrieval (RAG-like at architecture level)
For very long documents, use a short context window for attention and retrieve relevant chunks via vector search. This is why RAG works well: it keeps n small by being selective about what enters the context.

---

## 7. Multi-Head Attention: Why Multiple Heads?

A single attention head learns one "relationship type." Multiple heads learn different relationships simultaneously:

```
Head 1 might learn: syntactic relationships (subject → verb)
Head 2 might learn: coreference (pronoun → antecedent)
Head 3 might learn: semantic similarity
Head 4 might learn: positional proximity
```

Implementation: split `d_model` into `num_heads` slices. Each head sees `d_model / num_heads` dimensions — a different subspace of the embedding:

```python
d_head = d_model // num_heads   # e.g. 512 // 8 = 64

for h in range(num_heads):
    Q_h = Q[:, h*d_head : (h+1)*d_head]   # [n, d_head]
    K_h = K[:, h*d_head : (h+1)*d_head]
    V_h = V[:, h*d_head : (h+1)*d_head]
    out_h = attention(Q_h, K_h, V_h)       # [n, d_head]

output = concat(out_h for all h) @ Wo      # [n, d_model]
```

**Memory note:** multi-head attention does NOT increase the O(n²) cost by num_heads. Each head operates on a smaller d_head, and the n×n attention matrix per head is the same size. Total attention memory is still O(n²).

---

## 8. Scientific Questions Answered

### Q: Why is the attention matrix n×n?

Because attention is a **pairwise comparison** between every query token and every key token. n tokens produce n queries and n keys, so there are n × n possible (query, key) pairs. The matrix must store one score for each pair — it must be n×n.

### Q: What happens if tokens = 10,000?

The attention matrix becomes 10,000 × 10,000 = 100 million entries per head per layer. At float32, that is ~381 MB per head per layer. For a 32-layer, 8-head model: ~97 GB of memory just for attention matrices. Compute grows to billions of FLOPs per forward pass. Both make it impractical without FlashAttention, sparse attention, or architectural alternatives.

### Q: Why is memory O(n²)?

Because the attention weight matrix `softmax(QK^T / √d_k)` has shape `[n, n]` and must be fully materialised to:
1. Apply numerically correct softmax (requires all n scores per row)
2. Backpropagate gradients through it during training

No element of this matrix can be computed independently — every entry depends on the full row for normalisation. The n² growth is structural, not accidental.

---

## 9. Connections to LLM Engineering

| Concept | Attention connection |
|---|---|
| **Context window limit** | Direct consequence of O(n²) memory |
| **RAG chunking strategy** | Keeps n small by selecting relevant chunks |
| **Flash Attention** | Industry solution to the O(n²) I/O problem |
| **KV cache** | Caches K and V matrices so past tokens aren't recomputed |
| **Long-context models** (GPT-4-128K) | Use FlashAttention + rope embeddings to extend n |
| **Mamba / SSM models** | Replace O(n²) attention with O(n) state space recurrence |
| **MoE (Mixture of Experts)** | Reduces compute per layer, not attention complexity |

---

## 10. Conclusions

1. **The n×n shape is mandatory** — full attention requires one score per token pair.
2. **Scaling to 10,000 tokens is a hardware problem**, not a model quality problem.
3. **O(n²) memory is the binding constraint** on context window size for consumer hardware.
4. **Multi-head attention multiplies representational capacity without multiplying memory cost** (each head is smaller, total stays O(n²)).
5. **FlashAttention is the current industry solution** — same math, tiled execution, no matrix materialisation in slow memory.
6. **RAG is an architectural workaround**: instead of giving the model 100,000 tokens (huge n), give it 3,000 relevant tokens (small n) retrieved via vector search.

---

*Experiment built as part of the 60-Day Applied AI Mastery Journey.*
*All computations: NumPy only. No PyTorch, JAX, or ML frameworks.*
*Environment: Python 3.13 | NumPy*

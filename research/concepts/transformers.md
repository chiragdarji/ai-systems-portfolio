---
title: "Concept — Transformers"
tags: [research, concepts, transformer, attention, llm-internals, architecture, self-attention]
aliases: [transformers, transformer-architecture, attention-is-all-you-need]
---

# Transformers

> The neural network architecture that replaced RNNs and became the foundation of every major LLM.

---

## Definition

A Transformer is a deep learning architecture based entirely on **self-attention mechanisms** — without recurrence or convolution. Introduced in "Attention Is All You Need" (Vaswani et al., 2017), it processes entire sequences in parallel and captures long-range dependencies directly through pairwise token comparisons.

All modern LLMs (GPT-4, Claude, Gemini, Llama) are Transformer-based decoder models.

---

## How It Works

### High-Level Architecture

```
Input Tokens
     ↓
Token Embeddings + Positional Encoding
     ↓
┌─────────────────────────────────┐
│  Transformer Block × N layers   │
│  ┌───────────────────────────┐  │
│  │  Multi-Head Self-Attention│  │
│  │  + Add & LayerNorm        │  │
│  ├───────────────────────────┤  │
│  │  Feed-Forward Network     │  │
│  │  + Add & LayerNorm        │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
     ↓
Linear Projection → Softmax → Next Token Probabilities
```

### 1. Token Embeddings + Positional Encoding

Raw tokens are mapped to dense vectors in `d_model`-dimensional space. Since Transformers process all tokens in parallel (no sequential order), **positional encodings** are added to embed order information:

```
embedding(token_i) = token_embed(i) + positional_encode(position_i)
```

Modern LLMs use **Rotary Position Embeddings (RoPE)** instead of fixed sinusoidal encodings, enabling better generalisation to unseen sequence lengths.

### 2. Scaled Dot-Product Attention

The core operation — every token attends to every other token:

$$\text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{QK^T}{\sqrt{d_k}}\right) V$$

- **Q (Query):** "What am I looking for?"
- **K (Key):** "What do I contain?"
- **V (Value):** "What should I pass forward?"

The division by `√d_k` prevents softmax saturation in high-dimensional spaces.

### 3. Multi-Head Attention

Instead of one attention computation, the model runs `h` independent heads in parallel — each in a different `d_model/h`-dimensional subspace:

```python
for h in range(num_heads):
    Q_h, K_h, V_h = split into head h's subspace
    out_h = attention(Q_h, K_h, V_h)     # [n, d_head]

output = concat(all heads) @ W_o         # [n, d_model]
```

Each head learns a different relationship type (syntactic, semantic, positional, coreference). Multi-head attention does **not** increase memory beyond O(n²) — each head is smaller.

### 4. The n×n Attention Matrix

With `n` input tokens:

```
Q @ K.T = [n, d_k] × [d_k, n] = [n, n]
```

Entry `[i, j]` answers: *"How much should token i attend to token j?"*

This matrix is the source of Transformer power (global context) and cost (O(n²) memory).

| n_tokens | Attention matrix | Memory (float32) |
|---|---|---|
| 512 | 512 × 512 | ~1 MB |
| 2,048 | 2048 × 2048 | ~16 MB |
| 10,000 | 10K × 10K | ~381 MB per head |
| 128,000 | 128K × 128K | ~62 GB per head |

### 5. Feed-Forward Network (FFN)

After attention, each token's representation is processed independently through a two-layer MLP:

```
FFN(x) = max(0, xW₁ + b₁) W₂ + b₂
```

The FFN is where most of the model's **factual knowledge** is stored — it acts as a key-value memory over token representations.

### 6. Encoder vs Decoder

| Type | Attention mask | Used for | Examples |
|---|---|---|---|
| **Encoder** | Bidirectional (all tokens see all tokens) | Classification, embeddings | BERT, RoBERTa |
| **Decoder** | Causal (token i only sees tokens ≤ i) | Text generation | GPT-4, Claude, Llama |
| **Encoder-Decoder** | Encoder: bidirectional; Decoder: causal + cross-attention | Translation, summarisation | T5, BART |

LLMs used for chat are **decoder-only** with causal masking.

---

## Why It Matters

### 1. Parallelism over sequences
RNNs processed tokens sequentially — token n had to wait for token n-1. Transformers process all tokens simultaneously, making them orders of magnitude faster to train on modern GPU/TPU hardware.

### 2. Direct long-range dependencies
RNNs compressed all past context into a fixed hidden state. Transformers let token 1 and token 512 directly attend to each other with no information loss.

### 3. Scalability
Transformer performance scales predictably with model size, data, and compute (Kaplan et al., 2020 — Scaling Laws). This enabled GPT-3, GPT-4, Claude, and Gemini.

### 4. Universal architecture
The same architecture powers text, code, images (ViT), audio (Whisper), video, and multimodal models — only the tokenisation and training objectives change.

---

## Limitations

| Limitation | Root Cause | Current Solutions |
|---|---|---|
| **O(n²) memory** | `QK^T` attention matrix must be materialised | FlashAttention, sparse attention, SSMs |
| **Context window ceiling** | GPU memory cannot hold the full n×n matrix beyond a threshold | FlashAttention-2, RoPE, sliding window |
| **Positional generalisation** | Standard PE doesn't generalise beyond training length | RoPE, ALiBi |
| **Quadratic compute** | Each forward pass is O(n²·d) FLOPs | Efficient attention variants |
| **KV cache memory** | Storing past K/V pairs for autoregressive generation requires O(n·d) per layer | Grouped-query attention (GQA), MLA |

---

## Related Experiments

| Experiment | What It Tests | Key Finding |
|---|---|---|
| [Experiment 04 — Self-Attention](../../experiments/llm_behavior/attention/experiment.md) | Self-attention mechanics built from scratch with NumPy | At n=2048: 16 MB and 59 ms; O(n²) confirmed empirically |
| [Experiment 03 — Token Limit](../../experiments/llm_behavior/token_limit/experiment.md) | `max_tokens` and context window implications | Token budgeting is constrained by the same O(n²) memory |
| [Experiment 01 — Temperature](../../experiments/llm_behavior/temperature/experiment.md) | Sampling from the Transformer's output distribution | T=0 is not byte-exact due to distributed GPU FP non-associativity |

---

## Further Reading

- [Attention Is All You Need — Vaswani et al. (2017)](https://arxiv.org/abs/1706.03762)
- [FlashAttention — Dao et al. (2022)](https://arxiv.org/abs/2205.14135)
- [The Illustrated Transformer — Jay Alammar](https://jalammar.github.io/illustrated-transformer/)
- [Scaling Laws for Neural Language Models — Kaplan et al. (2020)](https://arxiv.org/abs/2001.08361)

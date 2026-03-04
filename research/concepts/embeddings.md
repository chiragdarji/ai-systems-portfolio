---
title: "Concept — Embeddings"
tags: [research, concepts, embeddings, vector-search, semantic-similarity, rag, llm-internals]
aliases: [embeddings, vector-embeddings, semantic-vectors]
---

# Embeddings

> Dense numerical representations of meaning — the bridge between language and mathematics.

---

## Definition

An embedding is a fixed-length vector of floating-point numbers that encodes the **semantic meaning** of a piece of text (token, sentence, document, or code). Semantically similar texts produce geometrically nearby vectors. This enables similarity search, clustering, and retrieval over language using pure linear algebra.

```
"The cat sat on the mat"  →  [0.021, -0.341, 0.887, ..., 0.102]  (1536 dimensions)
"A feline rested on a rug" → [0.019, -0.338, 0.891, ..., 0.097]  (nearby)
"Quarterly revenue report"  → [-0.612, 0.201, -0.345, ..., 0.553] (distant)
```

---

## How It Works

### 1. Token-Level Embeddings (Inside the Transformer)

At the input layer, every token is mapped to a dense vector via a **learned embedding matrix** `E ∈ ℝ^{vocab_size × d_model}`:

```
token_id → E[token_id] → d_model-dimensional vector
```

After passing through all Transformer layers, the hidden state at position `i` is a **contextualised** embedding — it encodes not just the token's identity but its meaning in context.

### 2. Sentence / Document Embeddings

To embed an entire sentence or document, a **dedicated embedding model** (e.g. `text-embedding-3-small`) processes the full text and pools the token representations into a single vector:

```
Document → Embedding Model → Single vector ∈ ℝ^d
```

Common pooling strategies:
- **[CLS] token** (BERT-style): take the representation of a special classification token
- **Mean pooling**: average all token vectors
- **Last token** (GPT-style): take the final token's representation

### 3. Cosine Similarity

Semantic similarity is measured by the angle between vectors, not their magnitude:

$$\text{cosine\_similarity}(A, B) = \frac{A \cdot B}{\|A\| \cdot \|B\|}$$

| Score | Interpretation |
|---|---|
| 1.0 | Identical meaning |
| 0.9+ | Very similar |
| 0.7–0.9 | Related topic |
| 0.5–0.7 | Loosely related |
| < 0.5 | Unrelated |

### 4. Vector Space Properties

Well-trained embeddings exhibit geometric regularities:

```
king - man + woman ≈ queen        (analogy arithmetic)
paris - france + italy ≈ rome     (capital relation)
```

This structure emerges from training on large corpora where co-occurrence statistics encode meaning.

### 5. The Embedding Pipeline

```
Raw text
   ↓
Tokenisation (BPE / WordPiece)
   ↓
Token IDs → Embedding Lookup → d_model vectors
   ↓
Transformer Layers (contextualisation)
   ↓
Pooling → Single vector
   ↓
[Optional] L2 Normalisation
   ↓
Store in Vector Database (Pinecone, Chroma, Weaviate, FAISS)
```

### 6. Approximate Nearest Neighbour Search (ANN)

Searching 1M+ vectors for the closest match is expensive at O(n·d) brute force. Production systems use ANN indices:

| Index Type | Algorithm | Tradeoff |
|---|---|---|
| **HNSW** | Hierarchical navigable small world | Fast query, high memory |
| **IVF** | Inverted file with clustering | Lower memory, approximate |
| **PQ** | Product quantisation | Very compressed, lossy |
| **Flat** | Exact brute-force | Exact results, slow at scale |

---

## Why It Matters

### 1. Enables semantic search over any corpus

Traditional keyword search (BM25, TF-IDF) matches exact terms. Embedding search matches **meaning** — finding "cardiac arrest" when searching for "heart attack".

### 2. Foundation of RAG

RAG pipelines convert every document chunk to an embedding at index time, then embed the user's query at retrieval time, and return the top-k most similar chunks. Without embeddings, RAG is impossible.

### 3. Cross-modal retrieval

The same embedding space can represent text and images (CLIP), text and code (CodeBERT), or text and audio — enabling multi-modal retrieval from a single query.

### 4. Clustering and classification

Embeddings can be clustered (k-means, HDBSCAN) without labels — useful for topic discovery, anomaly detection, and intent classification.

---

## Limitations

| Limitation | Description |
|---|---|
| **Fixed context window** | Embedding models have input limits (~8K tokens). Long documents must be chunked. |
| **Semantic drift** | Embeddings encode training distribution. Domain-specific language (legal, medical) may embed poorly without fine-tuning. |
| **Out-of-vocabulary concepts** | Very recent events, niche technical terms, or newly coined words may not embed meaningfully. |
| **Dimensionality vs cost** | Higher-dimensional embeddings (3072-d vs 1536-d) improve quality but double storage and compute costs. |
| **No explicit reasoning** | Embeddings encode surface meaning, not logical structure. "A is not B" and "A is B" may have similar embeddings. |
| **Chunk boundary sensitivity** | Splitting a document at the wrong boundary can cut a sentence mid-thought, degrading embedding quality for that chunk. |

---

## Related Experiments

| Experiment | What It Tests | Connection |
|---|---|---|
| [Experiment 04 — Self-Attention](../../experiments/llm_behavior/attention/experiment.md) | The attention mechanism that produces contextualised embeddings | Each Transformer layer refines token embeddings through self-attention |
| [Experiment 03 — Token Limit](../../experiments/llm_behavior/token_limit/experiment.md) | `max_tokens` and RAG chunk sizing | Chunk size must align with both embedding model limits and response budget |

---

## Planned Experiments

- **Experiment 05** — Compute sentence embeddings with `text-embedding-3-small`, measure cosine similarity across semantically close and distant pairs
- **Experiment 06** — Compare chunk sizes (128, 256, 512, 1024 tokens) and measure retrieval precision in a RAG pipeline

---

## Further Reading

- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [The Illustrated Word2Vec — Jay Alammar](https://jalammar.github.io/illustrated-word2vec/)
- [MTEB: Massive Text Embedding Benchmark](https://huggingface.co/spaces/mteb/leaderboard)
- [FAISS — Facebook AI Similarity Search](https://github.com/facebookresearch/faiss)

---
title: "Concept — Retrieval-Augmented Generation (RAG)"
tags: [research, concepts, rag, retrieval, embeddings, llm-behavior, hallucination, vector-search]
aliases: [rag, retrieval-augmented-generation, rag-architecture]
---

# Retrieval-Augmented Generation (RAG)

> Grounding LLM responses in external knowledge to reduce hallucination and extend past the training cutoff.

---

## Definition

Retrieval-Augmented Generation (RAG) is an architectural pattern that enhances LLM responses by dynamically injecting relevant external knowledge into the prompt at query time. Instead of relying solely on parametric knowledge (what the model learned during training), RAG retrieves relevant document chunks from a knowledge base and provides them as context.

**Core insight:** LLMs are fluent reasoners, not reliable knowledge stores. RAG separates these concerns — use the model for reasoning and language, use the retrieval system for facts.

---

## How It Works

### Architecture Overview

```
User Query
    ↓
[1] EMBED query → query_vector
    ↓
[2] SEARCH vector database → top-k relevant chunks
    ↓
[3] BUILD prompt:
      system: "Answer only from the provided context."
      context: [chunk_1, chunk_2, ..., chunk_k]
      user: original query
    ↓
[4] GENERATE response with LLM
    ↓
Response (grounded in retrieved documents)
```

### Phase 1 — Indexing (Offline)

```
Raw documents (PDFs, web pages, databases)
    ↓
Document Loader (LlamaIndex Readers, LangChain loaders)
    ↓
Text Splitter (chunk into n-token segments with overlap)
    ↓
Embedding Model → dense vector per chunk
    ↓
Vector Store (Chroma, Pinecone, Weaviate, FAISS)
         stores: (chunk_text, embedding, metadata)
```

### Phase 2 — Retrieval (Online, per query)

```
User query
    ↓
Embed query → query_vector
    ↓
ANN search in vector store → top-k chunks by cosine similarity
    ↓
[Optional] Re-ranking (cross-encoder, MMR, BM25 hybrid)
    ↓
Selected context chunks
```

### Phase 3 — Generation (Online, per query)

```
System prompt + context chunks + user query
    ↓
LLM (gpt-4o-mini, claude-3-haiku, etc.)
    ↓
Answer grounded in retrieved context
    ↓
[Optional] Citation extraction, faithfulness check
```

### Chunking Strategy

The chunk size used at index time is the most impactful RAG design decision:

| Chunk size | Precision | Recall | Use case |
|---|---|---|---|
| 128 tokens | High (tight) | Low (misses context) | Factual Q&A, entity lookup |
| 256–512 tokens | Balanced | Balanced | General RAG |
| 512–1024 tokens | Low (noisy) | High (broad context) | Summarisation, multi-hop reasoning |

**Chunk overlap** (e.g. 50–100 token overlap between consecutive chunks) prevents cutting sentences at boundaries and improves recall.

### Retrieval Strategies

| Strategy | Mechanism | Best for |
|---|---|---|
| **Dense retrieval** | Cosine similarity between embeddings | Semantic similarity |
| **Sparse retrieval (BM25)** | TF-IDF keyword matching | Exact term match |
| **Hybrid retrieval** | Combines dense + sparse scores | Best overall recall |
| **Multi-query** | Generates multiple query reformulations | Ambiguous queries |
| **HyDE** | Hypothetical document embedding | Queries with no close keyword match |

---

## Why It Matters

### 1. Eliminates training cutoff limitations
RAG can answer questions about events that occurred after the model's training cutoff by indexing current documents.

### 2. Dramatically reduces hallucination
When the model is instructed to answer only from provided context and the context is relevant, factual errors drop significantly. The model becomes a reader, not a guesser.

### 3. Enables private enterprise knowledge bases
A company can index its internal documentation, policies, and knowledge without fine-tuning any model weights. The knowledge lives in the vector store, not in the model.

### 4. Auditable and updatable
Knowledge can be updated by re-indexing documents — no model retraining required. Every answer can be attributed to source documents.

### 5. Cost-efficient alternative to fine-tuning
Fine-tuning is expensive and requires large labeled datasets. RAG achieves similar (often better) factual grounding using only indexed documents.

---

## Limitations

| Limitation | Description |
|---|---|
| **Retrieval failure** | If the relevant chunk is not retrieved (wrong embedding, poor chunking), the LLM has no grounding and may hallucinate anyway. |
| **Context window pressure** | Injecting k chunks reduces the space available for system prompt and response. |
| **Chunk boundary artifacts** | Splitting mid-sentence destroys the embedding quality for that chunk. |
| **Multi-hop reasoning** | Queries that require combining information from multiple non-adjacent chunks (e.g. "compare A and B") are hard for single-pass RAG. |
| **Embedding semantic gap** | Query embedding and document embedding may not align for complex or domain-specific queries. |
| **Stale index** | If the vector store is not re-indexed after document updates, the RAG system serves outdated information. |
| **Faithfulness** | The LLM may paraphrase retrieved content in ways that subtly change the meaning. Faithfulness evaluation is required in production. |

---

## RAG vs Fine-Tuning

| Dimension | RAG | Fine-Tuning |
|---|---|---|
| **Knowledge update** | Re-index documents | Retrain or LoRA adapt |
| **Cost** | Low (indexing + inference) | High (compute + data) |
| **Auditability** | High (source citations) | Low (parametric) |
| **Latency** | Adds retrieval step (~50–200ms) | Same as base model |
| **Best for** | Factual grounding, private knowledge | Style, format, task specialisation |

**Rule:** Use RAG for knowledge; use fine-tuning for behaviour.

---

## Token Budget Alignment

From Experiment 03, RAG factual answers use ~51 tokens regardless of budget. The binding constraint is the retrieval quality and prompt construction:

```
context_window = system_prompt_tokens
               + (chunk_tokens × num_chunks)
               + user_query_tokens
               + max_tokens (response budget)
               ≤ model_context_limit
```

Typical safe configuration for 128K-context models:
- System prompt: ~200 tokens
- Retrieved chunks: 3 × 500 tokens = 1,500 tokens
- User query: ~50 tokens
- Response budget: 300 tokens
- Total: ~2,050 tokens (well within limit)

---

## Related Experiments

| Experiment | What It Tests | Connection to RAG |
|---|---|---|
| [Experiment 03 — Token Limit](../../experiments/llm_behavior/token_limit/experiment.md) | `max_tokens`, finish_reason, token budgeting | RAG answers complete at ~51 tokens; chunk size must fit context budget |
| [Experiment 04 — Self-Attention](../../experiments/llm_behavior/attention/experiment.md) | O(n²) memory scaling | RAG keeps n small by selecting relevant chunks instead of feeding full documents |
| [Experiment 02 — System Prompt](../../experiments/llm_behavior/system_prompt/experiment.md) | System prompt as behaviour contract | RAG system prompts enforce "answer only from context" grounding |

---

## Planned Projects

- [`projects/rag_assistant/`](../../projects/rag_assistant/README.md) — Build a document-grounded Q&A system over a custom corpus using LlamaIndex + ChromaDB
- [`projects/rag_eval_pipeline/`](../../projects/rag_eval_pipeline/README.md) — Automated faithfulness and relevance evaluation using LLM-as-judge

---

## Further Reading

- [Retrieval-Augmented Generation for NLP — Lewis et al. (2020)](https://arxiv.org/abs/2005.11401)
- [LlamaIndex Documentation](https://docs.llamaindex.ai)
- [Pinecone RAG Guide](https://www.pinecone.io/learn/retrieval-augmented-generation/)
- [RAGAS — RAG Evaluation Framework](https://docs.ragas.io)

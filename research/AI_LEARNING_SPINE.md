---
title: "AI Learning Spine"
tags: [learning-path, curriculum, concepts, spine, ai-systems, roadmap]
aliases: [learning-spine, concept-spine, ai-curriculum]
---

# AI Learning Spine

Ordered sequence of 24 core concepts for mastering AI systems engineering.
Concepts must be studied in layer order — each layer depends on the previous.

> **Progress tracking:** [`AI_RESEARCH_INDEX.md`](../AI_RESEARCH_INDEX.md)
> **To add a missing concept:** `@add_concept <concept_name>`
> **To run an experiment on a concept:** `@create_experiment`

**Legend:**
- ✅ `concept file exists` — [`research/concepts/<name>.md`](concepts/)
- ⬜ `file missing` — run `@add_concept <name>` to create it
- 🔬 `experiment complete` — linked experiment result available
- 📋 `experiment planned` — in registry, not yet run

---

## Progress at a Glance

| Layer | Topic | Concepts | Files Done | Experiments Done |
|-------|-------|:--------:|:----------:|:----------------:|
| 1 | LLM Behavior | 5 | 2 / 5 | 4 / 5 |
| 2 | Transformer Fundamentals | 3 | 1 / 3 | 1 / 3 |
| 3 | Retrieval Systems | 4 | 1 / 4 | 0 / 4 |
| 4 | RAG Systems | 3 | 1 / 3 | 0 / 3 |
| 5 | Tool Use | 2 | 0 / 2 | 0 / 2 |
| 6 | Agents | 2 | 1 / 2 | 0 / 2 |
| 7 | Evaluation | 2 | 0 / 2 | 0 / 2 |
| 8 | Production AI | 3 | 0 / 3 | 0 / 3 |
| **Total** | | **24** | **6 / 24** | **5 / 24** |

---

## Layer 1 — LLM Behavior

> **Core question:** How do LLMs generate output — and what parameters control it?
> **Prerequisite:** None. This is where every AI engineer begins.
> **Chapter reference:** [Chapter 1 — LLM Behavior](../AI_RESEARCH_INDEX.md#chapter-1--llm-behavior)

---

### 1. `temperature`

**What it is:** The scalar that controls the entropy of the token-sampling probability distribution.
**Why it matters:** Every inference call has a temperature setting. Misunderstanding it causes unpredictable outputs in production.
**One-line rule:** High temperature = creative and varied. Low temperature = focused and deterministic. Zero temperature = not byte-exact deterministic.

| Asset | Status | Link |
|-------|:------:|------|
| Concept file | ✅ | [`research/concepts/llm_behavior.md`](concepts/llm_behavior.md) |
| Experiment | 🔬 | [`EXP-01 — Temperature`](../experiments/llm_behavior/temperature/experiment.md) |
| Research question | 🟢 Answered | [RQ-01](questions/open_questions.md#rq-01--temperature-seed-determinism) |

---

### 2. `seed_determinism`

**What it is:** The property (and limits) of using a fixed `seed` parameter to reproduce LLM outputs.
**Why it matters:** Production regression testing and audit trails require reproducibility. Understanding why seed is unreliable forces the correct architecture.
**One-line rule:** `seed` seeds the sampler, not the GPU arithmetic. At T=0 there is nothing to seed. Use response caching.

| Asset | Status | Link |
|-------|:------:|------|
| Concept file | ✅ | [`research/concepts/seed_determinism.md`](concepts/seed_determinism.md) |
| Experiment | 🔬 | [`EXP-05 — Seed Determinism`](../experiments/llm_behavior/seed_determinism/experiment.md) |
| Research question | 🟢 Answered | [RQ-01](questions/open_questions.md#rq-01--temperature-seed-determinism) |

---

### 3. `tokenization`

**What it is:** The process of splitting raw text into subword tokens that the model actually processes — not words, not characters.
**Why it matters:** Token counts drive cost, context window limits, and truncation behaviour. Miscounting tokens causes subtle bugs in production prompt engineering.
**One-line rule:** "Hello world" is 2 tokens. "antidisestablishmentarianism" is 6. Count tokens, not words.

| Asset | Status | Link |
|-------|:------:|------|
| Concept file | ⬜ | `@add_concept tokenization` |
| Experiment | ⬜ | `@create_experiment` after concept file exists |
| Research question | — | — |

---

### 4. `context_window`

**What it is:** The fixed-size input buffer (measured in tokens) that a model can attend to in a single forward pass.
**Why it matters:** Every system prompt + conversation history + response budget must fit inside it. Exceeding it causes hard errors or silent truncation depending on the framework.
**One-line rule:** Context window = the model's working memory. It resets on every call. Nothing persists unless you put it in the prompt.

| Asset | Status | Link |
|-------|:------:|------|
| Concept file | ⬜ | `@add_concept context_window` |
| Experiment | 📋 | Addressed partially in [`EXP-03 — Token Limit`](../experiments/llm_behavior/token_limit/experiment.md) |
| Research question | — | — |

---

### 5. `system_prompts`

**What it is:** The privileged instruction channel that sets model behaviour before any user turn — persona, constraints, output format, domain restriction.
**Why it matters:** In every deployed LLM product, the system prompt is the primary security and quality control mechanism. It is architecture, not configuration.
**One-line rule:** The system prompt is a behaviour contract. It is faithfully followed in cooperative conditions — and it is the first thing an adversary tries to override.

| Asset | Status | Link |
|-------|:------:|------|
| Concept file | ✅ | [`research/concepts/llm_behavior.md`](concepts/llm_behavior.md) *(section: "System Prompt")* |
| Experiment | 🔬 | [`EXP-02 — System Prompt Control`](../experiments/llm_behavior/system_prompt/experiment.md) |
| Research question | 🔴 Open | [RQ-02](questions/open_questions.md#rq-02--prompt-injection-resistance), [RQ-10](questions/open_questions.md#rq-10--system-vs-user-instruction-conflict) |

---

## Layer 2 — Transformer Fundamentals

> **Core question:** How does the transformer architecture compute meaning — and why does its memory scale with the square of sequence length?
> **Prerequisite:** Layer 1 complete. You must understand tokens and context windows before attention makes sense.
> **Chapter reference:** [Chapter 2 — Transformer Architecture](../AI_RESEARCH_INDEX.md#chapter-2--transformer-architecture)

---

### 6. `embeddings`

**What it is:** Dense vector representations that map tokens and sentences into a geometric space where semantic similarity corresponds to geometric proximity.
**Why it matters:** Embeddings are the input to every transformer layer, the basis for vector search, and the retrieval mechanism in RAG.
**One-line rule:** Meaning becomes geometry. "king" − "man" + "woman" ≈ "queen" is real arithmetic in embedding space.

| Asset | Status | Link |
|-------|:------:|------|
| Concept file | ✅ | [`research/concepts/embeddings.md`](concepts/embeddings.md) |
| Experiment | 📋 | EXP-06 — Sentence Embeddings *(planned)* |
| Research question | 🔴 Open | [RQ-05](questions/open_questions.md#rq-05--embedding-domain-degradation) |

---

### 7. `self_attention`

**What it is:** The mechanism by which each token in a sequence computes a weighted sum over all other tokens — producing a contextualised representation that captures dependencies regardless of distance.
**Why it matters:** Self-attention is why transformers outperform RNNs. It also produces the O(n²) memory and compute cost that limits context windows.
**One-line rule:** Every token attends to every other token. The price is an n×n matrix — 381 MB per head per layer at n=10,000.

| Asset | Status | Link |
|-------|:------:|------|
| Concept file | ✅ | [`research/concepts/transformers.md`](concepts/transformers.md) |
| Experiment | 🔬 | [`EXP-04 — Self-Attention Mechanics`](../experiments/llm_behavior/attention/experiment.md) |
| Research question | 🔴 Open | [RQ-04](questions/open_questions.md#rq-04--flashattention-tiled-computation), [RQ-11](questions/open_questions.md#rq-11--attention-head-specialisation-on-real-text) |

---

### 8. `positional_encoding`

**What it is:** The mechanism that injects token order information into embeddings — because self-attention is permutation-invariant and cannot distinguish "dog bites man" from "man bites dog" without it.
**Why it matters:** Position encoding determines how well a model handles long documents, code structure, and multi-turn conversations where order carries meaning.
**One-line rule:** Without positional encoding, a transformer sees a bag of tokens, not a sequence.

| Asset | Status | Link |
|-------|:------:|------|
| Concept file | ⬜ | `@add_concept positional_encoding` |
| Experiment | ⬜ | `@create_experiment` after concept file exists |
| Research question | — | — |

---

## Layer 3 — Retrieval Systems

> **Core question:** How do you find semantically relevant information at scale — faster than brute-force and more precise than keyword search?
> **Prerequisite:** Layer 2. Vector search only makes sense after embeddings make sense.
> **Chapter reference:** [Chapter 3 — Embeddings](../AI_RESEARCH_INDEX.md#chapter-3--embeddings)

---

### 9. `vector_embeddings`

**What it is:** Sentence- or passage-level embeddings (as opposed to token embeddings) used for semantic search and retrieval.
**Why it matters:** Vector embeddings are the index in every RAG system. Their quality determines retrieval precision before any other factor.
**One-line rule:** `text-embedding-3-small` maps a 1,000-word passage to a 1,536-dimensional vector. Retrieval is nearest-neighbour search in that space.

| Asset | Status | Link |
|-------|:------:|------|
| Concept file | ✅ | [`research/concepts/embeddings.md`](concepts/embeddings.md) *(section: "Sentence Embeddings")* |
| Experiment | 📋 | EXP-06 — Sentence Embeddings *(planned)* |
| Research question | 🔴 Open | [RQ-05](questions/open_questions.md#rq-05--embedding-domain-degradation) |

---

### 10. `vector_search`

**What it is:** Approximate nearest-neighbour (ANN) search algorithms — FAISS, HNSW, IVF — that find the top-k most similar vectors in a large index in sub-linear time.
**Why it matters:** Exact nearest-neighbour search over millions of vectors is too slow for real-time retrieval. ANN makes RAG production-viable.
**One-line rule:** FAISS can search 1M vectors in ~1 ms. Exact search at that scale would take seconds.

| Asset | Status | Link |
|-------|:------:|------|
| Concept file | ⬜ | `@add_concept vector_search` |
| Experiment | ⬜ | `@create_experiment` after concept file exists |
| Research question | — | — |

---

### 11. `chunking_strategies`

**What it is:** The set of techniques for splitting documents into passages before embedding — fixed-size, sentence-aware, semantic, recursive, and overlap strategies.
**Why it matters:** Chunk size is the single most impactful RAG design decision. Too small: context is lost. Too large: retrieval is imprecise.
**One-line rule:** Chunk size determines the granularity of what you can retrieve. There is no universal optimum — it depends on query type.

| Asset | Status | Link |
|-------|:------:|------|
| Concept file | ✅ | [`research/concepts/rag.md`](concepts/rag.md) *(section: "Chunking Strategies")* |
| Experiment | 📋 | EXP-08 — Chunk Size Optimisation *(planned)* |
| Research question | 🔴 Open | [RQ-07](questions/open_questions.md#rq-07--rag-chunk-size-optimum) |

---

### 12. `reranking`

**What it is:** A second-stage ranking step (using a cross-encoder or LLM) that re-orders the top-k retrieved chunks by relevance before passing them to the generator.
**Why it matters:** ANN retrieval optimises for speed, not precision. Reranking restores precision at the cost of latency — critical for high-stakes queries.
**One-line rule:** Retrieve broadly, rerank precisely. A bi-encoder gets the candidates; a cross-encoder picks the winner.

| Asset | Status | Link |
|-------|:------:|------|
| Concept file | ⬜ | `@add_concept reranking` |
| Experiment | ⬜ | `@create_experiment` after concept file exists |
| Research question | — | — |

---

## Layer 4 — RAG Systems

> **Core question:** How do you augment LLM generation with retrieved context — and what are the failure modes?
> **Prerequisite:** Layer 3. RAG is retrieval + generation. You must understand retrieval first.
> **Chapter reference:** [Chapter 4 — RAG](../AI_RESEARCH_INDEX.md#chapter-4--rag)

---

### 13. `rag_architecture`

**What it is:** The end-to-end pipeline combining document ingestion, embedding, indexing, retrieval, context assembly, and LLM generation into a single system.
**Why it matters:** RAG is the dominant architecture for grounded, up-to-date LLM responses without fine-tuning. Every production LLM product uses a variant of it.
**One-line rule:** RAG = long-term memory for LLMs. The model reasons over retrieved context, not memorised facts.

| Asset | Status | Link |
|-------|:------:|------|
| Concept file | ✅ | [`research/concepts/rag.md`](concepts/rag.md) |
| Experiment | 📋 | EXP-07 — Naive RAG Pipeline *(planned)* |
| Research question | 🔴 Open | [RQ-07](questions/open_questions.md#rq-07--rag-chunk-size-optimum) |

---

### 14. `retrieval_failure_modes`

**What it is:** The taxonomy of ways RAG retrieval can fail — missing chunks, wrong chunks, context overflow, embedding domain mismatch, stale index.
**Why it matters:** When a RAG answer is wrong, the bug is usually in retrieval, not generation. Engineers who cannot diagnose retrieval failures cannot fix them.
**One-line rule:** "The LLM hallucinated" is almost never the right diagnosis. Check if the right context was retrieved first.

| Asset | Status | Link |
|-------|:------:|------|
| Concept file | ⬜ | `@add_concept retrieval_failure_modes` |
| Experiment | ⬜ | `@create_experiment` after concept file exists |
| Research question | — | — |

---

### 15. `grounding_and_citations`

**What it is:** Techniques for ensuring LLM responses are attributable to specific retrieved chunks — including inline citations, source metadata, and faithfulness scoring.
**Why it matters:** Ungrounded responses are legally and ethically risky in enterprise deployments. Citation-enabled RAG makes answers auditable.
**One-line rule:** A grounded answer says "according to [doc X, para 3]". An ungrounded answer says "as is well known". Prefer the former in production.

| Asset | Status | Link |
|-------|:------:|------|
| Concept file | ⬜ | `@add_concept grounding_and_citations` |
| Experiment | ⬜ | `@create_experiment` after concept file exists |
| Research question | — | — |

---

## Layer 5 — Tool Use

> **Core question:** How do you give an LLM structured access to external systems — and how do you make tool calls reliable?
> **Prerequisite:** Layer 4. Tool use is function-calling inside a pipeline. You must understand RAG before you understand agents that use tools alongside retrieval.

---

### 16. `function_calling`

**What it is:** The model's ability to output a structured JSON object naming a function and its arguments rather than natural language — enabling deterministic execution of external actions.
**Why it matters:** Function calling is the bridge between LLM reasoning and real-world side effects. Hallucinated arguments crash production systems.
**One-line rule:** A function call is only as reliable as the tool schema and the temperature setting. Design schemas that leave no room for ambiguity.

| Asset | Status | Link |
|-------|:------:|------|
| Concept file | ⬜ | `@add_concept function_calling` |
| Experiment | ⬜ | `@create_experiment` after concept file exists |
| Research question | 🔴 Open | [RQ-08](questions/open_questions.md#rq-08--agent-temperature-reliability) |

---

### 17. `structured_outputs`

**What it is:** Constrained generation modes (JSON mode, response schemas, grammar-based decoding) that force the model to emit syntactically valid structured data.
**Why it matters:** Downstream parsers have zero tolerance for malformed output. Structured output modes trade generation flexibility for parse reliability.
**One-line rule:** JSON mode guarantees syntactically valid JSON. It does not guarantee semantically correct field values. Validate both.

| Asset | Status | Link |
|-------|:------:|------|
| Concept file | ⬜ | `@add_concept structured_outputs` |
| Experiment | ⬜ | `@create_experiment` after concept file exists |
| Research question | 🔴 Open | [RQ-09](questions/open_questions.md#rq-09--structured-output-truncation-failure) |

---

## Layer 6 — Agents

> **Core question:** How do you compose LLM reasoning, memory, and tools into a system that can autonomously complete multi-step tasks?
> **Prerequisite:** Layer 5. Agents are tool-using loops. Tool use must be solid before you build agents around it.
> **Chapter reference:** [Chapter 5 — Agents](../AI_RESEARCH_INDEX.md#chapter-5--agents)

---

### 18. `agent_planning`

**What it is:** The patterns by which an agent decides which action to take next — including ReAct (Reason + Act), chain-of-thought planning, and task decomposition.
**Why it matters:** An agent without a planning pattern loops indefinitely or takes the first plausible action regardless of fitness. Planning is what makes agents useful.
**One-line rule:** ReAct = Thought → Action → Observation → repeat. The loop terminates when the agent observes a satisfactory answer.

| Asset | Status | Link |
|-------|:------:|------|
| Concept file | ✅ | [`research/concepts/agents.md`](concepts/agents.md) *(section: "ReAct Loop")* |
| Experiment | 📋 | EXP-10 — Single-Tool Agent *(planned)* |
| Research question | 🔴 Open | [RQ-08](questions/open_questions.md#rq-08--agent-temperature-reliability) |

---

### 19. `multi_agent_systems`

**What it is:** Architectures in which multiple specialised agents coordinate — via orchestrators, handoffs, shared memory, or message passing — to complete tasks beyond a single agent's scope.
**Why it matters:** Complex workflows require specialisation. A multi-agent system decomposes a hard problem across agents with different tools and personas.
**One-line rule:** Orchestrator agents plan and delegate. Worker agents execute and report. Shared memory prevents information loss across handoffs.

| Asset | Status | Link |
|-------|:------:|------|
| Concept file | ✅ | [`research/concepts/agents.md`](concepts/agents.md) *(section: "Multi-Agent Systems")* |
| Experiment | 📋 | EXP-11 — Multi-Tool Agent *(planned)* |
| Research question | — | — |

---

## Layer 7 — Evaluation

> **Core question:** How do you measure whether an LLM system is correct — at scale, automatically, and in a way that production engineers can act on?
> **Prerequisite:** Layer 6. You cannot evaluate what you do not understand. Build agents first.
> **Chapter reference:** [Chapter 6 — Evaluation](../AI_RESEARCH_INDEX.md#chapter-6--evaluation)

---

### 20. `llm_evaluation`

**What it is:** The set of techniques for measuring LLM output quality — including LLM-as-judge, reference-based metrics (BLEU, ROUGE, BERTScore), human evaluation, and task-specific rubrics.
**Why it matters:** Without evaluation, you cannot detect regressions when the model or prompt changes. Evaluation is the test suite for LLM systems.
**One-line rule:** LLM-as-judge is fast and scalable but biased toward its own outputs. Always calibrate against a human-labelled gold set.

| Asset | Status | Link |
|-------|:------:|------|
| Concept file | ⬜ | `@add_concept llm_evaluation` |
| Experiment | 📋 | EXP-13 — LLM-as-Judge Evaluation *(planned)* |
| Research question | — | — |

---

### 21. `hallucination_detection`

**What it is:** Methods for identifying when an LLM generates confident-sounding statements that are factually unsupported or contradicted by the provided context.
**Why it matters:** Hallucinations are the primary trust failure mode in production LLM systems. Detecting them automatically is a prerequisite for safe deployment.
**One-line rule:** Hallucination ≠ "made something up". It means "stated something as fact that is not in the context or training data". Detection requires a ground truth.

| Asset | Status | Link |
|-------|:------:|------|
| Concept file | ⬜ | `@add_concept hallucination_detection` |
| Experiment | ⬜ | `@create_experiment` after concept file exists |
| Research question | — | — |

---

## Layer 8 — Production AI

> **Core question:** How do you move from a working prototype to a safe, observable, cost-efficient production system?
> **Prerequisite:** All previous layers. Production concerns cut across the entire stack.
> **Chapter reference:** [Chapter 7 — Production Systems](../AI_RESEARCH_INDEX.md#chapter-7--production-systems)

---

### 22. `observability`

**What it is:** The practice of instrumenting LLM systems to capture traces, spans, token counts, latencies, costs, error rates, and model version changes — enabling diagnosis and alerting in production.
**Why it matters:** LLM systems fail silently. A slow model version update changes all outputs without raising an exception. Observability is how you detect it.
**One-line rule:** Log `system_fingerprint` on every call. A change is a model version bump — invalidate caches and re-run evals.

| Asset | Status | Link |
|-------|:------:|------|
| Concept file | ⬜ | `@add_concept observability` |
| Experiment | ⬜ | `@create_experiment` after concept file exists |
| Research question | — | — |

---

### 23. `prompt_injection`

**What it is:** An attack class in which malicious content in user input or retrieved context overrides the system prompt's instructions — causing the model to behave outside its intended constraints.
**Why it matters:** Every deployed LLM product that processes user input is a prompt injection target. There is no patch — only defence-in-depth.
**One-line rule:** Indirect injection (via retrieved tool outputs or documents) is harder to defend than direct injection. RAG systems are especially vulnerable.

| Asset | Status | Link |
|-------|:------:|------|
| Concept file | ⬜ | `@add_concept prompt_injection` |
| Experiment | 📋 | EXP-15 — Prompt Injection Test Battery *(planned)* |
| Research question | 🔴 Open | [RQ-02](questions/open_questions.md#rq-02--prompt-injection-resistance) |

---

### 24. `latency_optimization`

**What it is:** The set of techniques for reducing end-to-end response latency in LLM pipelines — streaming, response caching, prompt compression, smaller models for classification steps, and batching.
**Why it matters:** Users abandon interactions above ~3s latency. In agentic systems, latency compounds across every tool call. Optimisation is not optional at scale.
**One-line rule:** Profile before optimising. The bottleneck is usually the LLM call itself — but the fix is often architectural (cache, stream, or skip the call entirely).

| Asset | Status | Link |
|-------|:------:|------|
| Concept file | ⬜ | `@add_concept latency_optimization` |
| Experiment | ⬜ | `@create_experiment` after concept file exists |
| Research question | — | — |

---

## Concept File Status

| # | Concept | File | Action needed |
|---|---------|:----:|--------------|
| 1 | `temperature` | ✅ | [`llm_behavior.md`](concepts/llm_behavior.md) — covered |
| 2 | `seed_determinism` | ✅ | [`seed_determinism.md`](concepts/seed_determinism.md) — complete |
| 3 | `tokenization` | ⬜ | `@add_concept tokenization` |
| 4 | `context_window` | ⬜ | `@add_concept context_window` |
| 5 | `system_prompts` | ✅ | [`llm_behavior.md`](concepts/llm_behavior.md) — covered |
| 6 | `embeddings` | ✅ | [`embeddings.md`](concepts/embeddings.md) — covered |
| 7 | `self_attention` | ✅ | [`transformers.md`](concepts/transformers.md) — covered |
| 8 | `positional_encoding` | ⬜ | `@add_concept positional_encoding` |
| 9 | `vector_embeddings` | ✅ | [`embeddings.md`](concepts/embeddings.md) — covered |
| 10 | `vector_search` | ⬜ | `@add_concept vector_search` |
| 11 | `chunking_strategies` | ✅ | [`rag.md`](concepts/rag.md) — covered |
| 12 | `reranking` | ⬜ | `@add_concept reranking` |
| 13 | `rag_architecture` | ✅ | [`rag.md`](concepts/rag.md) — covered |
| 14 | `retrieval_failure_modes` | ⬜ | `@add_concept retrieval_failure_modes` |
| 15 | `grounding_and_citations` | ⬜ | `@add_concept grounding_and_citations` |
| 16 | `function_calling` | ⬜ | `@add_concept function_calling` |
| 17 | `structured_outputs` | ⬜ | `@add_concept structured_outputs` |
| 18 | `agent_planning` | ✅ | [`agents.md`](concepts/agents.md) — covered |
| 19 | `multi_agent_systems` | ✅ | [`agents.md`](concepts/agents.md) — covered |
| 20 | `llm_evaluation` | ⬜ | `@add_concept llm_evaluation` |
| 21 | `hallucination_detection` | ⬜ | `@add_concept hallucination_detection` |
| 22 | `observability` | ⬜ | `@add_concept observability` |
| 23 | `prompt_injection` | ⬜ | `@add_concept prompt_injection` |
| 24 | `latency_optimization` | ⬜ | `@add_concept latency_optimization` |

**6 / 24 concept files exist. 18 need to be created.**

---

## Layer Dependency Map

```
Layer 1: LLM Behavior
  (temperature, seed_determinism, tokenization, context_window, system_prompts)
       │
       ▼
Layer 2: Transformer Fundamentals
  (embeddings, self_attention, positional_encoding)
       │
       ▼
Layer 3: Retrieval Systems
  (vector_embeddings, vector_search, chunking_strategies, reranking)
       │
       ▼
Layer 4: RAG Systems
  (rag_architecture, retrieval_failure_modes, grounding_and_citations)
       │
       ▼
Layer 5: Tool Use
  (function_calling, structured_outputs)
       │
       ▼
Layer 6: Agents
  (agent_planning, multi_agent_systems)
       │
       ▼
Layer 7: Evaluation
  (llm_evaluation, hallucination_detection)
       │
       ▼
Layer 8: Production AI
  (observability, prompt_injection, latency_optimization)
```

---

## Suggested Fill Order

Run these commands in sequence to build out the missing concept files:

```bash
# Layer 1 gaps
@add_concept tokenization
@add_concept context_window

# Layer 2 gaps
@add_concept positional_encoding

# Layer 3 gaps
@add_concept vector_search
@add_concept reranking

# Layer 4 gaps
@add_concept retrieval_failure_modes
@add_concept grounding_and_citations

# Layer 5 gaps
@add_concept function_calling
@add_concept structured_outputs

# Layer 7 gaps
@add_concept llm_evaluation
@add_concept hallucination_detection

# Layer 8 gaps
@add_concept observability
@add_concept prompt_injection
@add_concept latency_optimization
```

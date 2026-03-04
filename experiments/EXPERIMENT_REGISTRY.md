---
title: "Experiment Registry"
tags: [registry, experiments, tracking, llm-behavior, research]
aliases: [experiment-registry, experiments-index]
---

# Experiment Registry

Central tracking log for all experiments in this research portfolio.
Each row links to the full experiment folder containing `experiment.md`, `code.py`, `results.md`, and `analysis.md`.

**Status legend:**
`✅ Complete` · `🔄 In Progress` · `📋 Planned` · `⏸ On Hold`

---

## Registry Table

| ID | Topic | Folder | Hypothesis | Status | Key Insight | Next Question |
|----|-------|--------|------------|--------|-------------|---------------|
| [EXP-01](#exp-01--temperature) | Temperature & Output Entropy | [llm_behavior/temperature/](llm_behavior/temperature/) | `temperature` controls the entropy of the token-sampling distribution — higher values produce more varied output, lower values produce more deterministic output | ✅ Complete | `T=0` via the OpenAI API is **not** byte-exact deterministic due to distributed GPU floating-point non-associativity. Use `seed=` for reproducibility. | Does `seed` combined with `T=0` guarantee identical outputs across different deployment regions? |
| [EXP-02](#exp-02--system-prompt-control) | System Prompt as Behaviour Control | [llm_behavior/system_prompt/](llm_behavior/system_prompt/) | Changing only the system prompt — holding all else constant — produces measurably different outputs in tone, length, precision, and quality | ✅ Complete | The model faithfully follows even degraded instructions (`"You are a careless AI"`). System prompt is a **security boundary**, not just a hint. | How much of a system prompt can be overridden by a sufficiently crafted user message (prompt injection)? |
| [EXP-03](#exp-03--token-limit) | Token Limits, Truncation & Cost | [llm_behavior/token_limit/](llm_behavior/token_limit/) | `max_tokens` is a hard ceiling — responses exceeding the budget truncate mid-generation; optimal budget is domain-dependent | ✅ Complete | RAG factual answers use ~51 tokens regardless of budget (150→600). Code generation requires 800+ tokens for a class-level task. `max_tokens` is a ceiling, not a target. | How does truncation rate change across model sizes (gpt-4o-mini vs gpt-4o)? |
| [EXP-04](#exp-04--self-attention-mechanics) | Self-Attention Mechanics (NumPy) | [llm_behavior/attention/](llm_behavior/attention/) | Self-attention produces an n×n score matrix — every token attends to every other token — making memory complexity O(n²), the root cause of context window limits | ✅ Complete | Live sweep confirmed O(n²): n=512 → 1 MB / 4 ms; n=2048 → 16 MB / 59 ms. At n=10,000 → ~381 MB per head per layer. | How does FlashAttention achieve the same output with O(n) memory I/O through tiled computation? |
| EXP-05 | Sentence Embeddings & Cosine Similarity | `llm_behavior/embeddings/` *(planned)* | Semantically similar sentences should cluster geometrically in embedding space, measurable via cosine similarity | 📋 Planned | — | How does embedding quality degrade for domain-specific text (legal, medical) vs general language? |
| EXP-06 | Few-Shot vs Zero-Shot Prompting | `llm_behavior/few_shot/` *(planned)* | Providing in-context examples (few-shot) improves output format adherence and factual accuracy compared to zero-shot | 📋 Planned | — | How many examples are needed before few-shot accuracy plateaus? |
| EXP-07 | Chain-of-Thought Reasoning | `llm_behavior/chain_of_thought/` *(planned)* | Instructing the model to reason step-by-step before answering improves accuracy on multi-step reasoning tasks | 📋 Planned | — | Does chain-of-thought reasoning help on tasks where the answer is short but the path is complex? |
| EXP-08 | RAG Chunk Size Optimisation | `rag/chunk_size/` *(planned)* | Retrieval precision and recall are sensitive to chunk size — there is an optimal range per query type | 📋 Planned | — | Does semantic chunking (splitting at natural topic boundaries) outperform fixed-size chunking? |

---

## Detailed Entries

---

### EXP-01 — Temperature

| Field | Detail |
|---|---|
| **ID** | EXP-01 |
| **Phase** | LLM Behavior & Prompt Control |
| **Model** | gpt-4o-mini |
| **Status** | ✅ Complete |
| **Run date** | March 2026 |
| **Total API calls** | 40 (5 temps × 4 domains × 2 runs) |

**Hypothesis**
The `temperature` parameter controls the entropy of the token-sampling distribution. Higher values produce more varied, creative output; lower values produce more deterministic, conservative output.

**Key Insight**
`T=0` is not byte-exact deterministic via the OpenAI API. All 20 determinism checks (`run1 == run2`) returned `DIFFERS`. Distributed GPU floating-point math is non-associative — use `seed=<int>` alongside `T=0` for maximum reproducibility.

**Next Research Question**
Does `seed` combined with `T=0` guarantee identical outputs across different deployment regions or when `system_fingerprint` changes?

**Files**
- 📋 [experiment.md](llm_behavior/temperature/experiment.md) — Hypothesis, variables, method
- ▶️ [code.py](llm_behavior/temperature/code.py) — Runnable experiment
- 📊 [results.md](llm_behavior/temperature/results.md) — Live outputs, determinism checks
- 🔬 [analysis.md](llm_behavior/temperature/analysis.md) — Scientific analysis, risk table, decision framework

---

### EXP-02 — System Prompt Control

| Field | Detail |
|---|---|
| **ID** | EXP-02 |
| **Phase** | LLM Behavior & Prompt Control |
| **Model** | gpt-4o-mini |
| **Status** | ✅ Complete |
| **Run date** | March 2026 |
| **Total API calls** | 12 (3 personas × 4 prompts) |

**Hypothesis**
The system prompt is the primary behaviour-control layer. Changing only the system prompt — holding temperature and user prompts constant — produces measurably different outputs in tone, length, precision, and code quality.

**Key Insight**
The model faithfully executes even degraded system prompts (`"You are a careless AI assistant"`). System prompt is **architecture**, not configuration. It is simultaneously a behaviour contract, a security boundary, and a multi-tenant configuration switch.

**Next Research Question**
How much of a system prompt can be overridden by a sufficiently crafted user message? What is the real-world resistance to prompt injection at this layer?

**Files**
- 📋 [experiment.md](llm_behavior/system_prompt/experiment.md) — Hypothesis, personas, method
- ▶️ [code.py](llm_behavior/system_prompt/code.py) — Runnable experiment
- 📊 [results.md](llm_behavior/system_prompt/results.md) — Per-persona outputs, word counts
- 🔬 [analysis.md](llm_behavior/system_prompt/analysis.md) — Enterprise implications, key takeaways

---

### EXP-03 — Token Limit

| Field | Detail |
|---|---|
| **ID** | EXP-03 |
| **Phase** | LLM Behavior & Prompt Control |
| **Model** | gpt-4o-mini |
| **Status** | ✅ Complete |
| **Run date** | March 2026 |
| **Total API calls** | 16 (4 budgets × 4 domains) |
| **Truncated responses** | 10/16 |
| **Total cost** | ~$0.00187 |

**Hypothesis**
`max_tokens` is a hard ceiling — responses that exceed it truncate mid-generation (`finish_reason = "length"`). The token budget required for a complete response is domain-dependent.

**Key Insight**
`max_tokens` is a ceiling, not a target. RAG factual answers completed in ~51 tokens regardless of whether the budget was 150, 300, or 600. Code generation (VectorStore class) never completed even at 600 tokens — requiring 800+. `finish_reason = "length"` is the authoritative truncation signal.

**Next Research Question**
How does truncation rate compare across model sizes? Does gpt-4o produce more concise answers than gpt-4o-mini for the same task, allowing smaller budgets?

**Files**
- 📋 [experiment.md](llm_behavior/token_limit/experiment.md) — Hypothesis, domains, method
- ▶️ [code.py](llm_behavior/token_limit/code.py) — Runnable experiment
- 📊 [results.md](llm_behavior/token_limit/results.md) — Per-domain, per-budget results
- 🔬 [analysis.md](llm_behavior/token_limit/analysis.md) — Cost model, RAG chunking alignment, memory strategy

---

### EXP-04 — Self-Attention Mechanics

| Field | Detail |
|---|---|
| **ID** | EXP-04 |
| **Phase** | Transformer & Representation Learning |
| **Libraries** | NumPy only (no ML framework) |
| **Status** | ✅ Complete |
| **Run date** | March 2026 |
| **Token sweep** | n = 8, 64, 256, 512, 1024, 2048 |

**Hypothesis**
Self-attention requires every token to compare itself against every other token, producing an n×n score matrix. This makes memory complexity O(n²) in sequence length — the structural root cause of context window limits.

**Key Insight**
Live sweep confirmed O(n²): n=512 → 1 MB / 4 ms; n=2048 → 16 MB / 59 ms (~4× memory, ~15× compute per 2× tokens). At n=10,000: ~381 MB per head per layer. This is a hardware problem, not a model quality problem — the driver behind FlashAttention, sparse attention, and SSMs.

**Next Research Question**
How does FlashAttention achieve the same mathematical output with O(n) memory I/O through tiled GPU SRAM computation? Can we simulate this in NumPy?

**Files**
- 📋 [experiment.md](llm_behavior/attention/experiment.md) — Hypothesis, variables, method
- ▶️ [code.py](llm_behavior/attention/code.py) — NumPy attention simulator
- 📊 [results.md](llm_behavior/attention/results.md) — Attention matrices, complexity sweep
- 🔬 [analysis.md](llm_behavior/attention/analysis.md) — O(n²) proof, FlashAttention, SSM alternatives

---

## Cross-Experiment Insights

| Insight | Experiments |
|---|---|
| Even the most fundamental parameter (T=0) behaves differently in distributed cloud environments than in theory | EXP-01 |
| The three control surfaces (training, sampling, prompting) are fully orthogonal — change one without affecting the others | EXP-01, EXP-02 |
| Domain determines the optimal token budget — there is no single right value of `max_tokens` | EXP-03 |
| RAG's effectiveness comes partly from keeping n small — reducing quadratic attention cost | EXP-03, EXP-04 |
| O(n²) attention memory is the architectural reason for all LLM context window limits | EXP-04 |

---

## Adding a New Experiment

1. Copy [`experiment_template.md`](experiment_template.md) into a new folder under `experiments/`
2. Fill in all sections before writing code
3. Add a row to the [Registry Table](#registry-table) above with `📋 Planned` status
4. Update status to `🔄 In Progress` when running, `✅ Complete` when done
5. Link `results.md` and `analysis.md` once generated

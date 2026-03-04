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
| [EXP-05](#exp-05--seed-determinism) | Seed + T=0 Determinism | [llm_behavior/seed_determinism/](llm_behavior/seed_determinism/) | `seed=42` combined with `T=0` reduces but does not eliminate output variation; `system_fingerprint` monitors backend changes | ✅ Complete | **Seed has zero effect** — Δ identity rate = +0.0% across all prompts. Determinism is task-driven (short/canonical output), not seed-driven. Use application-layer response caching. | Does seed guarantee consistent tool-call selection in agents? ([RQ-08](../research/questions/open_questions.md#rq-08)) |
| [EXP-06](#exp-06--tokenization-domain-ratios) | Tokenization: Domain-Specific Token Ratios | [llm_behavior/tokenization/](llm_behavior/tokenization/) | Token-per-word ratio varies by ≥ 2× between common English prose and high-cost domains (non-Latin scripts, code, emoji) due to BPE vocabulary coverage | ✅ Complete | Spread = 29.55× (English 1.25 → Japanese 37.0). JSON = 3.32× premium; Arabic = 3.81×; Python = 1.68×. Word-count abstraction breaks for space-free scripts. | Does `o200k_base` (200K vocab) reduce Arabic/code token counts vs `cl100k_base` (100K vocab)? |
| EXP-07 | Sentence Embeddings & Cosine Similarity | `llm_behavior/embeddings/` *(planned)* | Semantically similar sentences should cluster geometrically in embedding space, measurable via cosine similarity | 📋 Planned | — | How does embedding quality degrade for domain-specific text (legal, medical) vs general language? |
| EXP-08 | Few-Shot vs Zero-Shot Prompting | `llm_behavior/few_shot/` *(planned)* | Providing in-context examples (few-shot) improves output format adherence and factual accuracy compared to zero-shot | 📋 Planned | — | How many examples are needed before few-shot accuracy plateaus? |
| EXP-09 | Chain-of-Thought Reasoning | `llm_behavior/chain_of_thought/` *(planned)* | Instructing the model to reason step-by-step before answering improves accuracy on multi-step reasoning tasks | 📋 Planned | — | Does chain-of-thought reasoning help on tasks where the answer is short but the path is complex? |
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

### EXP-05 — Seed Determinism

| Field | Detail |
|---|---|
| **ID** | EXP-05 |
| **Phase** | LLM Behavior — Reproducibility |
| **Libraries** | openai, python-dotenv |
| **Status** | ✅ Complete |
| **Run date** | 2026-03-04 |
| **Conditions** | 2 (T=0+seed vs T=0 no-seed) × 3 prompts × 10 calls = 60 API calls |

**Hypothesis**
`seed=42` combined with `T=0` reduces but does not eliminate output variation. `system_fingerprint` changes break reproducibility even with fixed seed.

**Key Insight**
Seed had **zero measurable effect** — identity rate delta was +0.0% across all prompt types. Non-determinism at T=0 is floating-point arithmetic noise, not random sampling, which seed cannot fix. Code outputs were 100% identical in *both* conditions — driven by task over-constraint, not seed. A `system_fingerprint` change was observed mid-experiment but did not affect the canonical code output.

**Next Research Question**
Does this task-driven non-determinism affect agent tool-call selection — where inconsistency is a correctness failure, not a style issue? ([RQ-08](../research/questions/open_questions.md#rq-08))

**Files**
- 📋 [experiment.md](llm_behavior/seed_determinism/experiment.md) — Hypothesis, RQ-01 link, variables
- ▶️ [code.py](llm_behavior/seed_determinism/code.py) — Seed vs no-seed comparison runner
- 📊 [results.md](llm_behavior/seed_determinism/results.md) — Per-call identity checks, fingerprints
- 🔬 [analysis.md](llm_behavior/seed_determinism/analysis.md) — FP non-associativity, production caching architecture

---

### EXP-06 — Tokenization: Domain-Specific Token Ratios

| Field | Detail |
|---|---|
| **ID** | EXP-06 |
| **Phase** | LLM Behavior — Tokenization |
| **Libraries** | `tiktoken` only (no API key required) |
| **Status** | ✅ Complete |
| **Run date** | 2026-03-04 |
| **Vocabulary** | `cl100k_base` (GPT-4 / GPT-4o, 100,277 tokens) |
| **Domains tested** | 8: common English, technical English, Python code, JSON, Japanese, Arabic, medical/legal, emoji |

**Hypothesis**
Token-per-word ratio varies by at least 2× between common English prose (1.0–1.3) and high-cost domains
(non-Latin scripts, code identifiers, emoji) because BPE vocabulary coverage is biased toward English
web text — forcing rare characters and sequences to decompose into shorter subword units.

**Key Insight**
Spread = **29.55×** (English 1.25 → Japanese 37.0 by word count; Arabic 4.77 is the cleanest non-Latin comparison at 3.81×). JSON at 4.15 tokens/word is the most impactful finding for English-language production systems — structured context injection pays a silent 3.32× token premium. Word-count abstraction is invalid for space-free scripts (Japanese, Chinese).

**Next Research Question**
Does the `o200k_base` vocabulary (200,019 tokens, used by GPT-4o newer versions and o1) reduce
token-per-word ratios for code and non-English text versus `cl100k_base` — making newer models
measurably cheaper on domain-specific workloads?

**Files**
- 📋 [experiment.md](llm_behavior/tokenization/experiment.md) — Hypothesis, 8 domains, variables
- ▶️ [code.py](llm_behavior/tokenization/code.py) — tiktoken analysis, boundary visualization, auto-writes results.md
- 📊 [results.md](llm_behavior/tokenization/results.md) — Domain ratio table, token boundary previews *(auto-generated)*
- 🔬 [analysis.md](llm_behavior/tokenization/analysis.md) — BPE mechanism, cost model, production implications


---

## Cross-Experiment Insights

| Insight | Experiments |
|---|---|
| Even the most fundamental parameter (T=0) behaves differently in distributed cloud environments than in theory | EXP-01 |
| The three control surfaces (training, sampling, prompting) are fully orthogonal — change one without affecting the others | EXP-01, EXP-02 |
| Domain determines the optimal token budget — there is no single right value of `max_tokens` | EXP-03 |
| RAG's effectiveness comes partly from keeping n small — reducing quadratic attention cost | EXP-03, EXP-04 |
| O(n²) attention memory is the architectural reason for all LLM context window limits | EXP-04 |
| `seed` has zero effect at T=0 — non-determinism is FP arithmetic noise, not random sampling | EXP-01, EXP-05 |
| Task over-constraint (canonical answer + short output) is the only reliable path to T=0 determinism | EXP-05 |
| The correct production reproducibility architecture is application-layer response caching, not API seed | EXP-05 |

---

## Adding a New Experiment

1. Copy [`experiment_template.md`](experiment_template.md) into a new folder under `experiments/`
2. Fill in all sections before writing code
3. Add a row to the [Registry Table](#registry-table) above with `📋 Planned` status
4. Update status to `🔄 In Progress` when running, `✅ Complete` when done
5. Link `results.md` and `analysis.md` once generated

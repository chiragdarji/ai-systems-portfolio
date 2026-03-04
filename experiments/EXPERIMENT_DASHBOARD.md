---
title: "Experiment Dashboard"
tags: [dashboard, experiments, navigation, llm-behavior, rag, agents, evaluation]
aliases: [experiment-dashboard, experiments-hub]
---

# Experiment Dashboard

> Quick navigation hub for all experiments in this research portfolio.
> For full tracking metadata, status, and cross-experiment insights → [`EXPERIMENT_REGISTRY.md`](EXPERIMENT_REGISTRY.md)

---

## Navigation

| Section | Experiments |
|---|---|
| [LLM Behavior](#-llm-behavior-experiments) | EXP-01 · EXP-02 · EXP-03 · EXP-04 · EXP-05 · EXP-06 · EXP-07 · EXP-08 · EXP-09 |
| [RAG](#-rag-experiments) | EXP-08 · EXP-09 · EXP-10 |
| [Agents](#-agent-experiments) | EXP-11 · EXP-12 · EXP-13 |
| [Evaluation](#-evaluation-experiments) | EXP-14 · EXP-15 |

**Status legend:** `✅ Complete` · `🔄 In Progress` · `📋 Planned`

---

## 🧠 LLM Behavior Experiments

> How LLMs produce output, what controls that output, and where they fail.
> **Concept reference:** [`research/concepts/llm_behavior.md`](../research/concepts/llm_behavior.md)

---

### EXP-01 — Temperature & Output Entropy `✅ Complete`

**Investigates:** How the `temperature` parameter shifts the model's token-sampling distribution — from near-deterministic (T=0) to highly varied (T=1.5) — across four real-world domains: general explanation, financial, legal, and code generation.

**Why it matters:** Temperature is the most commonly misunderstood inference parameter. Choosing the wrong setting in financial or legal contexts introduces dangerous variability; choosing it too low in creative tasks produces robotic output.

| Document | Link |
|---|---|
| Hypothesis & Setup | [experiment.md](llm_behavior/temperature/experiment.md) |
| Live Results | [results.md](llm_behavior/temperature/results.md) |
| Scientific Analysis | [analysis.md](llm_behavior/temperature/analysis.md) |
| Run | `python experiments/llm_behavior/temperature/code.py` |

**Key finding:** `T=0` via the OpenAI API is **not** byte-exact deterministic — all determinism checks returned `DIFFERS` due to distributed GPU floating-point non-associativity. Use `seed=<int>` for maximum reproducibility.

---

### EXP-02 — System Prompt as Behaviour Control `✅ Complete`

**Investigates:** How the system prompt functions as the primary behaviour-control layer. Three personas (BASELINE, CARELESS, RESEARCHER) are tested against identical user prompts with temperature held constant — isolating the system prompt as the sole variable.

**Why it matters:** In enterprise AI, the system prompt is the mechanism for enforcing tone, domain restrictions, safety guardrails, and compliance constraints across every user interaction — without touching model weights.

| Document | Link |
|---|---|
| Hypothesis & Setup | [experiment.md](llm_behavior/system_prompt/experiment.md) |
| Live Results | [results.md](llm_behavior/system_prompt/results.md) |
| Scientific Analysis | [analysis.md](llm_behavior/system_prompt/analysis.md) |
| Run | `python experiments/llm_behavior/system_prompt/code.py` |

**Key finding:** The model faithfully follows even destructive system prompts (`"You are a careless AI assistant"`). System prompt is **architecture**, not configuration — simultaneously a behaviour contract and a security boundary.

---

### EXP-03 — Token Limits, Truncation & Cost `✅ Complete`

**Investigates:** How `max_tokens` affects response completeness, truncation behaviour (`finish_reason`), token utilisation efficiency, and API cost across four domains: explanation, summarisation, code generation, and RAG-style factual Q&A.

**Why it matters:** `max_tokens` is the primary cost-control lever in production LLM systems. It directly determines the maximum output cost per call and interacts with RAG chunking strategy and chat memory design.

| Document | Link |
|---|---|
| Hypothesis & Setup | [experiment.md](llm_behavior/token_limit/experiment.md) |
| Live Results | [results.md](llm_behavior/token_limit/results.md) |
| Scientific Analysis | [analysis.md](llm_behavior/token_limit/analysis.md) |
| Run | `python experiments/llm_behavior/token_limit/code.py` |

**Key finding:** `max_tokens` is a ceiling, not a target. RAG factual answers completed at ~51 tokens regardless of budget (150→600). Code generation (class-level) never completed even at 600 tokens — requires 800+. `finish_reason = "length"` is the authoritative truncation signal.

---

### EXP-04 — Self-Attention Mechanics `✅ Complete`

**Investigates:** The mathematics of scaled dot-product attention and multi-head attention built from scratch using only NumPy. Includes a complexity sweep from n=8 to n=2048 measuring the real memory footprint and wall-clock time of the n×n attention weight matrix.

**Why it matters:** Understanding O(n²) attention complexity is essential for reasoning about context window limits, FlashAttention, RAG as an architectural workaround, and why LLMs cannot trivially process 100K-token inputs on consumer hardware.

| Document | Link |
|---|---|
| Hypothesis & Setup | [experiment.md](llm_behavior/attention/experiment.md) |
| Live Results | [results.md](llm_behavior/attention/results.md) |
| Scientific Analysis | [analysis.md](llm_behavior/attention/analysis.md) |
| Run | `python experiments/llm_behavior/attention/code.py` *(no API key needed)* |

**Key finding:** Live sweep confirmed O(n²): n=512 → 1 MB / 4 ms; n=2048 → 16 MB / 59 ms. At n=10,000: ~381 MB per head per layer — a hardware problem, not a model capability problem. This is what FlashAttention, Longformer, and Mamba address.

---

### EXP-05 — Seed + T=0 Determinism `✅ Complete`

**Investigates:** Whether `seed=42` combined with `T=0` guarantees byte-exact identical outputs across
repeated API calls — and what role `system_fingerprint` plays in tracking backend changes that break
reproducibility.

**Why it matters:** Connects EXP-01's T=0 non-determinism finding to a production fix. Establishes
that application-layer response caching — not API seed — is the correct reproducibility architecture
for production LLM systems.

| Document | Link |
|---|---|
| Hypothesis & Setup | [experiment.md](llm_behavior/seed_determinism/experiment.md) |
| Live Results | [results.md](llm_behavior/seed_determinism/results.md) |
| Scientific Analysis | [analysis.md](llm_behavior/seed_determinism/analysis.md) |
| Run | `python experiments/llm_behavior/seed_determinism/code.py` |

**Key finding:** Seed had **zero measurable effect** — identity rate Δ = +0.0% across all prompt types.
Non-determinism at T=0 is floating-point arithmetic noise, not random sampling; `seed` cannot fix it.
Task over-constraint (canonical short output) is the only reliable path to T=0 determinism.

---

### EXP-06 — Tokenization: Domain-Specific Token Ratios `📋 Planned`

**Investigates:** How token-per-word ratios vary across 8 input domains — common English prose,
technical English, Python code, JSON, Japanese, Arabic, medical/legal terminology, and emoji-heavy
text — using tiktoken's `cl100k_base` vocabulary (GPT-4 / GPT-4o tokenizer). No API calls required.

**Why it matters:** Every production cost estimate, context window budget, and `max_tokens` decision
operates in tokens, not words. The conventional "1,000 words ≈ 750 tokens" rule only holds for
English prose. This experiment quantifies the correction factor for each domain.

| Document | Link |
|---|---|
| Hypothesis & Setup | [experiment.md](llm_behavior/tokenization/experiment.md) |
| Live Results | [results.md](llm_behavior/tokenization/results.md) *(auto-generated on run)* |
| Scientific Analysis | [analysis.md](llm_behavior/tokenization/analysis.md) |
| Run | `pip install tiktoken && python experiments/llm_behavior/tokenization/code.py` |

**Hypothesis:** Token-per-word ratio varies by ≥ 2× between cheapest (English prose) and most
expensive (non-Latin script / emoji) domains due to BPE vocabulary coverage bias toward English.

---

### EXP-07 — Few-Shot vs Zero-Shot Prompting `📋 Planned`

**Investigates:** Whether providing in-context examples (few-shot) measurably improves output format adherence, factual accuracy, and task completion compared to zero-shot prompting — and how many examples are needed before accuracy plateaus.

**Why it matters:** Few-shot prompting is one of the cheapest techniques to improve LLM reliability without fine-tuning. Understanding its limits guides decisions about when to invest in fine-tuning instead.

| Document | Link |
|---|---|
| Hypothesis & Setup | *(not yet created)* |
| Live Results | *(pending)* |
| Scientific Analysis | *(pending)* |
| Template | [experiment_template.md](experiment_template.md) |

---

### EXP-07 — Chain-of-Thought Reasoning `📋 Planned`

**Investigates:** Whether instructing the model to reason step-by-step before answering (`"Think step by step"`) improves accuracy on multi-step arithmetic, logical deduction, and multi-hop factual questions compared to direct answering.

**Why it matters:** Chain-of-thought is a zero-cost accuracy improvement for reasoning-heavy tasks. It forms the basis of more advanced techniques (tree-of-thought, self-consistency) used in production agentic systems.

| Document | Link |
|---|---|
| Hypothesis & Setup | *(not yet created)* |
| Live Results | *(pending)* |
| Scientific Analysis | *(pending)* |
| Template | [experiment_template.md](experiment_template.md) |

---

## 📚 RAG Experiments

> How retrieval-augmented generation grounds LLM responses in external knowledge.
> **Concept reference:** [`research/concepts/rag.md`](../research/concepts/rag.md)

---

### EXP-08 — RAG Chunk Size Optimisation `📋 Planned`

**Investigates:** How chunk size (128, 256, 512, 1024 tokens) affects retrieval precision and recall in a RAG pipeline over a fixed document corpus. Tests fixed-size chunking vs sentence-boundary chunking.

**Why it matters:** Chunk size is the most impactful RAG design decision. Too small: chunks lose semantic coherence. Too large: noisy context degrades generation quality. Finding the optimal range per query type is foundational for production RAG.

| Document | Link |
|---|---|
| Hypothesis & Setup | *(not yet created)* |
| Live Results | *(pending)* |
| Scientific Analysis | *(pending)* |
| Template | [experiment_template.md](experiment_template.md) |

---

### EXP-09 — Dense vs Sparse vs Hybrid Retrieval `📋 Planned`

**Investigates:** Whether combining dense vector search (cosine similarity) with sparse keyword search (BM25) outperforms either method alone on a mixed query set containing both semantic and keyword-dependent queries.

**Why it matters:** Hybrid retrieval is the current best-practice in production RAG. Understanding when each strategy wins guides architectural decisions in RAG systems.

| Document | Link |
|---|---|
| Hypothesis & Setup | *(not yet created)* |
| Live Results | *(pending)* |
| Scientific Analysis | *(pending)* |
| Template | [experiment_template.md](experiment_template.md) |

---

### EXP-10 — RAG Faithfulness & Hallucination Rate `📋 Planned`

**Investigates:** Whether RAG-grounded responses are measurably more faithful to source documents than ungrounded responses, measured by LLM-as-judge faithfulness scoring using RAGAS-style evaluation.

**Why it matters:** RAG's core promise is hallucination reduction. This experiment quantifies that promise — and reveals the cases where RAG still fails (retrieval miss, context ignored by generator).

| Document | Link |
|---|---|
| Hypothesis & Setup | *(not yet created)* |
| Live Results | *(pending)* |
| Scientific Analysis | *(pending)* |
| Template | [experiment_template.md](experiment_template.md) |

---

## 🤖 Agent Experiments

> How LLMs reason, select tools, and iterate toward goals across multi-step tasks.
> **Concept reference:** [`research/concepts/agents.md`](../research/concepts/agents.md)

---

### EXP-11 — ReAct Agent with Tool Use `📋 Planned`

**Investigates:** How a ReAct-pattern agent decomposes a multi-step research task using web search, calculator, and RAG tools. Measures task completion rate, number of steps, and accuracy of final answer.

**Why it matters:** ReAct is the foundational agent pattern. Understanding its failure modes (tool hallucination, runaway loops, error propagation) is essential before building production agents.

| Document | Link |
|---|---|
| Hypothesis & Setup | *(not yet created)* |
| Live Results | *(pending)* |
| Scientific Analysis | *(pending)* |
| Template | [experiment_template.md](experiment_template.md) |

---

### EXP-12 — Temperature Effect on Agent Reliability `📋 Planned`

**Investigates:** How temperature affects tool-call accuracy in agentic workflows. Compares T=0 vs T=0.3 vs T=0.7 on structured tool-call JSON generation — measuring argument correctness, tool selection accuracy, and loop termination reliability.

**Why it matters:** Connects EXP-01 (temperature) findings to agents. Validates the hypothesis that agents should operate at low temperature for tool-call reliability.

| Document | Link |
|---|---|
| Hypothesis & Setup | *(not yet created)* |
| Live Results | *(pending)* |
| Scientific Analysis | *(pending)* |
| Template | [experiment_template.md](experiment_template.md) |

---

### EXP-13 — Multi-Agent Supervisor / Worker Pattern `📋 Planned`

**Investigates:** Whether a supervisor + specialised worker agent architecture outperforms a single all-purpose agent on a complex multi-step research and synthesis task — measuring output quality, step efficiency, and cost.

**Why it matters:** Multi-agent patterns are increasingly used in production AI. Understanding when decomposition helps (vs adding cost and complexity) is a core systems engineering question.

| Document | Link |
|---|---|
| Hypothesis & Setup | *(not yet created)* |
| Live Results | *(pending)* |
| Scientific Analysis | *(pending)* |
| Template | [experiment_template.md](experiment_template.md) |

---

## 📊 Evaluation Experiments

> How to measure whether AI systems behave reliably, accurately, and safely.

---

### EXP-14 — LLM-as-Judge Evaluation `📋 Planned`

**Investigates:** Whether using a stronger LLM (gpt-4o) to evaluate the outputs of a weaker model (gpt-4o-mini) produces consistent, reliable quality scores — and how those scores correlate with human judgement on a small labelled test set.

**Why it matters:** LLM-as-judge is the most practical automated evaluation method for open-ended tasks. Validating its reliability is a prerequisite for building any production evaluation pipeline.

| Document | Link |
|---|---|
| Hypothesis & Setup | *(not yet created)* |
| Live Results | *(pending)* |
| Scientific Analysis | *(pending)* |
| Template | [experiment_template.md](experiment_template.md) |

---

### EXP-15 — Prompt Injection Robustness `📋 Planned`

**Investigates:** How resistant different system prompt patterns are to adversarial user inputs designed to override system instructions. Tests direct injection, indirect injection via tool outputs, and role-play bypass techniques.

**Why it matters:** Prompt injection is the most critical security risk in deployed LLM systems. Quantifying resistance under different system prompt designs directly informs production security architecture.

| Document | Link |
|---|---|
| Hypothesis & Setup | *(not yet created)* |
| Live Results | *(pending)* |
| Scientific Analysis | *(pending)* |
| Template | [experiment_template.md](experiment_template.md) |

---

## Quick Reference

| ID | Title | Category | Status | Run command |
|----|-------|----------|--------|-------------|
| EXP-01 | Temperature & Output Entropy | LLM Behavior | ✅ | `python experiments/llm_behavior/temperature/code.py` |
| EXP-02 | System Prompt as Behaviour Control | LLM Behavior | ✅ | `python experiments/llm_behavior/system_prompt/code.py` |
| EXP-03 | Token Limits, Truncation & Cost | LLM Behavior | ✅ | `python experiments/llm_behavior/token_limit/code.py` |
| EXP-04 | Self-Attention Mechanics | LLM Behavior | ✅ | `python experiments/llm_behavior/attention/code.py` |
| EXP-05 | Seed + T=0 Determinism | LLM Behavior | ✅ | `python experiments/llm_behavior/seed_determinism/code.py` |
| EXP-06 | Tokenization Domain Ratios | LLM Behavior | 📋 | `pip install tiktoken && python experiments/llm_behavior/tokenization/code.py` |
| EXP-07 | Sentence Embeddings | LLM Behavior | 📋 | *(pending)* |
| EXP-08 | Few-Shot vs Zero-Shot | LLM Behavior | 📋 | *(pending)* |
| EXP-09 | Chain-of-Thought Reasoning | LLM Behavior | 📋 | *(pending)* |
| EXP-08 | RAG Chunk Size Optimisation | RAG | 📋 | *(pending)* |
| EXP-09 | Dense vs Sparse vs Hybrid Retrieval | RAG | 📋 | *(pending)* |
| EXP-10 | RAG Faithfulness & Hallucination Rate | RAG | 📋 | *(pending)* |
| EXP-11 | ReAct Agent with Tool Use | Agents | 📋 | *(pending)* |
| EXP-12 | Temperature Effect on Agent Reliability | Agents | 📋 | *(pending)* |
| EXP-13 | Multi-Agent Supervisor / Worker | Agents | 📋 | *(pending)* |
| EXP-14 | LLM-as-Judge Evaluation | Evaluation | 📋 | *(pending)* |
| EXP-15 | Prompt Injection Robustness | Evaluation | 📋 | *(pending)* |

---

*For detailed metadata, hypotheses, and cross-experiment insights → [`EXPERIMENT_REGISTRY.md`](EXPERIMENT_REGISTRY.md)*
*To start a new experiment → copy [`experiment_template.md`](experiment_template.md)*

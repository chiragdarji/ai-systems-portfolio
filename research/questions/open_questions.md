---
title: "Open Research Questions"
tags: [research, questions, open, llm-behavior, attention, rag, agents]
aliases: [open-questions, research-backlog]
---

# Open Research Questions

Active backlog of unanswered questions raised by experiments, papers, and observations.
Questions here drive the next experiments.

> For answered questions → [`answered_questions.md`](answered_questions.md)
> To add a new question → copy [`question_template.md`](question_template.md)
> To create the experiment → use `@create_experiment`

---

## Status Legend

| Symbol | Status |
|---|---|
| 🔴 Open | Question identified, no experiment planned yet |
| 🟡 In Progress | Experiment is planned or running |
| 🟢 Answered | Experiment complete — see answered_questions.md |
| ⏸ Deferred | Valid but deprioritised |

## Priority Legend

| Symbol | Priority |
|---|---|
| 🔥 Critical | Blocks other experiments or production decisions |
| ⬆ High | High research value, clear path to experiment |
| ➡ Medium | Interesting, no immediate dependency |
| ⬇ Low | Speculative or very long horizon |

---

## Open Questions Table

| ID | Question | Topic | Related Experiment | Priority | Status |
|----|----------|-------|--------------------|----------|--------|
| [RQ-01](#rq-01--temperature-seed-determinism) | Does `seed` combined with `T=0` guarantee byte-exact identical outputs across different deployment regions or when `system_fingerprint` changes? | Temperature / Determinism | [EXP-05](../../experiments/llm_behavior/seed_determinism/experiment.md) | 🔥 Critical | 🟢 Answered |
| [RQ-02](#rq-02--prompt-injection-resistance) | How much of a system prompt can be overridden by a sufficiently crafted user message? What is the real-world resistance to prompt injection? | System Prompt / Security | [EXP-02](../../experiments/llm_behavior/system_prompt/experiment.md) | 🔥 Critical | 🔴 Open |
| [RQ-03](#rq-03--token-budget-across-model-sizes) | Does gpt-4o produce more concise answers than gpt-4o-mini for the same task, allowing smaller `max_tokens` budgets and lower cost? | Token Limit / Cost | [EXP-03](../../experiments/llm_behavior/token_limit/experiment.md) | ⬆ High | 🔴 Open |
| [RQ-04](#rq-04--flashattention-tiled-computation) | How does FlashAttention achieve identical mathematical output to standard attention with O(n) memory I/O through tiled GPU SRAM computation? | Attention / Architecture | [EXP-04](../../experiments/llm_behavior/attention/experiment.md) | ⬆ High | 🔴 Open |
| [RQ-05](#rq-05--embedding-domain-degradation) | How does embedding quality degrade for domain-specific text (legal, medical, financial) vs general language? At what specialisation threshold does fine-tuning become necessary? | Embeddings / RAG | EXP-05 *(planned)* | ➡ Medium | 🔴 Open |
| [RQ-06](#rq-06--few-shot-plateau) | How many in-context examples are needed before few-shot accuracy plateaus? Is the marginal benefit of example N predictable? | Few-Shot Prompting | EXP-06 *(planned)* | ➡ Medium | 🔴 Open |
| [RQ-07](#rq-07--rag-chunk-size-optimum) | Is there a universal optimal chunk size for RAG, or is it always query-type dependent? Does semantic chunking outperform fixed-size chunking across all domains? | RAG / Chunking | EXP-08 *(planned)* | ⬆ High | 🔴 Open |
| [RQ-08](#rq-08--agent-temperature-reliability) | Does running agent tool-call generation at T=0 with `seed=` produce reliably consistent tool selection and argument generation across identical queries? | Agents / Reliability | EXP-12 *(planned)* | 🔥 Critical | 🔴 Open |
| [RQ-09](#rq-09--structured-output-truncation-failure) | Does `finish_reason="length"` produce silently invalid JSON/code at a higher rate than natural-language truncation — and is the failure detectable without running a parser? | Token Limit / Structured Output | [EXP-03](../../experiments/llm_behavior/token_limit/experiment.md) | 🔥 Critical | 🔴 Open |
| [RQ-10](#rq-10--system-vs-user-instruction-conflict) | When system prompt and user message directly contradict (language, tone, topic scope), which wins — and does the model's priority rule hold consistently across temperatures? | System Prompt / Control | [EXP-02](../../experiments/llm_behavior/system_prompt/experiment.md) | ⬆ High | 🔴 Open |
| [RQ-11](#rq-11--attention-head-specialisation-on-real-text) | When attention weights are computed over real semantic sentences (not random embeddings), do individual heads show interpretable specialisation — syntax vs coreference vs semantics? | Attention / Interpretability | [EXP-04](../../experiments/llm_behavior/attention/experiment.md) | ⬆ High | 🔴 Open |

---

## Detailed Entries

---

### RQ-01 — Temperature Seed Determinism

**Question:** Does `seed` combined with `T=0` guarantee byte-exact identical outputs across different OpenAI deployment regions or when `system_fingerprint` changes?

**Raised by:** [EXP-01 — Temperature](../../experiments/llm_behavior/temperature/experiment.md)
**Finding that raised it:** All 20 determinism checks at `T=0` returned `DIFFERS`. OpenAI documents `seed` as "high probability" not "guaranteed" determinism.

**Why it matters:**
Production systems that depend on reproducibility (regression testing, audit trails, cached responses) cannot be safely built on a probabilistic determinism guarantee. If `seed` is also unreliable, these architectures need a different approach (response caching, hash-based deduplication).

**Hypothesis:** `seed` reduces but does not eliminate output variation. `system_fingerprint` changes (backend model updates) will break reproducibility even with fixed `seed` and `T=0`.

**Proposed experiment:** EXP-05b — run 20 identical calls with `T=0, seed=42`, log `system_fingerprint`, test across multiple days to catch backend changes.
**Linked experiment:** [`EXP-01 — Temperature`](../../experiments/llm_behavior/temperature/experiment.md) *(raised this question)* · [`EXP-05 — Seed Determinism`](../../experiments/llm_behavior/seed_determinism/experiment.md) *(answered this question)*

**Concept reference:** [`research/concepts/llm_behavior.md`](../concepts/llm_behavior.md)

**Priority:** 🔥 Critical | **Status:** 🟢 Answered → [EXP-05](../../experiments/llm_behavior/seed_determinism/experiment.md) | [analysis.md](../../experiments/llm_behavior/seed_determinism/analysis.md)

---

### RQ-02 — Prompt Injection Resistance

**Question:** How much of a system prompt's constraints can be overridden by a sufficiently crafted user message? What patterns provide real-world resistance to prompt injection?

**Raised by:** [EXP-02 — System Prompt Control](../../experiments/llm_behavior/system_prompt/experiment.md)
**Finding that raised it:** The model faithfully follows even intentionally degraded system prompts — demonstrating that system prompt control is absolute in cooperative conditions, raising the question of adversarial conditions.

**Why it matters:**
Every deployed LLM product relies on system prompt constraints for safety, compliance, and domain restriction. If those constraints can be bypassed, the product's security model is broken. This is the most critical security question in production LLM deployment.

**Hypothesis:** Direct injection (`"Ignore your previous instructions"`) will be resisted by modern models, but indirect injection via tool outputs or multi-turn context accumulation will succeed at higher rates.

**Proposed experiment:** EXP-15 — systematic prompt injection test battery across direct, indirect (via tool output), and role-play bypass vectors.
**Linked experiment:** [`EXP-02 — System Prompt Control`](../../experiments/llm_behavior/system_prompt/experiment.md) *(raised this question)*

**Concept reference:** [`research/concepts/llm_behavior.md`](../concepts/llm_behavior.md)

**Priority:** 🔥 Critical | **Status:** 🔴 Open

---

### RQ-03 — Token Budget Across Model Sizes

**Question:** Does gpt-4o produce more concise, complete answers than gpt-4o-mini at the same `max_tokens` budget — reducing truncation rate and allowing cost optimisation through smaller budgets?

**Raised by:** [EXP-03 — Token Limit](../../experiments/llm_behavior/token_limit/experiment.md)
**Finding that raised it:** Code generation never completed even at 600 tokens for a class-level task on gpt-4o-mini. If gpt-4o is more efficient per token, the cost premium may be offset by needing fewer tokens.

**Why it matters:**
Token budget decisions in production are model-specific. If larger models are more token-efficient, the cost differential between models narrows or reverses at certain output lengths. This directly affects model selection for production deployments.

**Hypothesis:** gpt-4o will produce more semantically dense output per token — completing the same tasks at lower token counts — but will not eliminate the need for 800+ token budgets for complex code generation.

**Proposed experiment:** EXP-03b — rerun EXP-03 with gpt-4o, compare truncation rate, completion token count, and cost per completed response.
**Linked experiment:** [`EXP-03 — Token Limit`](../../experiments/llm_behavior/token_limit/experiment.md) *(raised this question)*

**Concept reference:** [`research/concepts/llm_behavior.md`](../concepts/llm_behavior.md)

**Priority:** ⬆ High | **Status:** 🔴 Open

---

### RQ-04 — FlashAttention Tiled Computation

**Question:** How does FlashAttention achieve identical mathematical output to standard attention with O(n) HBM memory I/O — and can this be simulated in NumPy to make the tiling mechanism tangible?

**Raised by:** [EXP-04 — Self-Attention Mechanics](../../experiments/llm_behavior/attention/experiment.md)
**Finding that raised it:** Live sweep showed n=2048 requires 16 MB and 59 ms for the attention matrix alone. FlashAttention claims to eliminate this with tiled SRAM computation — but the mechanism is not intuitively obvious.

**Why it matters:**
FlashAttention is the reason modern LLMs can operate at 128K+ token context windows. Understanding its tiling algorithm is foundational knowledge for any engineer designing or optimising LLM inference infrastructure.

**Hypothesis:** The tiling algorithm avoids materialising the full n×n matrix by computing softmax incrementally across tiles — the "online softmax" technique. This can be demonstrated in NumPy with explicit tile loops, making the O(n) I/O claim concrete and measurable.

**Proposed experiment:** EXP-04b — implement tiled attention in NumPy, verify numerical equivalence with standard attention, measure memory I/O difference.
**Linked experiment:** [`EXP-04 — Self-Attention Mechanics`](../../experiments/llm_behavior/attention/experiment.md) *(raised this question)*

**Concept reference:** [`research/concepts/transformers.md`](../concepts/transformers.md)

**Priority:** ⬆ High | **Status:** 🔴 Open

---

### RQ-05 — Embedding Domain Degradation

**Question:** At what level of domain specialisation does a general-purpose embedding model (text-embedding-3-small) fail to represent semantic similarity accurately — and does this failure appear in cosine similarity scores?

**Raised by:** [`research/concepts/embeddings.md`](../concepts/embeddings.md) *(planned experiment EXP-05)*

**Why it matters:**
RAG pipelines over specialised corpora (legal, medical, financial) depend on embedding quality for retrieval precision. Knowing when general embeddings degrade guides decisions about domain-specific fine-tuning.

**Hypothesis:** General embeddings will show degraded cosine similarity discrimination (similar-but-not-matching scores for domain-specific pairs) on legal and medical text, detectable by comparing same-domain vs cross-domain similarity distributions.

**Proposed experiment:** EXP-06 — sentence embeddings & cosine similarity.
**Linked experiment:** *(no completed experiment yet — see proposed experiment above)*

**Priority:** ➡ Medium | **Status:** 🔴 Open

---

### RQ-06 — Few-Shot Accuracy Plateau

**Question:** How many in-context examples are needed before few-shot prompting accuracy plateaus on a structured output task — and is the marginal benefit of each additional example predictable?

**Raised by:** [`experiments/EXPERIMENT_DASHBOARD.md`](../../experiments/EXPERIMENT_DASHBOARD.md) *(EXP-06 planned)*

**Why it matters:**
Every in-context example consumes prompt tokens. Knowing the accuracy-vs-example-count curve determines the minimum number of examples needed — directly reducing cost and context window pressure.

**Hypothesis:** Accuracy improves sharply from 0→1→2 examples, then plateaus by 3–4 examples for structured tasks. The plateau point is task-complexity dependent.

**Proposed experiment:** EXP-07 — few-shot vs zero-shot prompting.
**Linked experiment:** *(no completed experiment yet — see proposed experiment above)*

**Priority:** ➡ Medium | **Status:** 🔴 Open

---

### RQ-07 — RAG Chunk Size Optimum

**Question:** Does an optimal chunk size exist universally, or does it vary by query type? Does semantic chunking (splitting at natural topic boundaries) outperform fixed-size chunking across all domains?

**Raised by:** [`research/concepts/rag.md`](../concepts/rag.md) *(planned experiment EXP-08)*

**Why it matters:**
Chunk size is the single most impactful RAG design decision. A universal rule-of-thumb would simplify system design; query-type dependence would require adaptive chunking strategies in production.

**Hypothesis:** Optimal chunk size varies by query type (128–256 tokens for factual Q&A, 512–1024 for multi-hop reasoning). Semantic chunking outperforms fixed-size for long documents with natural section breaks.

**Proposed experiment:** EXP-08 — RAG chunk size optimisation.
**Linked experiment:** *(no completed experiment yet — see proposed experiment above)*

**Priority:** ⬆ High | **Status:** 🔴 Open

---

### RQ-08 — Agent Temperature and Tool-Call Reliability

**Question:** Does running agent tool-call generation at `T=0` with `seed=` produce reliably consistent tool selection and argument generation across identical queries — and how does reliability degrade as temperature increases?

**Raised by:** [`research/concepts/agents.md`](../concepts/agents.md) + EXP-01 finding

**Why it matters:**
EXP-01 showed T=0 is not byte-exact deterministic. For agents, inconsistent tool selection is not a style issue — it is a correctness issue. A financial agent that sometimes calls `transfer_funds` and sometimes calls `get_balance` for the same query is a production risk.

**Hypothesis:** Tool call correctness (correct function + correct arguments) degrades measurably above T=0.3. At T=0 + seed, correctness is high (>95%) but not guaranteed. At T=0.7+, correctness on ambiguous queries drops below acceptable production thresholds.

**Proposed experiment:** EXP-12 — temperature effect on agent reliability.
**Linked experiment:** [`EXP-05 — Seed Determinism`](../../experiments/llm_behavior/seed_determinism/experiment.md) *(EXP-05 raised this question — seed non-determinism must be tested in agent context)*

**Priority:** 🔥 Critical | **Status:** 🔴 Open

---

### RQ-09 — Structured Output Truncation Failure

**Question:** Does `finish_reason="length"` produce silently invalid JSON or code at a higher rate than natural-language truncation — and is the invalid output detectable without running a full parser?

**Raised by:** [EXP-03 — Token Limit](../../experiments/llm_behavior/token_limit/experiment.md)
**Finding that raised it:** Analysis noted that structured outputs (JSON, code, markdown tables) truncated at `max_tokens` produce syntactically invalid text that silently breaks downstream parsers — but this was observed qualitatively, never measured.

**Why it matters:**
Production systems that parse LLM outputs (agents calling tools via JSON, code generation pipelines, structured data extraction) have zero tolerance for silently invalid output. A natural-language truncation is ugly; a JSON truncation is a runtime crash. Knowing the failure rate guides whether to validate every response or only `length`-flagged responses.

**Hypothesis:** At equivalent truncation rates, structured output (JSON/code) will have a near-100% invalid-parse rate while natural-language truncation is always "valid" prose. A simple prefix check (last character is not `}` or `)`) catches >80% of JSON/code truncations without a full parser.

**Proposed experiment:** EXP-03c — run 30 calls per format type (JSON, Python function, plain text) with `max_tokens` set to force ~50% truncation. Measure: parse validity rate, truncation detection via `finish_reason` vs heuristic suffix check.
**Linked experiment:** [`EXP-03 — Token Limit`](../../experiments/llm_behavior/token_limit/experiment.md) *(raised this question — truncation of structured output observed qualitatively, not measured)*

**Priority:** 🔥 Critical | **Status:** 🔴 Open

---

### RQ-10 — System vs User Instruction Conflict

**Question:** When a system prompt and user message issue directly contradictory instructions (language, output format, topic scope), which instruction wins — and is the priority rule consistent across temperature values?

**Raised by:** [EXP-02 — System Prompt Control](../../experiments/llm_behavior/system_prompt/experiment.md)
**Finding that raised it:** EXP-02 showed that personas (cooperative instructions) are faithfully followed. It never tested adversarial or contradictory conditions — only measured cooperative compliance.

**Why it matters:**
The assumption in production system design is that the system prompt is authoritative. If a user message can override it under certain conditions (high temperature, ambiguous framing, polite phrasing), that assumption is broken. This affects every deployed LLM product's reliability guarantee.

**Hypothesis:** At T=0, the system prompt wins in >95% of direct contradictions. At T=0.7+, compliance becomes probabilistic. Politely-framed user overrides ("please ignore your previous instruction and...") will succeed at higher rates than direct contradictions.

**Proposed experiment:** EXP-02b — design 10 direct-contradiction test pairs (system: "respond only in French", user: "respond in English"). Run each at T=0, T=0.3, T=0.7. Measure system prompt adherence rate per temperature.
**Linked experiment:** [`EXP-02 — System Prompt Control`](../../experiments/llm_behavior/system_prompt/experiment.md) *(raised this question — cooperative personas tested, adversarial contradictions not tested)*

**Priority:** ⬆ High | **Status:** 🔴 Open

---

### RQ-11 — Attention Head Specialisation on Real Text

**Question:** When scaled dot-product attention is applied to real semantic sentence embeddings (not random vectors), do individual attention heads in a multi-head setup produce interpretably different patterns — revealing syntactic, coreference, or semantic specialisation?

**Raised by:** [EXP-04 — Self-Attention Mechanics](../../experiments/llm_behavior/attention/experiment.md)
**Finding that raised it:** EXP-04 implemented multi-head attention on random embeddings. The weight matrices were random, so the resulting attention patterns were arbitrary. The question of whether heads in real models specialise was documented but never tested.

**Why it matters:**
Attention head interpretability is foundational to understanding why transformers work — and to building interpretability tools for debugging and auditing production models. If heads specialise on real text, that validates the "multi-head allows attending to multiple relationship types" design claim.

**Hypothesis:** Using pretrained word embeddings (e.g. fastText or GloVe) on short sentences with known syntactic structure, different randomly-initialised heads will produce meaningfully different attention distributions — some focusing on adjacent tokens (local syntax), others on subject-verb pairs (semantic dependency). Differences will be visible in heatmap visualisation.

**Proposed experiment:** EXP-04b — load 50-dim GloVe vectors, construct 5-token sentences with clear subject-verb-object structure, run 4-head attention, visualise per-head attention matrices as heatmaps, label patterns.
**Linked experiment:** [`EXP-04 — Self-Attention Mechanics`](../../experiments/llm_behavior/attention/experiment.md) *(raised this question — random embeddings used; real semantic sentence patterns not tested)*

**Priority:** ⬆ High | **Status:** 🔴 Open

---
title: "Cursor Command — generate_learning_path"
tags: [command, cursor, learning-path, spine, concepts, workflow]
aliases: [generate-learning-path-command, next-concept, learning-path-generator]
---

# Command: `@generate_learning_path`

Reads the ordered learning spine, finds the next unstudied concept, and produces
a complete, actionable learning task — including sources, experiment design, and
an optional append to today's research log.

**Trigger:** `@generate_learning_path`

---

## When to Run This Command

Run `@generate_learning_path` when:
- Starting a new research session and unsure what to study next
- A concept chapter has just been closed and the next concept needs to be activated
- You want an automatically curated reading + experiment plan for the next gap in the spine

Run `@start_research_day` first if no daily log exists for today — the learning path
task will be appended to it automatically.

---

## Step-by-Step Execution

### Step 1: Read the full ordered concept list from the spine

Read `research/AI_LEARNING_SPINE.md`.

Extract the ordered list of all 24 concepts exactly as numbered:

```
1. temperature        9. vector_embeddings   17. structured_outputs
2. seed_determinism  10. vector_search       18. agent_planning
3. tokenization      11. chunking_strategies 19. multi_agent_systems
4. context_window    12. reranking           20. llm_evaluation
5. system_prompts    13. rag_architecture    21. hallucination_detection
6. embeddings        14. retrieval_failure.. 22. observability
7. self_attention    15. grounding_and_cit.. 23. prompt_injection
8. positional_enc..  16. function_calling    24. latency_optimization
```

Preserve the exact layer ordering. Never skip ahead.

### Step 2: Scan `research/concepts/` for existing files

List all `.md` files in `research/concepts/` (excluding `README.md`, `concept_summary_template.md`,
and files ending in `_summary.md`).

For each concept in the ordered list, check whether a corresponding concept file exists:

**Mapping rules:**
- Concept `temperature` → covered by `llm_behavior.md` *(check for section `## temperature` or explicit mention)*
- Concept `seed_determinism` → exact file `seed_determinism.md` ✅
- Concept `tokenization` → exact file `tokenization.md`
- Concept `context_window` → exact file `context_window.md`
- Concept `system_prompts` → covered by `llm_behavior.md`
- Concept `embeddings` → covered by `embeddings.md` ✅
- Concept `self_attention` → covered by `transformers.md` ✅
- Concept `positional_encoding` → exact file `positional_encoding.md`
- Concept `vector_embeddings` → covered by `embeddings.md` ✅
- Concept `vector_search` → exact file `vector_search.md`
- Concept `chunking_strategies` → covered by `rag.md` ✅
- Concept `reranking` → exact file `reranking.md`
- Concept `rag_architecture` → covered by `rag.md` ✅
- Concept `retrieval_failure_modes` → exact file `retrieval_failure_modes.md`
- Concept `grounding_and_citations` → exact file `grounding_and_citations.md`
- Concept `function_calling` → exact file `function_calling.md`
- Concept `structured_outputs` → exact file `structured_outputs.md`
- Concept `agent_planning` → covered by `agents.md` ✅
- Concept `multi_agent_systems` → covered by `agents.md` ✅
- Concept `llm_evaluation` → exact file `llm_evaluation.md`
- `hallucination_detection` → exact file `hallucination_detection.md`
- `observability` → exact file `observability.md`
- `prompt_injection` → exact file `prompt_injection.md`
- `latency_optimization` → exact file `latency_optimization.md`

**A concept is "complete" if its file OR covering file exists.**

### Step 3: Identify the next concept

Walk the ordered list from concept 1. Stop at the **first concept without a file**.
That is the target concept for this session.

**Respect layer ordering:**
- If any concept in Layer N is incomplete, do not suggest a concept from Layer N+1.
- Exception: if the user explicitly asks for a concept from a later layer, proceed
  but prepend a warning: "⚠ Layer N has gaps. Studying this concept out of order."

**Current state (as of 2026-03-04):**
```
✅ 1. temperature        (covered by llm_behavior.md)
✅ 2. seed_determinism   (seed_determinism.md)
⬜ 3. tokenization       ← NEXT TARGET
```

### Step 4: Generate the learning task

Produce a structured learning task with seven sections:

---

```markdown
## Learning Task — Concept N: `<concept_name>`

**Layer:** <N> — <Layer Name>
**Spine position:** #<N> of 24
**Why now:** <One sentence explaining why this concept comes at this point in the sequence.>

---

### What to Learn

**Definition in one sentence:**
<Precise technical definition — no analogies, no hedging.>

**Why it matters for AI systems engineering:**
<Specific production consequence of misunderstanding this concept.>

**One-line rule to remember:**
<A falsifiable, memorable claim. Examples: "At T=0 there is nothing to seed."
"Context window resets on every call. Nothing persists unless you put it in the prompt.">

---

### Suggested Reading Sources

Study these resources in order before running the experiment:

| # | Source | URL | What to read |
|---|--------|-----|-------------|
| 1 | <Primary source — prefer Anthropic/HuggingFace/DeepLearning.AI/OpenAI Docs> | <URL> | <Specific section or page> |
| 2 | <Secondary source> | <URL> | <Specific section or page> |
| 3 | <Optional deep dive — prefer paper or technical blog> | <URL> | <What to focus on> |

**Reading goal:** After reading, you should be able to answer these questions without looking:
1. <Question 1 — definition-level>
2. <Question 2 — mechanism-level>
3. <Question 3 — production-implication-level>

---

### Suggested Experiment

**Experiment topic:** `<descriptive_topic_name>`
**Experiment folder:** `experiments/<category>/<topic_folder>/`
**Experiment ID:** EXP-<NN> *(next available in EXPERIMENT_REGISTRY.md)*

**Hypothesis:**
> <One falsifiable sentence. Must be testable with code and a model API call.>

**Independent variable:** <what you change>
**Controlled variables:** <what you hold constant>
**Measured variable:** <what you observe>

**Suggested code approach:**
```python
# <2–4 lines of pseudocode showing the experimental setup>
# Example: call model with tokenizer.encode(text), compare token counts to word counts
```

**To scaffold this experiment:**
```
@create_experiment
Topic: <experiment_topic>
Category: <llm_behavior / embeddings / rag / agents / evaluation>
```

---

### After studying this concept

1. Run `@add_concept <concept_name>` to create the concept note
2. Run `@create_experiment` to scaffold the experiment
3. Fill `experiment.md` with the hypothesis above
4. Run `code.py`, fill `results.md`, fill `analysis.md`
5. Run `@link_experiment` to connect experiment ↔ concept ↔ RQ
6. Run `@generate_learning_path` again to advance to concept <N+1>
```

---

### Step 5: Append to today's daily log (if it exists)

Check `research/daily_logs/` for a file matching today's date: `YYYY-MM-DD_*.md`.

**If a daily log exists for today:**
Find the `## Experiments Planned` section. Append the following (idempotent — skip if concept already listed):

```markdown
### Next Concept: `<concept_name>` (Spine #N)

**Objective:** Understand <concept_name> deeply enough to explain it, build an experiment, and connect it to previous concepts.

**Reading:** <Primary source title + URL>

**Experiment hypothesis:** <one-sentence hypothesis from Step 4>

**Actions:**
- [ ] Read sources (listed in learning task above)
- [ ] `@add_concept <concept_name>`
- [ ] `@create_experiment` → `experiments/<category>/<topic>/`
- [ ] Run experiment → fill results.md + analysis.md
- [ ] `@link_experiment`
- [ ] `@generate_learning_path` (advance to next)
```

**If no daily log exists for today:**
Output: "No daily log found for today. Run `@start_research_day` first, then re-run `@generate_learning_path`."

---

## Source Priority Order

When selecting reading sources, always prefer in this order:

| Priority | Source | Base URL |
|:--------:|--------|---------|
| 1 | Anthropic Learn | `https://docs.anthropic.com/` |
| 2 | HuggingFace Learn / Course | `https://huggingface.co/learn/` |
| 3 | DeepLearning.AI Short Courses | `https://learn.deeplearning.ai/` |
| 4 | OpenAI Documentation | `https://platform.openai.com/docs/` |
| 5 | Google AI / Gemini Docs | `https://ai.google.dev/docs` |
| 6 | Original paper (arXiv) | `https://arxiv.org/` |
| 7 | LangChain / LlamaIndex Docs | Only for implementation concepts |

**Never recommend:**
- Medium/Substack articles as primary sources
- YouTube videos as primary sources (secondary only)
- Generic Wikipedia pages

---

## Pre-built Learning Tasks

Cursor must generate the full learning task dynamically for any concept.
For reference, here are the pre-seeded tasks for the most common next targets:

### Next concept: `tokenization` (Spine #3)

**Definition:** Tokenization is the process of splitting raw text into a sequence of integer IDs
(tokens) using a vocabulary-based subword algorithm (BPE, WordPiece, or Unigram) before
passing it to a transformer model.

**Why it matters:** Every cost calculation, context window check, and truncation decision
operates in tokens, not words. "gpt-4o-mini" charges per token. Miscounting silently
over-budgets or under-budgets every prompt in production.

**One-line rule:** Whitespace ≠ token boundary. "tokenization" is 3 tokens. A 1,000-word
document is ~1,300 tokens. Always call `tiktoken.encode()`, never estimate.

**Sources:**

| # | Source | URL | What to read |
|---|--------|-----|-------------|
| 1 | OpenAI Tokenizer (interactive) | https://platform.openai.com/tokenizer | Paste 10 different texts and count token splits |
| 2 | OpenAI Cookbook — Counting tokens | https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken | Full article — tiktoken usage |
| 3 | HuggingFace NLP Course — Tokenization | https://huggingface.co/learn/nlp-course/chapter2/4 | Chapter 2, sections 4–6 |
| 4 | Karpathy — "Let's build the GPT tokenizer" | https://www.youtube.com/watch?v=zduSFxRajkE | First 20 min — BPE algorithm |

**Hypothesis:** Token count per word varies systematically by language, domain, and word
frequency — common English words tokenize at ~1.0–1.3 tokens/word, while rare words,
code identifiers, and non-Latin scripts tokenize at 2–5+ tokens/word.

**Experiment folder:** `experiments/llm_behavior/tokenization/`

---

### Next concept: `context_window` (Spine #4)

**Definition:** The context window is the fixed-size input buffer (measured in tokens) that
a transformer model processes in a single forward pass — it includes all system prompt,
conversation history, retrieved context, and the generated response budget.

**Why it matters:** Exceeding the context window raises a hard API error or silently truncates
the oldest messages. Without monitoring, production applications fail on long sessions.

**One-line rule:** System prompt + history + retrieved chunks + max_tokens ≤ model_context_limit.
Always budget tokens before assembling the prompt. Never assemble then truncate.

**Sources:**

| # | Source | URL | What to read |
|---|--------|-----|-------------|
| 1 | OpenAI API Docs — Context window | https://platform.openai.com/docs/models | Model context window table |
| 2 | Anthropic Docs — Long context | https://docs.anthropic.com/en/docs/build-with-claude/context-window | Full article |
| 3 | DeepLearning.AI — LangChain course | https://learn.deeplearning.ai/langchain | Lesson 4: memory management |

**Hypothesis:** As conversation history grows, the system prompt gets evicted first when
the context window is exceeded using a naive "keep latest" truncation strategy — destroying
the model's persona and constraints silently.

**Experiment folder:** `experiments/llm_behavior/context_window/`

---

### Next concept: `positional_encoding` (Spine #8)

**Definition:** Positional encoding is the mechanism that injects token position information
into embeddings before the attention layers, because self-attention is permutation-invariant
and cannot distinguish token order without it.

**Why it matters:** The encoding scheme determines how well the model generalises to sequence
lengths longer than those seen during training — the root cause of degraded performance
at long contexts even within the nominal window limit.

**One-line rule:** Sinusoidal PE is fixed and extrapolates poorly. RoPE (Rotary PE) enables
better length generalisation — it is why modern LLMs handle 128K+ token contexts.

**Sources:**

| # | Source | URL | What to read |
|---|--------|-----|-------------|
| 1 | HuggingFace — Transformer internals | https://huggingface.co/learn/nlp-course/chapter1/4 | Chapter 1, section 4 |
| 2 | Original "Attention Is All You Need" | https://arxiv.org/abs/1706.03762 | Section 3.5 — Positional Encoding |
| 3 | RoFormer paper (RoPE) | https://arxiv.org/abs/2104.09864 | Abstract + Section 3 |

**Hypothesis:** A transformer receiving identical token sequences with shuffled positions
produces measurably different attention patterns — demonstrating that positional encoding
is load-bearing, not cosmetic.

**Experiment folder:** `experiments/llm_behavior/positional_encoding/`

---

## What Cursor Must NOT Do

- Never suggest a concept that already has a file in `research/concepts/`
- Never skip a concept in the ordered sequence without user confirmation
- Never use Wikipedia, Medium, or YouTube as the **primary** reading source
- Never generate a hypothesis that cannot be tested with a model API call or NumPy
- Never append to the daily log without checking for idempotency (same concept already listed?)
- Never suggest Spine #N+1 while Spine #N is incomplete in the same layer

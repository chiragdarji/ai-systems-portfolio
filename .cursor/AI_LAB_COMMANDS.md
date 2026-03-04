---
title: "AI Lab Command Center"
tags: [commands, workflow, cursor, research, automation]
aliases: [command-center, lab-commands, ai-lab-commands]
---

# AI Lab Command Center

Single reference for every Cursor command in this research lab.
Each command has a dedicated definition file in `.cursor/commands/`.

```
Daily research loop:
Learn → Experiment → Document → Insight → Next Question
```

> **Governance:** Before running any experiment command, Cursor checks
> [`AI_RESEARCH_INDEX.md`](../AI_RESEARCH_INDEX.md) for concept slot availability.
> Max 3 experiments per concept. Max 2 open research questions per concept.

---

## Command Index

| # | Command | Purpose | Output |
|---|---------|---------|--------|
| 1 | [`@start_research_day`](#1-start_research_day) | Open a daily research session | `research/daily_logs/YYYY-MM-DD_topic.md` |
| 2 | [`@create_experiment`](#2-create_experiment) | Scaffold a new experiment folder | `experiments/<category>/<topic>/` (4 files) |
| 3 | [`@register_experiment`](#3-register_experiment) | Add experiment to the central registry | Updated `EXPERIMENT_REGISTRY.md` |
| 4 | [`@generate_research_questions`](#4-generate_research_questions) | Extract new RQs from completed experiments | Appended entries in `open_questions.md` |
| 5 | [`@question_to_experiment`](#5-question_to_experiment) | Promote an open RQ into a full experiment | New experiment folder + registry update |
| 6 | [`@finalize_concept`](#6-finalize_concept) | Close a concept chapter and generate summary | `research/concepts/<concept>_summary.md` |
| 7 | [`@add_concept`](#7-add_concept) | Add a new concept note to the knowledge base | `research/concepts/<concept>.md` |
| 8 | [`@create_architecture`](#8-create_architecture) | Document an AI system architecture pattern | `docs/architectures/<name>.md` |
| 9 | [`@weekly_insight`](#9-weekly_insight) | Summarise the week's research progress | `research/insights/week_N_summary.md` |

---

## 1. `@start_research_day`

**Definition file:** [`.cursor/commands/start_research_day.md`](.cursor/commands/start_research_day.md)

**Purpose:** Open a structured daily research session. Forces an explicit objective before any code or experiments are written.

**Actions:**
1. Ask for today's topic (one phrase, e.g. `flashattention`, `rag-chunking`, `agent-reliability`)
2. Create `research/daily_logs/YYYY-MM-DD_<topic>.md`
3. Pre-populate with the sections below
4. Suggest which experiment or concept is next based on `AI_RESEARCH_INDEX.md`

**File created:**
```
research/daily_logs/YYYY-MM-DD_topic.md
```

**Sections generated:**
```markdown
## Objective
## Resources Studied
## Experiments Planned
## Insights
## Open Questions
## Session Wrap-up
```

**When to run:** First action of every research session. Nothing else happens until this file exists.

---

## 2. `@create_experiment`

**Definition file:** [`.cursor/commands/create_experiment.md`](.cursor/commands/create_experiment.md)

**Purpose:** Scaffold a complete, standards-compliant experiment folder. Enforces the hypothesis-first workflow — `experiment.md` is written before `code.py`.

**Governance check (runs automatically before scaffolding):**
- Read `AI_RESEARCH_INDEX.md` → check experiment slot count for the target concept
- If slots used = 3 → **STOP.** Prompt: "Concept `<name>` is at its 3-experiment limit. Run `@finalize_concept` first."
- If slots used < 3 → proceed

**Actions:**
1. Ask: experiment topic and target concept category (`llm_behavior`, `embeddings`, `rag`, `agents`)
2. Assign next available EXP-NN ID from `EXPERIMENT_REGISTRY.md`
3. Create folder: `experiments/<category>/<topic>/`
4. Generate all four required files using `experiments/experiment_template.md`
5. Register the experiment with status `📋 Planned` (see `@register_experiment`)
6. Update `AI_RESEARCH_INDEX.md` experiment slot count for the concept

**Files created:**
```
experiments/<category>/<topic>/
├── experiment.md   ← written first: hypothesis, variables, success criteria
├── code.py         ← boilerplate with run_experiment / print_report / write_markdown
├── results.md      ← stub (auto-populated when code.py runs)
└── analysis.md     ← stub with required section headers
```

**Template used:** [`experiments/experiment_template.md`](../experiments/experiment_template.md)

---

## 3. `@register_experiment`

**Definition file:** Inline — handled automatically by `@create_experiment` and `@question_to_experiment`.
Can be run standalone to register a manually created experiment.

**Purpose:** Add or update an experiment's entry in the central registry and dashboard.

**Actions:**
1. Ask for: Experiment ID, topic, folder path, one-sentence hypothesis, status
2. Add row to `experiments/EXPERIMENT_REGISTRY.md` registry table
3. Add entry to `experiments/EXPERIMENT_DASHBOARD.md` under the correct section
4. Update `AI_RESEARCH_INDEX.md` experiment slot for the concept

**Fields written to registry:**

| Field | Example |
|-------|---------|
| Experiment ID | `EXP-06` |
| Topic | `Sentence Embeddings & Cosine Similarity` |
| Folder | `experiments/embeddings/sentence_similarity/` |
| Hypothesis | `Semantically similar sentences cluster geometrically in embedding space` |
| Status | `📋 Planned` |
| Key Insight | `—` *(filled after completion)* |
| Next Question | *(filled after completion)* |

**Status progression:**
```
📋 Planned → 🔄 In Progress → ✅ Complete
```

---

## 4. `@generate_research_questions`

**Definition file:** [`.cursor/commands/generate_research_questions.md`](.cursor/commands/generate_research_questions.md)

**Purpose:** Systematically extract new research questions from completed experiment findings. Prevents questions from being forgotten and ensures the research backlog stays populated.

**Governance check (runs automatically):**
- For each generated question, check the target concept's RQ slot count in `AI_RESEARCH_INDEX.md`
- If slots used = 2 → set generated question status to `⏸ Deferred` instead of `🔴 Open`

**Actions:**
1. Read all `analysis.md` files for `✅ Complete` experiments
2. Identify: unresolved tensions, contradictions, "next step" observations, production implications not yet tested
3. Deduplicate against existing entries in `open_questions.md` and `answered_questions.md`
4. Generate exactly **3 new research questions** with:
   - Unique RQ-NN ID (next available)
   - Question, motivation, related experiment, proposed experiment, priority
5. Append to `research/questions/open_questions.md`
6. Update `AI_RESEARCH_INDEX.md` RQ slot counts for affected concepts

**Quality criteria for generated questions:**
- Must be **falsifiable** — an experiment could prove it wrong
- Must be **grounded** — cites a specific finding from a completed experiment
- Must be **novel** — not already in the backlog or answered

**Output appended to:**
```
research/questions/open_questions.md
```

---

## 5. `@question_to_experiment`

**Definition file:** [`.cursor/commands/question_to_experiment.md`](.cursor/commands/question_to_experiment.md)

**Purpose:** Promote an open research question directly into a fully scaffolded experiment, pre-populated from the RQ's details. Closes the `RQ → Experiment → Answer → New RQ` loop.

**Governance check (runs automatically):**
- Check the concept's experiment slot count in `AI_RESEARCH_INDEX.md`
- If slots used = 3 → STOP and run `@finalize_concept` first

**Actions:**
1. Ask for the Question ID (e.g. `RQ-04`)
2. Read the full RQ entry from `open_questions.md`
3. Assign the next EXP-NN ID
4. Create experiment folder in the appropriate concept category
5. Pre-populate `experiment.md` from the RQ's hypothesis, motivation, and proposed experiment fields
6. Generate `code.py`, `results.md`, `analysis.md` stubs
7. Register in `EXPERIMENT_REGISTRY.md` and `EXPERIMENT_DASHBOARD.md`
8. Update RQ status in `open_questions.md`: `🔴 Open` → `🟡 In Progress`
9. Update `AI_RESEARCH_INDEX.md` slot counts

**Files created:**
```
experiments/<category>/<rq-topic>/
├── experiment.md   ← pre-populated from RQ details
├── code.py         ← boilerplate
├── results.md      ← stub
└── analysis.md     ← stub
```

---

## 6. `@finalize_concept`

**Definition file:** [`.cursor/commands/close_concept.md`](.cursor/commands/close_concept.md)

**Purpose:** Close a concept chapter, synthesise all experiment findings into a permanent summary, and activate the next concept in the learning path. Prevents indefinite accumulation of experiments on a single topic.

**Hard rules enforced:**
- **Max 3 experiments per concept.** Running this command is required before slot 4 can be used on a new sub-concept.
- **Max 2 open RQs per concept.** Excess RQs are automatically deferred on closure.
- Cannot be run until all concept experiments are `✅ Complete`.

**Actions:**
1. Validate: all concept experiments at `✅ Complete`; all RQs answered or deferrable
2. Read all linked `analysis.md` files for this concept
3. Generate `research/concepts/<concept_name>_summary.md` from [`concept_summary_template.md`](../research/concepts/concept_summary_template.md)
4. Update `AI_RESEARCH_INDEX.md`: status → `✅ Complete`, add summary link, activate next concept
5. Move excess open RQs to `⏸ Deferred` in `open_questions.md`
6. Annotate the concept note with a closure banner
7. Suggest the first experiment of the next active concept

**File created:**
```
research/concepts/<concept_name>_summary.md
```

**Template used:** [`research/concepts/concept_summary_template.md`](../research/concepts/concept_summary_template.md)

**Summary sections:**
```markdown
## What We Set Out to Answer
## Experiments Run (table with verdict)
## 3 Key Mental Models
## Engineering Decisions Unlocked
## Deferred Questions
## Connection to Next Concept
## Concept-Level Insight
```

---

## 7. `@add_concept`

**Definition file:** [`.cursor/commands/add_concept.md`](.cursor/commands/add_concept.md)

**Purpose:** Add a new concept note to the research knowledge base. Creates a structured reference file for a single AI concept, mechanism, or technique — and registers it in `AI_RESEARCH_INDEX.md`.

**Distinction from `@finalize_concept`:**
- `@add_concept` writes a *reference note* — created **before or during** experiments to capture a concept you are studying
- `@finalize_concept` writes a *synthesis summary* — created **after** all experiments in a chapter complete

**Actions:**
1. Ask for: concept name, related experiments (optional), key insight in one sentence (optional)
2. Convert concept name to `snake_case` for the filename
3. Check for duplicates in `research/concepts/` and `AI_RESEARCH_INDEX.md`
4. Create `research/concepts/<snake_case_name>.md` using the structured template
5. Register the new concept in `AI_RESEARCH_INDEX.md` → `## Concepts Knowledge Base`
6. Confirm creation and suggest next step (`@create_experiment` or `@generate_research_questions`)

**File created:**
```
research/concepts/<snake_case_name>.md
```

**Sections generated:**
```markdown
## Definition
## Why It Matters
## How It Works
## Practical Observations
## Limitations
## Related Experiments
## Key Insight
## Open Questions
## References
```

**Naming examples:**

| Input | File created |
|-------|-------------|
| `Seed Determinism` | `seed_determinism.md` |
| `Online Softmax` | `online_softmax.md` |
| `FlashAttention` | `flash_attention.md` |
| `RAG Chunk Size` | `rag_chunk_size.md` |

**When to run:** When you encounter a new concept while studying, during an experiment debrief, or when a research question introduces a term that needs a reference note.

---

## 8. `@create_architecture`  

**Purpose:** Document a non-trivial AI system architecture pattern for future reference and portfolio demonstration.

**Actions:**
1. Ask for: architecture name and the problem it solves
2. Create `docs/architectures/<name>.md` using `docs/architecture_template.md`
3. Pre-populate with the provided problem statement

**File created:**
```
docs/architectures/<name>.md
```

**Template used:** [`docs/architecture_template.md`](../docs/architecture_template.md)

**Sections generated:**
```markdown
## Problem
## System Components
  (with responsibilities, failure modes, scaling notes per component)
## Data Flow
  input → [Component A] → [Component B] → output
## Scaling Considerations
  At N=1,000 req/day: ...
  At N=100,000 req/day: ...
## Failure Modes
  failure → detection signal → mitigation
## When To Use
## When NOT To Use
## Implementation Notes
## Related Experiments
```

**When to run:** After completing a concept that produces a deployable architecture (RAG, Agents, Production Systems).

---

## 9. `@weekly_insight`

**Purpose:** Synthesise the week's work into a permanent insight record. Prevents learnings from disappearing into daily logs that are never re-read.

**Actions:**
1. Ask for: week number or date range (e.g. `Week 1`, `2026-02-24 to 2026-03-04`)
2. Read all daily logs from `research/daily_logs/` created in that date range
3. Read all `✅ Complete` experiments' `analysis.md` files from that week
4. Generate `research/insights/week_<N>_summary.md`

**File created:**
```
research/insights/week_N_summary.md
```

**Sections generated:**
```markdown
## Week N — YYYY-MM-DD to YYYY-MM-DD

### Concepts Studied
### Experiments Completed
  (table: ID, topic, hypothesis verdict, key number)
### Major Insights
  (numbered, falsifiable, evidence-cited)
### Mental Models Developed
  (3 max — the ideas that will still matter in 1 year)
### Open Problems
  (what remains unresolved — feeds next week's @start_research_day)
### Concept Progress
  (which concepts advanced, which closed, which activated)
```

---

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│  DAILY LOOP                                                 │
│                                                             │
│  @start_research_day                                        │
│       │                                                     │
│       ├──► @add_concept  (new concept encountered?)         │
│       │         └── research/concepts/<name>.md             │
│       │                                                     │
│       ▼                                                     │
│  Check AI_RESEARCH_INDEX.md ── concept at limit? ──► @finalize_concept
│       │                                                     │
│       ▼                                                     │
│  @create_experiment  ◄──── @question_to_experiment          │
│       │                           ▲                         │
│       ▼                           │                         │
│  Run code.py (auto-generates results.md)                    │
│       │                           │                         │
│       ▼                           │                         │
│  Write analysis.md                │                         │
│       │                           │                         │
│       ▼                           │                         │
│  @register_experiment             │                         │
│       │                           │                         │
│       ▼                           │                         │
│  @generate_research_questions ────┘                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  WEEKLY LOOP                                                │
│                                                             │
│  @weekly_insight → review open problems → plan next week    │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  CONCEPT LOOP                                               │
│  (every 3 experiments)                                      │
│                                                             │
│  @finalize_concept → summary generated → next concept       │
│                      activated in AI_RESEARCH_INDEX.md      │
│                                                             │
│  @add_concept (anytime) → reference note added to           │
│                           Concepts Knowledge Base           │
└─────────────────────────────────────────────────────────────┘
```

---

## File Reference Map

| Command | Reads | Writes / Updates |
|---------|-------|-----------------|
| `@start_research_day` | `AI_RESEARCH_INDEX.md` | `research/daily_logs/YYYY-MM-DD_topic.md` |
| `@create_experiment` | `AI_RESEARCH_INDEX.md`, `experiment_template.md` | `experiments/<cat>/<topic>/` (4 files), `EXPERIMENT_REGISTRY.md`, `AI_RESEARCH_INDEX.md` |
| `@register_experiment` | `EXPERIMENT_REGISTRY.md` | `EXPERIMENT_REGISTRY.md`, `EXPERIMENT_DASHBOARD.md`, `AI_RESEARCH_INDEX.md` |
| `@generate_research_questions` | `experiments/**/analysis.md`, `open_questions.md` | `open_questions.md`, `AI_RESEARCH_INDEX.md` |
| `@question_to_experiment` | `open_questions.md`, `AI_RESEARCH_INDEX.md` | `experiments/<cat>/<topic>/` (4 files), `open_questions.md`, `EXPERIMENT_REGISTRY.md`, `AI_RESEARCH_INDEX.md` |
| `@finalize_concept` | `AI_RESEARCH_INDEX.md`, `experiments/**/analysis.md` | `research/concepts/<concept>_summary.md`, `AI_RESEARCH_INDEX.md`, `open_questions.md` |
| `@add_concept` | `AI_RESEARCH_INDEX.md`, `research/concepts/` (duplicate check) | `research/concepts/<name>.md`, `AI_RESEARCH_INDEX.md` (Concepts Knowledge Base) |
| `@create_architecture` | `architecture_template.md` | `docs/architectures/<name>.md` |
| `@weekly_insight` | `research/daily_logs/`, `experiments/**/analysis.md` | `research/insights/week_N_summary.md` |

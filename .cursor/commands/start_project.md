---
title: "Cursor Command — start_project"
tags: [command, cursor, projects, system-design, portfolio]
aliases: [start-project-command, project-scaffolder]
---

# Command: `@start_project`

Scaffolds a complete AI system project folder grounded in completed research concepts.
Projects are the output layer of the lab: where accumulated experiment knowledge becomes
a deployable, demonstrable system.

**Trigger:** `@start_project` or `@start_project <project_name>`

**All writes are idempotent — running this command twice produces identical files.**
**Projects must be grounded in at least one completed concept (✅ in AI_RESEARCH_INDEX.md).**

---

## When to Run This Command

Run `@start_project` when:
- One or more concepts in `AI_RESEARCH_INDEX.md` are `✅ Complete`
- You want to translate experiment findings into a working system
- You are starting a portfolio project that demonstrates mastery of a concept cluster
- A research question has produced enough knowledge to build something real

**Do NOT run before any concepts are complete.** A project without grounded concept
knowledge produces throwaway code, not portfolio-quality engineering.

---

## Concept → Project Mapping

Cursor uses this table to auto-suggest a project when concept completion is detected.
The user can override the suggestion at any time.

| Completed concepts required | Suggested project name | Description |
|----------------------------|:----------------------:|-------------|
| `temperature` + `system_prompts` | `prompt_playground` | Interactive prompt parameter explorer |
| `tokenization` + `llm_behavior` | `token_budget_manager` | Production token counting and context guard library |
| `tokenization` + `context_window` | `context_window_analyzer` | Visualise context fill across domains and models |
| `embeddings` + `vector_search` | `vector_search_engine` | Semantic search over a document corpus |
| `rag_architecture` + `chunking_strategies` | `rag_assistant` | Full RAG pipeline with configurable retrieval |
| `rag_architecture` + `reranking` | `rag_eval_pipeline` | RAG quality evaluation with scoring metrics |
| `function_calling` + `structured_outputs` | `tool_agent` | Single-agent with real tool use |
| `agent_planning` + `multi_agent_systems` | `multi_agent_system` | Supervisor + worker agent pattern |
| `observability` + `latency_optimization` | `production_llm_pipeline` | Production-ready LLM service with telemetry |
| `llm_evaluation` + `hallucination_detection` | `llm_eval_framework` | Automated quality and safety evaluator |

---

## Step-by-Step Execution

### Step 1: Read completed concepts

Read `AI_RESEARCH_INDEX.md` → scan `## Concepts` table for rows where Status = `✅ Complete`.

Build a list: `completed_concepts = [<concept_name>, ...]`

If no completed concepts exist, stop and output:

```
⛔ No completed concepts found.
Run @finalize_concept or complete at least one concept before starting a project.
The concept → project loop requires grounded research, not speculation.
```

### Step 2: Auto-suggest a project

Match `completed_concepts` against the **Concept → Project Mapping** table above.

- If exactly one mapping matches → auto-suggest that project and ask for confirmation
- If multiple mappings match → list all candidates and ask the user to choose
- If no mapping matches → ask the user to provide a project name and short description

**Output format:**

```
Completed concepts: temperature, seed_determinism, tokenization, llm_behavior

Suggested project based on your completed concepts:
  → token_budget_manager
     "Production token counting and context guard library"
     Concepts used: tokenization, llm_behavior

Confirm? (yes / enter a different project name)
```

### Step 3: Collect project inputs

If not auto-determined, ask:

```
1. Project name? (snake_case, e.g. rag_assistant, token_budget_manager)
2. One-sentence problem statement? (what real problem does this solve?)
3. Primary concept(s) this demonstrates? (from completed concepts list)
```

### Step 4: Validate — no duplicate project

Check `projects/` directory. If `projects/<project_name>/` already exists, stop:

```
⛔ projects/<project_name>/ already exists.
To continue work on it, open projects/<project_name>/project.md directly.
To create a variant, choose a different name.
```

### Step 5: Create the project folder structure

```
projects/<project_name>/
├── project.md          ← problem, goal, concept links, system overview
├── architecture.md     ← components, data flow, failure modes, scaling
├── README.md           ← quick start, what it demonstrates, how to run
├── implementation/     ← source code lives here
│   └── .gitkeep
├── experiments/        ← project-specific experiments (not in the main registry)
│   └── .gitkeep
└── evaluation/         ← evaluation scripts and results
    └── .gitkeep
```

Create all directories and files in this exact structure.

### Step 6: Populate `project.md`

```markdown
---
title: "Project — <Human Name>"
tags: [project, <concept-tags>, portfolio]
aliases: [<project_name>, <project_name>-project]
---

# Project: <Human Name>

**Name:** `<project_name>`
**Started:** YYYY-MM-DD
**Status:** 🚧 In Progress
**Concepts demonstrated:** [<Concept 1>](<relative_link>) · [<Concept 2>](<relative_link>)
**Related experiments:** [EXP-NN](<relative_link>) · [EXP-NN](<relative_link>)

---

## Problem

> <One-paragraph statement of the real-world problem this system addresses.>
> Frame as: "In production AI systems, X is a challenge because Y. When Z happens,
> the consequences are W. This project builds a system that solves this by..."

## Goal

> What a working version of this project must be able to do.
> Frame as numbered acceptance criteria — not aspirations.

1. [ ] <Acceptance criterion 1 — measurable, specific>
2. [ ] <Acceptance criterion 2>
3. [ ] <Acceptance criterion 3>

## Related Concepts

| Concept | What this project tests | File |
|---------|:----------------------:|------|
| <Concept 1> | <how the concept is applied here> | [research/concepts/<name>.md](<path>) |
| <Concept 2> | <how the concept is applied here> | [research/concepts/<name>.md](<path>) |

## Related Experiments

| Experiment | Finding used in this project |
|-----------|:----------------------------:|
| [EXP-NN — <Topic>](<path>) | <specific finding or mechanism this project builds on> |

## System Overview

<3–5 sentence description of what the system does and how it works at a high level.
Include: input → processing → output. Mention key libraries and APIs used.>

## Implementation Status

| Component | Status | Notes |
|-----------|:------:|-------|
| <Component 1> | ⬜ Not started | |
| <Component 2> | ⬜ Not started | |
| <Component 3> | ⬜ Not started | |

## Engineering Decisions

> Record significant design choices here as you make them.
> Format: **Decision:** X. **Why:** Y. **Trade-off:** Z.

*(none yet)*

## Open Questions

*(Unanswered engineering questions — link to open_questions.md entries if relevant)*

---

*Architecture → [`architecture.md`](architecture.md)*
*How to run → [`README.md`](README.md)*
```

### Step 7: Populate `architecture.md`

```markdown
---
title: "Architecture — <Human Name>"
tags: [architecture, <concept-tags>, system-design]
aliases: [<project_name>-architecture]
---

# Architecture: <Human Name>

> This document describes the system design of `projects/<project_name>/`.
> All architectural decisions are grounded in findings from the linked experiments.

---

## System Components

| Component | Responsibility | Key technology | Failure mode |
|-----------|:-------------:|:--------------:|:------------:|
| <Component 1> | <what it does> | <library/API> | <what breaks if this fails> |
| <Component 2> | <what it does> | <library/API> | <what breaks if this fails> |
| <Component 3> | <what it does> | <library/API> | <what breaks if this fails> |

---

## Data Flow

```
Input → [Component A] → [Component B] → [Component C] → Output

<Describe each arrow: what data is passed, in what format, at what rate>
```

---

## Failure Modes

| Failure | Detection signal | Mitigation |
|---------|:----------------:|-----------|
| <Failure 1> | <observable symptom> | <how to recover or prevent> |
| <Failure 2> | <observable symptom> | <how to recover or prevent> |
| <Failure 3> | <observable symptom> | <how to recover or prevent> |

---

## Scaling Considerations

**At 100 requests/day (prototype):**
> <What works fine, what needs to be watched>

**At 10,000 requests/day (production):**
> <What changes: caching, batching, async, cost controls>

**At 1,000,000 requests/day (scaled):**
> <What fundamentally changes: infrastructure, model selection, multi-region>

---

## Experiment-Grounded Decisions

| Decision | Grounded in | Evidence |
|----------|:-----------:|---------|
| <architectural choice> | [EXP-NN](<path>) | <specific finding that justifies this choice> |

---

## When To Use This Architecture

- <condition 1>
- <condition 2>

## When NOT To Use This Architecture

- <condition 1 — simpler approach exists>
- <condition 2 — this adds unnecessary complexity>
```

### Step 8: Populate `README.md`

```markdown
# <Human Project Name>

> <One-sentence description of what this project does and why it exists.>

Part of the [`ai-systems-portfolio`](../../README.md) research lab.
Built from findings in: <Concept 1>, <Concept 2>.

---

## What This Demonstrates

- <Capability 1 — connects to a specific experiment finding>
- <Capability 2>
- <Capability 3>

## Setup

```bash
# From repo root
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.template .env  # add API keys
```

## Usage

```bash
# Run the main implementation
python projects/<project_name>/implementation/main.py

# Run evaluation
python projects/<project_name>/evaluation/evaluate.py
```

## Key Files

| File | Purpose |
|------|---------|
| `project.md` | Problem, goals, concept links, implementation status |
| `architecture.md` | System design, data flow, failure modes |
| `implementation/` | Source code |
| `experiments/` | Project-specific experiments |
| `evaluation/` | Evaluation scripts and results |

## Related Research

| Asset | Link |
|-------|------|
| Concept notes | <links> |
| Key experiments | <links> |
```

### Step 9: Register in `AI_RESEARCH_INDEX.md`

Add a row to the `## Projects` section (create the section if it doesn't exist):

```markdown
## Projects

| Project | Folder | Concepts | Status | Started |
|---------|--------|:--------:|:------:|---------|
| [<Human Name>](projects/<project_name>/project.md) | `projects/<project_name>/` | <Concept 1>, <Concept 2> | 🚧 In Progress | YYYY-MM-DD |
```

**If `## Projects` section does not exist in `AI_RESEARCH_INDEX.md`**, insert it after `## Architectures`
and before `## Insights`.

### Step 10: Confirm all changes

Output a summary:

```
✅ @start_project complete

Project: <Human Name>
Folder:  projects/<project_name>/

Files created:
  ✓ projects/<project_name>/project.md
  ✓ projects/<project_name>/architecture.md
  ✓ projects/<project_name>/README.md
  ✓ projects/<project_name>/implementation/.gitkeep
  ✓ projects/<project_name>/experiments/.gitkeep
  ✓ projects/<project_name>/evaluation/.gitkeep

Registered in:
  ✓ AI_RESEARCH_INDEX.md → ## Projects

Concepts linked:
  ✓ <Concept 1> → research/concepts/<name>.md
  ✓ <Concept 2> → research/concepts/<name>.md

Next steps:
  1. Open project.md → fill in Problem and Acceptance Criteria
  2. Open architecture.md → design the system components and data flow
  3. Start implementation/main.py from the architecture
  4. Run @create_architecture to generate a standalone architecture doc
  5. Commit: git add projects/<project_name>/ && git commit
```

---

## Project Status Lifecycle

```
🚧 In Progress → 🔄 Active Development → ✅ Demo-Ready → 📦 Archived
```

| Status | Meaning |
|--------|---------|
| 🚧 In Progress | Folder created, design in progress |
| 🔄 Active Development | Implementation underway, not yet runnable end-to-end |
| ✅ Demo-Ready | Runs end-to-end; all acceptance criteria met; documented |
| 📦 Archived | Complete; referenced for future projects |

---

## Idempotency Rules

| Check | If already exists | Action |
|-------|:-----------------:|--------|
| `projects/<project_name>/` folder | EXISTS | Stop; report "project already exists" |
| `## Projects` section in `AI_RESEARCH_INDEX.md` | EXISTS | Append row only; do not recreate section |
| Project row in `## Projects` table | EXISTS | Skip; report as idempotency skip |

---

## Relative Path Reference

| Writing into | Link to experiments | Link to concepts | Link to AI_RESEARCH_INDEX.md |
|---|---|---|---|
| `projects/<name>/project.md` | `../../experiments/` | `../../research/concepts/` | `../../AI_RESEARCH_INDEX.md` |
| `projects/<name>/architecture.md` | `../../experiments/` | `../../research/concepts/` | `../../AI_RESEARCH_INDEX.md` |
| `AI_RESEARCH_INDEX.md` | `experiments/` | `research/concepts/` | `./` |

---

## Usage Examples

```
@start_project
→ auto-detects completed concepts, suggests token_budget_manager

@start_project rag_assistant
→ immediately scaffolds projects/rag_assistant/ (still validates concepts)

@start_project prompt_playground
→ scaffolds projects/prompt_playground/ using temperature + system_prompts
```

---

## What Cursor Must NOT Do

- Never scaffold a project without verifying at least one completed concept in `AI_RESEARCH_INDEX.md`
- Never use absolute file paths — all links must be relative
- Never create a project folder that already exists — validate first, then report
- Never write a `project.md` that doesn't link back to at least one concept note
- Never omit the `implementation/`, `experiments/`, and `evaluation/` subfolders
- Never skip the `AI_RESEARCH_INDEX.md` registration step

---

*Related commands: `@create_architecture` · `@finalize_concept` · `@link_experiment`*
*Project folders live in: [`projects/`](../../projects/)*
*Index registered in: [`AI_RESEARCH_INDEX.md`](../../AI_RESEARCH_INDEX.md)*

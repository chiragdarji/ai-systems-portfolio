---
title: "Cursor Command — link_experiment"
tags: [command, cursor, knowledge-graph, experiments, concepts, research-questions]
aliases: [link-experiment-command, experiment-linker]
---

# Command: `@link_experiment`

Links an experiment to a concept note and optionally a research question,
maintaining a structured knowledge graph across the repository.

**Trigger:** `@link_experiment`

**All links written are relative markdown links — never absolute paths.**
**All writes are idempotent — running this command twice produces identical files.**

---

## When to Run This Command

Run `@link_experiment` when:
- An experiment has been run and its concept connection was not set up by `@create_experiment`
- A new concept note was added via `@add_concept` and existing experiments should reference it
- A research question has been answered by an experiment and the link needs to be formalised
- You want to audit the knowledge graph and fill missing cross-links

---

## Step-by-Step Execution

### Step 1: Ask for three inputs

```
1. Experiment folder path?
   (relative from repo root — e.g. experiments/llm_behavior/temperature)

2. Concept name?
   (snake_case or human-readable — e.g. "seed_determinism" or "Seed Determinism")
   Cursor resolves to: research/concepts/<snake_case>.md

3. Research question ID? (optional — press Enter to skip)
   (e.g. RQ-01, RQ-04)
```

### Step 2: Validate all targets exist

Before writing anything, verify:

```
[ ] <experiment_folder>/experiment.md  exists?
[ ] research/concepts/<concept_name>.md  exists?
[ ] If RQ provided: entry ### RQ-NN exists in research/questions/open_questions.md?
```

If any target is missing, stop and report:
- Missing `experiment.md` → "Run `@create_experiment` first"
- Missing concept file → "Run `@add_concept <concept_name>` first"
- Missing RQ → "RQ-NN not found in open_questions.md. Check the ID and try again."

### Step 3: Update `experiment.md`

Read `<experiment_folder>/experiment.md`.

**Idempotency check:** Search for `## Links` section. If it already exists, check whether
the concept and RQ are already listed. Only append what is missing.

**If `## Links` section does not exist**, append it at the end of the file:

```markdown
---

## Links

**Concept:** [`<Concept Name>`](../../../research/concepts/<concept_name>.md)

**Research Question:** [RQ-NN](../../../research/questions/open_questions.md#rq-nn--<slug>)
```

**If `## Links` section exists but is missing the concept**, add the concept line.
**If `## Links` section exists but is missing the RQ**, add the RQ line.
**If no RQ was provided**, omit the Research Question line entirely.

**Relative path calculation for experiment.md:**
The path from `experiments/<category>/<folder>/experiment.md` to `research/` is `../../../research/`.

```
experiments/llm_behavior/temperature/experiment.md
  → ../../../research/concepts/seed_determinism.md  ✓
```

### Step 4: Update `research/concepts/<concept_name>.md`

Read the concept file and locate the `## Related Experiments` section.

**Idempotency check:** Scan the `## Related Experiments` section for a link containing
the experiment folder path. If it already exists, skip — do not duplicate.

**If `## Related Experiments` section does not exist**, append it before `## References`
(or at end of file if `## References` is absent):

```markdown
---

## Related Experiments

| Experiment | Relationship |
|-----------|-------------|
| [EXP-NN — <Topic>](<relative_path_to_experiment.md>) | <one-line description of what the experiment tests for this concept> |
```

**If `## Related Experiments` exists as a table (2-column format)**, append a new row:

```markdown
| [EXP-NN — <Topic>](<relative_path>) | <relationship description> |
```

**If `## Related Experiments` exists as a table (3-column format: Experiment / What It Tests / Key Finding)**,
append a new row:

```markdown
| [EXP-NN — <Topic>](<relative_path>) | <what it tests for this concept> | <key finding> |
```

**Match the existing table format exactly.** Do not change a 3-column table to a 2-column table.

**Relative path calculation for concept files:**
The path from `research/concepts/<file>.md` to `experiments/` is `../../experiments/`.

```
research/concepts/seed_determinism.md
  → ../../experiments/llm_behavior/temperature/experiment.md  ✓
```

**EXP number and title:**
Resolve the experiment number and title from `experiments/EXPERIMENT_REGISTRY.md` by
matching the folder path. Use the ID and topic from the registry row.

### Step 5: Update `research/questions/open_questions.md` (if RQ provided)

Read the detailed entry for RQ-NN (the `### RQ-NN` section).

**Idempotency check:** Search the entry for a line containing `**Linked experiment:**`.
If it already exists, skip.

**If not present**, add the following line immediately after the `**Proposed experiment:**` line:

```markdown
**Linked experiment:** [`<experiment_folder>/experiment.md`](<relative_path_to_experiment.md>)
```

**Relative path calculation for open_questions.md:**
The path from `research/questions/open_questions.md` to `experiments/` is `../../experiments/`.

```
research/questions/open_questions.md
  → ../../experiments/llm_behavior/temperature/experiment.md  ✓
```

**Do not change the RQ's status** — status updates are the user's responsibility
(or handled by `@question_to_experiment`).

### Step 6: Confirm all changes

Output a summary of every write made:

```
✅ @link_experiment complete

Experiment:  experiments/llm_behavior/temperature/
Concept:     research/concepts/seed_determinism.md
RQ:          RQ-01 (optional — only shown if provided)

Changes written:
  ✓ experiments/llm_behavior/temperature/experiment.md
      → Added ## Links section with concept and RQ references

  ✓ research/concepts/seed_determinism.md
      → Appended row to ## Related Experiments table

  ✓ research/questions/open_questions.md
      → Added Linked experiment line to RQ-01 entry

Skipped (already linked):
  — (list any idempotency skips here)
```

---

## Idempotency Rules

These checks must run before every write. If the content already exists, skip silently
and report it under "Skipped (already linked)" in the confirmation output.

| File | Idempotency check |
|------|-----------------|
| `experiment.md` | Search for concept filename in `## Links` section |
| `experiment.md` | Search for RQ-NN in `## Links` section |
| `concept.md` | Search for experiment folder path in `## Related Experiments` section |
| `open_questions.md` | Search for `**Linked experiment:**` in the RQ-NN entry |

---

## Relative Path Reference

| From file | To `experiments/` | To `research/concepts/` | To `research/questions/` |
|-----------|:-----------------:|:-----------------------:|:------------------------:|
| `experiments/<cat>/<folder>/experiment.md` | `./` (same tree) | `../../../research/concepts/` | `../../../research/questions/` |
| `research/concepts/<name>.md` | `../../experiments/` | `./` (same folder) | `../questions/` |
| `research/questions/open_questions.md` | `../../experiments/` | `../concepts/` | `./` (same folder) |

---

## Worked Example

**Input:**
```
Experiment folder: experiments/llm_behavior/temperature
Concept name:      seed_determinism
RQ ID:             RQ-01
```

**`experiment.md` — appended:**
```markdown
---

## Links

**Concept:** [`Seed Determinism`](../../../research/concepts/seed_determinism.md)

**Research Question:** [RQ-01](../../../research/questions/open_questions.md#rq-01--temperature-seed-determinism)
```

**`seed_determinism.md` — row appended to `## Related Experiments`:**
```markdown
| [EXP-01 — Temperature & Output Entropy](../../experiments/llm_behavior/temperature/experiment.md) | Established T=0 non-determinism baseline that raised RQ-01 |
```

**`open_questions.md` — line added to RQ-01 entry:**
```markdown
**Proposed experiment:** EXP-05b — run 20 identical calls...
**Linked experiment:** [`experiments/llm_behavior/temperature/experiment.md`](../../experiments/llm_behavior/temperature/experiment.md)
```

---

## What Cursor Must NOT Do

- Never use absolute paths — all links must be relative
- Never duplicate a link that already exists in the target section
- Never change a concept file's `## Related Experiments` table column count
- Never modify the RQ status field — only add the `Linked experiment` line
- Never create any of the three target files if they do not exist — validate first, then report
- Never write partial links (e.g. folder only without the `experiment.md` filename)

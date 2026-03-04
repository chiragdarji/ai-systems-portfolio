---
title: "Cursor Command — close_concept"
tags: [command, cursor, concept-governance, workflow]
aliases: [close-concept-command, concept-closure]
---

# Command: `@close_concept`

Closes a completed concept chapter, generates its summary file, updates `AI_RESEARCH_INDEX.md`,
and activates the next concept in the learning path.

**Trigger:** `@close_concept <concept_name>`
**Example:** `@close_concept llm_behavior`

---

## When to Run This Command

Run `@close_concept` when:
1. All experiments in the concept's chapter are `✅ Complete` in `EXPERIMENT_REGISTRY.md`
2. All research questions have been answered or explicitly deferred
3. The concept's experiment count has reached 3 (hard limit)

Cursor will refuse to add new experiments to a closed concept.
The only way to reopen a concept is to start a new sub-chapter with a new concept entry.

---

## Step-by-Step Execution

When the user runs `@close_concept <concept_name>`, Cursor must execute all steps in order:

### Step 1: Validate readiness

Read `AI_RESEARCH_INDEX.md` and check the concept's entry:

```
[ ] All experiments in the chapter are ✅ Complete?
[ ] All open RQs are either 🟢 Answered or ⏸ Deferred?
[ ] Status is not already ✅ Complete or 📦 Closed?
```

If any check fails, stop and report what is incomplete.

### Step 2: Read all analysis files for this concept

Read each `analysis.md` linked in the concept's experiment slots.
Extract: key insights, mental models, production implications, deferred questions.

### Step 3: Generate the concept summary file

Create `research/concepts/<concept_name>_summary.md` using `research/concepts/concept_summary_template.md`.

Populate with evidence from the analysis files:
- **Experiments Run** table → pulled from experiment.md files
- **3 Key Mental Models** → synthesised from the strongest findings across all analysis.md files
- **Engineering Decisions** → pulled from "Production Implications" sections of analysis.md files
- **Deferred Questions** → list any RQs that exceeded the 2-RQ slot limit
- **Connection to Next Concept** → read the next concept entry in AI_RESEARCH_INDEX.md

### Step 4: Update `AI_RESEARCH_INDEX.md`

Make the following changes:
1. Set concept status: `📖 Active` → `✅ Complete`
2. Add summary link: `research/concepts/<concept_name>_summary.md`
3. Update the Concept Status Overview table row
4. Update the Governance Counters table row (mark "Can Add Exp?" as ❌ Closed)
5. Add a row to the Concept Transition Log:
   ```
   | <date> | Concept closed | <concept_name> | Summary generated; next concept activated |
   ```
6. Set the next concept's status: `📋 Planned` → `📖 Active`

### Step 5: Update `open_questions.md`

For any RQs belonging to this concept that are still `🔴 Open`:
- If they exceed the 2-RQ slot limit → change status to `⏸ Deferred`
- Add a note: "Deferred at concept closure — revisit when Concept N becomes Active"

### Step 6: Update the concept note

In `research/concepts/<concept_name>.md`, add at the top (after YAML frontmatter):

```markdown
> ✅ **Chapter closed** — YYYY-MM-DD
> Concept summary: [`<concept_name>_summary.md`](<concept_name>_summary.md)
> Next concept: [<Next Concept>](../../AI_RESEARCH_INDEX.md#N-next-concept-name)
```

### Step 7: Suggest the next experiment

Read the next concept's experiment slots from `AI_RESEARCH_INDEX.md`.
Output a suggestion:

```
Concept '<concept_name>' is now closed.

Summary generated: research/concepts/<concept_name>_summary.md
Next active concept: <next_concept_name>

Suggested next experiment:
  @create_experiment <first_planned_experiment_from_next_concept>

Would you like to start <next_concept_name>?
```

---

## Template Values

When generating `<concept_name>_summary.md`, replace these placeholders:

| Placeholder | Replace with |
|-------------|-------------|
| `<Concept Name>` | Human-readable concept name (e.g. "LLM Behavior — Sampling & Control") |
| `<concept_name>` | File-safe concept name (e.g. `llm_behavior`) |
| `<concept-tag>` | Kebab-case tag (e.g. `llm-behavior`) |
| `<Next Concept Name>` | Name of next concept in learning path |
| `YYYY-MM-DD` | Today's date |
| `N / 3` | Actual experiment count |

---

## What Cursor Must NOT Do

- Do not close a concept with incomplete experiments
- Do not generate the summary without reading all linked analysis.md files first
- Do not skip updating `AI_RESEARCH_INDEX.md`
- Do not activate the next concept if the current one is not fully documented
- Do not add future experiments to the closed concept's experiment slots

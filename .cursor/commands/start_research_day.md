# Command: Start Research Day

Use this command to open each research session with a structured daily log.

**Trigger:** `@start_research_day` or say *"start research day"* or *"begin today's session"*

---

## What This Command Does

When triggered, Cursor will:

1. **Ask** the user for:
   - Today's research topic (e.g. `embeddings`, `rag_evaluation`, `attention_mechanisms`)
   - Optional: specific experiment to work on today (e.g. `EXP-05`)

2. **Create** a daily log file at:
   ```
   research/daily_logs/YYYY-MM-DD_<topic>.md
   ```
   Using today's actual date (not a placeholder).

3. **Generate** the log with all required sections pre-filled where possible:
   - Pull today's date automatically
   - Pre-link the relevant experiment from `EXPERIMENT_REGISTRY.md`
   - Pre-link the relevant concept note from `research/concepts/`
   - Suggest which experiment folder to work in based on the topic

4. **Confirm** the file path and show the next suggested action.

---

## Daily Log Template (Generated)

```markdown
---
title: "Research Log — YYYY-MM-DD — <Topic>"
tags: [daily-log, research, <topic-tag>, YYYY-MM]
aliases: [log-YYYY-MM-DD, <topic>-log]
---

# Research Log — YYYY-MM-DD

**Topic:** <topic>
**Session goal:** <one sentence — what do you want to accomplish today?>
**Related experiment:** [EXP-NN — <title>](../../experiments/EXPERIMENT_REGISTRY.md#exp-NN)
**Concept reference:** [research/concepts/<topic>.md](../concepts/<topic>.md)

---

## Objective

> What specific question or task are you addressing in this session?
> Write this before doing anything else.

**Today I want to:**
1.
2.
3.

**Session is successful if:**
-

---

## Resources Studied

> Log everything you read, watched, or referenced today.

| Resource | Type | Key takeaway |
|---|---|---|
| | Paper / Docs / Video / Blog | |
| | Paper / Docs / Video / Blog | |

**Reading notes:**

*(paste key quotes, formulas, or observations here)*

---

## Experiments Planned

> What experiments are you running or preparing today?

| Action | Experiment | Status |
|---|---|---|
| *(run / design / analyse)* | [EXP-NN](../../experiments/EXPERIMENT_REGISTRY.md) | 📋 / 🔄 / ✅ |

**Blockers:**
-

**Decisions made today:**
-

---

## Insights

> New understanding developed during this session.
> Be specific — cite sources or experiment results.

1. **<Insight title>:** <one sentence>. *(Source: ...)*
2. **<Insight title>:** <one sentence>. *(Source: ...)*
3. **<Insight title>:** <one sentence>. *(Source: ...)*

**Mental model update:**
> *(Did anything change how you think about a concept? Describe it.)*

---

## Open Questions

> Questions this session raised that you haven't answered yet.
> These become the seeds for future experiments or research sessions.

1. *What happens if ...?*
2. *Why does ...?*
3. *How would you test ...?*

**Highest priority question for next session:**
> *(This should connect to the "Next Research Question" in the current experiment.)*

---

## Session Wrap-up

**Completed today:**
- [ ]
- [ ]

**Commit made:** `<paste git commit hash or message>`

**Next session topic:** <topic>
**Next session goal:** <one sentence>
**Suggested experiment folder:** `experiments/<category>/<topic>/`
```

---

## File Naming Convention

```
research/daily_logs/YYYY-MM-DD_<topic>.md
```

**Examples:**
```
research/daily_logs/2026-03-02_temperature_experiment.md
research/daily_logs/2026-03-03_embeddings_cosine_similarity.md
research/daily_logs/2026-03-04_rag_chunking_strategy.md
research/daily_logs/2026-03-05_attention_flashattention.md
```

---

## Weekly Review (Optional Extension)

At the end of each week, say: *"create weekly research review"*

Cursor will scan the week's daily logs and generate:

```
research/daily_logs/YYYY-WNN_weekly_review.md
```

With sections:
- Experiments completed this week
- Key insights (aggregated from daily logs)
- Open questions (unresolved from daily logs)
- Plan for next week

---

## Usage Examples

```
@start_research_day
> What is today's topic? embeddings
> Any specific experiment? EXP-05

@start_research_day attention mechanisms
@start_research_day rag evaluation
@start_research_day agent reliability
```

---

## Suggested Morning Workflow

```
1. @start_research_day                  ← open the session
2. Read the concept note for today's topic
3. Open the experiment folder
4. Run any existing code.py to see current results
5. Write / update experiment.md
6. Code, run, document
7. Update daily log with insights and open questions
8. git commit with structured message
9. Update EXPERIMENT_REGISTRY.md status
```

---

*Daily logs are stored in `research/daily_logs/` and are tracked in git.*
*All logs follow YAML frontmatter standards from `.cursor/rules/ai_lab_rules.mdc`.*

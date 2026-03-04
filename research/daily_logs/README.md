---
title: "Research — Daily Logs"
tags: [research, daily-logs, journal, workflow]
aliases: [daily-logs, research-journal]
---

# Research Daily Logs

Session-by-session research journal. One file per working day.

---

## Purpose

Daily logs serve three functions:

1. **Accountability** — forces a session goal before starting work
2. **Insight capture** — prevents losing observations that don't fit anywhere else
3. **Continuity** — each session's open questions seed the next session's objective

---

## File Naming

```
YYYY-MM-DD_<topic>.md
```

**Examples:**
```
2026-03-02_temperature_experiment.md
2026-03-03_embeddings_cosine_similarity.md
2026-03-04_rag_chunking_strategy.md
```

---

## Creating a Log

Use the Cursor command:

```
@start_research_day
```

Cursor will ask for today's topic and generate the full log with all sections pre-filled.

Or copy [`research/concept_template.md`](../concept_template.md) and adapt it manually.

---

## Log Structure

Every log contains:

| Section | Purpose |
|---|---|
| **Objective** | Goal for the session — written before starting |
| **Resources Studied** | Everything read/watched with key takeaways |
| **Experiments Planned** | What is being run or designed today |
| **Insights** | New understanding, cited to sources or results |
| **Open Questions** | Unanswered questions — seeds for future sessions |
| **Session Wrap-up** | Completed items, commit hash, next session plan |

---

## Weekly Reviews

Every Friday (or end of week), create a weekly review:

```
YYYY-WNN_weekly_review.md
```

This aggregates insights and open questions from the week's daily logs.

---

*All daily logs follow YAML frontmatter standards from `.cursor/rules/ai_lab_rules.mdc`.*

---
title: "Experiment NN — <Short Title>"
tags: [experiment, <topic-tag>, <domain-tag>, <method-tag>]
aliases: [<topic>-experiment, exp-NN]
---

# Experiment NN — \<Short Title\>

**Phase:** \<Phase name from AI_Expert_Path.md\>
**Status:** 📋 Planned

> One-sentence summary of what this experiment investigates and why it matters.

---

## Experiment ID

| Field | Value |
|---|---|
| **ID** | EXP-NN |
| **Phase** | *(e.g. LLM Behavior & Prompt Control)* |
| **Model** | *(e.g. gpt-4o-mini)* |
| **Libraries** | *(e.g. openai, numpy — no ML framework)* |
| **Estimated cost** | *(e.g. < $0.01)* |
| **Estimated runtime** | *(e.g. ~3 minutes)* |

---

## Hypothesis

> State a clear, falsifiable hypothesis. What do you predict will happen and why?

*Template:* "If [variable] is changed in [way], then [outcome] will occur because [mechanism]."

---

## Setup

### Variables

| Variable | Type | Values |
|---|---|---|
| Independent | The thing being changed | *(e.g. temperature: 0.0, 0.3, 0.7, 1.0)* |
| Controlled | Held constant | *(e.g. model, prompt, seed)* |
| Measured | The output being observed | *(e.g. output text, token count, finish_reason)* |

### Prompts / Inputs

```
System: <system prompt used>

User: <user message used>
```

### Success Criteria

- [ ] Hypothesis confirmed or clearly refuted
- [ ] All runs complete without API errors
- [ ] Results written to `results.md`
- [ ] Key insight documented in one sentence

---

## Code

**Run command:**

```bash
python experiments/<folder>/code.py
```

**Expected outputs:**
- Console report with formatted results
- `results.md` auto-generated in this folder
- `analysis.md` updated with observations

**Key functions / classes:**
- `run_experiment()` — orchestrates all API calls
- `print_report()` — console output
- `write_markdown()` — auto-generates `results.md`

---

## Results

> This section is auto-populated when `code.py` is run.
> Replace this block with a summary after running the experiment.

**Run date:** YYYY-MM-DD
**Total API calls:** N
**Total tokens used:** N (prompt: N, completion: N)
**Estimated cost:** $X.XXXXX
**Truncated responses:** N/N

### Summary Table

| Variable | Metric 1 | Metric 2 | Observation |
|---|---|---|---|
| value_1 | — | — | *(fill after running)* |
| value_2 | — | — | *(fill after running)* |

### Unexpected Findings

- *(Document anything that surprised you)*

---

## Analysis

> Write this section after reviewing the results. Be evidence-based — cite specific numbers from results.md.

### What the results show

*(2–3 paragraphs)*

### What was confirmed

- Hypothesis [confirmed / partially confirmed / refuted] because ...

### What was surprising

- ...

### Comparison to prior experiments

| This experiment | Prior experiment | Relationship |
|---|---|---|
| *(finding)* | *(EXP-NN finding)* | *(how they connect)* |

---

## Insights

> Distil the experiment into discrete, reusable insights. Each insight should be a single falsifiable claim.

1. **[Insight title]:** One-sentence statement. *(Evidence: cite specific numbers.)*
2. **[Insight title]:** One-sentence statement.
3. **[Insight title]:** One-sentence statement.

---

## Next Research Question

> The most important unanswered question raised by this experiment. This becomes the hypothesis for the next experiment.

**Question:** *What happens if...?*

**Why it matters:** *Practical implication if answered...*

**Suggested next experiment:** EXP-NN+1 — `<folder name>`

---

## Related Work

| Resource | Type | Relevance |
|---|---|---|
| [Experiment NN](../path/experiment.md) | Prior experiment | *(how it connects)* |
| [Concept: Topic](../../research/concepts/topic.md) | Concept note | *(theoretical foundation)* |
| [Paper title](../../research/papers/) | Research paper | *(relevant finding)* |

---

*Add this experiment to [EXPERIMENT_REGISTRY.md](../EXPERIMENT_REGISTRY.md) before starting.*

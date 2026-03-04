---
title: "Command — Generate Research Questions"
tags: [command, research, questions, experiments, automation]
aliases: [generate-research-questions, research-questions-command]
---

# Command: Generate Research Questions

Scan completed experiments, extract unresolved insights, and append new research questions to the open questions backlog.

**Trigger:** `@generate_research_questions` or say *"generate research questions from experiments"*

---

## What This Command Does

When triggered, Cursor will:

1. **Read** every completed experiment's files from `experiments/`:
   - `*/experiment.md` — hypothesis and key questions
   - `*/analysis.md` — scientific conclusions and limitations
   - `*/results.md` — raw data, unexpected findings, finish_reason signals

2. **Read** the current question backlogs:
   - `research/questions/open_questions.md` — avoid duplicating existing RQ-IDs
   - `research/questions/answered_questions.md` — avoid re-raising answered questions

3. **Identify** gaps by looking for:
   - "Next Research Question" sections in `experiment.md` files
   - Limitations tables in `analysis.md` files
   - Unexpected findings in `results.md` files
   - Hypotheses that were partially confirmed (not fully confirmed or refuted)
   - Cross-experiment tensions (finding in EXP-A contradicts or complicates EXP-B)

4. **Generate** 3–5 new research questions, each with full detail.

5. **Determine** the next available RQ-ID by reading the highest existing ID in `open_questions.md`.

6. **Append** the new questions to `research/questions/open_questions.md`:
   - Add rows to the summary table
   - Append full detail entries at the bottom of the file

7. **Confirm** how many questions were added and list their IDs and titles.

---

## Question Generation Criteria

Cursor must only generate questions that meet **all** of these criteria:

| Criterion | Requirement |
|---|---|
| **Grounded** | Must trace directly to a finding, limitation, or anomaly in an existing experiment or analysis file |
| **Specific** | Must be answerable by a concrete experiment — not a vague philosophical question |
| **Novel** | Must not already appear in `open_questions.md` or `answered_questions.md` |
| **Actionable** | Must have a plausible proposed experiment that fits the repo structure |
| **Scoped** | Must be answerable within a single experiment — not a multi-year research programme |

Questions that are too broad, already answered, or untestable in this repo will be discarded.

---

## Output Format

Each generated question is appended in two places:

### 1. Summary table row (appended to the table in `open_questions.md`)

```markdown
| [RQ-NN](#rq-NN--<slug>) | <one-sentence question> | <topic> | [EXP-NN](<path>/experiment.md) | <priority> | 🔴 Open |
```

### 2. Full detail entry (appended after the last existing detail entry)

```markdown
---

### RQ-NN — <Short Title>

**Question:** <precise, falsifiable question>

**Raised by:** [EXP-NN — <title>](<path>/experiment.md)
**Finding that raised it:** <specific finding — cite numbers where possible>

**Why it matters:**
<Engineering implication — what production decision does the answer affect?>
<Scientific implication — what does the answer reveal about LLMs/transformers/RAG?>

**Hypothesis:** <falsifiable prediction in "If X then Y because Z" form>

**Proposed experiment:** EXP-NN — `experiments/<category>/<topic>/`
**Method outline:**
1. <step>
2. <step>
3. <step>

**Variables:**
| Type | Variable | Values |
|---|---|---|
| Independent | | |
| Controlled | | |
| Measured | | |

**Concept reference:** [`research/concepts/<topic>.md`](../concepts/<topic>.md)

**Priority:** <🔥 Critical · ⬆ High · ➡ Medium · ⬇ Low> | **Status:** 🔴 Open
```

---

## Priority Assignment Rules

Cursor must assign priority using these rules — not arbitrarily:

| Assign | When |
|---|---|
| 🔥 Critical | Answer affects production safety, security, or correctness |
| ⬆ High | Answer directly unblocks a planned experiment or project |
| ➡ Medium | Answer improves understanding but has no immediate dependency |
| ⬇ Low | Speculative, very long horizon, or requires external resources |

---

## Source Scanning Logic

Cursor reads these specific signals when scanning experiments:

### From `experiment.md`
```
## Next Research Question     ← highest priority source
## Key Questions              ← secondary source
```

### From `analysis.md`
```
## Limitations                ← each limitation row → potential question
## Conclusions                ← each conclusion → "what if" question
## What was surprising        ← unexpected findings → new hypotheses
```

### From `results.md`
```
Determinism checks            ← DIFFERS result → reproducibility questions
finish_reason = "length"      ← truncation patterns → budget questions
Unexpected Findings           ← anomalies → new hypotheses
```

### Cross-experiment tensions
```
EXP-01: T=0 is non-deterministic
EXP-12 (planned): agents need reliable tool calls at T=0
→ tension: what is the actual failure rate of T=0 tool calls?
```

---

## Example Run

**Input:** User types `@generate_research_questions`

**Cursor reads:**
- `experiments/llm_behavior/temperature/analysis.md` → finds "T=0 non-determinism with seed untested"
- `experiments/llm_behavior/token_limit/results.md` → finds code never completes at 600 tokens
- `experiments/llm_behavior/attention/analysis.md` → finds "FlashAttention not implemented"
- Cross-references with `open_questions.md` → RQ-01 through RQ-08 exist

**Cursor generates:**

```
RQ-09: What is the minimum max_tokens required for complete code generation
       across function, class, and module levels?
       → Raised by: EXP-03 truncation at 600 tokens
       → Proposed: EXP-03b — token budget calibration by code complexity

RQ-10: Does adding seed= to T=0 API calls produce statistically identical
       outputs (>99% token-level match) across 100 repeated calls?
       → Raised by: EXP-01 T=0 non-determinism + RQ-01 still open
       → Proposed: EXP-01b — seed reproducibility stress test

RQ-11: Does multi-head attention produce qualitatively different relationship
       patterns per head on real language (not random embeddings)?
       → Raised by: EXP-04 used random embeddings only
       → Proposed: EXP-04b — attention head visualisation on real tokens
```

**Cursor appends** RQ-09, RQ-10, RQ-11 to `open_questions.md` with full detail.

**Cursor confirms:**
```
Added 3 research questions: RQ-09, RQ-10, RQ-11
Appended to: research/questions/open_questions.md
Next available ID: RQ-12
```

---

## Usage

```
@generate_research_questions
```

No arguments needed — Cursor reads all experiments automatically.

**Optional focus:**
```
@generate_research_questions from temperature experiments
@generate_research_questions from rag experiments
@generate_research_questions from attention
```

Cursor will restrict scanning to the specified category.

---

## After Running This Command

1. Review the generated questions — edit any that need refinement
2. Promote the highest-priority question to `🟡 In Progress` by running `@create_experiment`
3. Commit the updated `open_questions.md`:
   ```
   research: add RQ-NN to RQ-NN from <category> experiment scan
   ```

---

*Questions generated by this command follow [`research/questions/question_template.md`](../../research/questions/question_template.md)*
*All appended questions are grounded in experiment data — not hypothetical.*

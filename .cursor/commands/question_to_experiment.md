---
title: "Command — Question to Experiment"
tags: [command, research, questions, experiments, automation, workflow]
aliases: [question-to-experiment, rq-to-experiment]
---

# Command: Question to Experiment

Convert an open research question directly into a fully scaffolded, registry-registered experiment.

**Trigger:** `@question_to_experiment` or say *"convert question RQ-NN to experiment"*

---

## What This Command Does

When triggered, Cursor will:

1. **Ask** the user for the Question ID (e.g. `RQ-03`)
2. **Read** the full question detail from `research/questions/open_questions.md`
3. **Determine** the correct experiment category folder based on the question's topic
4. **Assign** the next available experiment ID from `experiments/EXPERIMENT_REGISTRY.md`
5. **Create** the experiment folder at `experiments/<category>/<topic>/`
6. **Generate** all four required experiment files
7. **Register** the experiment in `EXPERIMENT_REGISTRY.md` and `EXPERIMENT_DASHBOARD.md`
8. **Update** `research/questions/open_questions.md` — mark question status as `🟡 In Progress`
9. **Confirm** every file path created and show the run command

---

## Step-by-Step Execution

### Step 1 — Read the question

Cursor reads the detail entry for the given RQ-ID from `open_questions.md`.

It extracts:
- `Question` — becomes the experiment hypothesis
- `Motivation` — becomes the Background section
- `Hypothesis` — pre-fills the Hypothesis section of `experiment.md`
- `Proposed Experiment` — determines the folder name, category, and method steps
- `Variables` table — pre-fills the Setup section
- `Concept reference` — linked in Background

If the question ID does not exist or is already `🟢 Answered`, Cursor stops and reports the issue.

---

### Step 2 — Determine category and folder

Cursor maps the question's topic to the correct category folder:

| Question topic | Experiment folder |
|---|---|
| Temperature, system prompt, token limit, determinism | `experiments/llm_behavior/<topic>/` |
| Embeddings, cosine similarity | `experiments/embeddings/<topic>/` |
| RAG, chunking, retrieval, faithfulness | `experiments/rag/<topic>/` |
| Agents, tool use, multi-agent | `experiments/agents/<topic>/` |
| Evaluation, LLM-as-judge, prompt injection | `experiments/evaluation/<topic>/` |

If the topic is ambiguous, Cursor asks: *"Which category does this experiment belong to?"*

---

### Step 3 — Generate experiment files

All four files are created in order: `experiment.md` → `code.py` → `results.md` → `analysis.md`

#### `experiment.md` (populated from `experiment_template.md` + question content)

```markdown
---
title: "Experiment NN — <Topic derived from RQ title>"
tags: [experiment, <topic-tag>, <category-tag>]
aliases: [<topic>-experiment, exp-NN]
---

# Experiment NN — <Topic>

**ID:** EXP-NN
**Phase:** <category>
**Status:** 🔄 In Progress
**Model:** gpt-4o-mini
**Source question:** [RQ-NN](../../research/questions/open_questions.md#rq-NN)

---

## Hypothesis

> <copied directly from RQ hypothesis field>

**Prediction:** <from RQ>
**Because:** <from RQ motivation>

---

## Background

> <from RQ motivation — engineering + scientific implication>

**Source question:** [RQ-NN — <title>](../../research/questions/open_questions.md#rq-NN)
**Concept reference:** [research/concepts/<topic>.md](../../research/concepts/<topic>.md)
**Prior experiments this builds on:** <from RQ "Raised by" field>

---

## Setup

### Variables

| Type | Variable | Values |
|---|---|---|
| Independent | <from RQ variables table> | |
| Controlled | <from RQ variables table> | |
| Measured | <from RQ variables table> | |

### Success Criteria

- [ ] Hypothesis confirmed or refuted with cited evidence
- [ ] All runs complete without error
- [ ] results.md auto-generated
- [ ] Key insight in one sentence
- [ ] open_questions.md updated to 🟢 Answered

---

## Code

**Run:**
\`\`\`bash
python experiments/<category>/<topic>/code.py
\`\`\`

---

## Results

> Auto-populated when code.py is run.

---

## Analysis

> Write after results.md is generated.

---

## Key Insight

> Fill after analysis.

---

## Next Research Question

> Fill after completing analysis.
```

#### `code.py` (standard boilerplate scaffold)

```python
"""
Experiment NN — <Topic>
========================
Source question: RQ-NN — <question text>
<one-line purpose>

Usage:
    python experiments/<category>/<topic>/code.py

Outputs:
    - Console report
    - results.md (auto-generated)
"""

from __future__ import annotations

import time
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

MODEL = "gpt-4o-mini"

# ── Constants ──────────────────────────────────────────────────────────────────
# Define experimental variables here — derived from RQ variables table


# ── Core call ──────────────────────────────────────────────────────────────────
def call_model(system: str, user: str, **kwargs) -> tuple[str, int, int, float]:
    start = time.perf_counter()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
        **kwargs,
    )
    elapsed_ms = (time.perf_counter() - start) * 1000
    content = response.choices[0].message.content or ""
    usage = response.usage
    return content, usage.prompt_tokens, usage.completion_tokens, elapsed_ms


# ── Experiment runner ──────────────────────────────────────────────────────────
def run_experiment():
    """Execute all experimental conditions."""
    pass  # implement based on RQ method steps


# ── Console report ─────────────────────────────────────────────────────────────
def print_report(results) -> None:
    """Formatted console output."""
    pass  # implement


# ── Markdown writer ────────────────────────────────────────────────────────────
def write_markdown(results, out_path: Path) -> None:
    """Write results.md — auto-called on every run."""
    lines: list[str] = []
    out_path.write_text("".join(lines), encoding="utf-8")
    print(f"\n  Results written → {out_path}")


# ── Entry point ────────────────────────────────────────────────────────────────
def main() -> None:
    print(f"\n{'=' * 72}")
    print(f"  Experiment NN — <Topic>")
    print(f"  Source: RQ-NN — <question>")
    print(f"{'=' * 72}\n")

    results = run_experiment()
    print_report(results)
    write_markdown(results, Path(__file__).parent / "results.md")


if __name__ == "__main__":
    main()
```

#### `results.md` (stub with frontmatter)

```markdown
---
title: "Experiment NN — <Topic> Results"
tags: [experiment, <topic>, results]
aliases: [<topic>-results, exp-NN-results]
---

# Experiment NN — <Topic>: Results

> Auto-generated by code.py. Do not edit manually.

**Run date:** —
**Total API calls:** —
**Total tokens:** —
**Estimated cost:** $—
```

#### `analysis.md` (stub with all section headers)

```markdown
---
title: "Experiment NN — <Topic> Analysis"
tags: [experiment, <topic>, analysis]
aliases: [<topic>-analysis, exp-NN-analysis]
---

# Experiment NN — <Topic>: Analysis

**Source question:** [RQ-NN](../../research/questions/open_questions.md#rq-NN)

> Write after results.md is generated. Cite specific numbers.

## What the Data Shows

## Hypothesis Verdict

- [ ] Confirmed
- [ ] Partially confirmed
- [ ] Refuted

**Because:** <cite evidence>

## Comparison to Prior Experiments

| Finding here | Prior experiment | Relationship |
|---|---|---|
| | | |

## Key Insights

1.
2.
3.

## Next Research Question

**Question:**
**Suggested next experiment:** EXP-NN+1
```

---

### Step 4 — Register the experiment

**Appended to `EXPERIMENT_REGISTRY.md` table:**

```markdown
| EXP-NN | <topic> | `experiments/<category>/<topic>/` | <hypothesis from RQ> | 🔄 In Progress | — | — |
```

**Added to `EXPERIMENT_DASHBOARD.md`** under the correct section:

```markdown
### EXP-NN — <Topic> `🔄 In Progress`

**Investigates:** <from RQ question + motivation>
**Source question:** [RQ-NN](../research/questions/open_questions.md#rq-NN)

| Document | Link |
|---|---|
| Hypothesis & Setup | [experiment.md](experiments/<category>/<topic>/experiment.md) |
| Live Results | [results.md](experiments/<category>/<topic>/results.md) |
| Scientific Analysis | [analysis.md](experiments/<category>/<topic>/analysis.md) |
| Run | `python experiments/<category>/<topic>/code.py` |
```

---

### Step 5 — Update open_questions.md

Cursor makes two targeted edits to `research/questions/open_questions.md`:

**1. Update the summary table row** — change status column:
```markdown
| 🔴 Open |   →   | 🟡 In Progress |
```

**2. Update the detail entry** — add experiment link:
```markdown
**Will be answered by:**
- [EXP-NN — <title>](../../experiments/<category>/<topic>/experiment.md) 🔄 In Progress
```

---

## Confirmation Output

After completing all steps, Cursor prints:

```
✅ Question RQ-NN converted to experiment EXP-NN

Files created:
  experiments/<category>/<topic>/experiment.md
  experiments/<category>/<topic>/code.py
  experiments/<category>/<topic>/results.md
  experiments/<category>/<topic>/analysis.md

Registered in:
  experiments/EXPERIMENT_REGISTRY.md    (status: 🔄 In Progress)
  experiments/EXPERIMENT_DASHBOARD.md   (added to <Category> section)

Question updated:
  research/questions/open_questions.md  (RQ-NN → 🟡 In Progress)

Next step:
  1. Open experiments/<category>/<topic>/experiment.md
  2. Complete the Setup and Key Questions sections
  3. Implement run_experiment() in code.py
  4. Run: python experiments/<category>/<topic>/code.py
```

---

## Usage Examples

```
@question_to_experiment RQ-01
@question_to_experiment RQ-04
@question_to_experiment RQ-07
```

Or in natural language:
```
Convert RQ-03 into an experiment
Turn the FlashAttention question into an experiment
Make RQ-08 into an experiment
```

---

## Full Lifecycle This Command Enables

```
research/questions/open_questions.md
         ↓  @question_to_experiment RQ-NN
experiments/<category>/<topic>/
         ↓  implement code.py, run experiment
results.md auto-generated
         ↓  write analysis.md
research/questions/open_questions.md  → 🟡 In Progress
         ↓  experiment complete
research/questions/answered_questions.md  → 🟢 Answered
         ↓  @generate_research_questions
research/questions/open_questions.md  → new RQ-NN+1 appended
```

Every question becomes an experiment. Every experiment answers a question and raises new ones.

---

## Related Commands

| Command | When to use |
|---|---|
| [`@create_experiment`](create_experiment.md) | Start an experiment without a prior question |
| [`@generate_research_questions`](generate_research_questions.md) | Generate new questions from completed experiments |
| [`@start_research_day`](start_research_day.md) | Open a session, choose today's question to work on |

---

*All generated files follow `.cursor/rules/ai_lab_rules.mdc` standards.*
*Template source: [`experiments/experiment_template.md`](../../experiments/experiment_template.md)*
*Question source: [`research/questions/open_questions.md`](../../research/questions/open_questions.md)*

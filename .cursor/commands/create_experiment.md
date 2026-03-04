# Command: Create Experiment

Use this command to scaffold a complete, registry-registered experiment from scratch.

**Trigger:** `@create_experiment` or say *"create experiment [topic]"*

---

## What This Command Does

When triggered, Cursor will:

1. **Ask** the user for:
   - Experiment topic / short name (e.g. `embeddings`, `few_shot`, `rag_chunk_size`)
   - Experiment category folder (choose from: `llm_behavior` · `embeddings` · `rag` · `agents` · `evaluation`)
   - Next available experiment ID (check `EXPERIMENT_REGISTRY.md` for the current highest EXP-NN)
   - Model to use (default: `gpt-4o-mini`)
   - Estimated cost (optional)

2. **Create** the experiment folder:
   ```
   experiments/<category>/<topic>/
   ```

3. **Generate all four required files** in this exact order:

   | File | Generated from | Contents |
   |---|---|---|
   | `experiment.md` | `experiment_template.md` | Filled with the provided topic, ID, hypothesis scaffold |
   | `code.py` | Standard scaffold below | Boilerplate with all required functions |
   | `results.md` | Stub | Placeholder — will be overwritten by `code.py` |
   | `analysis.md` | Stub | Section headers ready to fill |

4. **Register** the experiment in `experiments/EXPERIMENT_REGISTRY.md`:
   ```markdown
   | EXP-NN | <Topic> | `experiments/<category>/<topic>/` | <hypothesis> | 📋 Planned | — | — |
   ```

5. **Add an entry** to `experiments/EXPERIMENT_DASHBOARD.md` under the correct section with status `📋 Planned`.

6. **Confirm** all files were created and show the run command.

---

## Experiment Folder Structure (Generated)

```
experiments/<category>/<topic>/
├── experiment.md    ← hypothesis, variables, method — fill before coding
├── code.py          ← runnable script — write after experiment.md is done
├── results.md       ← stub — auto-overwritten by code.py on each run
└── analysis.md      ← stub — fill after reviewing results.md
```

---

## Code Scaffold (Generated `code.py`)

```python
"""
Experiment NN — <Topic Title>
==============================
<one-line purpose>

Usage:
    python experiments/<category>/<topic>/code.py

Outputs:
    - Console report
    - results.md (auto-generated in this folder)
"""

from __future__ import annotations

import os
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

MODEL = "gpt-4o-mini"
# ── Constants ──────────────────────────────────────────────────────────────────
# Define your experimental variables here


# ── Data model ─────────────────────────────────────────────────────────────────
# Add dataclasses for Run and Results here


# ── Core API call ──────────────────────────────────────────────────────────────
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
    """Execute all experimental conditions and collect results."""
    pass  # implement


# ── Console report ─────────────────────────────────────────────────────────────
def print_report(results) -> None:
    """Print formatted results to console."""
    pass  # implement


# ── Markdown writer ────────────────────────────────────────────────────────────
def write_markdown(results, out_path: Path) -> None:
    """Write results to results.md — called automatically on every run."""
    lines: list[str] = []
    # build markdown content
    out_path.write_text("".join(lines), encoding="utf-8")
    print(f"\n  Results written → {out_path}")


# ── Entry point ────────────────────────────────────────────────────────────────
def main() -> None:
    print(f"\n{'=' * 72}")
    print(f"  Experiment NN — <Topic>")
    print(f"{'=' * 72}\n")

    results = run_experiment()
    print_report(results)

    out = Path(__file__).parent / "results.md"
    write_markdown(results, out)


if __name__ == "__main__":
    main()
```

---

## `experiment.md` Stub (Generated)

```markdown
---
title: "Experiment NN — <Topic>"
tags: [experiment, <topic>, <category>]
aliases: [<topic>-experiment, exp-NN]
---

# Experiment NN — <Topic>

**ID:** EXP-NN
**Phase:** <category>
**Status:** 📋 Planned
**Model:** gpt-4o-mini

## Hypothesis

> Fill in before writing code.

## Background

> Link to relevant concept note and prior experiment.

## Setup

### Variables
| Type | Variable | Values |
|---|---|---|
| Independent | | |
| Controlled | | |
| Measured | | |

## Key Questions
-

## Run
\`\`\`bash
python experiments/<category>/<topic>/code.py
\`\`\`

## Outputs
- results.md (auto-generated)
- analysis.md (written manually after results)
```

---

## `analysis.md` Stub (Generated)

```markdown
---
title: "Experiment NN — <Topic> Analysis"
tags: [experiment, <topic>, analysis]
aliases: [<topic>-analysis, exp-NN-analysis]
---

# Experiment NN — <Topic>: Analysis

> Write this after results.md is generated. Cite specific numbers.

## What the Data Shows

## Hypothesis Verdict

- [ ] Confirmed
- [ ] Partially confirmed
- [ ] Refuted

## Key Insights

1.
2.
3.

## Next Research Question

**Question:**
**Suggested next experiment:** EXP-NN+1
```

---

## Registry Entry (Added to EXPERIMENT_REGISTRY.md)

```markdown
| EXP-NN | <Topic> | `experiments/<category>/<topic>/` | <hypothesis> | 📋 Planned | — | — |
```

---

## Usage Examples

```
@create_experiment embeddings
@create_experiment rag_chunk_size
@create_experiment few_shot_prompting
@create_experiment agent_tool_use
```

Cursor will ask for the category and ID, then scaffold everything.

---

*All generated files follow `.cursor/rules/ai_lab_rules.mdc` standards.*
*Template source: [`experiments/experiment_template.md`](../../experiments/experiment_template.md)*

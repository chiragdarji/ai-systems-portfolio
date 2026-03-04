---
title: "Cursor Command — add_concept"
tags: [command, cursor, concepts, knowledge-base, research]
aliases: [add-concept-command, new-concept]
---

# Command: `@add_concept`

Adds a new AI concept to the research knowledge base at `research/concepts/`.
Creates a fully populated concept note and registers it in `AI_RESEARCH_INDEX.md`.

**Trigger:** `@add_concept`
**Example use cases:**
- `@add_concept` → "seed determinism"
- `@add_concept` → "online softmax"
- `@add_concept` → "cosine similarity"

---

## When to Run This Command

Run `@add_concept` when:
- You encounter a concept that needs a reference note before starting an experiment
- An experiment produced a finding that introduces a new concept worth capturing
- You're studying a paper or resource and want to record the key idea permanently
- A research question requires a concept that doesn't yet have a note in `research/concepts/`

Do NOT run `@add_concept` to close a concept chapter — use `@finalize_concept` for that.
Do NOT confuse concept notes with concept summaries:
- **Concept note** (`@add_concept`) = reference you write *before or during* experiments
- **Concept summary** (`@finalize_concept`) = synthesis you write *after* all experiments complete

---

## Step-by-Step Execution

### Step 1: Ask the user three questions

```
1. Concept name?
   (e.g. "Seed Determinism", "Online Softmax", "Cosine Similarity")

2. Related experiments? (optional — press Enter to skip)
   (e.g. EXP-04, EXP-05)

3. Key insight in one sentence? (optional — press Enter to skip)
   (e.g. "seed has no effect at T=0 because there is nothing random to seed")
```

Accept partial answers. All three fields can be filled in later.

### Step 2: Derive the filename

Convert the concept name to `snake_case`:

| User input | Filename |
|-----------|---------|
| `Seed Determinism` | `seed_determinism.md` |
| `Online Softmax` | `online_softmax.md` |
| `Cosine Similarity` | `cosine_similarity.md` |
| `FlashAttention` | `flash_attention.md` |
| `RAG Chunk Size` | `rag_chunk_size.md` |

Rules for conversion:
- Lowercase all characters
- Replace spaces and hyphens with underscores
- Remove special characters (parentheses, slashes, etc.)
- Abbreviations stay together: `RAG` → `rag`, `LLM` → `llm`

### Step 3: Check for duplicates

Before creating the file:
1. Check if `research/concepts/<snake_case_name>.md` already exists
2. Scan `AI_RESEARCH_INDEX.md` → `## Concepts Knowledge Base` for a matching entry
3. If a duplicate is found → stop and report: "Concept `<name>` already exists at `research/concepts/<file>.md`. Open that file to edit it."

### Step 4: Create the concept note

Create `research/concepts/<snake_case_name>.md` using the template below.
Replace all `<placeholder>` values. Leave section bodies as instructive stubs where the user has not provided content — never leave a section completely empty.

```markdown
---
title: "Concept — <Concept Name>"
tags: [research, concepts, <kebab-case-name>, <related-tag-1>, <related-tag-2>]
aliases: [<kebab-case-name>, <alternative-name>]
---

# Concept: <Concept Name>

> <One-line framing question this concept answers.>

**Added:** YYYY-MM-DD
**Related experiments:** <EXP-NN links or "None yet">
**Concept chapter:** <Learning path chapter this belongs to, from AI_RESEARCH_INDEX.md>

---

## Definition

<Brief, precise explanation of what this concept is. 2–4 sentences.
Define the term as you would in a technical glossary — no fluff, no analogies yet.>

---

## Why It Matters

<Why does an AI systems engineer need to understand this concept?
What goes wrong in production if this is misunderstood?
Connect to a real engineering decision where possible.>

---

## How It Works

<Technical explanation. Use sub-sections, numbered steps, or pseudocode as appropriate.
Prefer concrete over abstract — if there is a formula, write it. If there is an algorithm, outline it.>

---

## Practical Observations

<Insights from experiments or real-world usage that are specific to this concept.
If no experiments have run yet, write: "No experiments run yet — see proposed experiment below."
If an experiment has run, cite it: "EXP-NN showed that...">

---

## Limitations

<Where does this concept break down? What are the edge cases?
What does this concept NOT explain or NOT solve?>

---

## Related Experiments

<List links to experiments that test or demonstrate this concept.
Use the format: [EXP-NN — Topic](../../experiments/<category>/<folder>/experiment.md)
If none yet: "Planned — see Open Questions below.">

---

## Key Insight

> <One falsifiable sentence that captures the most important thing about this concept.
> Must be grounded in evidence or well-established theory.
> Example: "seed has zero effect at T=0 because temperature=0 eliminates random sampling — there is nothing for the RNG to seed.">

---

## Open Questions

<Unanswered research questions about this concept that could become experiments.
Format each as: **RQ-NN** or **(proposed)** if not yet registered in open_questions.md.>

- *(proposed)* <Question 1?>
- *(proposed)* <Question 2?>

---

## References

- <Paper, documentation, or resource that best explains this concept>
- <Link to related concept note in research/concepts/>
```

### Step 5: Register in `AI_RESEARCH_INDEX.md`

Append a new row to the `## Concepts` section table in `AI_RESEARCH_INDEX.md`.
The table header is:

```
| Concept | File | Chapter | Experiments | Status |
```

Add the new row immediately before the blank line that separates the table from the
"Concept summaries" sub-section:

```markdown
| <Concept Name> | [`research/concepts/<file>.md`](research/concepts/<file>.md) | <N or —> | <EXP-NN or *(none yet)*> | 📖 Active |
```

If the user provided related experiments, list them comma-separated in the Experiments column.
If none provided, use `*(none yet)*`.
For Chapter, use the chapter number from the learning path if this concept belongs to one, otherwise `—`.

### Step 6: Confirm and suggest next step

Output a confirmation message:

```
✅ Concept note created: research/concepts/<snake_case_name>.md
✅ Registered in: AI_RESEARCH_INDEX.md → Concepts Knowledge Base

Stub sections to fill in:
  - Definition
  - How It Works
  - Practical Observations (after running experiments)
  - Key Insight

Suggested next step:
  If you want to run an experiment on this concept → @create_experiment
  If this concept raises a research question → @generate_research_questions
```

---

## Naming Conventions

| Concept Type | Example Name | Example File |
|-------------|-------------|-------------|
| Algorithm / mechanism | Online Softmax | `online_softmax.md` |
| Architectural pattern | FlashAttention | `flash_attention.md` |
| API behaviour | Seed Determinism | `seed_determinism.md` |
| Evaluation metric | ROUGE-L | `rouge_l.md` |
| Data pattern | Chunking Strategy | `chunking_strategy.md` |
| Failure mode | Hallucination | `hallucination.md` |

---

## What Cursor Must NOT Do

- Do not create a concept note in any folder other than `research/concepts/`
- Do not skip the YAML frontmatter
- Do not leave a section completely empty — every section must have at least one instructive stub line
- Do not add the concept to the learning-path chapter table in `AI_RESEARCH_INDEX.md` — only to `## Concepts Knowledge Base`
- Do not create a concept summary (`<name>_summary.md`) — that is `@finalize_concept`'s job
- Do not overwrite an existing concept note without asking the user first

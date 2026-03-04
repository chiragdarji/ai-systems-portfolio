---
title: "Concept — <Concept Name>"
tags: [research, concepts, <topic-tag>, <domain-tag>]
aliases: [<concept-name>, <alternative-name>]
---

# \<Concept Name\>

> One-sentence definition. What is this, and why does it exist?

---

## Definition

> Precise, technical definition. Write for an engineer who has not encountered this concept before.
> Avoid analogies in this section — save them for "How It Works".

**Formal definition:**

**In plain terms:**

**Key distinction from related concepts:**
- \<This concept\> vs \<related concept A\>: ...
- \<This concept\> vs \<related concept B\>: ...

---

## How It Works

> Step-by-step mechanistic explanation. Use diagrams, pseudocode, or numbered steps.
> The goal: a reader should be able to implement a minimal version from this section alone.

### Step-by-step

1. ...
2. ...
3. ...

### Diagram / pseudocode

```
<input>
    ↓
[Component A] → does X
    ↓
[Component B] → does Y
    ↓
<output>
```

### Key parameters / hyperparameters

| Parameter | Effect | Typical range |
|---|---|---|
| \<param\> | \<what it controls\> | \<values\> |

---

## Mathematical Intuition

> The core equation(s) driving this concept. Explain every symbol.
> If no math applies, describe the computational structure instead.

$$
\text{<Formula name>} = \text{<formula>}
$$

**Where:**
- \<symbol\> = \<meaning\>
- \<symbol\> = \<meaning\>

**Intuition:** *(what does this equation "do" in plain language?)*

**Edge cases:**
- When \<parameter\> → 0: ...
- When \<parameter\> → ∞: ...

---

## Why It Matters for AI Systems

> The engineering and systems-design implications. Connect to production AI.

### 1. \<Implication title\>

*(explanation)*

### 2. \<Implication title\>

*(explanation)*

### 3. \<Implication title\>

*(explanation)*

### Decision framework

> When should an engineer use this concept / technique?

```
Is <condition A> true?
├── YES → use <this approach> because ...
└── NO  → consider <alternative> because ...
```

---

## Limitations

> Be honest about where this concept breaks down. Good research identifies failure modes.

| Limitation | Root cause | Known mitigation |
|---|---|---|
| \<limitation\> | \<why it happens\> | \<current solution or "open problem"\> |
| \<limitation\> | \<why it happens\> | \<current solution or "open problem"\> |
| \<limitation\> | \<why it happens\> | \<current solution or "open problem"\> |

---

## Related Experiments

> Link to experiments in this repository that demonstrate this concept in practice.

| Experiment | What it tests | Connection to this concept |
|---|---|---|
| [EXP-NN — \<title\>](../experiments/<category>/<topic>/experiment.md) | \<brief description\> | \<how it demonstrates this concept\> |

**Planned experiments:**
- EXP-NN — \<topic\> *(see [`EXPERIMENT_DASHBOARD.md`](../experiments/EXPERIMENT_DASHBOARD.md))*

---

## References

> Primary sources only. Prefer original papers over blog posts.

| Resource | Type | Key contribution |
|---|---|---|
| [\<Title\> — \<Authors\> (\<year\>)](\<url\>) | Paper | \<what it established\> |
| [\<Title\>](\<url\>) | Documentation | \<what it covers\> |
| [\<Title\>](\<url\>) | Tutorial | \<what it explains\> |

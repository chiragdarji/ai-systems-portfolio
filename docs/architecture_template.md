---
title: "Architecture — <Pattern Name>"
tags: [architecture, <pattern-tag>, <domain-tag>, production]
aliases: [<pattern-name>, <short-name>]
---

# Architecture Pattern — \<Pattern Name\>

> One-sentence description of what this pattern does and the problem it solves.

**Pattern type:** \<e.g. RAG pipeline · Agent loop · API gateway · Evaluation framework\>
**Complexity:** \<Low · Medium · High\>
**Maturity:** \<Experimental · Production-proven · Industry standard\>

---

## Problem

> What specific, concrete problem does this architecture solve?
> Describe the pain point before the solution.

**Without this pattern:**
*(what breaks, degrades, or becomes impossible?)*

**With this pattern:**
*(what becomes possible or reliable?)*

**When this pattern is needed:**
- *(condition 1)*
- *(condition 2)*
- *(condition 3)*

---

## System Components

> Every component that makes up this architecture.
> For each: what it does, what it owns, what it must not do.

| Component | Responsibility | Owns | Must NOT |
|---|---|---|---|
| \<Component A\> | \<what it does\> | \<what data/state it controls\> | \<boundary violation\> |
| \<Component B\> | \<what it does\> | \<what data/state it controls\> | \<boundary violation\> |
| \<Component C\> | \<what it does\> | \<what data/state it controls\> | \<boundary violation\> |

### Component detail

#### \<Component A\>

```
Role: <one sentence>
Input: <what it receives>
Output: <what it produces>
Technology options: <e.g. ChromaDB · Pinecone · FAISS>
```

#### \<Component B\>

```
Role: <one sentence>
Input: <what it receives>
Output: <what it produces>
Technology options: <e.g. LangChain · LlamaIndex · custom>
```

---

## Data Flow

> Trace every piece of data from entry point to output.
> Show both the happy path and the error paths.

### Happy path

```
User input
    ↓
[Component A] — does X
    ↓
[Component B] — does Y
    ↓
[Component C] — does Z
    ↓
Output to user
```

### Error paths

```
User input
    ↓
[Component A] — FAILS (reason)
    ↓
Error handler → <fallback behaviour>
```

### Sequence diagram (text)

```
User        →  API Layer     : sends query
API Layer   →  Retriever     : embed + search
Retriever   →  Vector Store  : ANN query
Vector Store → Retriever     : top-k chunks
Retriever   →  Generator     : chunks + query
Generator   →  LLM API       : completion request
LLM API     →  Generator     : response
Generator   →  API Layer     : formatted output
API Layer   →  User          : final answer
```

---

## Scaling Considerations

> How does this architecture behave as load increases?
> Give concrete estimates, not vague statements.

| Scale | Bottleneck | Mitigation |
|---|---|---|
| 100 requests/day | *(component)* | *(action)* |
| 10,000 requests/day | *(component)* | *(action)* |
| 1,000,000 requests/day | *(component)* | *(action)* |

### Cost scaling

| Volume | Estimated cost/month | Dominant cost driver |
|---|---|---|
| 1K requests | $— | \<component\> |
| 100K requests | $— | \<component\> |
| 10M requests | $— | \<component\> |

### What to cache

- \<what\>: cached because \<why\> — TTL: \<duration\>
- \<what\>: cached because \<why\> — TTL: \<duration\>

---

## Failure Modes

> Every realistic way this system can fail.
> For each: how to detect it, how to recover, how to prevent it.

| Failure | Detection signal | Recovery action | Prevention |
|---|---|---|---|
| \<failure\> | \<metric / error / symptom\> | \<what to do\> | \<design change\> |
| \<failure\> | \<metric / error / symptom\> | \<what to do\> | \<design change\> |
| \<failure\> | \<metric / error / symptom\> | \<what to do\> | \<design change\> |

### Cascading failure scenario

> Describe the worst realistic failure chain and how to break it.

*(Component A fails → Component B receives bad input → Component C produces incorrect output → user receives confident wrong answer)*

**Circuit breaker:** *(where to add a hard stop)*

---

## When To Use

> Specific conditions that make this pattern the right choice.

- ✅ \<condition\>
- ✅ \<condition\>
- ✅ \<condition\>

---

## When NOT To Use

> Conditions where this pattern adds cost or complexity without benefit.

- ❌ \<condition\> → use \<simpler alternative\> instead
- ❌ \<condition\> → use \<simpler alternative\> instead
- ❌ \<condition\> → use \<simpler alternative\> instead

---

## Implementation Notes

> Practical engineering decisions for teams building this.

### Key configuration decisions

```python
# Critical parameters to tune per deployment
CHUNK_SIZE = 512          # tokens — tune per domain
TOP_K = 5                 # retrieved chunks — tune per query type
MAX_TOKENS = 300          # response budget — tune per use-case
TEMPERATURE = 0.3         # low for factual, higher for creative
```

### Observability checklist

- [ ] Log `finish_reason` on every LLM call
- [ ] Track retrieval latency separately from generation latency
- [ ] Record top-k chunk scores for retrieval quality monitoring
- [ ] Alert on `finish_reason == "length"` rate > 5%

---

## Related Patterns

| Pattern | Relationship |
|---|---|
| \<Pattern A\> | \<how it compares or combines\> |
| \<Pattern B\> | \<how it compares or combines\> |

## Related Experiments

| Experiment | What it validates |
|---|---|
| [EXP-NN](../experiments/<category>/<topic>/experiment.md) | \<which component or assumption this tests\> |

## References

| Resource | Key insight |
|---|---|
| [\<title\>](\<url\>) | \<what it covers\> |

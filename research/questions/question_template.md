---
title: "Research Question — RQ-NN: <Short Title>"
tags: [research, question, <topic-tag>, <domain-tag>]
aliases: [rq-NN, <topic>-question]
---

# Research Question — RQ-NN

> One sentence capturing the core of this question.

**ID:** RQ-NN
**Status:** `🔴 Open` · `🟡 In Progress` · `🟢 Answered` · `⏸ Deferred`
**Priority:** `🔥 Critical` · `⬆ High` · `➡ Medium` · `⬇ Low`
**Source:** *(experiment, paper, observation, or open curiosity)*
**Raised:** YYYY-MM-DD
**Answered:** *(fill when resolved)*

---

## Question

> State the question precisely and unambiguously.
> A good research question: specific, falsifiable, answerable by experiment.

**Primary question:**

**Sub-questions:**
1.
2.
3.

---

## Motivation

> Why does this question matter? What breaks or remains unknown without the answer?

**Engineering implication:**
*(What production decision does the answer affect?)*

**Scientific implication:**
*(What does the answer reveal about how LLMs / transformers / RAG work?)*

**Current gap:**
*(What is currently assumed or unknown?)*

---

## Related Experiments

> Which completed experiments surface this question?
> Which planned experiments will attempt to answer it?

**Raised by:**
- [EXP-NN — \<title\>](../../experiments/<category>/<topic>/experiment.md) — *\<which finding raised this question\>*

**Will be answered by:**
- [EXP-NN — \<title\>](../../experiments/<category>/<topic>/experiment.md) *(planned)* — *\<how it addresses this question\>*

**Related concept notes:**
- [`research/concepts/<topic>.md`](../concepts/<topic>.md)

---

## Hypothesis

> Before running an experiment, state a falsifiable prediction.

**Prediction:**
*"If [condition], then [outcome] because [mechanism]."*

**Confidence:** `High` · `Medium` · `Low` · `Speculative`

**Based on:**
*(prior experiments, papers, or reasoning)*

---

## Proposed Experiment

> Concrete experimental design to answer this question.

**Experiment ID:** EXP-NN *(assign from registry)*
**Folder:** `experiments/<category>/<topic>/`
**Method:**

1.
2.
3.

**Variables:**

| Type | Variable | Values |
|---|---|---|
| Independent | | |
| Controlled | | |
| Measured | | |

**Estimated cost:** $—
**Estimated runtime:** —

---

## Expected Outcome

> What result would confirm the hypothesis? What would refute it?

**If confirmed:**
*(what the data would show, what it implies)*

**If refuted:**
*(what the data would show, what it implies)*

**Surprising outcome to watch for:**
*(something unexpected that would change the direction of research)*

---

## Impact

> What changes — in the codebase, architecture, or understanding — once this is answered?

**If confirmed:**
- Code / architecture change: *(e.g. "always set seed= alongside T=0 in production")*
- Updated concept note: *(e.g. "`research/concepts/llm_behavior.md` — determinism section")*
- New rule / standard: *(e.g. "add to `.cursor/rules/ai_lab_rules.mdc`")*

**If refuted:**
- *(revised understanding)*

**Downstream questions this will raise:**
1.
2.

---

*Add this question to [`open_questions.md`](open_questions.md) when created.*
*Move to [`answered_questions.md`](answered_questions.md) when the experiment is complete.*

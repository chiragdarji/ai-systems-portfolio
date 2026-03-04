---
title: "Experiment 02 — System Prompt Control"
tags: [experiment, system-prompt, llm-behavior, persona, enterprise-ai]
aliases: [system-prompt-experiment, exp-02]
---

# Experiment 02 — System Prompt Control

**Phase:** LLM Behavior & Prompt Control
**Status:** Complete

---

## Hypothesis

The system prompt acts as the primary behaviour-control layer in an LLM deployment. Changing only the system prompt — while holding temperature and user prompts constant — should produce measurably different outputs in tone, length, precision, and quality.

## Variables

| Variable | Values |
|---|---|
| System prompt (persona) | BASELINE, CARELESS, RESEARCHER |
| Temperature | 0.7 (fixed) |
| User prompts | explain_llm, explain_rag, explain_hallucination, code_task |
| Model | gpt-4o-mini |

## Method

Run 4 identical user prompts through 3 different system prompt personas. Hold temperature constant. Measure word count, token usage, and qualitative differences in tone, precision, and code quality.

## Key Questions

- How much does the system prompt change output quality?
- Can a single word ("careless") measurably degrade response quality?
- How does this pattern apply in enterprise AI systems?
- What is the risk of prompt injection at this layer?

## Run

```bash
python experiments/llm_behavior/system_prompt/code.py
```

## Outputs

| File | Contents |
|---|---|
| `results.md` | Raw per-persona outputs with token/word counts |
| `analysis.md` | Enterprise implications, tone breakdown, key takeaways |

## Key Finding

Even a deliberately degraded system prompt (`"You are a careless AI assistant"`) is faithfully followed by the model. This demonstrates that the system prompt is **architecture**, not configuration — a security boundary and a behaviour contract simultaneously.

---

## Links

**Concepts:**
- [`LLM Behavior`](../../../research/concepts/llm_behavior.md) — system prompt as a control surface; behaviour contract vs style hint

**Research Questions raised:**
- [RQ-02](../../../research/questions/open_questions.md#rq-02--prompt-injection-resistance) — How much of a system prompt can be overridden by a crafted user message?
- [RQ-10](../../../research/questions/open_questions.md#rq-10--system-vs-user-instruction-conflict) — When system prompt and user message directly contradict, which wins?

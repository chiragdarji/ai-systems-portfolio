# Research — Insights

Original observations, mental models, and cross-domain connections developed through experiments and research.

## Format

Each insight note follows this structure:

```
# Insight: <title>

**Source:** experiment | paper | observation
**Date:** YYYY-MM-DD

## Observation
What was noticed.

## Why It Matters
Engineering or design implication.

## Open Questions
What this raises.
```

## Insights So Far

- [Temperature is a specificity vs diversity dial, not a quality dial](../../../experiments/llm_behavior/temperature/analysis.md)
- [T=0 via OpenAI API is not byte-exact deterministic — distributed GPU non-determinism persists](../../../experiments/llm_behavior/temperature/analysis.md)
- [System prompt is architecture, not configuration — it is a security boundary](../../../experiments/llm_behavior/system_prompt/analysis.md)
- [max_tokens is a ceiling, not a target — RAG needs only ~50 tokens, code needs 800+](../../../experiments/llm_behavior/token_limit/analysis.md)
- [O(n²) attention memory is the root cause of context window limits, not model capability](../../../experiments/llm_behavior/attention/analysis.md)

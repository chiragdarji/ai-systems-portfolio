---
title: "Architecture — LLM Behavior Explorer"
tags: [architecture, llm-behavior, tokenization, system-design, portfolio]
aliases: [llm-behavior-architecture, llm-explorer-architecture]
---

# Architecture: LLM Behavior Explorer

> This document describes the system design of `projects/llm_behavior/`.
> Every architectural decision is grounded in specific findings from EXP-01 through EXP-06.

---

## System Components

| Component | Responsibility | Key technology | Failure mode |
|-----------|:-------------:|:--------------:|:------------:|
| `TokenBudgetGuard` | Pre-flight: encode prompt with tiktoken, check against context limit, raise before any API call | `tiktoken cl100k_base` | Raises `TokenBudgetError` if prompt + response_budget > max_context |
| `DomainCostEstimator` | Return token count + USD cost for a text string, with domain-adjusted ratio from EXP-06 | `tiktoken`, EXP-06 ratio table | Falls back to English prose ratio if domain is unrecognised |
| `TemperatureSweep` | Run N calls at each temperature value; measure output variance and determinism rate | `openai.ChatCompletion` | API timeout → partial results written; rate limit → exponential backoff |
| `SystemPromptAuditor` | Run A/B comparison of two system prompts; compute word count delta, compliance verdict | `openai.ChatCompletion` | Model ignores system prompt entirely (EXP-02 showed this is possible with degraded prompts) |
| `DeterminismProbe` | Run M identical calls at T=0; measure identity rate, detect `system_fingerprint` changes | `openai.ChatCompletion` | `system_fingerprint` change mid-run → flag as backend drift, not non-determinism |
| `ReportWriter` | Write markdown report to `results/<module>_YYYY-MM-DD.md` on every run | Standard library `pathlib` | File write fails → log to stderr, do not crash the run |
| `CLI` (`main.py`) | Parse command-line arguments and route to the correct module | `argparse` | Invalid argument → print usage, exit 0 |

---

## Data Flow

```
User (CLI or import)
       │
       ▼
  main.py  ──── argparse ────► TokenBudgetGuard ──► raises TokenBudgetError (no API call)
       │                                │
       │                                ▼ (budget OK)
       │                       DomainCostEstimator ──► cost estimate (no API call)
       │
       ├──► TemperatureSweep
       │         │  system + user prompt, temp range, N runs
       │         ▼
       │     openai.ChatCompletion (one call per temp × N repetitions)
       │         │
       │         ▼  (content, prompt_tokens, completion_tokens, finish_reason)
       │     Result dataclass
       │         │
       ├──► SystemPromptAuditor
       │         │  system_A, system_B, user prompt
       │         ▼
       │     openai.ChatCompletion (2 calls)
       │         │
       │         ▼  (response_A, response_B, word_counts, compliance_verdict)
       │     AuditResult dataclass
       │
       ├──► DeterminismProbe
       │         │  prompt, T=0, M repetitions
       │         ▼
       │     openai.ChatCompletion (M calls)
       │         │
       │         ▼  (identity_rate, unique_count, fingerprints, verdict)
       │     DeterminismResult dataclass
       │
       ▼
  ReportWriter
       │  Any result dataclass
       ▼
  results/<module>_YYYY-MM-DD.md
```

---

## Failure Modes

| Failure | Detection signal | Mitigation |
|---------|:----------------:|-----------|
| Prompt exceeds context window | `TokenBudgetGuard` raises `TokenBudgetError` before any API call | Caller truncates system prompt or reduces retrieved context; see EXP-03 finding |
| `max_tokens` too low for domain | `finish_reason == "length"` in result | `DomainCostEstimator` warns when `max_tokens` is below the domain-average completion length; raise before calling |
| T=0 non-determinism reported as failure | Identical `system_fingerprint` across all calls but outputs differ | `DeterminismProbe` separates FP-noise non-determinism from `system_fingerprint`-change non-determinism; EXP-05 established that both produce identical identity rates |
| OpenAI rate limit (429) | `openai.RateLimitError` exception | Exponential backoff with jitter: wait 2^n seconds up to 60s; log each retry |
| API key missing | `openai.AuthenticationError` | Check at startup; `TokenBudgetGuard` and `DomainCostEstimator` continue without key |
| Arabic/Japanese word-count used for budget | Silent cost underestimate | `TokenBudgetGuard` always uses `tiktoken.encode()` — never word count. EXP-06 established this is the only safe method |
| `system_fingerprint` changes mid-experiment | Outputs shift unexpectedly | `DeterminismProbe` records fingerprint per call; flags backend model drift separately from output variance |

---

## Scaling Considerations

**At 100 requests/day (prototype / research tool):**
- Single Python process, synchronous API calls
- `results/` folder accumulates markdown files — no database needed
- `TokenBudgetGuard` adds ~0.5ms per prompt (tiktoken is local)
- Total cost at 100 calls/day with `gpt-4o-mini`: ~$0.002–0.005/day

**At 10,000 requests/day (team tool / CI integration):**
- Async API calls with `asyncio` + `openai.AsyncOpenAI` for sweep modules
- `TokenBudgetGuard` still synchronous (no API call, always fast)
- Results written to a shared `results/` path or a lightweight SQLite store
- Rate limit handling becomes critical — implement token-bucket throttle
- Consider response caching for `DeterminismProbe` (EXP-05's key recommendation)

**At 1,000,000 requests/day (production quality gate):**
- `TokenBudgetGuard` and `DomainCostEstimator` deployed as a sidecar service (zero API calls)
- `TemperatureSweep` and `DeterminismProbe` become async background workers with result queues
- Full observability: latency per module, token cost per call, non-determinism rate over time
- Model version tracking via `system_fingerprint` becomes a change-detection signal for deployment gates

---

## Experiment-Grounded Decisions

| Architectural decision | Grounded in | Evidence |
|------------------------|:-----------:|---------|
| `TokenBudgetGuard` uses tiktoken, never word count | [EXP-06](../../experiments/llm_behavior/tokenization/experiment.md) | JSON text costs 4.15 tokens/word — 3.32× more than English. Word-count estimates undercount by 3× for structured context. |
| `DeterminismProbe` tracks `system_fingerprint` separately from output variance | [EXP-05](../../experiments/llm_behavior/seed_determinism/experiment.md) | `system_fingerprint` changed mid-experiment without affecting canonical code output — the two signals are orthogonal. |
| No `seed` parameter in `DeterminismProbe` — it is not exposed to the user | [EXP-05](../../experiments/llm_behavior/seed_determinism/experiment.md) | Seed had zero measurable effect (Δ identity rate = +0.0%). Exposing it would suggest false control. |
| Each module writes markdown results, not JSON | EXP-01 through EXP-06 | All experiments use the same 4-file contract. Markdown is diff-able, readable inline, and links directly into `experiment.md`. |
| `SystemPromptAuditor` flags when model ignores persona constraints | [EXP-02](../../experiments/llm_behavior/system_prompt/experiment.md) | Model faithfully followed even destructive system prompts. The compliance verdict is the most important output — not just word count. |
| `max_tokens` defaults to domain-appropriate ceiling, not a fixed number | [EXP-03](../../experiments/llm_behavior/token_limit/experiment.md) | RAG answers complete at ~51 tokens; code requires 800+. A fixed default of 256 would be too small for code and wasteful for factual Q&A. |

---

## When To Use This Architecture

- When you need a pre-flight token budget check before any API call in a production system
- When auditing whether a system prompt change altered model behaviour in a measurable way
- When investigating whether T=0 outputs are stable enough to cache (use `DeterminismProbe`)
- When estimating API cost for a mixed-domain workload (English + code + JSON + non-English)
- As a teaching tool: each module directly demonstrates one experiment's findings

## When NOT To Use This Architecture

- When you need streaming responses — this toolkit uses blocking calls only; streaming changes the `finish_reason` semantics
- When you need multi-turn conversation memory — each module is stateless; use a chat wrapper layer on top
- When you need batch processing at scale — the synchronous design hits rate limits quickly above ~1,000 calls/run; use the async patterns described in the 10K/day scaling section above
- When comparing Claude vs GPT-4o — `TokenBudgetGuard` uses `cl100k_base` (OpenAI only); Anthropic has a different tokenizer

---

*Project details → [`project.md`](project.md)*
*How to run → [`README.md`](README.md)*

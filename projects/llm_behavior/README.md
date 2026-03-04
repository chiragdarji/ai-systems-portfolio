---
title: "LLM Behavior Explorer"
tags: [project, llm-behavior, tokenization, temperature, seed-determinism, portfolio]
aliases: [llm-behavior-explorer, llm-toolkit]
---

# LLM Behavior Explorer

> A production-pattern Python toolkit that translates six LLM behavior experiments
> into runnable, auditable tools — token budget guards, temperature sweeps, system
> prompt audits, cost estimators, and non-determinism probes.

Part of the [`ai-systems-portfolio`](../../README.md) research lab.
Built from empirical findings in: **EXP-01 through EXP-06** (LLM Behavior layer).

---

## What This Demonstrates

- **Token budget pre-flight** — encode any prompt with tiktoken before calling the API; raise a structured error before a single token is wasted *(grounded in EXP-06: JSON costs 3.32× more than English prose per word)*
- **Temperature parameter sweep** — measure output entropy and determinism rate across T=0.0 → T=1.0 *(grounded in EXP-01: T=0 via OpenAI API is NOT byte-exact deterministic)*
- **System prompt auditing** — A/B compare two system prompts; detect when the model ignores or violates persona constraints *(grounded in EXP-02: system prompt is architecture, not config)*
- **Domain cost estimation** — predict token count and USD cost for any text, adjusted for domain (code, JSON, Arabic, etc.) *(grounded in EXP-06 ratio table)*
- **Non-determinism probing** — run M identical T=0 calls; distinguish FP-noise non-determinism from backend model drift via `system_fingerprint` *(grounded in EXP-05: seed has zero effect at T=0)*

---

## Setup

```bash
# 1. From repo root — activate virtual environment
source .venv/bin/activate

# 2. Install dependencies (tiktoken is the only new one — openai already installed)
pip install -r requirements.txt

# 3. Set API key (only needed for modules that call the OpenAI API)
cp .env.template .env
# Edit .env → set OPENAI_API_KEY=sk-...
```

---

## Usage

### Token budget pre-flight (no API key needed)

```python
from projects.llm_behavior.implementation.token_budget import TokenBudgetGuard

guard = TokenBudgetGuard(model="gpt-4o-mini", response_budget=500)

# Raises TokenBudgetError if prompt would exceed context window
messages = guard.check([
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user",   "content": "Explain transformers in detail..."},
])
# Returns approved messages if budget is OK
```

### Domain cost estimate (no API key needed)

```python
from projects.llm_behavior.implementation.token_cost import estimate_domain_cost

result = estimate_domain_cost(
    text=my_json_payload,
    domain="json_structured",   # or "common_english", "python_code", "arabic", etc.
    model="gpt-4o-mini",
    cost_per_1k_tokens=0.00015,
)
print(f"{result.token_count} tokens — estimated ${result.usd_cost:.6f}")
```

### Temperature sweep

```bash
python projects/llm_behavior/implementation/temperature_sweep.py \
  --prompt "Explain what a transformer model is in two sentences." \
  --temps 0.0 0.3 0.7 1.0 \
  --runs 3
# Writes: projects/llm_behavior/results/temperature_sweep_YYYY-MM-DD.md
```

### System prompt audit

```bash
python projects/llm_behavior/implementation/system_prompt_audit.py \
  --prompt "What is the capital of France?" \
  --system-a "You are a precise, factual assistant." \
  --system-b "You are a creative storyteller."
# Writes: projects/llm_behavior/results/system_prompt_audit_YYYY-MM-DD.md
```

### Non-determinism probe

```bash
python projects/llm_behavior/implementation/determinism_probe.py \
  --prompt "Write a Python function to compute fibonacci(n)." \
  --runs 10
# Writes: projects/llm_behavior/results/determinism_probe_YYYY-MM-DD.md
```

### Run everything

```bash
python projects/llm_behavior/implementation/main.py --all
# Runs all modules with default settings; writes all reports to results/
```

---

## Project Structure

```
projects/llm_behavior/
├── project.md              ← problem, goals, concept links, implementation status
├── architecture.md         ← system components, data flow, failure modes
├── README.md               ← this file
├── implementation/
│   ├── token_budget.py     ← TokenBudgetGuard (no API key)
│   ├── token_cost.py       ← DomainCostEstimator (no API key)
│   ├── temperature_sweep.py
│   ├── system_prompt_audit.py
│   ├── determinism_probe.py
│   └── main.py             ← CLI entry point
├── experiments/            ← project-specific experiments
├── evaluation/             ← evaluation scripts and baseline comparisons
└── results/                ← auto-generated markdown reports (created on first run)
```

---

## Key Files

| File | Purpose |
|------|---------|
| [`project.md`](project.md) | Problem statement, acceptance criteria, engineering decisions |
| [`architecture.md`](architecture.md) | System components, data flow diagram, failure modes, scaling |
| [`implementation/token_budget.py`](implementation/token_budget.py) | Pre-flight token check — the most reusable component |
| [`implementation/determinism_probe.py`](implementation/determinism_probe.py) | T=0 stability audit; uses EXP-05 findings |

---

## Related Research

| Asset | Link |
|-------|------|
| LLM Behavior concept | [research/concepts/llm_behavior.md](../../research/concepts/llm_behavior.md) |
| Seed Determinism concept | [research/concepts/seed_determinism.md](../../research/concepts/seed_determinism.md) |
| Tokenization concept | [research/concepts/tokenization.md](../../research/concepts/tokenization.md) |
| EXP-01 — Temperature | [experiments/llm_behavior/temperature/](../../experiments/llm_behavior/temperature/experiment.md) |
| EXP-02 — System Prompt | [experiments/llm_behavior/system_prompt/](../../experiments/llm_behavior/system_prompt/experiment.md) |
| EXP-03 — Token Limit | [experiments/llm_behavior/token_limit/](../../experiments/llm_behavior/token_limit/experiment.md) |
| EXP-05 — Seed Determinism | [experiments/llm_behavior/seed_determinism/](../../experiments/llm_behavior/seed_determinism/experiment.md) |
| EXP-06 — Tokenization Ratios | [experiments/llm_behavior/tokenization/](../../experiments/llm_behavior/tokenization/experiment.md) |

---

## Status

| Module | Status |
|--------|:------:|
| `token_budget.py` | ⬜ Not started |
| `token_cost.py` | ⬜ Not started |
| `temperature_sweep.py` | ⬜ Not started |
| `system_prompt_audit.py` | ⬜ Not started |
| `determinism_probe.py` | ⬜ Not started |
| `main.py` | ⬜ Not started |
| Evaluation | ⬜ Not started |

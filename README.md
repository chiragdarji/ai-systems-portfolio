# AI Systems Portfolio

**A structured research portfolio for applied AI systems engineering.**
Focus: LLM internals, RAG pipelines, autonomous agents, evaluation, and production AI architecture.

---

## Repository Structure

```
ai-systems-portfolio/
│
├── experiments/                    # Controlled, reproducible LLM experiments
│   └── llm_behavior/               # Phase 1–2: LLM behavior & transformer internals
│       ├── temperature/            # Exp 01 — Temperature & output entropy
│       │   ├── experiment.md       # Hypothesis, variables, method, key findings
│       │   ├── code.py             # Runnable experiment script
│       │   ├── results.md          # Auto-generated live results
│       │   └── analysis.md         # Scientific analysis & decision framework
│       ├── system_prompt/          # Exp 02 — System prompt as behaviour control
│       ├── token_limit/            # Exp 03 — max_tokens, truncation, cost
│       └── attention/              # Exp 04 — Self-attention mechanics (NumPy only)
│
├── projects/                       # End-to-end AI system builds
│   ├── rag_assistant/              # RAG pipeline over custom documents
│   ├── rag_eval_pipeline/          # Automated RAG evaluation framework
│   ├── ai_agents/                  # Single-agent tool-use systems
│   ├── multi_agent_system/         # Multi-agent orchestration
│   ├── production_llm_pipeline/    # FastAPI + LLM production service
│   └── domain_ai_solution/         # Domain-specific AI application
│
├── research/                       # Reading notes, paper summaries, insights
│   ├── concepts/                   # Core AI/ML concept deep-dives
│   ├── papers/                     # Annotated paper notes
│   └── insights/                   # Original observations & mental models
│
├── docs/                           # Architecture diagrams, learning path, case studies
│   ├── AI_Expert_Path.md           # 60-day structured learning roadmap
│   ├── architectures/              # System architecture diagrams
│   └── case_studies/               # Real-world AI system analyses
│
├── verify_env.py                   # Environment & API connectivity health check
├── requirements.txt                # Pinned Python dependencies (106 packages)
├── .env.template                   # API key template — copy to .env
└── .gitignore                      # Excludes .env, .venv, __pycache__, caches
```

---

## Environment Setup

### 1. Clone and enter the repo

```bash
git clone https://github.com/chiragdarji/ai-systems-portfolio.git
cd ai-systems-portfolio
```

### 2. Create and activate virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure API keys

```bash
cp .env.template .env
# Edit .env and add your real API keys
```

### 5. Verify everything works

```bash
python verify_env.py
```

Expected output on full pass:

```
  [PASS] ✓  Env: OpenAI       OPENAI_API_KEY is set
  [PASS] ✓  Import: LangChain langchain imported successfully
  [PASS] ✓  API: OpenAI       Connected — 116 models available
  ...
  13/13 checks passed
```

---

## Running Experiments

Each experiment is self-contained inside its folder. Run any experiment with:

```bash
python experiments/llm_behavior/temperature/code.py
python experiments/llm_behavior/system_prompt/code.py
python experiments/llm_behavior/token_limit/code.py
python experiments/llm_behavior/attention/code.py   # No API key needed
```

Every script:
- Prints a formatted console report
- Auto-generates / overwrites `results.md` in the same folder
- Is reproducible with fixed seeds where applicable

---

## Experiment Workflow

Every experiment follows this standard structure:

```
1. experiment.md  ← Read first: hypothesis, variables, method, key questions
2. code.py        ← Run to generate live results
3. results.md     ← Auto-generated output — raw API responses, stats
4. analysis.md    ← Scientific interpretation, decision frameworks, implications
```

When adding a new experiment:

1. Create a new folder under `experiments/llm_behavior/` (or a new category)
2. Write `experiment.md` before writing code — define the hypothesis first
3. Keep `code.py` runnable from the repo root
4. Write `analysis.md` after reviewing results — observations should be evidence-based

---

## Core Libraries

| Library | Purpose |
|---|---|
| `openai` | GPT-4o, embeddings, function calling |
| `anthropic` | Claude 3.x models |
| `langchain` | Chains, agents, prompt templates |
| `llama-index` | Document ingestion, RAG pipelines |
| `python-dotenv` | Secure `.env` loading |
| `fastapi` | Production API server |
| `uvicorn` | ASGI server for FastAPI |
| `numpy` | Numerical computing (attention simulator) |

---

## Project Roadmap

### Phase 1 — LLM Behavior (experiments/llm_behavior/)

| # | Experiment | Status |
|---|---|---|
| 01 | Temperature & output entropy | ✅ Complete |
| 02 | System prompt as behaviour control layer | ✅ Complete |
| 03 | Token limits, truncation, cost | ✅ Complete |
| 04 | Self-attention mechanics (NumPy) | ✅ Complete |
| 05 | Embeddings & cosine similarity | Planned |
| 06 | Few-shot vs zero-shot prompting | Planned |
| 07 | Chain-of-Thought reasoning | Planned |

### Phase 2 — RAG Systems (projects/)

| Project | Description | Status |
|---|---|---|
| `rag_assistant` | Document-grounded Q&A over custom corpus | Planned |
| `rag_eval_pipeline` | Automated faithfulness & relevance evaluation | Planned |

### Phase 3 — Agents (projects/)

| Project | Description | Status |
|---|---|---|
| `ai_agents` | Single agent with tool use (search, code exec) | Planned |
| `multi_agent_system` | Planner + executor multi-agent workflow | Planned |

### Phase 4 — Production (projects/)

| Project | Description | Status |
|---|---|---|
| `production_llm_pipeline` | FastAPI service with caching, tracing, rate limiting | Planned |
| `domain_ai_solution` | End-to-end domain-specific AI application | Planned |

---

## Research Log

Key findings documented so far:

| Insight | Source |
|---|---|
| `T=0` is not byte-exact deterministic via OpenAI API — use `seed=` | Exp 01 |
| System prompt is a security boundary and behaviour contract, not just a hint | Exp 02 |
| `max_tokens` is a ceiling not a target — RAG needs ~50 tokens, code needs 800+ | Exp 03 |
| Attention memory is O(n²) — the structural root cause of context window limits | Exp 04 |

---

## Security Notes

- `.env` is listed in `.gitignore` — API keys are never committed
- Only `.env.template` (with placeholders) is tracked in Git
- Rotate any key immediately if accidentally exposed

---

*60-Day Applied AI Mastery Journey — LLM Systems · RAG · Agents · Evaluation · Production AI*

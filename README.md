# AI Systems Portfolio

**60-Day Applied AI Mastery Journey**
Focus: LLM Systems, RAG, Agents, Evaluation, Production AI

---

## Project Structure

```
ai-systems-portfolio/
├── 01_prompt_playground/       # Prompt engineering experiments
├── 02_rag_assistant/           # Retrieval-Augmented Generation
├── 03_rag_eval_pipeline/       # RAG evaluation framework
├── 04_ai_agents/               # Single-agent systems
├── 05_multi_agent_system/      # Multi-agent orchestration
├── 06_production_llm_pipeline/ # Production-grade LLM pipelines
├── 07_domain_ai_solution/      # Domain-specific AI application
├── Docs/                       # Architecture diagrams & notes
├── .env.template               # Environment variable template
├── requirements.txt            # Pinned Python dependencies
└── verify_env.py               # Environment & API health check
```

---

## Environment Setup

### Prerequisites

- Python 3.11+
- Git

### 1. Clone and enter the repo

```bash
git clone https://github.com/<your-username>/ai-systems-portfolio.git
cd ai-systems-portfolio
```

### 2. Create and activate the virtual environment

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

### 4. Configure environment variables

```bash
cp .env.template .env
```

Open `.env` and replace the placeholder values with your real API keys:

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | OpenAI platform key |
| `ANTHROPIC_API_KEY` | Anthropic console key |
| `LANGCHAIN_API_KEY` | LangSmith tracing (optional) |
| `LLAMA_CLOUD_API_KEY` | LlamaCloud services (optional) |

### 5. Verify the setup

```bash
python verify_env.py
```

A passing run looks like:

```
============================================================
  AI Systems Portfolio — Environment Check
============================================================
  [PASS] ✓  Env: OpenAI
  [PASS] ✓  Env: Anthropic
  ...
  [PASS] ✓  API: OpenAI       Connected — 42 models available
  [PASS] ✓  API: Anthropic    Connected successfully
============================================================
  10/10 checks passed
============================================================
```

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

---

## Running a FastAPI Server

```bash
uvicorn 06_production_llm_pipeline.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Security Notes

- `.env` is listed in `.gitignore` — it will never be committed.
- Only `.env.template` (with placeholder values) is tracked in Git.
- Rotate any API key immediately if it is ever accidentally exposed.

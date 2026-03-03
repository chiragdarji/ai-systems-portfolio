"""
Experiment 03 — Token Limit Analysis
======================================
Systematically tests how max_tokens affects output quality, truncation
behaviour, finish_reason, and cost across four real-world use cases.

Domains tested:
  - explanation   : conceptual explanation (open-ended, favours more tokens)
  - summarisation : condense a paragraph (bounded task)
  - code          : write a working function (structure-sensitive)
  - rag_chunk     : answer a question from a simulated document chunk

Token budgets tested: 50, 150, 300, 600

Outputs:
  - Console report with finish_reason, token stats, truncation detection
  - token_limit_results.md (auto-generated)

Usage:
    python 01_prompt_playground/experiment_03_token_limit.py
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from textwrap import indent

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

# ── Config ─────────────────────────────────────────────────────────────────────
MODEL = "gpt-4o-mini"
TEMPERATURE = 0.3   # low variance so token budget is the only variable
TOKEN_BUDGETS = [50, 150, 300, 600]
REPEAT_RUNS = 1     # single run per config — finish_reason is deterministic

# Truncation heuristics: responses that end mid-sentence are likely truncated
TRUNCATION_ENDINGS = (".", "!", "?", "```", "---")

PROMPTS: dict[str, tuple[str, str]] = {
    "explanation": (
        "You are a precise AI educator.",
        (
            "Explain how Retrieval-Augmented Generation (RAG) works. "
            "Cover: what it is, why it exists, how retrieval and generation interact, "
            "and when you would use it over fine-tuning."
        ),
    ),
    "summarisation": (
        "You are a concise summariser. Summarise the text accurately.",
        (
            "Summarise the following in your own words:\n\n"
            "Large Language Models (LLMs) are deep learning systems trained on massive "
            "corpora of text. They learn statistical patterns over tokens and can generate "
            "coherent, contextually relevant text. However, they are prone to hallucination — "
            "generating plausible-sounding but factually incorrect content — because they "
            "optimise for fluency rather than factual accuracy. This makes them powerful for "
            "drafting and exploration but unreliable for high-stakes factual retrieval without "
            "grounding mechanisms such as RAG or tool use."
        ),
    ),
    "code": (
        "You are an expert Python developer. Return only clean, working Python code with a docstring.",
        (
            "Write a Python class called VectorStore that supports: "
            "add(id, embedding, metadata), search(query_embedding, top_k) using cosine similarity, "
            "and delete(id). Use only the Python standard library."
        ),
    ),
    "rag_chunk": (
        "You are a helpful assistant. Answer only from the context provided. Do not speculate.",
        (
            "Context: LlamaIndex is a data framework for LLM applications. It provides tools for "
            "ingesting, indexing, and querying data. Its core components include data connectors "
            "(called Readers), indexes (VectorStoreIndex, SummaryIndex, KnowledgeGraphIndex), "
            "query engines, and agent tools. LlamaIndex supports OpenAI, Anthropic, and local models "
            "via LiteLLM. It integrates with vector databases such as Pinecone, Weaviate, and Chroma.\n\n"
            "Question: What are the core components of LlamaIndex and which vector databases does it support?"
        ),
    ),
}

# ── Data model ─────────────────────────────────────────────────────────────────
@dataclass
class Run:
    domain: str
    max_tokens: int
    content: str
    finish_reason: str
    prompt_tokens: int
    completion_tokens: int
    latency_ms: float

    @property
    def truncated(self) -> bool:
        """Heuristic: finish_reason='length' is definitive; also flag mid-sentence endings."""
        if self.finish_reason == "length":
            return True
        stripped = self.content.strip()
        return bool(stripped) and not stripped.endswith(TRUNCATION_ENDINGS)

    @property
    def cost_usd(self) -> float:
        """Approximate cost at gpt-4o-mini pricing (Mar 2026): $0.15/1M input, $0.60/1M output."""
        return (self.prompt_tokens * 0.00000015) + (self.completion_tokens * 0.00000060)

    @property
    def utilisation_pct(self) -> float:
        """How much of the token budget was actually consumed."""
        return (self.completion_tokens / self.max_tokens) * 100


@dataclass
class Results:
    runs: list[Run] = field(default_factory=list)

    def by_domain(self, domain: str) -> list[Run]:
        return [r for r in self.runs if r.domain == domain]

    def by_budget(self, budget: int) -> list[Run]:
        return [r for r in self.runs if r.max_tokens == budget]


# ── API call ───────────────────────────────────────────────────────────────────
def call_model(system: str, user: str, max_tokens: int) -> Run:
    start = time.perf_counter()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
        temperature=TEMPERATURE,
        max_tokens=max_tokens,
    )
    elapsed_ms = (time.perf_counter() - start) * 1000
    choice = response.choices[0]
    usage  = response.usage
    return Run(
        domain="",  # set by caller
        max_tokens=max_tokens,
        content=choice.message.content or "",
        finish_reason=choice.finish_reason,
        prompt_tokens=usage.prompt_tokens,
        completion_tokens=usage.completion_tokens,
        latency_ms=elapsed_ms,
    )


# ── Experiment runner ──────────────────────────────────────────────────────────
def run_experiment() -> Results:
    results = Results()
    total = len(PROMPTS) * len(TOKEN_BUDGETS)
    n = 0

    for domain, (system_prompt, user_prompt) in PROMPTS.items():
        for budget in TOKEN_BUDGETS:
            n += 1
            truncation_flag = ""
            print(
                f"  [{n:>2}/{total}]  domain={domain:<15} max_tokens={budget:<4}",
                end=" ... ",
                flush=True,
            )
            run = call_model(system_prompt, user_prompt, budget)
            run.domain = domain
            results.runs.append(run)
            truncation_flag = " ⚠ TRUNCATED" if run.truncated else ""
            print(
                f"{run.latency_ms:>6.0f} ms | {run.completion_tokens:>3}/{budget} tokens "
                f"({run.utilisation_pct:>5.1f}%) | finish={run.finish_reason}{truncation_flag}"
            )

    return results


# ── Console report ─────────────────────────────────────────────────────────────
def print_report(results: Results) -> None:
    sep = "=" * 76

    for domain in PROMPTS:
        print(f"\n{sep}")
        print(f"  DOMAIN: {domain.upper()}")
        print(sep)

        domain_runs = results.by_domain(domain)
        for run in domain_runs:
            trunc_badge = "  ⚠  TRUNCATED" if run.truncated else "  ✓  COMPLETE"
            print(f"\n  ── max_tokens={run.max_tokens}{trunc_badge}")
            print(f"     finish_reason={run.finish_reason!r}  |  "
                  f"tokens={run.completion_tokens}/{run.max_tokens}  |  "
                  f"utilisation={run.utilisation_pct:.1f}%  |  "
                  f"cost≈${run.cost_usd:.6f}")
            print()
            print(indent(run.content, "     "))

        # Cross-budget comparison for this domain
        print(f"\n  {'─' * 60}")
        print(f"  Budget comparison — {domain}")
        print(f"  {'max_tokens':<12} {'tokens used':<14} {'finish':<10} {'truncated':<11} {'cost USD'}")
        print(f"  {'─' * 60}")
        for run in domain_runs:
            trunc = "YES ⚠" if run.truncated else "no"
            print(f"  {run.max_tokens:<12} {run.completion_tokens:<14} {run.finish_reason:<10} {trunc:<11} ${run.cost_usd:.6f}")

    # Global summary
    print(f"\n{sep}")
    total_cost  = sum(r.cost_usd for r in results.runs)
    total_out   = sum(r.completion_tokens for r in results.runs)
    total_in    = sum(r.prompt_tokens for r in results.runs)
    trunc_count = sum(1 for r in results.runs if r.truncated)
    print(f"  Total prompt tokens      : {total_in}")
    print(f"  Total completion tokens  : {total_out}")
    print(f"  Total estimated cost     : ${total_cost:.5f}")
    print(f"  Truncated responses      : {trunc_count}/{len(results.runs)}")
    print(sep)


# ── Markdown writer ────────────────────────────────────────────────────────────
def write_markdown(results: Results, out_path: Path) -> None:
    lines: list[str] = []
    a = lines.append

    a("# Experiment 03 — Token Limit Analysis Results\n\n")
    a(f"> **Model**: `{MODEL}` | **Temperature**: `{TEMPERATURE}` | "
      f"**Budgets**: {TOKEN_BUDGETS}\n\n")
    a("---\n\n")

    # Per-domain tables + outputs
    for domain, (_, user_prompt) in PROMPTS.items():
        a(f"## Domain: `{domain}`\n\n")
        a(f"**Prompt (truncated):** *{user_prompt[:120]}{'...' if len(user_prompt) > 120 else ''}*\n\n")

        # Comparison table
        a("| max_tokens | Used | Utilisation | finish_reason | Truncated | Cost USD |\n")
        a("|------------|------|-------------|---------------|-----------|----------|\n")
        for run in results.by_domain(domain):
            trunc = "**YES ⚠**" if run.truncated else "no"
            a(f"| {run.max_tokens} | {run.completion_tokens} | "
              f"{run.utilisation_pct:.1f}% | `{run.finish_reason}` | {trunc} | "
              f"`${run.cost_usd:.6f}` |\n")
        a("\n")

        for run in results.by_domain(domain):
            badge = "⚠ TRUNCATED" if run.truncated else "✓ Complete"
            a(f"### `max_tokens={run.max_tokens}` — {badge}\n\n")
            a(f"```\n{run.content.strip()}\n```\n\n")

        a("---\n\n")

    # Global summary
    a("## Global Summary\n\n")
    a("| Domain | Budget | Used | finish_reason | Truncated | Cost |\n")
    a("|--------|--------|------|---------------|-----------|------|\n")
    for run in results.runs:
        trunc = "YES ⚠" if run.truncated else "no"
        a(f"| {run.domain} | {run.max_tokens} | {run.completion_tokens} | "
          f"`{run.finish_reason}` | {trunc} | `${run.cost_usd:.6f}` |\n")

    total_cost = sum(r.cost_usd for r in results.runs)
    trunc_count = sum(1 for r in results.runs if r.truncated)
    a(f"\n**Total estimated cost:** `${total_cost:.5f}`  \n")
    a(f"**Truncated responses:** `{trunc_count}/{len(results.runs)}`\n")

    out_path.write_text("".join(lines), encoding="utf-8")
    print(f"\n  Results written → {out_path}")


# ── Entry point ────────────────────────────────────────────────────────────────
def main() -> None:
    print(f"\n{'=' * 76}")
    print("  Experiment 03 — Token Limit Analysis")
    print(f"  Model: {MODEL}  |  Budgets: {TOKEN_BUDGETS}  |  Domains: {list(PROMPTS)}")
    print(f"{'=' * 76}\n")

    results = run_experiment()
    print_report(results)

    out = Path(__file__).parent / "experiment_03_token_limit_results.md"
    write_markdown(results, out)


if __name__ == "__main__":
    main()

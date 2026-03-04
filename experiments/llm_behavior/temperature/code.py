"""
Experiment 01 — LLM Temperature Analysis
=========================================
Systematically probes how OpenAI's temperature parameter affects output
across four domains: general explanation, financial, legal, and code.

Usage:
    python experiments/llm_behavior/temperature/code.py

Outputs:
    - Formatted console report with token usage stats
    - results.md  (auto-generated observations file)
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

# ── Constants ──────────────────────────────────────────────────────────────────
MODEL = "gpt-4o-mini"
TEMPERATURES = [0.0, 0.3, 0.7, 1.0, 1.5]
REPEAT_RUNS = 2          # runs per temp for determinism check (temp=0 should be identical)

PROMPTS: dict[str, tuple[str, str]] = {
    "general": (
        "You are a precise AI assistant.",
        "Explain what an LLM is in one paragraph.",
    ),
    "financial": (
        "You are a financial analyst. Be accurate and factual.",
        "Summarise the key risk factors an investor should consider before buying a tech stock.",
    ),
    "legal": (
        "You are a legal summariser. Be precise and avoid speculation.",
        "Summarise the key clauses typically found in a software licence agreement.",
    ),
    "code": (
        "You are an expert Python developer. Return only clean, working code.",
        "Write a Python function that calculates compound interest given principal, rate, time, and n.",
    ),
}

# ── Data model ─────────────────────────────────────────────────────────────────
@dataclass
class Run:
    domain: str
    temperature: float
    run_index: int
    content: str
    prompt_tokens: int
    completion_tokens: int
    latency_ms: float


@dataclass
class ExperimentResults:
    runs: list[Run] = field(default_factory=list)

    def by_domain(self, domain: str) -> list[Run]:
        return [r for r in self.runs if r.domain == domain]

    def by_temp(self, temp: float) -> list[Run]:
        return [r for r in self.runs if r.temperature == temp]


# ── Core call ──────────────────────────────────────────────────────────────────
def call_model(system: str, user: str, temperature: float) -> tuple[str, int, int, float]:
    start = time.perf_counter()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
        temperature=temperature,
        max_tokens=400,
    )
    elapsed_ms = (time.perf_counter() - start) * 1000
    content = response.choices[0].message.content or ""
    usage = response.usage
    return content, usage.prompt_tokens, usage.completion_tokens, elapsed_ms


# ── Experiment runner ──────────────────────────────────────────────────────────
def run_experiment() -> ExperimentResults:
    results = ExperimentResults()
    total_calls = len(PROMPTS) * len(TEMPERATURES) * REPEAT_RUNS
    call_num = 0

    for domain, (system_prompt, user_prompt) in PROMPTS.items():
        for temp in TEMPERATURES:
            for run_idx in range(REPEAT_RUNS):
                call_num += 1
                print(f"  [{call_num:>2}/{total_calls}] domain={domain:<10} temp={temp}  run={run_idx + 1}", end=" ... ", flush=True)
                content, p_tok, c_tok, latency = call_model(system_prompt, user_prompt, temp)
                results.runs.append(Run(domain, temp, run_idx, content, p_tok, c_tok, latency))
                print(f"{latency:>6.0f} ms  |  {c_tok} tokens")

    return results


# ── Console report ─────────────────────────────────────────────────────────────
def print_report(results: ExperimentResults) -> None:
    sep = "=" * 72

    for domain in PROMPTS:
        print(f"\n{sep}")
        print(f"  DOMAIN: {domain.upper()}")
        print(sep)
        domain_runs = results.by_domain(domain)

        for temp in TEMPERATURES:
            temp_runs = [r for r in domain_runs if r.temperature == temp]
            print(f"\n  ── Temperature {temp} ──")
            for r in temp_runs:
                tag = f"Run {r.run_index + 1}"
                print(f"\n  [{tag}]  ({r.completion_tokens} tokens, {r.latency_ms:.0f} ms)")
                print(indent(r.content, "    "))

            # Determinism check for runs at same temp
            if len(temp_runs) == 2:
                identical = temp_runs[0].content.strip() == temp_runs[1].content.strip()
                marker = "IDENTICAL" if identical else "DIFFERS"
                print(f"\n  >> Determinism check (run1 vs run2): {marker}")

    print(f"\n{sep}")
    total_tokens = sum(r.completion_tokens for r in results.runs)
    avg_latency  = sum(r.latency_ms for r in results.runs) / len(results.runs)
    print(f"  Total completion tokens used : {total_tokens}")
    print(f"  Average latency per call     : {avg_latency:.0f} ms")
    print(sep)


# ── Markdown results writer ────────────────────────────────────────────────────
def write_markdown(results: ExperimentResults, out_path: Path) -> None:
    lines: list[str] = []
    a = lines.append

    a("# Experiment 01 — Temperature Analysis Results\n")
    a(f"> **Model**: `{MODEL}`  |  **Temperatures tested**: {TEMPERATURES}  |  **Runs per config**: {REPEAT_RUNS}\n")
    a("---\n")

    for domain, (_, user_prompt) in PROMPTS.items():
        a(f"## Domain: `{domain}`\n")
        a(f"**Prompt:** *{user_prompt}*\n")

        domain_runs = results.by_domain(domain)

        for temp in TEMPERATURES:
            temp_runs = [r for r in domain_runs if r.temperature == temp]
            a(f"### Temperature `{temp}`\n")

            for r in temp_runs:
                a(f"**Run {r.run_index + 1}** — {r.completion_tokens} tokens, {r.latency_ms:.0f} ms\n")
                a(f"```\n{r.content.strip()}\n```\n")

            if len(temp_runs) == 2:
                identical = temp_runs[0].content.strip() == temp_runs[1].content.strip()
                badge = "`IDENTICAL`" if identical else "`DIFFERS`"
                a(f"**Determinism check (run 1 vs run 2):** {badge}\n")

        a("---\n")

    # Summary table
    a("## Summary Stats\n")
    a("| Domain | Temp | Avg Tokens | Avg Latency (ms) |\n")
    a("|--------|------|------------|------------------|\n")
    for domain in PROMPTS:
        for temp in TEMPERATURES:
            runs = [r for r in results.by_domain(domain) if r.temperature == temp]
            if runs:
                avg_tok = sum(r.completion_tokens for r in runs) / len(runs)
                avg_lat = sum(r.latency_ms for r in runs) / len(runs)
                a(f"| {domain} | {temp} | {avg_tok:.0f} | {avg_lat:.0f} |\n")

    out_path.write_text("".join(lines), encoding="utf-8")
    print(f"\n  Results written to: {out_path}")


# ── Entry point ────────────────────────────────────────────────────────────────
def main() -> None:
    print(f"\n{'=' * 72}")
    print("  Experiment 01 — Temperature Analysis")
    print(f"  Model: {MODEL}  |  Temps: {TEMPERATURES}  |  Domains: {list(PROMPTS)}")
    print(f"{'=' * 72}\n")

    results = run_experiment()
    print_report(results)

    out_path = Path(__file__).parent / "results.md"
    write_markdown(results, out_path)


if __name__ == "__main__":
    main()

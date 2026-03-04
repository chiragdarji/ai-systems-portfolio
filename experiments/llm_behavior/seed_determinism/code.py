"""
Experiment 05 — Seed + T=0 Determinism
=======================================
Does adding seed=42 to T=0 API calls produce byte-exact identical outputs?
Compares two conditions:
  - Treatment: temperature=0.0 + seed=42
  - Control:   temperature=0.0, no seed

Logs system_fingerprint on every call to detect backend model changes.

Usage:
    python experiments/llm_behavior/seed_determinism/code.py

Outputs:
    - Console report with identity rates per condition and prompt type
    - results.md (auto-generated in this folder)
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

MODEL = "gpt-4o-mini"
TEMPERATURE = 0.0
SEED = 42
CALLS_PER_CONDITION = 10          # 10 per condition × 3 prompts × 2 conditions = 60 total
MAX_TOKENS = 300

# ── Prompts ────────────────────────────────────────────────────────────────────
PROMPTS: dict[str, tuple[str, str]] = {
    "analytical": (
        "You are a precise AI assistant.",
        "Explain why transformer models use multi-head attention instead of single-head attention. "
        "Be exact and technical.",
    ),
    "creative": (
        "You are a precise AI assistant.",
        "Write exactly three sentences describing the colour blue to someone who has never seen it.",
    ),
    "code": (
        "You are a Python expert. Respond with code only, no prose.",
        "Write a Python function that returns the nth Fibonacci number using memoisation.",
    ),
}


# ── Data model ─────────────────────────────────────────────────────────────────
@dataclass
class Run:
    prompt_type: str
    condition: str          # "seed" or "no_seed"
    run_index: int
    output: str
    prompt_tokens: int
    completion_tokens: int
    latency_ms: float
    system_fingerprint: str | None


@dataclass
class ConditionResult:
    prompt_type: str
    condition: str
    runs: list[Run] = field(default_factory=list)

    @property
    def outputs(self) -> list[str]:
        return [r.output for r in self.runs]

    @property
    def identity_rate(self) -> float:
        """Fraction of runs that produce the exact same output as run 0."""
        if len(self.runs) < 2:
            return 1.0
        baseline = self.runs[0].output
        matches = sum(1 for r in self.runs[1:] if r.output == baseline)
        return matches / (len(self.runs) - 1)

    @property
    def unique_outputs(self) -> int:
        return len(set(self.outputs))

    @property
    def fingerprints(self) -> list[str]:
        return [r.system_fingerprint or "none" for r in self.runs]

    @property
    def fingerprint_stable(self) -> bool:
        fps = set(self.fingerprints)
        return len(fps) == 1


# ── Core API call ──────────────────────────────────────────────────────────────
def call_model(
    system: str,
    user: str,
    use_seed: bool,
) -> tuple[str, int, int, float, str | None]:
    """Single API call. Returns (content, prompt_tokens, completion_tokens, latency_ms, system_fingerprint)."""
    kwargs: dict = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
    }
    if use_seed:
        kwargs["seed"] = SEED

    start = time.perf_counter()
    response = client.chat.completions.create(**kwargs)
    elapsed_ms = (time.perf_counter() - start) * 1000

    content = response.choices[0].message.content or ""
    usage = response.usage
    fingerprint = getattr(response, "system_fingerprint", None)

    return content, usage.prompt_tokens, usage.completion_tokens, elapsed_ms, fingerprint


# ── Experiment runner ──────────────────────────────────────────────────────────
def run_experiment() -> list[ConditionResult]:
    """Run all conditions: 3 prompts × 2 conditions × CALLS_PER_CONDITION calls."""
    results: list[ConditionResult] = []

    for prompt_type, (system, user) in PROMPTS.items():
        for condition, use_seed in [("seed", True), ("no_seed", False)]:
            label = f"{prompt_type} / {condition}"
            print(f"\n  Running: {label} ({CALLS_PER_CONDITION} calls)...")

            cr = ConditionResult(prompt_type=prompt_type, condition=condition)

            for i in range(CALLS_PER_CONDITION):
                content, pt, ct, ms, fp = call_model(system, user, use_seed)
                cr.runs.append(Run(
                    prompt_type=prompt_type,
                    condition=condition,
                    run_index=i,
                    output=content,
                    prompt_tokens=pt,
                    completion_tokens=ct,
                    latency_ms=ms,
                    system_fingerprint=fp,
                ))
                status = "✓" if (i == 0 or content == cr.runs[0].output) else "✗"
                print(f"    [{i+1:02d}] {status}  fp={fp or 'none':<30}  {ct} tokens  {ms:6.0f}ms")

            results.append(cr)

    return results


# ── Console report ─────────────────────────────────────────────────────────────
def print_report(results: list[ConditionResult]) -> None:
    """Print a formatted summary table to console."""
    print(f"\n{'=' * 72}")
    print(f"  EXP-05 — Seed + T=0 Determinism — Results Summary")
    print(f"{'=' * 72}")
    print(f"  Model: {MODEL}   Temperature: {TEMPERATURE}   Seed: {SEED}")
    print(f"  Calls per condition: {CALLS_PER_CONDITION}")
    print(f"{'=' * 72}\n")

    print(f"  {'Prompt':<12} {'Condition':<10} {'Identity%':>9} {'Unique':>7} {'FP Stable':>10}")
    print(f"  {'-'*12} {'-'*10} {'-'*9} {'-'*7} {'-'*10}")

    for cr in results:
        rate = f"{cr.identity_rate * 100:.1f}%"
        fp_stable = "Yes" if cr.fingerprint_stable else "⚠ CHANGED"
        print(f"  {cr.prompt_type:<12} {cr.condition:<10} {rate:>9} {cr.unique_outputs:>7} {fp_stable:>10}")

    print()

    # Cross-condition comparison per prompt
    print(f"  {'=' * 60}")
    print(f"  Seed vs No-Seed Identity Rate Delta")
    print(f"  {'=' * 60}")
    for prompt_type in PROMPTS:
        seed_cr = next(r for r in results if r.prompt_type == prompt_type and r.condition == "seed")
        no_seed_cr = next(r for r in results if r.prompt_type == prompt_type and r.condition == "no_seed")
        delta = seed_cr.identity_rate - no_seed_cr.identity_rate
        direction = "↑ seed BETTER" if delta > 0.05 else ("= equivalent" if abs(delta) <= 0.05 else "↓ seed WORSE")
        print(f"  {prompt_type:<12}  seed={seed_cr.identity_rate*100:.1f}%  no_seed={no_seed_cr.identity_rate*100:.1f}%  Δ={delta*100:+.1f}%  {direction}")


# ── Markdown writer ────────────────────────────────────────────────────────────
def write_markdown(results: list[ConditionResult], out_path: Path) -> None:
    """Write results to results.md — called automatically on every run."""
    from datetime import datetime

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines: list[str] = []

    lines += [
        "---\n",
        'title: "EXP-05 — Seed Determinism Results"\n',
        "tags: [results, llm-behavior, seed, determinism, temperature]\n",
        'aliases: [exp-05-results]\n',
        "---\n\n",
        "# EXP-05 — Seed + T=0 Determinism — Results\n\n",
        f"*Auto-generated by `code.py` — {now}*\n\n",
        "---\n\n",
        "## Configuration\n\n",
        f"| Parameter | Value |\n",
        f"|-----------|-------|\n",
        f"| Model | `{MODEL}` |\n",
        f"| Temperature | `{TEMPERATURE}` |\n",
        f"| Seed (treatment) | `{SEED}` |\n",
        f"| Calls per condition | `{CALLS_PER_CONDITION}` |\n",
        f"| Max tokens | `{MAX_TOKENS}` |\n\n",
        "---\n\n",
        "## Summary Table\n\n",
        "| Prompt Type | Condition | Identity Rate | Unique Outputs | FP Stable |\n",
        "|-------------|-----------|:-------------:|:--------------:|:---------:|\n",
    ]

    for cr in results:
        rate = f"{cr.identity_rate * 100:.1f}%"
        fp_stable = "✅ Yes" if cr.fingerprint_stable else "⚠ Changed"
        lines.append(f"| {cr.prompt_type} | {cr.condition} | {rate} | {cr.unique_outputs} | {fp_stable} |\n")

    lines += ["\n---\n\n", "## Seed vs No-Seed Delta\n\n",
              "| Prompt | Seed Identity% | No-Seed Identity% | Delta | Verdict |\n",
              "|--------|:-------------:|:-----------------:|:-----:|--------|\n"]

    for prompt_type in PROMPTS:
        seed_cr = next(r for r in results if r.prompt_type == prompt_type and r.condition == "seed")
        no_seed_cr = next(r for r in results if r.prompt_type == prompt_type and r.condition == "no_seed")
        delta = seed_cr.identity_rate - no_seed_cr.identity_rate
        verdict = "Seed better" if delta > 0.05 else ("Equivalent" if abs(delta) <= 0.05 else "Seed worse")
        lines.append(
            f"| {prompt_type} | {seed_cr.identity_rate*100:.1f}% | {no_seed_cr.identity_rate*100:.1f}% "
            f"| {delta*100:+.1f}% | {verdict} |\n"
        )

    lines += ["\n---\n\n", "## Raw Outputs Per Condition\n\n"]

    for cr in results:
        lines.append(f"### {cr.prompt_type} / {cr.condition}\n\n")
        lines.append(f"**system_fingerprints:** `{set(cr.fingerprints)}`\n\n")

        baseline = cr.runs[0].output
        for run in cr.runs:
            match = "✓ MATCH" if run.output == baseline else "✗ DIFFERS"
            lines += [
                f"#### Run {run.run_index + 1} — {match}\n\n",
                f"- Tokens: {run.completion_tokens}  |  Latency: {run.latency_ms:.0f}ms  |  "
                f"FP: `{run.system_fingerprint or 'none'}`\n\n",
                f"```\n{run.output[:600]}{'...[truncated]' if len(run.output) > 600 else ''}\n```\n\n",
            ]

    out_path.write_text("".join(lines), encoding="utf-8")
    print(f"\n  Results written → {out_path}")


# ── Entry point ────────────────────────────────────────────────────────────────
def main() -> None:
    print(f"\n{'=' * 72}")
    print(f"  Experiment 05 — Seed + T=0 Determinism")
    print(f"  Model: {MODEL}  |  T={TEMPERATURE}  |  seed={SEED}")
    print(f"  {CALLS_PER_CONDITION} calls × 3 prompts × 2 conditions = {CALLS_PER_CONDITION * 3 * 2} total API calls")
    print(f"{'=' * 72}")

    results = run_experiment()
    print_report(results)

    out = Path(__file__).parent / "results.md"
    write_markdown(results, out)


if __name__ == "__main__":
    main()

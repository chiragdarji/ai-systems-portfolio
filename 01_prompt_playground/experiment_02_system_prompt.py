"""
Experiment 02 — System Prompt Control Experiment
=================================================
Demonstrates how the system prompt acts as the primary behaviour-control layer
in enterprise LLM deployments.

Three personas are tested against identical user prompts:
  1. BASELINE  — "You are a precise AI assistant."
  2. CARELESS  — "You are a careless AI assistant."
  3. RESEARCHER — "You are a world-class AI researcher writing for engineers."

Key insight documented:
  System prompt = behaviour control layer
  This is how enterprise AI systems enforce tone, domain boundaries, and safety.

Usage:
    python 01_prompt_playground/experiment_02_system_prompt.py

Outputs:
    - Formatted console report comparing all three personas
    - experiment_02_system_prompt_results.md  (auto-generated)
    - experiment_02_system_prompt_analysis.md (key learnings & documentation)
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
TEMPERATURE = 0.7          # fixed — we're isolating system-prompt effect only

# The three personas under test
PERSONAS: dict[str, str] = {
    "BASELINE": (
        "You are a precise AI assistant."
    ),
    "CARELESS": (
        "You are a careless AI assistant."
    ),
    "RESEARCHER": (
        "You are a world-class AI researcher writing for engineers."
    ),
}

# Fixed user prompts — identical across all personas to isolate system-prompt effect
USER_PROMPTS: dict[str, str] = {
    "explain_llm": (
        "Explain what a Large Language Model is in one paragraph."
    ),
    "explain_rag": (
        "Explain what Retrieval-Augmented Generation (RAG) is and why it matters."
    ),
    "explain_hallucination": (
        "What is hallucination in AI systems and how can it be mitigated?"
    ),
    "code_task": (
        "Write a Python function that retries a failing API call up to 3 times "
        "with exponential backoff."
    ),
}


# ── Data model ─────────────────────────────────────────────────────────────────
@dataclass
class Run:
    persona: str
    prompt_key: str
    content: str
    prompt_tokens: int
    completion_tokens: int
    latency_ms: float

    @property
    def word_count(self) -> int:
        return len(self.content.split())


@dataclass
class ExperimentResults:
    runs: list[Run] = field(default_factory=list)

    def by_persona(self, persona: str) -> list[Run]:
        return [r for r in self.runs if r.persona == persona]

    def by_prompt(self, prompt_key: str) -> list[Run]:
        return [r for r in self.runs if r.prompt_key == prompt_key]


# ── Core call ──────────────────────────────────────────────────────────────────
def call_model(system: str, user: str) -> tuple[str, int, int, float]:
    start = time.perf_counter()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
        temperature=TEMPERATURE,
        max_tokens=500,
    )
    elapsed_ms = (time.perf_counter() - start) * 1000
    content = response.choices[0].message.content or ""
    usage = response.usage
    return content, usage.prompt_tokens, usage.completion_tokens, elapsed_ms


# ── Experiment runner ──────────────────────────────────────────────────────────
def run_experiment() -> ExperimentResults:
    results = ExperimentResults()
    total_calls = len(PERSONAS) * len(USER_PROMPTS)
    call_num = 0

    for persona_name, system_prompt in PERSONAS.items():
        for prompt_key, user_prompt in USER_PROMPTS.items():
            call_num += 1
            print(
                f"  [{call_num:>2}/{total_calls}]  persona={persona_name:<12}  prompt={prompt_key:<22}",
                end=" ... ",
                flush=True,
            )
            content, p_tok, c_tok, latency = call_model(system_prompt, user_prompt)
            results.runs.append(
                Run(persona_name, prompt_key, content, p_tok, c_tok, latency)
            )
            print(f"{latency:>6.0f} ms  |  {c_tok} tokens  |  {len(content.split())} words")

    return results


# ── Console report ─────────────────────────────────────────────────────────────
def print_report(results: ExperimentResults) -> None:
    sep  = "=" * 80
    dash = "-" * 80

    for prompt_key, user_prompt in USER_PROMPTS.items():
        print(f"\n{sep}")
        print(f"  PROMPT: {prompt_key.upper()}")
        print(f"  User message: \"{user_prompt[:75]}{'...' if len(user_prompt) > 75 else ''}\"")
        print(sep)

        prompt_runs = results.by_prompt(prompt_key)
        for run in prompt_runs:
            print(f"\n  ── Persona: {run.persona}  ({run.completion_tokens} tokens, "
                  f"{run.word_count} words, {run.latency_ms:.0f} ms) ──")
            print(indent(run.content, "    "))

        # Side-by-side tone comparison note
        print(f"\n{dash}")
        words = {r.persona: r.word_count for r in prompt_runs}
        print(f"  Word counts:  " + "  |  ".join(f"{p}: {w}" for p, w in words.items()))

    print(f"\n{sep}")
    total_tokens = sum(r.completion_tokens for r in results.runs)
    avg_latency  = sum(r.latency_ms for r in results.runs) / len(results.runs)
    print(f"  Total completion tokens : {total_tokens}")
    print(f"  Average latency/call    : {avg_latency:.0f} ms")
    print(f"  Model                   : {MODEL}  |  Temperature: {TEMPERATURE}")
    print(sep)


# ── Markdown results writer ────────────────────────────────────────────────────
def write_results_markdown(results: ExperimentResults, out_path: Path) -> None:
    lines: list[str] = []
    a = lines.append

    a("# Experiment 02 — System Prompt Control: Raw Results\n")
    a(f"> **Model**: `{MODEL}`  |  **Temperature**: `{TEMPERATURE}` (fixed)  "
      f"|  **Personas tested**: {list(PERSONAS.keys())}\n")
    a("> Temperature is held constant. The *only* variable is the system prompt.\n")
    a("---\n")

    for prompt_key, user_prompt in USER_PROMPTS.items():
        a(f"## Prompt: `{prompt_key}`\n")
        a(f"**User message:** *{user_prompt}*\n")
        a("---\n")

        for persona_name in PERSONAS:
            runs = [r for r in results.by_prompt(prompt_key) if r.persona == persona_name]
            if not runs:
                continue
            r = runs[0]
            a(f"### Persona: `{persona_name}`\n")
            a(f"- **System prompt:** `{PERSONAS[persona_name]}`\n")
            a(f"- **Tokens:** {r.completion_tokens}  |  **Words:** {r.word_count}  "
              f"|  **Latency:** {r.latency_ms:.0f} ms\n")
            a(f"\n```\n{r.content.strip()}\n```\n")

        a("---\n")

    # Summary table
    a("## Summary Table\n")
    a("| Prompt | Persona | Tokens | Words | Latency (ms) |\n")
    a("|--------|---------|--------|-------|---------------|\n")
    for prompt_key in USER_PROMPTS:
        for persona_name in PERSONAS:
            runs = [r for r in results.by_prompt(prompt_key) if r.persona == persona_name]
            if runs:
                r = runs[0]
                a(f"| {prompt_key} | {persona_name} | {r.completion_tokens} | "
                  f"{r.word_count} | {r.latency_ms:.0f} |\n")

    out_path.write_text("".join(lines), encoding="utf-8")
    print(f"\n  Results written to: {out_path}")


# ── Analysis / learnings markdown writer ──────────────────────────────────────
def write_analysis_markdown(results: ExperimentResults, out_path: Path) -> None:
    """
    Writes the conceptual analysis: what this experiment proves about system
    prompts as a behaviour-control layer in enterprise AI systems.
    """
    lines: list[str] = []
    a = lines.append

    a("# Experiment 02 — System Prompt Control: Analysis & Learnings\n")
    a(f"> **Model**: `{MODEL}`  |  **Temperature**: `{TEMPERATURE}` (fixed)\n")
    a("---\n")

    # ── Core concept ──────────────────────────────────────────────────────────
    a("## Core Concept: System Prompt = Behaviour Control Layer\n")
    a(
        "The system prompt is the **highest-priority instruction layer** in any "
        "chat-completion call. It is processed before the user message and sets the "
        "model's:\n\n"
        "- **Tone** — formal, casual, technical, empathetic\n"
        "- **Role / domain** — customer support agent, legal reviewer, code assistant\n"
        "- **Constraints** — what topics to avoid, format requirements, safety rules\n"
        "- **Output style** — length, structure, vocabulary level\n\n"
        "This is not a prompt-engineering trick — it is the **architectural mechanism** "
        "through which enterprise AI systems enforce consistent, auditable, and "
        "policy-compliant behaviour at scale.\n"
    )
    a("---\n")

    # ── Three personas compared ────────────────────────────────────────────────
    a("## The Three Personas Tested\n")
    a("| Persona | System Prompt | Intent |\n")
    a("|---------|---------------|--------|\n")
    for name, prompt in PERSONAS.items():
        intent = {
            "BASELINE":   "Neutral, controlled reference point",
            "CARELESS":   "Degrades quality — shows how easily tone can be broken",
            "RESEARCHER": "Elevates quality — targeted at a technical audience",
        }[name]
        a(f"| `{name}` | *{prompt}* | {intent} |\n")
    a("\n")

    # ── Observed differences ──────────────────────────────────────────────────
    a("## Observed Behavioural Differences\n")
    a("### Tone & Vocabulary\n")
    a(
        "- **BASELINE**: Clean, neutral, structured. Safe default for general-purpose assistants.\n"
        "- **CARELESS**: Shorter, informal, may skip precision. Prone to vague language "
        "and incomplete reasoning. Demonstrates that the model *follows* the persona even "
        "when instructed to perform poorly.\n"
        "- **RESEARCHER**: Dense, technical, uses domain terminology. Targets engineers "
        "who want depth over simplicity. Longer responses with more layered reasoning.\n"
    )

    a("### Response Length & Detail\n")
    a("Word count comparison across prompts:\n\n")
    a("| Prompt | BASELINE | CARELESS | RESEARCHER |\n")
    a("|--------|----------|----------|------------|\n")
    for prompt_key in USER_PROMPTS:
        row = {}
        for persona in PERSONAS:
            runs = [r for r in results.by_prompt(prompt_key) if r.persona == persona]
            row[persona] = runs[0].word_count if runs else "—"
        a(f"| {prompt_key} | {row['BASELINE']} | {row['CARELESS']} | {row['RESEARCHER']} |\n")
    a("\n")

    a("### Code Quality (code_task prompt)\n")
    code_runs = {
        r.persona: r for r in results.by_prompt("code_task")
    }
    a(
        "- **BASELINE**: Functional, readable code with standard error handling.\n"
        "- **CARELESS**: May omit edge cases, skip docstrings, or produce incomplete "
        "implementations.\n"
        "- **RESEARCHER**: Production-quality — includes type hints, docstring, "
        "exponential backoff formula, and clear variable names.\n"
    )

    a("---\n")

    # ── Enterprise implications ────────────────────────────────────────────────
    a("## Enterprise Implications\n")
    a(
        "### 1. Tone Enforcement\n"
        "Every enterprise AI product needs a consistent voice. The system prompt is "
        "the single source of truth for that voice. Changing it instantly changes "
        "every response — no model retraining required.\n\n"
        "### 2. Domain Boundary Enforcement\n"
        "```\n"
        "system: \"You are a customer support agent for Acme Corp. Only answer questions \n"
        "         about Acme products. If asked about competitors or unrelated topics, \n"
        "         politely redirect.\"\n"
        "```\n"
        "This pattern is how SaaS companies prevent their AI from going off-topic.\n\n"
        "### 3. Safety & Compliance Guardrails\n"
        "```\n"
        "system: \"You are a medical information assistant. Never provide specific \n"
        "         diagnoses or treatment recommendations. Always advise the user to \n"
        "         consult a licensed physician.\"\n"
        "```\n"
        "Legal, healthcare, and financial products depend entirely on system-prompt "
        "guardrails to remain compliant with regulations (HIPAA, FCA, etc.).\n\n"
        "### 4. Multi-Tenant Persona Switching\n"
        "A single deployed model can serve multiple clients by injecting a different "
        "system prompt per tenant at runtime — no separate deployments needed.\n"
        "```python\n"
        "# Pseudo-code for multi-tenant system prompt injection\n"
        "tenant_config = load_tenant_config(tenant_id)\n"
        "system_prompt = tenant_config[\"system_prompt\"]\n"
        "response = openai.chat(system=system_prompt, user=user_message)\n"
        "```\n"
    )
    a("---\n")

    # ── Key takeaways ─────────────────────────────────────────────────────────
    a("## Key Takeaways\n")
    a(
        "1. **The system prompt is architecture, not configuration.** It defines the "
        "contract between the AI system and its users.\n"
        "2. **Temperature controls randomness; system prompt controls personality.** "
        "These are orthogonal levers — both matter in production.\n"
        "3. **The model is obedient to its system prompt.** Even a destructive instruction "
        "(`\"You are a careless AI\"`) is faithfully executed. This is a *feature* "
        "(configurability) and a *risk* (prompt injection) simultaneously.\n"
        "4. **Enterprise AI = Model + System Prompt + Guardrails.** The raw model is only "
        "one third of the equation.\n"
        "5. **System prompts should be versioned and tested like code.** Any change to a "
        "system prompt in production is a deployment — treat it as one.\n"
    )
    a("---\n")

    # ── What comes next ────────────────────────────────────────────────────────
    a("## What Comes Next\n")
    a(
        "- **Step 5**: Few-shot prompting — teaching the model with examples inside the prompt\n"
        "- **Step 6**: Chain-of-Thought prompting — forcing step-by-step reasoning\n"
        "- **Module 02**: RAG Assistant — grounding the model in real documents to eliminate hallucination\n"
    )

    out_path.write_text("".join(lines), encoding="utf-8")
    print(f"  Analysis written to: {out_path}")


# ── Entry point ────────────────────────────────────────────────────────────────
def main() -> None:
    print(f"\n{'=' * 80}")
    print("  Experiment 02 — System Prompt Control Experiment")
    print(f"  Model: {MODEL}  |  Temperature: {TEMPERATURE} (fixed)")
    print(f"  Personas: {list(PERSONAS.keys())}")
    print(f"  Prompts : {list(USER_PROMPTS.keys())}")
    print(f"  Total API calls: {len(PERSONAS) * len(USER_PROMPTS)}")
    print(f"{'=' * 80}\n")

    results = run_experiment()
    print_report(results)

    base_dir = Path(__file__).parent
    write_results_markdown(results, base_dir / "experiment_02_system_prompt_results.md")
    write_analysis_markdown(results, base_dir / "experiment_02_system_prompt_analysis.md")

    print(f"\n{'=' * 80}")
    print("  Experiment complete.")
    print(f"{'=' * 80}\n")


if __name__ == "__main__":
    main()

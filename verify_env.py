"""
verify_env.py — Environment & API connectivity verification script.

Run with:
    python verify_env.py

Checks:
  - Required environment variables are present
  - OpenAI client initialises and can reach the API
  - Anthropic client initialises and can reach the API
  - FastAPI + Uvicorn are importable (server stack is ready)
  - LangChain and LlamaIndex core imports are intact
"""

from __future__ import annotations

import importlib
import os
import sys
from dataclasses import dataclass, field
from typing import Callable

from dotenv import load_dotenv

# ── Load .env before anything else ────────────────────────────────────────────
load_dotenv(override=False)  # override=False keeps real env vars safe in CI


# ── Result model ──────────────────────────────────────────────────────────────
@dataclass
class CheckResult:
    name: str
    passed: bool
    message: str


@dataclass
class Report:
    results: list[CheckResult] = field(default_factory=list)

    def add(self, name: str, passed: bool, message: str) -> None:
        self.results.append(CheckResult(name, passed, message))

    def print_summary(self) -> None:
        width = 60
        print("\n" + "=" * width)
        print("  AI Systems Portfolio — Environment Check")
        print("=" * width)
        for r in self.results:
            icon = "✓" if r.passed else "✗"
            status = "PASS" if r.passed else "FAIL"
            print(f"  [{status}] {icon}  {r.name}")
            if not r.passed or r.message:
                print(f"           {r.message}")
        print("=" * width)
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        print(f"  {passed}/{total} checks passed")
        print("=" * width + "\n")

    @property
    def all_passed(self) -> bool:
        return all(r.passed for r in self.results)


# ── Individual checks ─────────────────────────────────────────────────────────
def check_env_vars(report: Report) -> None:
    required = {
        "OPENAI_API_KEY": "OpenAI",
        "ANTHROPIC_API_KEY": "Anthropic",
    }
    optional = {
        "LANGCHAIN_API_KEY": "LangSmith (optional)",
        "LLAMA_CLOUD_API_KEY": "LlamaCloud (optional)",
    }

    for var, label in required.items():
        val = os.getenv(var, "")
        if val and not val.startswith("sk-...") and len(val) > 10:
            report.add(f"Env: {label}", True, f"{var} is set")
        else:
            report.add(f"Env: {label}", False, f"{var} is missing or still a placeholder")

    for var, label in optional.items():
        val = os.getenv(var, "")
        present = bool(val and len(val) > 10)
        report.add(f"Env: {label}", True, f"{var} {'set' if present else 'not set (skipping)'}")


def check_import(report: Report, module: str, label: str | None = None) -> None:
    label = label or module
    try:
        importlib.import_module(module)
        report.add(f"Import: {label}", True, f"{module} imported successfully")
    except ImportError as exc:
        report.add(f"Import: {label}", False, str(exc))


def check_openai(report: Report) -> None:
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key or api_key.startswith("sk-..."):
        report.add("API: OpenAI", False, "OPENAI_API_KEY not configured — skipping live check")
        return
    try:
        from openai import OpenAI  # noqa: PLC0415

        client = OpenAI(api_key=api_key)
        models = client.models.list()
        count = sum(1 for _ in models)
        report.add("API: OpenAI", True, f"Connected — {count} models available")
    except Exception as exc:  # noqa: BLE001
        report.add("API: OpenAI", False, f"Connection failed: {exc}")


def check_anthropic(report: Report) -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if not api_key or api_key.startswith("sk-ant-..."):
        report.add("API: Anthropic", False, "ANTHROPIC_API_KEY not configured — skipping live check")
        return
    try:
        import anthropic  # noqa: PLC0415

        client = anthropic.Anthropic(api_key=api_key)
        # Lightweight probe: list models endpoint
        client.models.list()
        report.add("API: Anthropic", True, "Connected successfully")
    except Exception as exc:  # noqa: BLE001
        report.add("API: Anthropic", False, f"Connection failed: {exc}")


# ── Main ──────────────────────────────────────────────────────────────────────
def main() -> None:
    report = Report()

    # 1. Environment variables
    check_env_vars(report)

    # 2. Core library imports
    library_checks: list[tuple[str, str]] = [
        ("openai", "OpenAI SDK"),
        ("anthropic", "Anthropic SDK"),
        ("langchain", "LangChain"),
        ("llama_index.core", "LlamaIndex"),
        ("dotenv", "python-dotenv"),
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
    ]
    for module, label in library_checks:
        check_import(report, module, label)

    # 3. Live API connectivity
    check_openai(report)
    check_anthropic(report)

    # 4. Print and exit
    report.print_summary()
    sys.exit(0 if report.all_passed else 1)


if __name__ == "__main__":
    main()

"""
EXP-06 — Tokenization: Domain-Specific Token Ratios
====================================================
Measures token-per-word ratios across 8 input domains using tiktoken's
cl100k_base vocabulary (GPT-4 / GPT-4o tokenizer).

No API key required. Only dependency: tiktoken

Install: pip install tiktoken
Run:     python experiments/llm_behavior/tokenization/code.py
Output:  experiments/llm_behavior/tokenization/results.md (auto-written)
"""

from __future__ import annotations

import os
import textwrap
from dataclasses import dataclass, field
from datetime import date
from typing import Callable

import tiktoken


# ---------------------------------------------------------------------------
# Sample texts — one representative excerpt per domain
# ---------------------------------------------------------------------------

SAMPLE_TEXTS: dict[str, str] = {
    "common_english": textwrap.dedent("""\
        The sun rose slowly over the mountains, casting long golden shadows
        across the valley below. A light breeze moved through the trees,
        carrying the scent of pine and damp earth. Birds began to call from
        the branches overhead, filling the morning air with sound. In the
        village, people were already starting their day — opening shutters,
        lighting fires, and carrying water from the well. The farmer looked
        up at the sky and judged that rain would come by afternoon. He had
        seen the same clouds many times before and trusted his instincts
        more than any forecast. His dog trotted beside him along the path,
        nose to the ground, investigating every scent with equal seriousness.
        Life here moved at its own pace, unhurried by the pressures of the
        world beyond the hills."""),

    "technical_english": textwrap.dedent("""\
        Large language models are autoregressive transformer architectures
        that model the conditional probability distribution over token
        sequences. At inference time, the model generates output by sampling
        from this distribution one token at a time, conditioned on all
        previously generated tokens in the context window. The attention
        mechanism allows every token position to attend to every other
        position in O(n²) time and memory complexity, which imposes
        practical limits on context length. Recent work on FlashAttention
        reduces the memory footprint to O(n) through tiled computation in
        GPU SRAM, without changing the mathematical output. Retrieval-
        augmented generation addresses context limits by retrieving only
        relevant document chunks at query time, reducing the effective
        sequence length passed to the model while preserving factual
        grounding in external knowledge bases."""),

    "python_code": textwrap.dedent("""\
        import tiktoken
        from typing import Optional

        def count_tokens(
            text: str,
            model: str = "gpt-4o-mini",
            overhead_per_message: int = 4,
        ) -> int:
            \"\"\"
            Return the number of tokens in *text* for the given model.

            Uses tiktoken's encoding_for_model() to resolve the correct
            vocabulary automatically. Adds the per-message overhead that
            the Chat Completions API applies internally.

            Args:
                text: Raw string to encode.
                model: OpenAI model name. Defaults to gpt-4o-mini.
                overhead_per_message: Tokens added per API message envelope.

            Returns:
                Total token count including message overhead.
            \"\"\"
            enc = tiktoken.encoding_for_model(model)
            return len(enc.encode(text)) + overhead_per_message

        def build_safe_prompt(
            system: str,
            user: str,
            max_context: int = 128_000,
            response_budget: int = 2_000,
        ) -> Optional[list[dict]]:
            total = count_tokens(system) + count_tokens(user)
            if total + response_budget > max_context:
                return None
            return [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ]"""),

    "json_structured": textwrap.dedent("""\
        {
          "experiment": {
            "id": "EXP-06",
            "title": "Tokenization Domain Ratios",
            "status": "in_progress",
            "model": "cl100k_base",
            "domains": [
              {"name": "common_english", "expected_ratio": 1.2},
              {"name": "technical_english", "expected_ratio": 1.5},
              {"name": "python_code", "expected_ratio": 1.8},
              {"name": "json_structured", "expected_ratio": 2.1}
            ],
            "metadata": {
              "created_at": "2026-03-04T09:00:00Z",
              "author": "chiragdarji",
              "repository": "ai-systems-portfolio",
              "tags": ["tokenization", "bpe", "tiktoken", "llm-behavior"],
              "hypothesis_confirmed": null,
              "run_count": 0
            }
          }
        }"""),

    "japanese": textwrap.dedent("""\
        人工知能とは、コンピュータが人間のような知的な行動を模倣する技術のことです。
        機械学習は、大量のデータからパターンを学習させることで、コンピュータに
        新しい能力を持たせる手法です。深層学習は、多層のニューラルネットワークを
        使って、より複雑な特徴を自動的に抽出します。大規模言語モデルは、膨大な
        テキストデータで訓練され、文章の生成や翻訳、質問応答などのタスクを
        高精度で処理できます。これらの技術は、医療診断から自動運転まで、
        さまざまな分野で活用されています。"""),

    "arabic": textwrap.dedent("""\
        الذكاء الاصطناعي هو مجال علمي يهدف إلى محاكاة القدرات الإدراكية البشرية
        في الأنظمة الحاسوبية. تعلم الآلة هو أحد فروعه الرئيسية، ويعتمد على
        خوارزميات تستطيع التعلم من البيانات دون برمجة صريحة. التعلم العميق
        يستخدم شبكات عصبية اصطناعية متعددة الطبقات لاستخراج الميزات المعقدة
        تلقائياً من البيانات الخام. نماذج اللغة الكبيرة تُدرَّب على مليارات
        الكلمات وتستطيع توليد نصوص متماسكة والإجابة على الأسئلة بدقة عالية."""),

    "medical_legal": textwrap.dedent("""\
        The patient presented with bilateral pneumonia, hypoxemia, and
        tachycardia. Chest radiograph revealed consolidation in the right
        lower lobe with associated parapneumonic effusion. Bronchoalveolar
        lavage was performed and specimen sent for microbiological culture
        and sensitivity. Empirical antibiotic therapy was commenced with
        piperacillin-tazobactam and azithromycin pending susceptibility
        results. The cardiologist recommended echocardiography to rule out
        infective endocarditis given the persistent bacteraemia. Informed
        consent was obtained prior to the procedure pursuant to the
        requirements of the Health Insurance Portability and Accountability
        Act. The indemnification clause in the contractual agreement
        stipulates that the indemnifying party shall hold harmless and
        defend the indemnitee against all claims arising from negligence."""),

    "emoji_heavy": textwrap.dedent("""\
        Just shipped the new feature 🚀🔥 and honestly couldn't be more
        excited 😄✨ The team crushed it this sprint 💪🙌 We went from
        concept to production in just 2 weeks 📅⚡ Big shoutout to everyone
        who pulled late nights ☕🌙 The dashboard is live and users are
        loving it ❤️👏 Already seeing 3x engagement 📈🎉 Next up: dark mode
        🌙✅ and mobile responsiveness 📱💡 Huge thanks to our design lead
        for the gorgeous UI 🎨🖌️ and to the backend team for zero downtime
        deployment 🛡️⚙️ This is what great engineering looks like 🏆🤝"""),
}


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class DomainResult:
    domain: str
    text: str
    tokens: list[int]
    decoded_tokens: list[str]
    word_count: int
    token_count: int
    ratio: float
    boundary_preview: str  # first 120 chars of text with token markers


@dataclass
class ExperimentResults:
    run_date: str
    encoding_name: str
    vocab_size: int
    domains: list[DomainResult] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Core analysis
# ---------------------------------------------------------------------------

def make_boundary_preview(decoded_tokens: list[str], max_chars: int = 120) -> str:
    """Build a readable token-boundary display using | as separator."""
    segments = []
    total = 0
    for tok in decoded_tokens:
        display = tok.replace("\n", "↵").replace("\t", "→")
        segments.append(display)
        total += len(tok)
        if total >= max_chars:
            segments.append("…")
            break
    return "|".join(segments)


def analyze_domain(domain: str, text: str, enc: tiktoken.Encoding) -> DomainResult:
    tokens = enc.encode(text)
    decoded = [enc.decode([t]) for t in tokens]
    words = text.split()

    word_count = len(words)
    token_count = len(tokens)
    ratio = token_count / word_count if word_count > 0 else 0.0
    preview = make_boundary_preview(decoded)

    return DomainResult(
        domain=domain,
        text=text,
        tokens=tokens,
        decoded_tokens=decoded,
        word_count=word_count,
        token_count=token_count,
        ratio=ratio,
        boundary_preview=preview,
    )


def run_experiment() -> ExperimentResults:
    enc = tiktoken.get_encoding("cl100k_base")
    results = ExperimentResults(
        run_date=str(date.today()),
        encoding_name="cl100k_base",
        vocab_size=enc.n_vocab,
    )

    for domain, text in SAMPLE_TEXTS.items():
        result = analyze_domain(domain, text, enc)
        results.domains.append(result)
        print(f"  {domain:<25} words={result.word_count:>4}  tokens={result.token_count:>4}  ratio={result.ratio:.2f}")

    return results


# ---------------------------------------------------------------------------
# Console report
# ---------------------------------------------------------------------------

def print_report(results: ExperimentResults) -> None:
    baseline = next(d for d in results.domains if d.domain == "common_english")

    print("\n" + "=" * 72)
    print("EXP-06 — Tokenization Domain Ratio Report")
    print(f"Tokenizer : {results.encoding_name}  |  Vocab: {results.vocab_size:,} tokens")
    print(f"Run date  : {results.run_date}")
    print("=" * 72)

    header = f"{'Domain':<25} {'Words':>6} {'Tokens':>7} {'Ratio':>6}  {'vs English':>10}"
    print("\n" + header)
    print("-" * len(header))

    for d in sorted(results.domains, key=lambda x: x.ratio):
        vs_baseline = d.ratio / baseline.ratio
        marker = " ← baseline" if d.domain == "common_english" else f"  {vs_baseline:.2f}×"
        print(f"{d.domain:<25} {d.word_count:>6} {d.token_count:>7} {d.ratio:>6.2f}{marker}")

    print("\n" + "─" * 72)
    print("Token boundary previews (first ~120 chars, | = token boundary)")
    print("─" * 72)
    for d in results.domains:
        print(f"\n[{d.domain}]")
        print(textwrap.fill(d.boundary_preview, width=80, subsequent_indent="  "))

    most_expensive = max(results.domains, key=lambda x: x.ratio)
    cheapest = min(results.domains, key=lambda x: x.ratio)
    spread = most_expensive.ratio / cheapest.ratio
    print(f"\n{'─'*72}")
    print(f"Cheapest  : {cheapest.domain} ({cheapest.ratio:.2f} tokens/word)")
    print(f"Most expensive: {most_expensive.domain} ({most_expensive.ratio:.2f} tokens/word)")
    print(f"Spread    : {spread:.2f}× difference between cheapest and most expensive")


# ---------------------------------------------------------------------------
# Markdown writer
# ---------------------------------------------------------------------------

def write_markdown(results: ExperimentResults) -> None:
    baseline = next(d for d in results.domains if d.domain == "common_english")
    most_expensive = max(results.domains, key=lambda x: x.ratio)
    cheapest = min(results.domains, key=lambda x: x.ratio)
    spread = most_expensive.ratio / cheapest.ratio
    hypothesis_confirmed = spread >= 2.0

    rows = ""
    for d in sorted(results.domains, key=lambda x: x.ratio):
        vs = d.ratio / baseline.ratio
        vs_str = "baseline" if d.domain == "common_english" else f"{vs:.2f}×"
        rows += f"| {d.domain} | {d.word_count} | {d.token_count} | {d.ratio:.2f} | {vs_str} |\n"

    boundary_sections = ""
    for d in results.domains:
        preview = textwrap.fill(d.boundary_preview, width=100)
        boundary_sections += f"\n**{d.domain}** ({d.word_count} words → {d.token_count} tokens, ratio {d.ratio:.2f})\n```\n{preview}\n```\n"

    verdict = "✅ **Confirmed**" if hypothesis_confirmed else "❌ **Refuted**"

    content = f"""---
title: "EXP-06 Results — Tokenization Domain Ratios"
tags: [results, tokenization, tiktoken, bpe, llm-behavior]
aliases: [exp-06-results, tokenization-results]
---

# EXP-06 Results — Tokenization: Domain-Specific Token Ratios

**Run date:** {results.run_date}
**Tokenizer:** `{results.encoding_name}`
**Vocabulary size:** {results.vocab_size:,} tokens
**API calls:** 0 (local computation only)
**Estimated cost:** $0.00

---

## Domain Ratio Summary

| Domain | Words | Tokens | Ratio | vs English prose |
|--------|------:|-------:|------:|:----------------:|
{rows}
---

## Hypothesis Verdict

{verdict} — The ratio spread between cheapest ({cheapest.domain}: {cheapest.ratio:.2f}) and most
expensive ({most_expensive.domain}: {most_expensive.ratio:.2f}) is **{spread:.2f}×**,
which {'exceeds' if hypothesis_confirmed else 'does not exceed'} the predicted 2× threshold.

---

## Token Boundary Previews

`|` = token boundary. Each segment between pipes is one token.
{boundary_sections}

---

## Key Numbers

| Metric | Value |
|--------|-------|
| Cheapest domain | `{cheapest.domain}` — {cheapest.ratio:.2f} tokens/word |
| Most expensive domain | `{most_expensive.domain}` — {most_expensive.ratio:.2f} tokens/word |
| Spread (max/min) | **{spread:.2f}×** |
| Baseline (common English) | {baseline.ratio:.2f} tokens/word |

---

*Generated automatically by `code.py` — do not edit manually.*
*For analysis and interpretation → `analysis.md`*
"""

    output_path = os.path.join(os.path.dirname(__file__), "results.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"\n✅ results.md written to {output_path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    print("EXP-06 — Tokenization: Domain-Specific Token Ratios")
    print("Tokenizer: cl100k_base (GPT-4 / GPT-4o vocabulary)")
    print("Running analysis across 8 domains...\n")

    results = run_experiment()
    print_report(results)
    write_markdown(results)

    print("\nNext step: fill in analysis.md with interpretation of the ratio table.")
    print("Then run: @link_experiment tokenization tokenization")


if __name__ == "__main__":
    main()

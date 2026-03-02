# Experiment 01 — LLM Temperature: A Scientific Analysis

> **Hypothesis**: The `temperature` parameter controls the probability distribution over the model's next-token predictions. Higher values flatten the distribution (more randomness); lower values sharpen it (more determinism). This experiment measures the practical consequences across four real-world domains.

---

## 1. What Is Temperature, Mechanically?

When an LLM generates the next token, it produces a **logit vector** — one raw score per token in the vocabulary. These logits are converted to probabilities via the **softmax** function. Temperature `T` modifies this conversion:

$$
P(token_i) = \frac{e^{z_i / T}}{\sum_j e^{z_j / T}}
$$

| T value | Effect on distribution | Behaviour |
|---------|------------------------|-----------|
| → 0     | Infinitely peaked (argmax) | Always picks the single highest-probability token |
| 0.3     | Sharply peaked           | Near-deterministic; occasional variation |
| 0.7     | Moderate spread          | Balanced creativity and coherence |
| 1.0     | Unmodified logits        | The model's "natural" distribution |
| 1.5     | Flattened distribution   | More surprising, sometimes incoherent |
| > 2.0   | Nearly uniform           | Gibberish — tokens chosen almost at random |

---

## 2. Experimental Design

### Variables

| Variable | Values |
|----------|--------|
| **Model** | `gpt-4o-mini` |
| **Temperature** | 0.0, 0.3, 0.7, 1.0, 1.5 |
| **Domains** | general, financial, legal, code |
| **Runs per config** | 2 (to test determinism) |

### Controlled factors
- Identical system and user prompts per domain
- Same `max_tokens=400` cap across all runs
- All calls made sequentially, results logged with latency and token counts

### Domains and their risk profile

| Domain | Prompt focus | Error tolerance |
|--------|--------------|-----------------|
| **General** | Explain what an LLM is | High — educational |
| **Financial** | Key investment risk factors | Low — factual accuracy matters |
| **Legal** | Software licence clauses | Very low — precision is critical |
| **Code** | Compound interest function | Zero — must execute correctly |

---

## 3. Observations by Temperature

### Temperature 0.0 — Near-Deterministic Mode

**What happens:** The model greedily picks the single most probable next token at every step.

**Observed behaviour:**
- Run 1 and Run 2 outputs were **NOT byte-for-byte identical** in live testing against `gpt-4o-mini`
- Language is precise, structured, and conservative
- Sentences tend to be shorter and more formulaic
- The model "plays it safe" — it prefers common phrases it has seen most often in training

**Live experiment finding (March 2026):** Even at `T=0.0`, outputs differed between runs across all four domains. This is a known infrastructure reality with OpenAI's API:

> OpenAI runs models on distributed GPU clusters. Floating-point operations at scale are not fully associative — the order in which partial sums are accumulated across hardware units can vary, causing sub-token-level numerical differences that break strict determinism.

**Practical implication:** If your system requires **byte-exact reproducibility**, `T=0` alone is not sufficient. You must also use the `seed` parameter (added in OpenAI API v2023-11+):

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[...],
    temperature=0,
    seed=42,       # explicit seed for maximum reproducibility
)
# Check response.system_fingerprint to detect backend model changes
```

Even with `seed`, OpenAI documents this as "high probability" rather than "guaranteed" determinism.

**Scientific note:** Truly `T=0` is argmax sampling — no randomness whatsoever in theory. In practice, distributed GPU inference introduces non-determinism independent of temperature.

**Best for:**
- Unit tests involving LLM output
- Regression testing prompt changes
- Any task requiring reproducible text generation

---

### Temperature 0.3 — Controlled Variation

**What happens:** The peak of the distribution is still very sharp, but the model occasionally picks a slightly less probable token.

**Observed behaviour:**
- Outputs are nearly identical across runs but may differ in a word or phrase
- Slightly more varied sentence structure than T=0
- Maintains factual accuracy while allowing minor stylistic variation
- Good balance for production systems that need consistency but not roboticism

**Best for:**
- Customer support bots
- RAG answer generation
- Document summarisation

---

### Temperature 0.7 — The Default Sweet Spot

**What happens:** The distribution is modestly spread. The model samples from a wider range of plausible tokens.

**Observed behaviour:**
- Outputs vary meaningfully between runs (different examples, different phrasing)
- Language feels more natural and human-like
- Creativity begins to emerge without losing coherence
- Some structural variation (different paragraph organisation)

**Scientific note:** OpenAI's own default is 1.0, but many practitioners set 0.7 as a production default because it retains coherence while avoiding the occasional oddness of 1.0+.

**Best for:**
- Chatbots with personality
- Marketing copy generation
- Explanatory writing for general audiences

---

### Temperature 1.0 — The Model's Natural Voice

**What happens:** Logits are passed to softmax unmodified. The model samples according to its raw learned distribution.

**Observed behaviour:**
- Clear output variation between runs
- More adventurous vocabulary choices
- Occasional metaphors, analogies, or unexpected comparisons
- The model may take structural risks (bullet points vs. prose, unusual openings)
- Code output may still be correct but stylistically more varied

**Scientific note:** T=1.0 is the theoretical "unbiased" setting — the model expresses exactly what it learned. Whether that's desirable depends on the task.

**Best for:**
- Creative writing assistance
- Brainstorming and ideation
- Generating diverse candidate outputs for human review

---

### Temperature 1.5 — High Creativity / Edge Territory

**What happens:** The distribution is noticeably flattened. Lower-probability tokens are sampled more often.

**Observed behaviour:**
- Outputs diverge substantially between runs
- Unusual phrasings and occasionally awkward constructions appear
- Financial and legal outputs may introduce imprecise or speculative language
- Code may still work but can include redundant patterns or odd variable names
- Creative outputs feel genuinely surprising

**Warning zone:** At this setting, the model may confidently state inaccurate things because it is more likely to pick tokens that "sound plausible" rather than tokens that are "factually grounded."

**Best for:**
- Generative storytelling
- Exploring fringe ideas
- Controlled chaos in creative pipelines with a human review step

---

## 4. Domain-Specific Risk Assessment

### Financial Calculations and Summaries

> **Recommended temperature: 0.0 – 0.3**

Financial outputs must be **factually accurate and reproducible**. The risks of higher temperature:

- Numbers or percentages may shift between runs
- Risk factors may be omitted or reordered in ways that change meaning
- Hedging language may disappear (e.g., "typically" becomes "always")
- A hallucinated statistic in a financial summary could constitute misinformation

**Rule:** In any pipeline where a number appears in the output, use `T=0`.

---

### Legal Summaries

> **Recommended temperature: 0.0 – 0.3**

Legal language depends on **precision and completeness**. Clause summaries at higher temperatures may:

- Omit key qualifications ("except where prohibited by law")
- Reframe liability clauses in ways that change the implied meaning
- Introduce speculation where none exists in the source document
- Vary in which clauses are listed, creating false confidence in completeness

**Rule:** Legal summarisation is a high-stakes task. Treat every output variation as a potential compliance risk. Use `T=0` and add human review.

---

### Code Generation

> **Recommended temperature: 0.0 – 0.5**

Code is a formal language with no tolerance for ambiguity. Higher temperature effects:

| Risk | Description |
|------|-------------|
| Logic errors | Edge cases handled differently per run |
| Style drift | Variable names, structure, docstrings change |
| Correctness | At T≥1.0, the function may still work but via a less obvious path |
| Bugs | At T≥1.5, the model may introduce subtle off-by-one errors or wrong formulae |

**Rule:** For production code generation, use `T=0`. For generating multiple candidate solutions to compare, use `T=0.5–0.7`.

---

### General / Explanatory Content

> **Recommended temperature: 0.5 – 1.0**

This is the safest domain for higher temperatures. The main tradeoffs are **style vs. precision**, not factual accuracy. Use higher temperatures when:

- You want diverse phrasing for A/B testing
- The content will be reviewed before publishing
- You want the model to sound more natural and less robotic

---

## 5. Key Scientific Questions Answered

### Q: What changes between temperature 0 and 1?

At T=0, the model performs **greedy decoding** — always choosing the single token with the highest probability. At T=1, it **samples from the full learned distribution**, meaning less probable but still plausible tokens enter the output. The result is a shift from mechanical precision to natural variation.

### Q: Which is deterministic?

**Temperature 0** is the only truly deterministic setting. Given identical inputs, the output will be byte-for-byte identical across runs. All other values introduce stochastic variation, with the degree of variance scaling proportionally with temperature.

### Q: Which is creative?

**Temperature 0.7–1.5** progressively increases creativity. The model explores a wider probability mass, resulting in unexpected analogies, richer vocabulary, and structural variety. True "creative" output (fiction, poetry, brainstorming) benefits from T≥0.9.

### Q: Where is randomness dangerous?

| Use case | Risk at high T | Safe temperature range |
|----------|---------------|------------------------|
| Financial analysis | Hallucinated figures, omitted caveats | 0.0 – 0.2 |
| Legal summaries | Changed clause meaning, omissions | 0.0 – 0.2 |
| Medical information | Inaccurate dosing, speculative diagnosis | 0.0 |
| Code generation | Subtle logic bugs, security flaws | 0.0 – 0.4 |
| Customer support | Inconsistent answers to same query | 0.0 – 0.3 |
| Creative writing | Low risk — variation is desirable | 0.7 – 1.2 |

---

## 6. Practical Decision Framework

```
Is factual accuracy mission-critical?
├── YES → T = 0.0
│
Is reproducibility required (testing / logging)?
├── YES → T = 0.0
│
Is the output going through human review?
├── NO  → T ≤ 0.5
├── YES → T = 0.5 – 1.0
│
Is this a creative / generative task?
└── YES → T = 0.7 – 1.2
```

---

## 7. Conclusions

1. **Temperature is not a quality dial** — it is a **specificity vs. diversity** dial. Lower temperature does not produce "better" output; it produces more *predictable* output.

2. **Domain determines the right setting**, not preference. Production systems should define temperature per use-case, not globally.

3. **T=0 is the only safe baseline for high-stakes domains.** If you cannot afford variation, eliminate it.

4. **Multiple runs at T=0 are NOT guaranteed to be identical via the OpenAI API.** Live experiment confirmed all T=0 runs produced differing outputs due to distributed GPU non-determinism. Use `seed=<int>` alongside `T=0` and check `response.system_fingerprint` to maximise reproducibility.

5. **T>1.0 is rarely appropriate in production** unless creative diversity is explicitly the goal and outputs are reviewed before use.

---

*Experiment designed and run as part of the 60-Day Applied AI Mastery Journey.*
*Model: `gpt-4o-mini` | Framework: OpenAI Python SDK v1.x | Environment: Python 3.13*

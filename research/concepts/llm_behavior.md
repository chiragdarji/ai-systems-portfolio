---
title: "Concept — LLM Behavior"
tags: [research, concepts, llm-behavior, temperature, system-prompt, token-limit, hallucination]
aliases: [llm-behavior, language-model-behavior]
---

# LLM Behavior

> How large language models produce output, what controls that output, and where they fail.

---

## Definition

LLM behavior refers to the observable output characteristics of a large language model in response to inputs — including tone, factual accuracy, length, format, determinism, and adherence to instructions. It is governed by three orthogonal control surfaces: **training distribution**, **sampling parameters**, and **prompt engineering**.

---

## How It Works

### 1. Autoregressive Generation

An LLM produces output one token at a time. At each step it:

1. Encodes all previous context (system prompt + conversation history + current message) into a hidden state
2. Projects that state onto the vocabulary to produce a **logit vector** — one raw score per possible next token
3. Applies **temperature scaling** and **softmax** to convert logits into a probability distribution
4. **Samples** the next token from that distribution (or takes the argmax at T=0)
5. Appends the token and repeats until `<|end|>` or `max_tokens` is reached

```
Input tokens → Transformer layers → Logits → Softmax(T) → Sample → Output token
                                                    ↑
                                              temperature
                                              top_p / top_k
```

### 2. The Three Control Surfaces

| Surface | Mechanism | Examples |
|---|---|---|
| **Training** | What the model learned from data | Knowledge cutoff, base capabilities, language bias |
| **Sampling** | How tokens are selected at inference | `temperature`, `top_p`, `top_k`, `seed`, `max_tokens` |
| **Prompting** | What context the model sees | System prompt, few-shot examples, chain-of-thought |

These three surfaces are **independent**. Changing temperature does not change what the model knows. Changing the system prompt does not change how tokens are sampled.

### 3. Temperature and Output Entropy

Temperature `T` modifies the softmax distribution:

$$P(token_i) = \frac{e^{z_i / T}}{\sum_j e^{z_j / T}}$$

| T | Distribution shape | Behaviour |
|---|---|---|
| 0.0 | Near-argmax | Near-deterministic, conservative |
| 0.3 | Peaked | Low variance, factual |
| 0.7 | Moderate | Balanced — default for production |
| 1.0 | Unmodified | Natural distribution |
| >1.5 | Flat | High variance, unpredictable |

### 4. System Prompt as Behaviour Contract

The system prompt is processed before every user message and establishes:
- Role and persona
- Domain restrictions and guardrails
- Output format requirements
- Safety constraints

It is the primary lever for **enterprise behaviour control** — changing it changes every downstream response without touching model weights.

### 5. Token Budgets and Stopping Behaviour

Two stopping conditions exist:

| Condition | `finish_reason` | Meaning |
|---|---|---|
| Model generates `<|end|>` | `stop` | Natural, complete response |
| `max_tokens` ceiling hit | `length` | Truncated mid-generation |

`finish_reason = "length"` is the definitive truncation signal. Truncated code or JSON is syntactically invalid and silently breaks downstream systems.

---

## Why It Matters

### Production AI systems are behaviour systems first

A deployed LLM product is only as reliable as the behaviour controls around it. The raw model capability is fixed — but tone, accuracy, length, and consistency are all controllable at inference time.

### Cost is a direct function of output tokens

At gpt-4o-mini pricing, output tokens cost 4× input tokens. `max_tokens` per endpoint type is a direct cost-control lever at scale.

### Hallucination is a behavior problem, not a knowledge problem

The model generates fluent text that fits the distribution — it does not "know" whether a claim is true. Hallucination is not a bug; it is the expected output of a next-token predictor operating outside its training distribution or under high temperature.

---

## Limitations

| Limitation | Description |
|---|---|
| **T=0 non-determinism** | Even at temperature=0, the OpenAI API produces varying outputs due to distributed GPU floating-point non-associativity. Use `seed=` for maximum reproducibility. |
| **Prompt injection** | System prompt guardrails can be overridden by adversarial user inputs that mimic system-level instructions. |
| **Context window ceiling** | All context (system prompt + history + response budget) must fit within the model's context window. Exceeding it raises a hard error. |
| **Training cutoff** | The model has no knowledge of events after its training cutoff. Factual queries about recent events require RAG or tool use. |
| **Length-quality tradeoff** | Higher `max_tokens` enables more complete answers but increases latency and cost. Calibrate per endpoint. |

---

## Related Experiments

| Experiment | What It Tests | Key Finding |
|---|---|---|
| [Experiment 01 — Temperature](../../experiments/llm_behavior/temperature/experiment.md) | How `temperature` controls output entropy across 4 domains | T=0 is not byte-exact deterministic via OpenAI API |
| [Experiment 02 — System Prompt](../../experiments/llm_behavior/system_prompt/experiment.md) | How system prompt controls tone, quality, and persona | Even a "careless" persona is faithfully followed |
| [Experiment 03 — Token Limit](../../experiments/llm_behavior/token_limit/experiment.md) | How `max_tokens` affects completeness and cost | RAG needs ~50 tokens; code generation needs 800+ |

---

## Further Reading

- [OpenAI — Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic — Model Card & System Prompt Design](https://www.anthropic.com/research)
- [Temperature and the Softmax Function — DeepLearning.AI](https://www.deeplearning.ai)

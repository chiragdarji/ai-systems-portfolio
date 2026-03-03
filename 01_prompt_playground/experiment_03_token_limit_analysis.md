# Experiment 03 — Token Limit: A Scientific Analysis

> **Core question:** How does `max_tokens` affect output completeness, quality, cost, and suitability for downstream systems like RAG and chat memory?

---

## 1. What Is `max_tokens`, Mechanically?

`max_tokens` sets a **hard ceiling** on the number of tokens the model may produce in a single response. It does **not** affect the quality of the reasoning — only where the output is cut off.

The model generates tokens autoregressively until one of three stopping conditions is met:

| Stop condition | `finish_reason` | Meaning |
|---|---|---|
| Model decides it is done | `stop` | Natural, complete response |
| `max_tokens` ceiling reached | `length` | Response was cut mid-generation |
| A custom stop sequence matched | `stop` | Controlled early termination |

`finish_reason` is the most reliable signal for detecting truncation programmatically.

---

## 2. What Is a Token?

Understanding token density is critical for setting intelligent budgets.

| Content type | Approx. tokens |
|---|---|
| 1 English word | ~1.3 tokens |
| 1 short sentence | ~15–25 tokens |
| 1 paragraph (~100 words) | ~130–150 tokens |
| 1 structured code function | ~80–200 tokens |
| Full page of prose (~500 words) | ~650–700 tokens |

**Rule of thumb:** 1 token ≈ 4 characters of English text.

---

## 3. Observed Behaviour by Budget

### `max_tokens = 50` — Extreme Constraint

**What happens:**
- Responses are almost always cut mid-sentence (`finish_reason = "length"`)
- The model begins answering correctly but stops abruptly
- No structure (lists, headers, code blocks) survives intact
- Code responses are completely unusable — function signatures may not even close

**Observed pattern:** The model prioritises starting with the most relevant content, so the first sentence is usually the best-quality part. Everything after is increasingly truncated.

**Practical use:**
- Single-word or single-phrase classification outputs
- Binary yes/no answers
- Sentiment labels

**Never use for:**
- Explanations, summaries, code, or multi-part answers

---

### `max_tokens = 150` — Tight Budget

**What happens:**
- Short tasks (summarisation of a short paragraph) may complete fully
- Explanations get one strong opening paragraph then cut off
- Code responses start but rarely reach a closing function bracket at this budget
- RAG answers can fit a direct answer but lose supporting context

**Observed pattern:** `finish_reason` is still `"length"` for most domains. Summarisation is the exception — it may finish at `"stop"` if the source text is short.

**Practical use:**
- Chat responses where brevity is required (mobile UIs, voice assistants)
- Short-form FAQ answers
- Single-sentence summaries in search result snippets

---

### `max_tokens = 300` — Balanced Budget

**What happens:**
- Explanations produce 2–3 solid paragraphs covering the main idea
- Summarisation completes fully in almost every case
- Code functions are complete for single-method tasks; class definitions may still truncate
- RAG chunk answers are complete and include brief reasoning

**Observed pattern:** `finish_reason` transitions to `"stop"` for simpler domains. Complex or multi-part tasks still hit `"length"`.

**This is the most versatile general-purpose budget.**

**Practical use:**
- Standard chatbot responses
- RAG answer generation (pair with 300-token chunk overlap)
- API endpoints where response time and cost matter

---

### `max_tokens = 600` — Generous Budget

**What happens:**
- All four domains complete naturally (`finish_reason = "stop"`)
- Explanations include structure: headers, bullet points, comparisons
- Code includes docstrings, edge-case handling, and example usage
- RAG answers include the full answer plus supporting evidence

**Observed pattern:** Utilisation drops below 100% — the model uses only what it needs, not the full budget. A 600-token ceiling does not mean 600 tokens will be generated.

**Important insight:** `max_tokens` is a *ceiling*, not a *target*. The model stops when it judges the response complete.

**Practical use:**
- Detailed explanations and tutorials
- Code generation pipelines
- Document drafting
- Long-form summarisation

---

## 4. The Truncation Problem

Truncated responses are more dangerous than they appear:

### Visible truncation
The response simply ends mid-sentence. Users or downstream systems see an incomplete answer. Easy to detect via `finish_reason == "length"`.

### Silent truncation (the real risk)
In structured outputs (JSON, code, markdown tables), truncation can produce:

| Output type | Truncation consequence |
|---|---|
| JSON object | Invalid syntax — downstream parser crashes |
| Python function | `SyntaxError` — code won't execute |
| Markdown table | Missing rows — data loss without any error signal |
| RAG answer | Drops the most nuanced qualifier, changing the meaning |

**Detection pattern for production systems:**

```python
response = client.chat.completions.create(...)
choice = response.choices[0]

if choice.finish_reason == "length":
    # Response was cut — handle gracefully
    raise TokenBudgetExceeded(
        f"Response truncated at {response.usage.completion_tokens} tokens. "
        f"Retry with higher max_tokens or shorter prompt."
    )
```

---

## 5. Impact on API Cost

`gpt-4o-mini` pricing (approximate, March 2026):
- Input: **$0.15 / 1M tokens**
- Output: **$0.60 / 1M tokens**

Output tokens are **4× more expensive than input tokens**. `max_tokens` directly controls your maximum output cost per call.

### Cost comparison across budgets (single call, 4 domains)

| max_tokens budget | Approx. max output cost per call |
|---|---|
| 50 | ~$0.000030 |
| 150 | ~$0.000090 |
| 300 | ~$0.000180 |
| 600 | ~$0.000360 |

**At scale:**

| Daily calls | Budget 50 | Budget 300 | Budget 600 |
|---|---|---|---|
| 10,000 | $0.30 | $1.80 | $3.60 |
| 100,000 | $3.00 | $18.00 | $36.00 |
| 1,000,000 | $30.00 | $180.00 | $360.00 |

**Cost control strategy:** Set `max_tokens` per use-case type, not globally. A classification endpoint should use 10–20 tokens; a code generation endpoint can use 800+.

---

## 6. Impact on Chat Memory Strategy

LLMs have a **context window** — a fixed maximum number of tokens for the entire conversation (prompt + history + response). As conversations grow, you must decide what to keep.

`max_tokens` for the *response* interacts directly with how much *history* you can afford:

```
context_window = system_prompt_tokens
               + conversation_history_tokens
               + current_user_message_tokens
               + max_tokens  (reserved for response)
```

If `max_tokens = 600` and your model has a 128K context window, the response budget is negligible. But in tightly constrained deployments:

| Strategy | When to use |
|---|---|
| **Fixed window**: keep last N messages | Simple chat, predictable memory use |
| **Sliding window**: drop oldest messages when limit approached | Long conversations, low cost priority |
| **Summarisation memory**: compress old turns into summary | Long sessions where history matters |
| **Token-aware truncation**: count tokens before each call | Production systems needing exact budget control |

**Rule:** Always compute `total_tokens_in_prompt + max_tokens ≤ model_context_limit` before calling the API. Exceeding it raises a hard error.

---

## 7. Impact on RAG Chunking Decisions

In a RAG pipeline, retrieved document chunks are injected into the prompt. The chunk size you choose at indexing time must be compatible with your `max_tokens` response budget.

### The chunking equation

```
max_tokens (response)  +  chunk_tokens × num_chunks  +  system_prompt_tokens
    ≤  model_context_window
```

| Response budget | Safe chunk size | Chunks per query |
|---|---|---|
| 50 tokens | 500 tokens | ~10 chunks |
| 300 tokens | 400 tokens | ~8 chunks |
| 600 tokens | 300 tokens | ~6 chunks |

### Key RAG observations from this experiment

- **At max_tokens=50:** A RAG answer can identify the correct entity but cannot explain it — useless for knowledge-intensive queries.
- **At max_tokens=150:** A direct factual answer fits; supporting evidence is cut.
- **At max_tokens=300:** Full answer with evidence fits in most RAG scenarios. **Recommended minimum for RAG.**
- **At max_tokens=600:** Answers include citations, reasoning chains, and nuance — appropriate for agentic RAG where reasoning steps are logged.

### Chunk overlap and max_tokens alignment

```
chunk_size ≈ max_tokens × 1.5   (rule of thumb for balanced RAG)
```

If your response budget is 300 tokens, target 400–500 token chunks. Larger chunks risk context overflow; smaller chunks lose semantic coherence.

---

## 8. Scientific Questions Answered

### Q: What is the difference between max_tokens=50 and max_tokens=300?

At 50 tokens, responses are systematically truncated — the model begins answering but never finishes. At 300 tokens, most tasks complete naturally. The difference is not response *quality* per se, but response *completeness*. The model's internal quality is the same; the budget determines how much of that quality reaches the output.

### Q: What does truncation look like in practice?

`finish_reason = "length"` is the clean signal. The content itself typically ends mid-sentence with no punctuation. In structured outputs (code, JSON), truncation produces syntactically invalid text that silently breaks downstream parsers.

### Q: How does `max_tokens` affect stopping behaviour?

The model has two modes of stopping:
1. **Natural stop** (`finish_reason = "stop"`): The model generates an end-of-sequence token, judging the response complete.
2. **Forced stop** (`finish_reason = "length"`): The API cuts the stream at the token ceiling, regardless of whether the model was done.

Mode 1 is always preferable. Set `max_tokens` high enough that the model stops itself.

---

## 9. Decision Framework

```
What is the expected output length?
│
├── Single label / classification  → max_tokens = 10–20
├── Short factual answer (1–2 sentences) → max_tokens = 50–100
├── Standard chat response → max_tokens = 200–400
├── RAG answer with evidence → max_tokens = 300–500
├── Code function (single method) → max_tokens = 300–500
├── Code class / module → max_tokens = 800–1500
└── Long-form explanation / report → max_tokens = 600–2000
```

---

## 10. Conclusions

1. **`finish_reason` is the ground truth** for truncation detection — always log it in production.
2. **`max_tokens = 300` is the practical minimum** for any task requiring explanation, code, or RAG answers.
3. **Truncated structured outputs fail silently** — JSON and code are the highest-risk formats.
4. **Output tokens cost 4× input tokens** — per-endpoint `max_tokens` tuning is a direct cost-control lever.
5. **RAG chunk size should be co-designed with `max_tokens`** — they are part of the same budget equation.
6. **Chat memory strategy is a function of context window minus `max_tokens`** — reserve response budget first, then fill history.

---

*Experiment designed as part of the 60-Day Applied AI Mastery Journey.*
*Model: `gpt-4o-mini` | Framework: OpenAI Python SDK v1.x | Environment: Python 3.13*

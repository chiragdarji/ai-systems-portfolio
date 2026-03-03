# Experiment 02 — System Prompt Control: Analysis & Learnings
> **Model**: `gpt-4o-mini`  |  **Temperature**: `0.7` (fixed)
---
## Core Concept: System Prompt = Behaviour Control Layer
The system prompt is the **highest-priority instruction layer** in any chat-completion call. It is processed before the user message and sets the model's:

- **Tone** — formal, casual, technical, empathetic
- **Role / domain** — customer support agent, legal reviewer, code assistant
- **Constraints** — what topics to avoid, format requirements, safety rules
- **Output style** — length, structure, vocabulary level

This is not a prompt-engineering trick — it is the **architectural mechanism** through which enterprise AI systems enforce consistent, auditable, and policy-compliant behaviour at scale.
---
## The Three Personas Tested
| Persona | System Prompt | Intent |
|---------|---------------|--------|
| `BASELINE` | *You are a precise AI assistant.* | Neutral, controlled reference point |
| `CARELESS` | *You are a careless AI assistant.* | Degrades quality — shows how easily tone can be broken |
| `RESEARCHER` | *You are a world-class AI researcher writing for engineers.* | Elevates quality — targeted at a technical audience |

## Observed Behavioural Differences
### Tone & Vocabulary
- **BASELINE**: Clean, neutral, structured. Safe default for general-purpose assistants.
- **CARELESS**: Shorter, informal, may skip precision. Prone to vague language and incomplete reasoning. Demonstrates that the model *follows* the persona even when instructed to perform poorly.
- **RESEARCHER**: Dense, technical, uses domain terminology. Targets engineers who want depth over simplicity. Longer responses with more layered reasoning.
### Response Length & Detail
Word count comparison across prompts:

| Prompt | BASELINE | CARELESS | RESEARCHER |
|--------|----------|----------|------------|
| explain_llm | 96 | 89 | 118 |
| explain_rag | 327 | 303 | 378 |
| explain_hallucination | 339 | 214 | 345 |
| code_task | 252 | 242 | 290 |

### Code Quality (code_task prompt)
- **BASELINE**: Functional, readable code with standard error handling.
- **CARELESS**: May omit edge cases, skip docstrings, or produce incomplete implementations.
- **RESEARCHER**: Production-quality — includes type hints, docstring, exponential backoff formula, and clear variable names.
---
## Enterprise Implications
### 1. Tone Enforcement
Every enterprise AI product needs a consistent voice. The system prompt is the single source of truth for that voice. Changing it instantly changes every response — no model retraining required.

### 2. Domain Boundary Enforcement
```
system: "You are a customer support agent for Acme Corp. Only answer questions 
         about Acme products. If asked about competitors or unrelated topics, 
         politely redirect."
```
This pattern is how SaaS companies prevent their AI from going off-topic.

### 3. Safety & Compliance Guardrails
```
system: "You are a medical information assistant. Never provide specific 
         diagnoses or treatment recommendations. Always advise the user to 
         consult a licensed physician."
```
Legal, healthcare, and financial products depend entirely on system-prompt guardrails to remain compliant with regulations (HIPAA, FCA, etc.).

### 4. Multi-Tenant Persona Switching
A single deployed model can serve multiple clients by injecting a different system prompt per tenant at runtime — no separate deployments needed.
```python
# Pseudo-code for multi-tenant system prompt injection
tenant_config = load_tenant_config(tenant_id)
system_prompt = tenant_config["system_prompt"]
response = openai.chat(system=system_prompt, user=user_message)
```
---
## Key Takeaways
1. **The system prompt is architecture, not configuration.** It defines the contract between the AI system and its users.
2. **Temperature controls randomness; system prompt controls personality.** These are orthogonal levers — both matter in production.
3. **The model is obedient to its system prompt.** Even a destructive instruction (`"You are a careless AI"`) is faithfully executed. This is a *feature* (configurability) and a *risk* (prompt injection) simultaneously.
4. **Enterprise AI = Model + System Prompt + Guardrails.** The raw model is only one third of the equation.
5. **System prompts should be versioned and tested like code.** Any change to a system prompt in production is a deployment — treat it as one.
---
## What Comes Next
- **Step 5**: Few-shot prompting — teaching the model with examples inside the prompt
- **Step 6**: Chain-of-Thought prompting — forcing step-by-step reasoning
- **Module 02**: RAG Assistant — grounding the model in real documents to eliminate hallucination

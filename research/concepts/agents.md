---
title: "Concept — AI Agents"
tags: [research, concepts, agents, tool-use, planning, autonomous, multi-agent, langchain]
aliases: [ai-agents, llm-agents, autonomous-agents]
---

# AI Agents

> LLMs that take actions in the world by reasoning, selecting tools, and iterating toward a goal.

---

## Definition

An AI agent is a system where an LLM is used not just to generate a single response, but to **reason about a goal, select and execute tools, observe results, and iterate** until the goal is achieved or a stopping condition is met. Agents transform LLMs from responders into actors.

The key distinction from standard LLM prompting:

| Paradigm | Flow | Control |
|---|---|---|
| **Prompting** | Input → Single LLM call → Output | Deterministic, one-shot |
| **Agentic** | Goal → Loop(Reason → Act → Observe) → Output | Dynamic, multi-step |

---

## How It Works

### The Agent Loop (ReAct Pattern)

The most common agent pattern is **ReAct** (Reasoning + Acting), where the LLM alternates between:

1. **Thought** — reason about what to do next
2. **Action** — call a tool with specific arguments
3. **Observation** — receive the tool's output
4. **Repeat** until the goal is reached or `max_iterations` hit

```
User goal: "What is the current weather in London and should I bring an umbrella?"

Thought: I need to look up the current weather in London.
Action: weather_tool(city="London")
Observation: {"temp": 12, "condition": "rain", "humidity": 90}

Thought: It is raining. I should recommend an umbrella.
Action: final_answer("It's 12°C and raining in London. Yes, bring an umbrella.")
```

### Core Components

```
┌─────────────────────────────────────────────────────┐
│                    AI Agent                          │
│                                                     │
│  ┌─────────────┐    ┌──────────────┐                │
│  │   LLM Brain │ ←→ │    Memory    │                │
│  │ (reasoning) │    │ (short-term) │                │
│  └──────┬──────┘    └──────────────┘                │
│         │                                           │
│  ┌──────▼──────────────────────────────────┐       │
│  │            Tool Registry               │       │
│  │  search | code_exec | api_call | RAG   │       │
│  └──────────────────────────────────────── ┘       │
└─────────────────────────────────────────────────────┘
```

### 1. The LLM as Reasoning Engine

The LLM is given a system prompt that defines:
- Available tools (name, description, input schema)
- The current task and conversation history
- Reasoning format (ReAct, chain-of-thought, function-calling)

It outputs structured calls to tools, not free-text responses.

### 2. Tool Use / Function Calling

Modern LLMs support native **function calling** — structured JSON output that specifies which tool to call and with what arguments:

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for current information",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    }
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "What happened in AI this week?"}],
    tools=tools,
    tool_choice="auto",
)
```

The model decides which tool to call, with what arguments, based on the task.

### 3. Memory Types

| Memory Type | Scope | Implementation |
|---|---|---|
| **In-context (short-term)** | Current conversation | Messages array |
| **External (long-term)** | Persistent across sessions | Vector store + retrieval |
| **Episodic** | Past task outcomes | Structured log / DB |
| **Semantic** | World knowledge | RAG over knowledge base |

### 4. Multi-Agent Systems

Complex tasks can be decomposed across specialised agents:

```
Orchestrator Agent
    ↓ delegates sub-tasks
┌───────────┐   ┌───────────┐   ┌───────────┐
│  Researcher│   │  Writer   │   │  Reviewer │
│  (web RAG) │   │ (drafting)│   │(QA checks)│
└───────────┘   └───────────┘   └───────────┘
```

Patterns:
- **Supervisor / Worker**: one orchestrator routes tasks to specialised workers
- **Pipeline**: fixed sequence of agents each adding to the output
- **Debate**: two agents argue opposing positions, a judge decides
- **Swarm**: many peer agents collaborate without central coordination

---

## Why It Matters

### 1. Extends beyond the context window
Agents can retrieve, summarise, and iteratively build context — overcoming the single-call context limit.

### 2. Enables real-world actions
With the right tools (browser, code interpreter, APIs, databases), agents can book flights, write and run code, send emails, and interact with external systems.

### 3. Handles multi-step reasoning
Tasks like "research a topic, draft a report, and format it as a PDF" require coordination that single-call prompting cannot achieve.

### 4. Scales cognitive work
A single agent can complete tasks that would require hours of human effort — research synthesis, data analysis, code review — in minutes.

---

## Limitations

| Limitation | Description |
|---|---|
| **Hallucinated tool calls** | The LLM may call tools with incorrect arguments or fabricate tool outputs. |
| **Runaway loops** | Without clear stopping conditions, agents can loop indefinitely. Always set `max_iterations`. |
| **Compounding errors** | Mistakes in early steps propagate. A wrong intermediate answer leads to a wrong final answer. |
| **Cost explosion** | Multi-step agents make many LLM calls. A 10-step agent at 300 tokens/call costs 10× a single call. |
| **Unpredictability** | At higher temperatures or on ambiguous tasks, agent behaviour is hard to test and guarantee. |
| **Tool reliability** | Agents are only as reliable as the tools they call. A flaky API breaks the agent. |
| **Prompt injection** | Malicious content in tool outputs (e.g. a web page saying "ignore previous instructions") can hijack agent behaviour. |

### When NOT to use agents

- Task can be solved in a single LLM call → use direct prompting
- Strict latency requirements → sequential tool calls add 200-500ms per step
- Auditable, reproducible pipelines → agentic behaviour is non-deterministic
- Safety-critical domains without human-in-the-loop → agents can take irreversible actions

---

## Related Experiments

| Experiment | What It Tests | Connection to Agents |
|---|---|---|
| [Experiment 02 — System Prompt](../../experiments/llm_behavior/system_prompt/experiment.md) | System prompt as behaviour control | Agent behaviour is entirely governed by the system prompt — persona, tool descriptions, stopping conditions |
| [Experiment 01 — Temperature](../../experiments/llm_behavior/temperature/experiment.md) | Output entropy | Agents should run at T=0–0.3 for tool calls — randomness in tool selection is dangerous |
| [Experiment 03 — Token Limit](../../experiments/llm_behavior/token_limit/experiment.md) | Token budgeting | Each agent step consumes tokens; multi-step agents require careful budget management |

---

## Planned Projects

- [`projects/ai_agents/`](../../projects/ai_agents/README.md) — Build a single agent with web search, code execution, and RAG tools using LangChain
- [`projects/multi_agent_system/`](../../projects/multi_agent_system/README.md) — Implement a supervisor + worker multi-agent pipeline for research synthesis

---

## Further Reading

- [ReAct: Synergizing Reasoning and Acting — Yao et al. (2022)](https://arxiv.org/abs/2210.03629)
- [LangChain Agents Documentation](https://python.langchain.com/docs/modules/agents/)
- [AutoGen — Microsoft Multi-Agent Framework](https://microsoft.github.io/autogen/)
- [Anthropic — Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)

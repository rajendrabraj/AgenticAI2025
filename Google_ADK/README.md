
## What is ADK (Agent Development Kit)?

**ADK** is a flexible, modular framework for building and deploying **AI agents**, optimized for **Gemini** but **model-agnostic** (you can also use GPT/Claude) and **deployment-agnostic** (local or cloud). It aims to make agent development feel like standard software engineering: clear configs, testable units, composable workflows, and an integrated developer experience (CLI + web UI).

**Key ideas**:
- **Agents** are self-contained execution units that pursue goals, call tools, and can coordinate with other agents.
- **Tools** give agents capabilities (search, code execution, RAG, custom Python functions, third-party APIs).
- **Workflows** orchestrate agents (e.g., run in sequence, in parallel, or iterate in loops).
- **Memory/Session State** lets agents carry context across steps/sessions.
- **Callbacks/Guardrails** hook into lifecycle stages for safety, logging, and control.
- **Dev Experience** includes an `adk` CLI and an interactive web UI for local testing.

We’ll dive deeper into ## Core Concepts: Agents, Tools, Workflows, Memory, Callbacks

### Agents
- An **Agent** is a goal-driven unit that can reason, call tools, and produce outputs.
- A **root agent** is your entry point. It can delegate work to **sub-agents** specialized for tasks (research, coding, analysis, etc.).
- Multi-agent systems in ADK are built by composing multiple agents with defined responsibilities.

### Tools
- **Built-in tools** (e.g., Google Search, code executors, RAG) enable common capabilities out-of-the-box.
- **Function tools** are custom Python functions you expose to agents.
- **Third-party tools** or even **agents-as-tools** can be integrated for complex workloads.

### Workflows
- **Sequential**: sub-agents run in a fixed order (A → B → C).
- **Parallel**: sub-agents run concurrently and aggregate results.
- **Loop**: iterate until a condition or iteration budget is met (e.g., refine a draft until it passes checks).

### Memory & Session State
- Persist useful state across turns or app restarts (e.g., user profile, intermediate artifacts).

### Callbacks / Guardrails
- Hook into agent lifecycle (before/after tool calls, on error) to enforce constraints, redact data, or log decisions.each of these in the next sections and hands-on modules.


## Strengths, Limitations & Gotchas (ADK)

**Strengths**
- Clean separation of **agents, tools, and workflows**.
- Built-in **Sequential/Parallel/Loop** workflow agents.
- Solid **dev experience**: CLI, local web UI, samples, codelabs.
- Works beyond Gemini (bring GPT/Claude), while keeping Gemini-first ergonomics.

**Limitations / Gotchas**
- Certain **built-in tools are Gemini-only**; plan non-Gemini fallbacks.
- Some **built-in tools may not be callable from sub-agents**; design tool usage near the root if you hit errors.
- An agent instance is typically added **once** as a sub-agent (clone if needed under different names).
- As with other frameworks, **APIs evolve**. Keep an eye on release notes and `adk --help` output.

We’ll show workarounds (e.g., wrapping capabilities as function tools) in later modules.


## When to Choose Which Framework?

- **Choose ADK** when you want:
  - First-class **workflow agents** (sequential/parallel/loop) and a cohesive DX.
  - Strong Gemini integration but flexibility to use non-Gemini models.
  - A clean separation between agents, tools, and orchestration.

- **Choose LangChain/LangGraph** when you want:
  - Maximum ecosystem integrations and **graph semantics** (stateful nodes, retries, persistence).
  - LangSmith tracing/evals and platform deployment options.

- **Choose CrewAI** when you want:
  - Persona-driven **crews** collaborating autonomously, or **Flows** for deterministic control.

- **Choose AutoGen** when you want:
  - Event-driven **multi-agent conversations** (agents + humans + tools) as the primary abstraction.

You can also **mix and match**: wrap an ADK agent as a function/tool inside another framework, or vice versa, if a particular capability is missing.


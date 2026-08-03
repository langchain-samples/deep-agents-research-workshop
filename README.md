# Modular Workshops — LangChain Agent Demo

A hands-on, guided demo of **building, shipping, and improving an agent** with LangChain, Deep Agents, and LangSmith. It runs as a series of Jupyter notebooks, designed to be worked through live with a LangChain engineer (a condensed take on [LangChain Academy](https://academy.langchain.com/courses/intro-to-langgraph)).

Each module is self-contained — you can run the **core** path on its own, and add the **optional** modules if there's time or interest.

## The demo path

**Build → Ship → Improve** — three ~40-minute core modules, with a quick **LangSmith tracing checkpoint** between each: hop into the LangSmith UI to *see* what the agent just did before moving on. Those traces are also what Module 3 (Engine) works from.

### Core

**1 · Deep Agents** — *~40 min* · `modules/01_deep_agents.ipynb`
Build a planning research agent from scratch: custom tools, isolated subagents, long-term memory, human-in-the-loop approval, and skills.
> **↳ Tracing checkpoint** — open the run in LangSmith: watch tool calls, subagent delegation, and token usage (this is also where the multimodal image attachment shows up).

**2 · Deploy + Govern** — *~40 min* · `modules/02_deploy_and_govern.ipynb`
Put a **LangSmith Gateway** policy in front of the model (PII/secrets redaction), deploy the agent to LangSmith, and **chat with it in a real UI** via the hosted Agent Chat UI — no frontend code.
> **↳ Tracing checkpoint** — trace the deployed agent's runs; confirm every model call is flowing through the governed gateway.

**3 · Engine** — *~40 min* · `modules/04_engine.ipynb`
The visual finale, live in the LangSmith **UI**: **LangSmith Engine** reads the traces you've been generating, auto-detects a recurring failure, diagnoses the root cause against your source, and opens a fix PR — the full detect → diagnose → PR → evaluator loop, watched on screen.

### Optional deep-dive

**LangSmith (hands-on)** — `modules/03_langsmith.ipynb` — Prompt Hub versioning, the trace-query filter DSL, latency debugging (subagents & sequential tool calls), and offline + online evaluations + annotation queues. Pull this in when the audience wants the evaluation story in depth (the tracing checkpoints above are the quick version).

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (recommended) or pip

## Setup

```bash
# 1. Install dependencies
uv sync

# 2. Configure environment variables
cp .env.example .env
# Edit .env and fill in your keys

# 3. Start Jupyter
uv run jupyter notebook
```

Then open `modules/` and run whichever modules your session calls for.

### Keys

| Key | Needed for | Get one |
|-----|--------------|---------|
| `OPENAI_API_KEY` | **Core** — default model (all modules) | <https://platform.openai.com> |
| `TAVILY_API_KEY` | **Core** — web search (used by the research agent) | <https://tavily.com> |
| `LANGSMITH_API_KEY` | **Core** — tracing everywhere + Module 2 deploy; also Modules 3 & 4 | <https://smith.langchain.com> |
| `LANGSMITH_API_KEY_GATEWAY` / `WORKSPACE_ID` | **Core** — Module 2 gateway policy | same value as `LANGSMITH_API_KEY`; workspace ID from LangSmith → Settings → Workspace |

**LangSmith key types matter for deploy.** Tracing works with any key, but Module 2's `langgraph deploy` step needs a **service key** — `lsv2_sk_…`, created under **LangSmith → Settings → API Keys**. A personal key (`lsv2_pt_…`) will fail deploy with a `403`. Put that same service-key value in **both** `LANGSMITH_API_KEY` and `LANGSMITH_API_KEY_GATEWAY` (the deploy step strips the first, so the deployed agent reads the second).

> **Only running Module 1?** You just need `OPENAI_API_KEY` + `TAVILY_API_KEY`. The tracing checkpoints, Engine, and the optional LangSmith deep-dive all reuse the same `LANGSMITH_API_KEY` — nothing extra.

## Switching models

All modules import `model` from `utils/models.py`. Change one line there to swap providers — no notebook edits required.

```python
# utils/models.py

# OpenAI (default)
model = init_chat_model("openai:gpt-5.4-mini")

# Anthropic
# model = init_chat_model("anthropic:claude-sonnet-4-5")

# Azure OpenAI
# from langchain_openai import AzureChatOpenAI
# model = AzureChatOpenAI(azure_deployment="gpt-5.4-mini", streaming=True)

# AWS Bedrock
# from langchain_aws import ChatBedrockConverse
# model = ChatBedrockConverse(provider="anthropic", model_id="...")
```

`utils/models.py` also ships a commented-out **LangSmith Gateway** block. Module 2 §1.4 walks through flipping the default to it so every model call — notebooks *and* the deployed agent — is routed through the gateway and subject to workspace policies.

## Highlights (what's new in this build)

- **Zero-code chat frontend** (Module 2 §2.4): run `langgraph dev --port 2024`, then point the hosted [Agent Chat UI](https://agentchat.vercel.app) at `http://localhost:2024` (graph `deep_agent`) to chat with the agent — no install, no frontend code.
- **Multimodal traces** (Module 1 · Deep Agents, §1.2): the agent's `analyze_image` tool (`utils/vision.py`) reads a local image with a vision model and uploads it to the LangSmith trace as an `Attachment`, so you can see exactly what the agent saw — the payoff for the first tracing checkpoint.

## Project structure

```
modular-workshops-core/
├── README.md                       (this file)
├── pyproject.toml                  (shared dependencies)
├── .env.example
├── langgraph.json                  (registers agents/deep_agent for langgraph dev + deploy)
├── utils/                          (models, search, vision, tracing helpers)
├── agents/
│   ├── research_agent.py           (shared research agent — used by Deep Agents + the LangSmith deep-dive)
│   └── deep_agent/                 (deployable + governed agent — powers Deploy + Govern and Engine)
│       ├── agent.py
│       ├── AGENTS.md
│       └── skills/
└── modules/
    ├── 01_deep_agents.ipynb        (Core 1 · Build)
    ├── 02_deploy_and_govern.ipynb  (Core 2 · Ship + Govern)
    ├── 03_langsmith.ipynb          (Optional deep-dive · tracing + evals)
    └── 04_engine.ipynb             (Core 3 · Improve — Engine, in the UI)
```

## For LangChain internal users

See the [Notion doc](https://app.notion.com/p/Modular-Workshops-37d808527b1780318063fd210446aa03?source=copy_link) for setup and facilitation notes.

# Modular Workshops — LangChain Agent Demo

A hands-on, guided demo of **building, shipping, and improving an agent** with LangChain, Deep Agents, and LangSmith. It runs as a series of Jupyter notebooks, designed to be worked through live with a LangChain engineer (a condensed take on [LangChain Academy](https://academy.langchain.com/courses/intro-to-langgraph)).

Each module is self-contained — you can run the **core** path on its own, and add the **optional** modules if there's time or interest.

## The demo path

### Core

| Module | ~Time | What you'll see |
|--------|-------|-----------------|
| **1 · Deep Agents** | ~25 min | Build a planning research agent from scratch — custom tools, isolated subagents, long-term memory, human-in-the-loop approval, and skills. |
| **2 · Deploy + Govern** | ~25 min | Put a **LangSmith Gateway** policy in front of the model (PII/secrets redaction), deploy the agent to LangSmith, and **chat with it in a real UI** via the hosted Agent Chat UI — no frontend code. |

### Optional

| Module | ~Time | What you'll see |
|--------|-------|-----------------|
| **3 · LangSmith** *(optional)* | ~25 min | Prompt engineering, tracing & querying, **multimodal traces** (the agent reads an image and the file is attached to the trace), and offline + online evaluations. |
| **4 · Engine** *(optional)* | ~15 min | **LangSmith Engine** watches production traces, auto-detects a recurring failure, diagnoses the root cause against your source, and proposes a fix as a GitHub PR. Builds on the Module 2 deployment. |

> **Shortest path:** Modules 1 & 2 are a complete, satisfying demo on their own. Modules 3 & 4 are add-ons.

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
| `TAVILY_API_KEY` | **Core** — web search (Modules 1–3) | <https://tavily.com> |
| `LANGSMITH_API_KEY` | **Core** — tracing everywhere + Module 2 deploy; also Modules 3 & 4 | <https://smith.langchain.com> |
| `LANGSMITH_API_KEY_GATEWAY` / `WORKSPACE_ID` | **Core** — Module 2 gateway policy | same value as `LANGSMITH_API_KEY`; workspace ID from LangSmith → Settings → Workspace |

**LangSmith key types matter for deploy.** Tracing works with any key, but Module 2's `langgraph deploy` step needs a **service key** — `lsv2_sk_…`, created under **LangSmith → Settings → API Keys**. A personal key (`lsv2_pt_…`) will fail deploy with a `403`. Put that same service-key value in **both** `LANGSMITH_API_KEY` and `LANGSMITH_API_KEY_GATEWAY` (the deploy step strips the first, so the deployed agent reads the second).

> **Only running Module 1?** You just need `OPENAI_API_KEY` + `TAVILY_API_KEY`. Modules 3 & 4 reuse the same keys — nothing extra.

## Switching models

All modules import `model` from `utils/models.py`. Change one line there to swap providers — no notebook edits required.

```python
# utils/models.py

# OpenAI (default)
model = init_chat_model("openai:gpt-4.1-mini")

# Anthropic
# model = init_chat_model("anthropic:claude-sonnet-4-5")

# Azure OpenAI
# from langchain_openai import AzureChatOpenAI
# model = AzureChatOpenAI(azure_deployment="gpt-4.1-mini", streaming=True)

# AWS Bedrock
# from langchain_aws import ChatBedrockConverse
# model = ChatBedrockConverse(provider="anthropic", model_id="...")
```

`utils/models.py` also ships a commented-out **LangSmith Gateway** block. Module 2 §1.4 walks through flipping the default to it so every model call — notebooks *and* the deployed agent — is routed through the gateway and subject to workspace policies.

## Highlights (what's new in this build)

- **Zero-code chat frontend** (Module 2 §2.4): run `langgraph dev --port 2024`, then point the hosted [Agent Chat UI](https://agentchat.vercel.app) at `http://localhost:2024` (graph `deep_agent`) to chat with the agent — no install, no frontend code.
- **Multimodal traces** (Module 3 §2.3): the agent's `analyze_image` tool (`utils/vision.py`) reads a local image with a vision model and uploads it to the LangSmith trace as an `Attachment`, so you can see exactly what the agent saw.

## Project structure

```
modular-workshops-core/
├── README.md                       (this file)
├── pyproject.toml                  (shared dependencies)
├── .env.example
├── langgraph.json                  (registers agents/deep_agent for langgraph dev + deploy)
├── utils/                          (models, search, vision, tracing helpers)
├── agents/
│   ├── research_agent.py           (shared research agent — Module 1 references, Module 3 imports)
│   └── deep_agent/                 (deployable + governed agent for Modules 2 & 4)
│       ├── agent.py
│       ├── AGENTS.md
│       └── skills/
└── modules/
    ├── 01_deep_agents.ipynb        (Module 1 · core)
    ├── 02_deploy_and_govern.ipynb  (Module 2 · core)
    ├── 03_langsmith.ipynb          (Module 3 · optional)
    └── 04_engine.ipynb             (Module 4 · optional)
```

## For LangChain internal users

See the [Notion doc](https://app.notion.com/p/Modular-Workshops-37d808527b1780318063fd210446aa03?source=copy_link) for setup and facilitation notes.

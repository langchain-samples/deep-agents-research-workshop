# Modular Workshops — LangChain Agent Demo

A hands-on, guided session for **building and shipping an agent** with LangChain, Deep Agents, and LangSmith — run live with a LangChain engineer (a condensed take on [LangChain Academy](https://academy.langchain.com/courses/intro-to-langgraph)).

- **In the workshop → Modules 1 & 2.** Build a deep agent, then govern + deploy it — with a quick hop into the LangSmith UI between them to see what it did.
- **After the workshop → Modules 3 & 4.** Self-paced depth: the full LangSmith observability/evaluation story, and LangSmith Engine's automated improvement loop.

---

## Workshop Prework

Please complete this in advance (Modules 1 & 2) so we can dive straight into building.

**Prerequisites:** Python 3.11+ and [uv](https://docs.astral.sh/uv/getting-started/installation/).

```bash
# 1. Install dependencies
uv sync

# 2. Create your env file
cp .env.example .env
#    ...then fill in the keys below

# 3. Launch
uv run jupyter notebook   # then open modules/01_deep_agents.ipynb
```

### Keys you need for Modules 1 & 2

| Key | Why | Get one |
|-----|-----|---------|
| `LANGSMITH_API_KEY` | Tracing (Module 1) **and deploying** (Module 2) | see the callout below |
| `LANGSMITH_API_KEY_GATEWAY` | Gateway auth for the deployed agent (Module 2) | **same value** as `LANGSMITH_API_KEY` |
| `WORKSPACE_ID` | Gateway policy target (Module 2) | LangSmith → Settings → Workspace |
| `OPENAI_API_KEY` | The model (both modules) | <https://platform.openai.com> |
| `TAVILY_API_KEY` | Web search tool (both modules) | <https://tavily.com> |

> ### ⚠️ The LangSmith key must be a **service key**
> Module 2 runs `langgraph deploy`, which **requires a service key** — one that starts with **`lsv2_sk_`**, created under **LangSmith → Settings → API Keys** (give it deployment permissions).
> A **personal** key (`lsv2_pt_…`) will trace fine but **fails deploy with a `403`**.
>
> Put that **same `lsv2_sk_…` value** in **both** `LANGSMITH_API_KEY` and `LANGSMITH_API_KEY_GATEWAY` — `langgraph deploy` strips the first on upload, so the deployed agent reads the second.

---

## The workshop — Modules 1 & 2

**1 · Deep Agents** — *~40 min* · `modules/01_deep_agents.ipynb`
Build a planning research agent from scratch: custom tools, isolated subagents, long-term memory, human-in-the-loop approval, and skills.
> **↳ Tracing checkpoint** — open the run in LangSmith: tool calls, subagent delegation, token usage (and the multimodal image attachment).

**2 · Deploy + Govern** — *~40 min* · `modules/02_deploy_and_govern.ipynb`
Put a **LangSmith Gateway** policy in front of the model (PII/secrets redaction), **create your own deep agent**, and deploy — your agent ships alongside the demo agent. Chat with it in a real UI via the hosted Agent Chat UI (no frontend code).
> **↳ Tracing checkpoint** — trace the deployed runs; confirm every model call flows through the governed gateway.

## After the workshop — Modules 3 & 4

Optional, self-paced, for more detail.

**3 · LangSmith** · `modules/03_langsmith.ipynb`
The full observability + evaluation story: Prompt Hub versioning, the trace-query filter DSL, latency debugging (subagents & sequential tool calls), and offline + online evaluations + annotation queues. (The tracing checkpoints in Modules 1 & 2 are the quick version of this.)

**4 · Engine** · `modules/04_engine.ipynb`
**LangSmith Engine** reads your deployed agent's production traces, auto-detects a recurring failure, diagnoses the root cause against your source, and opens a fix PR — the full detect → diagnose → PR → evaluator loop, watched in the UI. Builds on your Module 2 deployment.

---

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

## Highlights

- **Create your own deep agent** (Module 2 §2.5): `my_agent/agent.py` is a blank scaffold, pre-registered in `langgraph.json` — customize it and it deploys alongside the demo agent in one `langgraph deploy`.
- **Zero-code chat frontend** (Module 2 §2.4): run `langgraph dev --port 2024`, then point the hosted [Agent Chat UI](https://agentchat.vercel.app) at `http://localhost:2024` to chat with any registered graph — no install, no frontend code.
- **Multimodal traces** (Module 1 §1.2): the `analyze_image` tool (`utils/vision.py`) reads a local image and uploads it to the LangSmith trace as an `Attachment`, so you can see exactly what the agent saw.

## Project structure

```
modular-workshops-core/
├── README.md                       (this file)
├── pyproject.toml
├── .env.example
├── langgraph.json                  (registers deep_agent + my_agent for langgraph dev + deploy)
├── utils/                          (models, search, vision, tracing helpers)
├── agents/
│   └── deep_agent/                 (the deployable + governed demo agent)
├── my_agent/                       (blank scaffold — attendees build their own in §2.5)
└── modules/
    ├── 01_deep_agents.ipynb        (Workshop · Module 1 — Build)
    ├── 02_deploy_and_govern.ipynb  (Workshop · Module 2 — Deploy + Govern)
    ├── 03_langsmith.ipynb          (After · Module 3 — LangSmith deep-dive)
    └── 04_engine.ipynb             (After · Module 4 — Engine)
```

## For LangChain internal users

See the [Notion doc](https://app.notion.com/p/Modular-Workshops-37d808527b1780318063fd210446aa03?source=copy_link) for setup and facilitation notes.

# Modular Workshops — LangChain Agent Demo

A hands-on, guided session for **building and shipping an agent** with LangChain, Deep Agents, and LangSmith — run live with a LangChain engineer (a condensed take on [LangChain Academy](https://academy.langchain.com/courses/intro-to-langgraph)).

- **In the workshop → Modules 1 & 2.** Build a deep agent, then push its context to LangSmith Context Hub and deploy it — with a quick hop into the LangSmith UI between them to see what it did.
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
| `LANGSMITH_API_KEY` | Tracing (Module 1), Context Hub + deploying (Module 2) | see the callout below |
| `OPENAI_API_KEY` | The model — default is OpenAI (or use your own provider/gateway) | <https://platform.openai.com> |
| `TAVILY_API_KEY` | Web search tool (both modules) | <https://tavily.com> |

> ### ⚠️ The LangSmith key must be a **service key**
> Module 2 runs `langgraph deploy`, which **requires a service key** — one that starts with **`lsv2_sk_`**, created under **LangSmith → Settings → API Keys** (give it deployment permissions).
> A **personal** key (`lsv2_pt_…`) will trace fine but **fails deploy with a `403`**.

> **Using your own model provider or gateway?** You may not need `OPENAI_API_KEY` at all — point the workshop at another provider, an internal OpenAI-compatible gateway, or a keyless endpoint. See **Switching models** below. (LangSmith keys are still needed for tracing + deploy.)

---

## The workshop — Modules 1 & 2

**1 · Deep Agents** — *~40 min* · `modules/01_deep_agents.ipynb`
Build a planning research agent from scratch: custom tools, isolated subagents, long-term memory, sandboxed code execution, human-in-the-loop approval, and skills.
> **↳ Tracing checkpoint** — open the run in LangSmith: tool calls, subagent delegation, token usage (and the multimodal image attachment).

**2 · Deploy + Context Hub** — *~40 min* · `modules/02_deploy_and_manage_context.ipynb`
Push the agent's context (`AGENTS.md` + skills) to **LangSmith Context Hub** as versioned, reusable repos, **create your own deep agent**, and deploy — your agent ships alongside the demo agent. Chat with it in a real UI via the hosted Agent Chat UI (no frontend code).
> **↳ Tracing checkpoint** — trace the deployed runs end to end in the LangSmith UI.

## After the workshop — Modules 3 & 4

Optional, self-paced, for more detail.

**3 · LangSmith** · `modules/03_langsmith.ipynb`
The full observability + evaluation story: Prompt Hub versioning, the trace-query filter DSL, latency debugging (subagents & sequential tool calls), and offline + online evaluations + annotation queues. (The tracing checkpoints in Modules 1 & 2 are the quick version of this.)

**4 · Engine** · `modules/04_engine.ipynb`
**LangSmith Engine** reads your deployed agent's production traces, auto-detects a recurring failure, diagnoses the root cause against your source, and opens a fix PR — the full detect → diagnose → PR → evaluator loop, watched in the UI. Builds on your Module 2 deployment.

---

## Switching models

Every notebook **and** the deployed agent import one `model` object from `utils/models.py` — that's the single swap point. Change it once and everything (including the deployment) follows; no notebook edits.

```python
# utils/models.py — set `model` to ONE of these:
import os
from langchain.chat_models import init_chat_model

# 1) OpenAI (default) — needs OPENAI_API_KEY
model = init_chat_model("openai:gpt-5.4-mini")

# 2) Another provider — needs that provider's key
# model = init_chat_model("anthropic:claude-sonnet-4-5")
# model = init_chat_model("google_genai:gemini-2.5-pro")
# from langchain_aws import ChatBedrockConverse
# model = ChatBedrockConverse(provider="anthropic", model_id="...")

# 3) Your company's OpenAI-compatible gateway (internal LLM proxy) —
#    any endpoint that speaks the OpenAI API works; just set base_url.
# model = init_chat_model(
#     "openai:<your-model-name>",
#     base_url="https://llm-gateway.yourco.internal/v1",
#     api_key=os.environ.get("YOURCO_LLM_TOKEN", "EMPTY"),
# )

# 4) A no-key gateway (auth via your network / IAM / mTLS / headers) —
#    the client still wants a non-empty string, so pass a placeholder.
# model = init_chat_model(
#     "openai:<your-model-name>",
#     base_url="https://llm-gateway.yourco.internal/v1",
#     api_key="EMPTY",
#     default_headers={"Authorization": "Bearer <token>"},  # optional
# )
```

**Prefer env vars, no code change?** LangChain's OpenAI client honors `OPENAI_BASE_URL` and `OPENAI_API_KEY`, so a team can redirect the default at their gateway just by setting them in `.env`:

```bash
OPENAI_BASE_URL="https://llm-gateway.yourco.internal/v1"
OPENAI_API_KEY="EMPTY"   # or whatever token the gateway expects
```


## Highlights

- **Create your own deep agent** (Module 2 §2.5): `my_agent/agent.py` is a blank scaffold, pre-registered in `langgraph.json` — customize it and it deploys alongside the demo agent in one `langgraph deploy`.
- **Context Hub** (Module 2 §1): push `AGENTS.md` + skills to LangSmith Context Hub as versioned, reusable repos (`push_skill` / `push_agent`); the deployed agent reads its context from the Hub via `ContextHubBackend`.
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
│   └── deep_agent/                 (the deployable demo agent)
├── my_agent/                       (blank scaffold — attendees build their own in §2.5)
└── modules/
    ├── 01_deep_agents.ipynb        (Workshop · Module 1 — Build)
    ├── 02_deploy_and_manage_context.ipynb  (Workshop · Module 2 — Deploy + Context Hub)
    ├── 03_langsmith.ipynb          (After · Module 3 — LangSmith deep-dive)
    └── 04_engine.ipynb             (After · Module 4 — Engine)
```

## For LangChain internal users

See the [Notion doc](https://app.notion.com/p/Modular-Workshops-37d808527b1780318063fd210446aa03?source=copy_link) for setup and facilitation notes.

"""Centralized model initialization.

The notebooks all import `model` from here, so swapping providers
(OpenAI / Anthropic / Azure / Bedrock) only requires editing this file.

The default is OpenAI. Swap providers by editing the active line below.
"""

import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="../.env", override=True)

from langchain.chat_models import init_chat_model

# --- Default: OpenAI, direct ---
model = init_chat_model("openai:gpt-5.4-mini")

# --- Your own OpenAI-compatible gateway (internal LLM proxy) ---
# Any endpoint that speaks the OpenAI API works — just set base_url. For a
# gateway that needs no key (auth via network / IAM / headers), pass a
# placeholder api_key like "EMPTY". You can also skip this block entirely and
# set OPENAI_BASE_URL / OPENAI_API_KEY in .env instead.
# model = init_chat_model(
#     "openai:<your-model-name>",
#     base_url="https://llm-gateway.yourco.internal/v1",
#     api_key=os.environ.get("YOURCO_LLM_TOKEN", "EMPTY"),
#     # default_headers={"Authorization": "Bearer <token>"},  # optional
# )


# --- Anthropic ---
# model = init_chat_model("anthropic:claude-sonnet-4-5")

# --- Azure OpenAI ---
# from langchain_openai import AzureChatOpenAI
# model = AzureChatOpenAI(azure_deployment="gpt-4.1-mini", streaming=True)

# --- AWS Bedrock ---
# from langchain_aws import ChatBedrockConverse
# model = ChatBedrockConverse(
#     provider="anthropic",
#     model_id="anthropic.claude-sonnet-4-20250514-v1:0",
# )

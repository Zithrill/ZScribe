import os
from typing import Dict, Any

# Define supported models and their corresponding providers
MODEL_PROVIDER_MAP = {
    "gpt-3.5-turbo": "openai",
    "gpt-4": "openai",
    "claude-2": "anthropic",
    "claude-instant-1": "anthropic",
    "amazon.titan-tg1-large": "bedrock",
    "anthropic.claude-v2": "bedrock",
    "meta.llama2-70b-chat-v1": "bedrock",
    "mistral-7b": "ollama",
    "llama2": "ollama",
    "llm-studio-custom": "llm_studio",
}


def get_model_config() -> Dict[str, Any]:
    model = os.environ.get("ZSCRIBE_MODEL", "claude-2").lower()
    if model not in MODEL_PROVIDER_MAP:
        raise ValueError(f"Unsupported model: {model}")

    provider = MODEL_PROVIDER_MAP[model]

    return {
        "model": model,
        "provider": provider,
    }
import os
from typing import Dict, Any


def get_model_config() -> Dict[str, Any]:
    from scribe.model_utils import get_model_provider_map

    model_provider_map = get_model_provider_map()
    model = os.environ.get("ZSCRIBE_MODEL", "claude-3-5-sonnet-20240620").lower()

    if model not in model_provider_map:
        available_models = ", ".join(model_provider_map.keys())
        raise ValueError(
            f"Unsupported model: {model}. Available models are: {available_models}"
        )

    provider = model_provider_map[model]

    return {
        "model": model,
        "provider": provider,
    }

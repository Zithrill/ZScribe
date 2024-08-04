from typing import Dict


def get_model_provider_map() -> Dict[str, str]:
    from scribe.plugins import list_available_models

    available_models = list_available_models()
    model_provider_map = {}
    for provider, models in available_models.items():
        for model in models:
            model_provider_map[model] = provider
    return model_provider_map
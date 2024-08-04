from .openai import OpenAIPlugin
from .anthropic import AnthropicPlugin
from .bedrock import BedrockPlugin
from .ollama import OllamaPlugin
from scribe.config import MODEL_PROVIDER_MAP

PROVIDER_PLUGIN_MAP = {
    "openai": OpenAIPlugin,
    "anthropic": AnthropicPlugin,
    "bedrock": BedrockPlugin,
    "ollama": OllamaPlugin,
}


def get_plugin(config):
    PluginClass = PROVIDER_PLUGIN_MAP.get(config["provider"])
    if not PluginClass:
        raise ValueError(f"Unsupported provider: {config['provider']}")
    return PluginClass(config["model"])


def list_available_models():
    available_models = {}
    for provider, PluginClass in PROVIDER_PLUGIN_MAP.items():
        available_models[provider] = PluginClass.list_models()
    return available_models

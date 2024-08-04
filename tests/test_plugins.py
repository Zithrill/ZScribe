import pytest
from scribe.plugins import get_plugin, list_available_models
from scribe.plugins.openai import OpenAIPlugin
from scribe.plugins.anthropic import AnthropicPlugin
from scribe.plugins.bedrock import BedrockPlugin
from scribe.plugins.ollama import OllamaPlugin

def test_get_plugin():
    config = {"provider": "openai", "model": "gpt-3.5-turbo"}
    plugin = get_plugin(config)
    assert isinstance(plugin, OpenAIPlugin)

    config = {"provider": "anthropic", "model": "claude-3-5-sonnet-20240620"}
    plugin = get_plugin(config)
    assert isinstance(plugin, AnthropicPlugin)

    config = {"provider": "bedrock", "model": "anthropic.claude-v2"}
    plugin = get_plugin(config)
    assert isinstance(plugin, BedrockPlugin)

    config = {"provider": "ollama", "model": "llama2"}
    plugin = get_plugin(config)
    assert isinstance(plugin, OllamaPlugin)

def test_list_available_models(mocker):
    mocker.patch('scribe.plugins.openai.OpenAIPlugin.list_models', return_value=["gpt-3.5-turbo", "gpt-4"])
    mocker.patch('scribe.plugins.anthropic.AnthropicPlugin.list_models', return_value=["claude-3-5-sonnet-20240620"])
    mocker.patch('scribe.plugins.bedrock.BedrockPlugin.list_models', return_value=["anthropic.claude-v2"])
    mocker.patch('scribe.plugins.ollama.OllamaPlugin.list_models', return_value=["llama2"])

    models = list_available_models()
    assert isinstance(models, dict)
    assert "openai" in models
    assert "anthropic" in models
    assert "bedrock" in models
    assert "ollama" in models
    assert models["openai"] == ["gpt-3.5-turbo", "gpt-4"]
    assert models["anthropic"] == ["claude-3-5-sonnet-20240620"]
    assert models["bedrock"] == ["anthropic.claude-v2"]
    assert models["ollama"] == ["llama2"]
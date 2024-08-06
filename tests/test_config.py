import pytest
from scribe.config import get_model_config


def test_get_model_config_openai(monkeypatch):
    monkeypatch.setenv("ZSCRIBE_MODEL", "gpt-3.5-turbo")
    config = get_model_config()
    assert config["model"] == "gpt-3.5-turbo"
    assert config["provider"] == "openai"


def test_get_model_config_anthropic(monkeypatch):
    monkeypatch.setenv("ZSCRIBE_MODEL", "claude-3-5-sonnet-20240620")
    config = get_model_config()
    assert config["model"] == "claude-3-5-sonnet-20240620"
    assert config["provider"] == "anthropic"


def test_get_model_config_invalid_model(monkeypatch):
    monkeypatch.setenv("ZSCRIBE_MODEL", "invalid-model")
    with pytest.raises(ValueError):
        get_model_config()

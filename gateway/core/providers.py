from typing import Tuple
from gateway.adapters.openai import OpenAIProvider
from gateway.adapters.mock import MockProvider
from gateway.core.config import settings

_openai = OpenAIProvider(api_key=settings.OPENAI_API_KEY)
_mock = MockProvider()

def pick(model: str | None) -> Tuple[str, str, object]:
    # model is like "openai:gpt-4o-mini" or "mock:any"
    m = (model or settings.DEFAULT_MODEL).strip()
    if ":" not in m:
        # default provider is openai
        provider_name, model_name = "openai", m
    else:
        provider_name, model_name = m.split(":", 1)
    provider_name = provider_name.lower()

    if provider_name == "openai":
        return provider_name, model_name, _openai
    if provider_name == "mock":
        return provider_name, model_name, _mock
    raise ValueError(f"Unknown provider: {provider_name}")

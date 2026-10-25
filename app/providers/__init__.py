from typing import Optional, Any
from app.providers.gemini_provider import GeminiProvider
from app.providers.openai_provider import OpenAIProvider
from app.providers.mock_provider import MockGeminiProvider
from app.config import (
    is_gemini_configured,
    is_openai_configured,
    get_default_provider_name,
)


def get_llm_provider(
    provider_name: Optional[str] = None,
    use_mock: bool = False,
) -> Any:
    """
    Factory function to resolve and instantiate the requested or best available LLM provider.
    Supported provider names: "openai", "gemini", "mock".
    """
    if use_mock:
        return MockGeminiProvider()

    target = (provider_name or "").strip().lower()
    if not target:
        target = get_default_provider_name()

    if target == "openai":
        if is_openai_configured():
            return OpenAIProvider()
        elif is_gemini_configured():
            return GeminiProvider()
        return MockGeminiProvider()

    elif target == "gemini":
        if is_gemini_configured():
            return GeminiProvider()
        elif is_openai_configured():
            return OpenAIProvider()
        return MockGeminiProvider()

    elif target == "mock":
        return MockGeminiProvider()

    # Fallback to default
    if is_openai_configured():
        return OpenAIProvider()
    if is_gemini_configured():
        return GeminiProvider()
    return MockGeminiProvider()


__all__ = [
    "GeminiProvider",
    "OpenAIProvider",
    "MockGeminiProvider",
    "get_llm_provider",
]

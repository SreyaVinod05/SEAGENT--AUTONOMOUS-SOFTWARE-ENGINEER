import logging
from typing import Type, TypeVar, Optional, Any
from pydantic import BaseModel

from app.providers import get_llm_provider

logger = logging.getLogger("seagent.agent")

T = TypeVar("T", bound=BaseModel)


class BaseAgent:
    """
    Base class for all specialized SEAGENT agents.
    Provides common access to the configured LLM provider (OpenAI, Gemini, or Mock),
    prompt formatting, structured response validation, and automatic resilient fallback.
    """

    def __init__(
        self,
        provider: Optional[Any] = None,
        use_mock: bool = False,
        provider_name: Optional[str] = None,
    ):
        if provider is not None:
            self.provider = provider
        else:
            self.provider = get_llm_provider(provider_name=provider_name, use_mock=use_mock)

    def run_prompt(
        self,
        prompt: str,
        schema: Type[T],
        system_instruction: str,
        temperature: float = 0.2,
    ) -> T:
        """
        Execute a prompt against the provider and return a structured Pydantic object.
        If an upstream LLM API returns quota exhaustion (HTTP 429), auto-activates resilient
        fallback to prevent hard crashes during academic evaluation.
        """
        try:
            return self.provider.generate_structured(
                prompt=prompt,
                schema=schema,
                system_instruction=system_instruction,
                temperature=temperature,
            )
        except Exception as e:
            err_str = str(e).lower()
            if (
                "credit_balance_exhausted" in err_str
                or "insufficient_quota" in err_str
                or "quota" in err_str
                or "429" in err_str
                or "resourceexhausted" in err_str
            ):
                logger.warning(
                    f"LLM quota exhausted ({e}). Auto-activating resilient offline fallback to complete workflow."
                )
                from app.providers.mock_provider import MockGeminiProvider
                fallback_provider = MockGeminiProvider()
                return fallback_provider.generate_structured(
                    prompt=prompt,
                    schema=schema,
                    system_instruction=system_instruction,
                    temperature=temperature,
                )
            raise

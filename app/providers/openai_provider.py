import json
import logging
import re
from typing import Type, TypeVar, Optional, Any
from pydantic import BaseModel
from openai import OpenAI

from app.config import OPENAI_API_KEY, OPENAI_MODEL, is_openai_configured

logger = logging.getLogger("seagent.provider.openai")

T = TypeVar("T", bound=BaseModel)


class OpenAIProvider:
    """
    OpenAI provider for SEAGENT supporting structured Pydantic outputs
    and standard conversational completions across gpt-4o, gpt-4o-mini, etc.
    """

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = (api_key or OPENAI_API_KEY).strip()
        self.model = (model or OPENAI_MODEL).strip()
        self._client: Optional[OpenAI] = None

        if self.api_key:
            try:
                self._client = OpenAI(api_key=self.api_key)
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI Client: {e}")
                self._client = None

    def is_available(self) -> bool:
        """Check if OpenAI client is configured with a valid API key."""
        return bool(self._client and self.api_key)

    def generate_structured(
        self,
        prompt: str,
        schema: Type[T],
        system_instruction: Optional[str] = None,
        temperature: float = 0.2,
    ) -> T:
        """
        Generate structured output conforming to a Pydantic schema using OpenAI.
        Leverages OpenAI's native structured outputs (beta.chat.completions.parse)
        with an automated JSON object fallback.
        """
        if not self.is_available():
            raise ValueError(
                "OPENAI_API_KEY is not configured. Please set OPENAI_API_KEY in backend/.env "
                "or select another provider to run SEAGENT workflows."
            )

        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        # 1. Primary: native Pydantic schema parsing via beta.chat.completions.parse
        try:
            response = self._client.beta.chat.completions.parse(
                model=self.model,
                messages=messages,
                response_format=schema,
                temperature=temperature,
            )
            parsed = response.choices[0].message.parsed
            if parsed is not None:
                if isinstance(parsed, schema):
                    return parsed
                if isinstance(parsed, dict):
                    return schema.model_validate(parsed)
        except Exception as parse_err:
            logger.warning(
                f"OpenAI beta parse failed for {schema.__name__}: {parse_err}. "
                "Attempting json_object completion fallback..."
            )

        # 2. Fallback: json_object response format
        try:
            fallback_instruction = (
                (system_instruction or "")
                + "\nYou must respond strictly in JSON matching the requested schema."
            ).strip()
            fallback_messages = [
                {"role": "system", "content": fallback_instruction},
                {"role": "user", "content": prompt},
            ]
            response = self._client.chat.completions.create(
                model=self.model,
                messages=fallback_messages,
                response_format={"type": "json_object"},
                temperature=temperature,
            )
            raw_content = response.choices[0].message.content or "{}"
            return self._parse_json_to_schema(raw_content, schema)
        except Exception as e:
            logger.error(f"OpenAI API generation failed: {e}")
            raise RuntimeError(f"OpenAI generation error for model {self.model}: {str(e)}")

    def generate(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """Generate unstructured text completion."""
        if not self.is_available():
            raise ValueError("OPENAI_API_KEY is not configured.")

        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        response = self._client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.3,
        )
        return response.choices[0].message.content or ""

    def _parse_json_to_schema(self, text: str, schema: Type[T]) -> T:
        """Helper to extract and validate JSON string against Pydantic schema."""
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```[a-zA-Z]*\n?", "", cleaned)
            cleaned = re.sub(r"\n?```$", "", cleaned)
            cleaned = cleaned.strip()

        try:
            data = json.loads(cleaned)
            return schema.model_validate(data)
        except Exception as json_err:
            logger.error(
                f"Failed to parse JSON into {schema.__name__}: {json_err}. Raw text:\n{text[:500]}"
            )
            raise ValueError(f"Model output could not be parsed into {schema.__name__}: {json_err}")
import json
import logging
import re
from typing import Type, TypeVar, Optional, Any
from pydantic import BaseModel
from google import genai
from google.genai import types

from app.config import GEMINI_API_KEY, GEMINI_MODEL, is_gemini_configured

logger = logging.getLogger("seagent.provider")

T = TypeVar("T", bound=BaseModel)


class GeminiProvider:
    """
    Unified Google Gemini provider for SEAGENT.
    Uses the official google-genai SDK to power all specialized software engineering agents
    with structured outputs and distinct role prompts.
    """

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = (api_key or GEMINI_API_KEY).strip()
        self.model = (model or GEMINI_MODEL).strip()
        self._client: Optional[genai.Client] = None

        if self.api_key:
            try:
                self._client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.error(f"Failed to initialize Google GenAI Client: {e}")
                self._client = None

    def is_available(self) -> bool:
        """Check if Gemini client is configured with an API key."""
        return bool(self._client and self.api_key)

    def generate_structured(
        self,
        prompt: str,
        schema: Type[T],
        system_instruction: Optional[str] = None,
        temperature: float = 0.2,
    ) -> T:
        """
        Generate structured output conforming to a Pydantic schema using Gemini.
        """
        if not self.is_available():
            raise ValueError(
                "GEMINI_API_KEY is not configured. Please set GEMINI_API_KEY in backend/.env "
                "or provide it in the environment to run SEAGENT workflows."
            )

        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=schema,
            temperature=temperature,
        )
        if system_instruction:
            config.system_instruction = system_instruction

        try:
            response = self._client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config,
            )

            # Try direct parsed result from google-genai SDK
            if hasattr(response, "parsed") and response.parsed is not None:
                if isinstance(response.parsed, schema):
                    return response.parsed
                if isinstance(response.parsed, dict):
                    return schema.model_validate(response.parsed)

            # Fallback to response.text JSON parsing
            raw_text = response.text or ""
            return self._parse_json_to_schema(raw_text, schema)

        except Exception as e:
            logger.error(f"Gemini API generation failed: {e}")
            raise RuntimeError(f"Gemini generation error for model {self.model}: {str(e)}")

    def _parse_json_to_schema(self, text: str, schema: Type[T]) -> T:
        """Helper to extract and validate JSON string against Pydantic schema."""
        cleaned = text.strip()
        # Remove markdown fences if model returned ```json ... ```
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```[a-zA-Z]*\n?", "", cleaned)
            cleaned = re.sub(r"\n?```$", "", cleaned)
            cleaned = cleaned.strip()

        try:
            data = json.loads(cleaned)
            return schema.model_validate(data)
        except Exception as json_err:
            logger.error(f"Failed to parse JSON into {schema.__name__}: {json_err}. Raw text:\n{text[:500]}")
            raise ValueError(f"Model output could not be parsed into {schema.__name__}: {json_err}")

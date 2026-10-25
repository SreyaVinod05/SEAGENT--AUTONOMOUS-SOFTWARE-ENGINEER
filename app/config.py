import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from backend directory
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# OpenAI Configuration
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()

# Gemini Configuration
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()

# Default LLM Provider preference ("openai", "gemini", or "mock")
DEFAULT_LLM_PROVIDER: str = os.getenv("DEFAULT_LLM_PROVIDER", "").strip().lower()

# Workflow & Execution Settings
MAX_DEBUG_RETRIES: int = int(os.getenv("MAX_DEBUG_RETRIES", "3"))
CODE_EXECUTION_TIMEOUT_SECONDS: int = int(os.getenv("CODE_EXECUTION_TIMEOUT_SECONDS", "25"))
DATA_DIR: Path = Path(__file__).resolve().parent.parent / os.getenv("SEAGENT_DATA_DIR", "data/workflows")
DATA_DIR.mkdir(parents=True, exist_ok=True)


def is_openai_configured() -> bool:
    """Returns True if a valid-looking OPENAI_API_KEY is present."""
    return bool(OPENAI_API_KEY and len(OPENAI_API_KEY) > 10)


def is_gemini_configured() -> bool:
    """Returns True if a valid-looking GEMINI_API_KEY is present."""
    return bool(GEMINI_API_KEY and len(GEMINI_API_KEY) > 5)


def get_default_provider_name() -> str:
    """Determine the active provider based on environment and available keys."""
    if DEFAULT_LLM_PROVIDER in ("openai", "gemini", "mock"):
        return DEFAULT_LLM_PROVIDER
    if is_gemini_configured():
        return "gemini"
    return "mock"
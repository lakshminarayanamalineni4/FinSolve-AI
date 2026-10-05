from app.core.config import settings
from app.services.llm.client import LLMClient
from app.services.llm.providers.openrouter import OpenRouterProvider


def get_llm_client() -> LLMClient:
    """Create an LLM client based on the configured provider."""

    provider = settings.llm_provider.lower().strip()

    if provider == "openrouter":
        return OpenRouterProvider()

    raise ValueError(
        f"Unsupported LLM provider: {provider}"
    )

# uv run python -c "from app.services.llm.factory import get_llm_client; from app.services.llm.client import LLMClient; client = get_llm_client(); print(type(client).__name__); print(isinstance(client, LLMClient))"
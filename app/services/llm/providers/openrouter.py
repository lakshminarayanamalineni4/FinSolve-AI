import httpx

from app.core.config import settings
from app.services.llm.client import LLMClient


class OpenRouterProvider(LLMClient):
    """OpenRouter implementation of the LLMClient interface."""

    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(self) -> None:
        self.api_key = settings.llm_api_key
        self.model = settings.llm_model
        self.temperature = settings.llm_temperature
        self.max_tokens = settings.llm_max_tokens

    def generate(self, prompt: str) -> str:
        """Generate a text response using OpenRouter."""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        try:
            response = httpx.post(
                self.BASE_URL,
                headers=headers,
                json=payload,
                timeout=60.0,
            )

            response.raise_for_status()

            # print("OpenRouter status:", response.status_code)
            # print("OpenRouter response:", response.text)

            response_data = response.json()

            return response_data["choices"][0]["message"]["content"]

        except httpx.HTTPError as exc:
            raise RuntimeError(
                "OpenRouter request failed."
            ) from exc

        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(
                "Unexpected response format from OpenRouter."
            ) from exc

# uv run python -c "from app.services.llm.providers.openrouter import OpenRouterProvider; from app.services.llm.client import LLMClient; print(issubclass(OpenRouterProvider, LLMClient))"
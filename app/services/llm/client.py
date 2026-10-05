from abc import ABC, abstractmethod


class LLMClient(ABC):
    """Interface for interacting with an LLM provider."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate a response from the LLM."""
        raise NotImplementedError
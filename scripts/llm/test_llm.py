
from app.services.llm.factory import get_llm_client


def main() -> None:
    """Manually test the LLM integration."""

    llm_client = get_llm_client()

    prompt = (
        "Explain role-based access control (RBAC) "
        "in one or two simple sentences."
    )

    print("Sending request to LLM...")

    response = llm_client.generate(prompt)

    print("\nLLM Response:")
    print(response)

    print("\nResponse type:")
    print(type(response).__name__)


if __name__ == "__main__":
    main()

# uv run python -m scripts.llm.test_llm
 
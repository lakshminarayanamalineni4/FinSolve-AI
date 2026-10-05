from app.services.rag.prompt import RAGPrompt


def main() -> None:
    prompt = RAGPrompt().build(
        retrieved_context=(
            "[Source: travel_policy.md]\n"
            "Domestic travel reimbursement is limited to ₹5,000 per trip."
        ),
        user_question="What is the domestic travel reimbursement limit?",
    )

    print(prompt)


if __name__ == "__main__":
    main()

# uv run python -m scripts.rag.test_rag_prompt
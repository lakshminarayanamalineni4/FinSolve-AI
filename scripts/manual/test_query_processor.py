from app.services.query.processor import (
    QueryProcessor,
    QueryValidationError,
)


def main() -> None:
    processor = QueryProcessor()

    query = processor.process(
        "   What   is the\nfinance\tpolicy?   "
    )

    print("Original:")
    print(repr(query.original))

    print("\nProcessed:")
    print(repr(query.processed))

    print("\nTesting empty query...")

    try:
        processor.process("   ")
    except QueryValidationError as exc:
        print(f"Validation error: {exc}")

    print("\nQuery processor validation successful.")


if __name__ == "__main__":
    main()

# uv run python -m scripts.manual.test_query_processor
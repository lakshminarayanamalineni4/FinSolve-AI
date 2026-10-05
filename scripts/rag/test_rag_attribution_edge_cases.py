from app.services.rag.attribution import SourceAttributor
from app.services.retrieval.models import RetrievalResult


def main() -> None:
    attributor = SourceAttributor()

    print("\n=== TEST 1: Empty Sources ===")
    print(attributor.build([]))

    print("\n=== TEST 2: Single Source ===")
    single_source = [
        RetrievalResult(
            point_id="point-1",
            score=0.95,
            document_id=10,
            chunk_index=2,
            department="Finance",
            required_permission="finance.read",
            content="Finance policy content.",
        )
    ]
    print(attributor.build(single_source))

    print("\n=== TEST 3: Multiple Chunks Same Document ===")
    same_document = [
        RetrievalResult(
            point_id="point-1",
            score=0.92,
            document_id=10,
            chunk_index=2,
            department="Finance",
            required_permission="finance.read",
            content="First chunk.",
        ),
        RetrievalResult(
            point_id="point-2",
            score=0.89,
            document_id=10,
            chunk_index=3,
            department="Finance",
            required_permission="finance.read",
            content="Second chunk.",
        ),
    ]
    print(attributor.build(same_document))

    print("\n=== TEST 4: Multiple Documents ===")
    multiple_documents = [
        RetrievalResult(
            point_id="point-1",
            score=0.91,
            document_id=10,
            chunk_index=2,
            department="Finance",
            required_permission="finance.read",
            content="Finance content.",
        ),
        RetrievalResult(
            point_id="point-2",
            score=0.88,
            document_id=25,
            chunk_index=1,
            department="HR",
            required_permission="hr.read",
            content="HR content.",
        ),
    ]
    print(attributor.build(multiple_documents))


if __name__ == "__main__":
    main()


# uv run python -m scripts.rag.test_rag_attribution_edge_cases

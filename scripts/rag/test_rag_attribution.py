from app.services.rag.attribution import SourceAttributor
from app.services.retrieval.models import RetrievalResult


def main() -> None:
    sources = [
        RetrievalResult(
            point_id="point-1",
            score=0.92,
            document_id=12,
            chunk_index=4,
            department="Finance",
            required_permission="finance.read",
            content="Domestic travel reimbursement is limited to ₹5,000 per trip.",
        ),
        RetrievalResult(
            point_id="point-2",
            score=0.87,
            document_id=27,
            chunk_index=1,
            department="Finance",
            required_permission="finance.read",
            content="Business travel expenses require manager approval.",
        ),
    ]

    attributor = SourceAttributor()
    sources_output = attributor.build(sources)

    print("\n=== SOURCE ATTRIBUTION ===")

    for source in sources_output:
        print(f"- {source}")


if __name__ == "__main__":
    main()
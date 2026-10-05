from app.core.database import SessionLocal
from app.services.ingestion.loaders.csv_loader import CSVLoader
from app.services.ingestion.loaders.markdown_loader import MarkdownLoader
from app.services.ingestion.normalizer import DocumentNormalizer
from app.services.ingestion.repository import DocumentRepository


def main():
    markdown_loader = MarkdownLoader("resources/data")
    csv_loader = CSVLoader("resources/data")

    documents = (
        markdown_loader.load()
        + csv_loader.load()
    )

    normalizer = DocumentNormalizer()

    normalized_documents = [
        normalizer.normalize(document)
        for document in documents
    ]

    db = SessionLocal()

    try:
        repository = DocumentRepository(db)

        for document in normalized_documents:
            repository.save(document)

        db.commit()

        print(
            f"Successfully persisted "
            f"{len(normalized_documents)} documents."
        )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()

# uv run python -m app.scripts.ingest_documents
from app.services.ingestion.loaders.csv_loader import CSVLoader
from app.services.ingestion.loaders.markdown_loader import MarkdownLoader
from app.services.ingestion.normalizer import DocumentNormalizer


def main():
    markdown_loader = MarkdownLoader("resources/data")
    csv_loader = CSVLoader("resources/data")

    markdown_documents = markdown_loader.load()
    csv_documents = csv_loader.load()

    documents = markdown_documents + csv_documents

    normalizer = DocumentNormalizer()

    normalized_documents = [
        normalizer.normalize(document)
        for document in documents
    ]

    print(f"Normalized {len(normalized_documents)} documents")

    for document in normalized_documents:
        print("\n---")
        print(f"Name: {document.name}")
        print(f"Type: {document.file_type}")
        print(f"Path: {document.source_path}")
        print(f"Characters: {len(document.content)}")
        print(f"Department: {document.department}")
        print(f"Permission: {document.required_permission}")

if __name__ == "__main__":
    main()

# uv run python -m app.scripts.test_normalizer
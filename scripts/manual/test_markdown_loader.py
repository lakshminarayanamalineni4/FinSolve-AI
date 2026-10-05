from app.services.ingestion.loaders.markdown_loader import MarkdownLoader


def main():
    loader = MarkdownLoader("resources/data")

    documents = loader.load()

    print(f"Loaded {len(documents)} Markdown documents")

    for document in documents:
        print("\n---")
        print(f"Name: {document.name}")
        print(f"Path: {document.source_path}")
        print(f"Characters: {len(document.content)}")


if __name__ == "__main__":
    main()

# uv run python -m app.scripts.test_markdown_loader
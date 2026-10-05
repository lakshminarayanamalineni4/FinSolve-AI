from app.services.ingestion.loaders.csv_loader import CSVLoader


def main():
    loader = CSVLoader("resources/data")

    documents = loader.load()

    print(f"Loaded {len(documents)} CSV documents")

    for document in documents:
        print("\n---")
        print(f"Name: {document.name}")
        print(f"Path: {document.source_path}")
        print(f"Characters: {len(document.content)}")
        print("\nContent preview:")
        print(document.content[:500])


if __name__ == "__main__":
    main()
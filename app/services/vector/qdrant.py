from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PayloadSchemaType,
    VectorParams,
)


COLLECTION_NAME = "finsolve_chunks"
VECTOR_SIZE = 1024


class QdrantService:
    def __init__(self) -> None:
        self.client = QdrantClient(
            host="localhost",
            port=6333,
        )

    def create_collection(self) -> None:
        if self.client.collection_exists(COLLECTION_NAME):
            print(f"Collection '{COLLECTION_NAME}' already exists.")
            return

        self.client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )

        self.client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name="document_id",
            field_schema=PayloadSchemaType.INTEGER,
        )

        self.client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name="department",
            field_schema=PayloadSchemaType.KEYWORD,
        )

        self.client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name="required_permission",
            field_schema=PayloadSchemaType.KEYWORD,
        )
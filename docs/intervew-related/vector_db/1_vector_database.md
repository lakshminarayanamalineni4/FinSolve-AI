## What is a vector database, and why are you using Qdrant in FinSolve AI?

A vector database is designed to efficiently store and search vector embeddings. In FinSolve AI, we generate embeddings for document chunks using Qwen and store those vectors in Qdrant along with metadata such as document and access-control information. When a user asks a question, we generate an embedding for the query and perform a similarity search in Qdrant. We also apply metadata filters so that the retrieval is restricted to documents the user is authorized to access. I chose Qdrant because it supports vector similarity search, metadata filtering, and the 1024-dimensional vectors used by our embedding configuration.


## What is stored in a Qdrant record/point in your FinSolve AI system?

Qdrant stores the vector along with useful metadata, for example:

document/chunk information
document ID
resource information
access-control metadata
original chunk text or a reference to it

When the user asks a question:

Question → Embedding → Qdrant similarity search → Relevant chunks

The important distinction is:

A traditional database primarily retrieves data using structured fields or exact/keyword conditions, while a vector database allows us to retrieve data based on similarity between embeddings.